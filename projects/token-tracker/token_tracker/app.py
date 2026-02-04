# main FastAPI application
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from dotenv import load_dotenv

from token_tracker.telemetry.context import set_usage_context
from token_tracker.telemetry.sink import (
    StdoutSink,
    AsyncQueueSink,
    DatabaseSink,
    DynamoDBSink,
    MultiSink,
)
from token_tracker.telemetry.db_connector import DatabaseConnector, DatabaseConfig
from token_tracker.telemetry.dynamodb_table import DynamoDBTable
from token_tracker.telemetry.litellm_instrumentation import LiteLLMInstrumentation

from token_tracker.routes.chat import router as chat_router
from token_tracker.routes.telemetry import router as telemetry_router

app = FastAPI()


def _load_env_files() -> None:
    current_file = Path(__file__).resolve()
    candidates = [
        Path.cwd() / ".env",
        current_file.parent / ".env",
        current_file.parent.parent / ".env",
    ]
    for candidate in candidates:
        if candidate.exists():
            load_dotenv(dotenv_path=candidate, override=False)
            break


_load_env_files()

# Allow browser-based frontends served from other ports (simple dev CORS policy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def attach_identity(request: Request, call_next):
    # Replace with your real auth/session extraction:
    user_id = request.headers.get("x-user-id", "unknown")
    org_id = request.headers.get("x-org-id", "unknown")
    session_id = request.headers.get("x-session-id", "unknown")
    set_usage_context(user_id=user_id, org_id=org_id, session_id=session_id)
    return await call_next(request)


@app.on_event("startup")
async def startup():
    db_type = os.getenv("TOKEN_TRACKER_DB_TYPE", "sqlite")
    db_path = os.getenv("TOKEN_TRACKER_DB_PATH", "usage_events.db")
    db_connector = DatabaseConnector(DatabaseConfig(db_type=db_type, database=db_path))
    db_sink = DatabaseSink(db_connector)

    dynamodb_table_name = os.getenv("TOKEN_TRACKER_DYNAMODB_TABLE", "usage_events")
    dynamodb_table = DynamoDBTable.from_env(table_name=dynamodb_table_name)
    dynamodb_sink = DynamoDBSink(dynamodb_table)

    base_sink = MultiSink([StdoutSink(), db_sink, dynamodb_sink])
    queue_sink = AsyncQueueSink(base_sink)

    app.state.usage_sink = queue_sink
    app.state.usage_worker_task = __import__("asyncio").create_task(queue_sink.worker())
    app.state.db_connector = db_connector
    app.state.dynamodb_table = dynamodb_table

    instr = LiteLLMInstrumentation(sink=queue_sink)
    instr.install()
    app.state.litellm_instr = instr


@app.on_event("shutdown")
async def shutdown():
    instr = getattr(app.state, "litellm_instr", None)
    if instr:
        instr.uninstall()
    db_connector = getattr(app.state, "db_connector", None)
    if db_connector:
        db_connector.close()


# ----------------------------
# Include routers
# ----------------------------
# If you want these endpoints at the root:
app.include_router(chat_router)
app.include_router(telemetry_router)

# If you want them under a prefix (recommended), use:
# app.include_router(chat_router, prefix="/api")
