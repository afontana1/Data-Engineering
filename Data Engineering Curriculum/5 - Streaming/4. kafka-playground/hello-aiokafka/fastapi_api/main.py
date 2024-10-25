from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer 
from sqlmodel import SQLModel

import asyncio
import json
import logging

from fastapi_api.consumer import consume
from fastapi_api.settings import loop, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC


logging.basicConfig(level=logging.INFO)

class Message(SQLModel):
    message : str

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    asyncio.create_task(consume())
    yield

app = FastAPI(lifespan=lifespan)

@app.post('/create_message')
async def send(message: Message):
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        logging.info(f'MESSAGE: {message}')
        value_json = json.dumps(message.__dict__).encode('utf-8')
        await producer.send_and_wait(topic=KAFKA_TOPIC, value=value_json)
    finally:
        await producer.stop()