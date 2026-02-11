from fastapi import FastAPI
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.consumer import consume_todo_events

# Set up logging
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.info("Starting Kafka consumer...")
    asyncio.create_task(consume_todo_events())
    logging.info("Kafka consumer started!!")
    yield


app = FastAPI(lifespan=lifespan, root_path="/ai-eng")


@app.get("/")
def read_root():
    """Simple API to return 'Hello World'."""
    return {"Hello": "AI Recommendations"}
