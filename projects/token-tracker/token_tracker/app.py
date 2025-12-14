# main FastAPI application
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from token_tracker.telemetry.context import set_usage_context
from token_tracker.telemetry.sink import StdoutSink, AsyncQueueSink
from token_tracker.telemetry.litellm_instrumentation import LiteLLMInstrumentation

from token_tracker.routes.chat import router as chat_router

app = FastAPI()

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
    base_sink = StdoutSink()
    queue_sink = AsyncQueueSink(base_sink)

    app.state.usage_sink = queue_sink
    app.state.usage_worker_task = __import__("asyncio").create_task(queue_sink.worker())

    instr = LiteLLMInstrumentation(sink=queue_sink)
    instr.install()
    app.state.litellm_instr = instr


@app.on_event("shutdown")
async def shutdown():
    instr = getattr(app.state, "litellm_instr", None)
    if instr:
        instr.uninstall()


# ----------------------------
# Include routers
# ----------------------------
# If you want these endpoints at the root:
app.include_router(chat_router)

# If you want them under a prefix (recommended), use:
# app.include_router(chat_router, prefix="/api")
