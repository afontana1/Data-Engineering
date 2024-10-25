from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from contextlib import asynccontextmanager
import logging
import asyncio
from app.consumer import consumer_book_order

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting consumer Again")
    asyncio.create_task(consumer_book_order())

    yield
    logging.info("Stopping consumer")
    

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World from microservice2"}

