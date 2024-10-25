# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncGenerator
from aiokafka import AIOKafkaConsumer
import asyncio

from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer

from __generated__.schemas import todo_pb2

import logging

logging.basicConfig(level=logging.INFO)

# KAFKA VARS
BROKER_URL = "broker:19092"
TODO_TOPIC = "todo"


async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    protobuf_deserializer = ProtobufDeserializer(
        todo_pb2.Todo, {'use.deprecated.format': False})

    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="ms2-group",
        auto_offset_reset='earliest',
        value_deserializer=lambda v: protobuf_deserializer(
            v, SerializationContext(topic, MessageField.VALUE))
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            logging.info(f"Received message: {message} CONTEXT: {
                message.value} on topic {message.topic}")
            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()


# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # print("Creating tables..")
    logging.info("Starting Kafka Consumer..")
    asyncio.create_task(consume_messages(TODO_TOPIC, BROKER_URL))
    logging.info("Started Kafka Consumer")
    yield


app = FastAPI(lifespan=lifespan, title="Hello World API with DB",
              version="0.0.1",
              servers=[
                  {
                      "url": "http://127.0.0.1:8002",  # ADD NGROK URL Here Before Creating GPT Action
                      "description": "Development Server"
                  }, {
                      "url": "http://127.0.0.1:8000",  # ADD NGROK URL Here Before Creating GPT Action
                      "description": "Development Server"
                  }
              ])


@app.get("/")
def read_root():
    return {"App": "Service 2"}
