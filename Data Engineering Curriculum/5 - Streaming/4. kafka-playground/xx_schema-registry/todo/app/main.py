# main.py
from contextlib import asynccontextmanager
from typing import Optional, Annotated
from sqlmodel import Field, SQLModel
from fastapi import FastAPI, Depends
from typing import AsyncGenerator
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from __generated__.schemas import todo_pb2

# KAFKA VARS
BROKER_URL = "broker:19092"
TODO_TOPIC = "todo"

# Schema Registry configuration
schema_registry_conf = {'url': 'http://host.docker.internal:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Protobuf Serializer
protobuf_serializer = ProtobufSerializer(
    todo_pb2.Todo, schema_registry_client, {'use.deprecated.format': False})


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)


async def consume_messages(topic, bootstrap_servers):

    protobuf_deserializer = ProtobufDeserializer(
        todo_pb2.Todo, {'use.deprecated.format': False})

    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="todo-group",
        auto_offset_reset='earliest',
        value_deserializer=lambda v: protobuf_deserializer(
            v, SerializationContext(topic, MessageField.VALUE))
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for msg in consumer:
            print(f"Consumed record with value {
                  msg.value} on topic {msg.topic}")

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Init.. Kafka ....")
    asyncio.create_task(consume_messages(TODO_TOPIC, BROKER_URL))
    print("Started Kafka Consumer..")
    yield


app = FastAPI(lifespan=lifespan)


# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=BROKER_URL,
        value_serializer=lambda v: protobuf_serializer(
            v, SerializationContext(TODO_TOPIC, MessageField.VALUE))
    )
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()


@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]) -> Todo:
    
    todo_protbuf = todo_pb2.Todo(id=todo.id, content=todo.content)

    # Produce message
    await producer.send_and_wait(topic=TODO_TOPIC,
                                 value=todo_protbuf,
                                 )

    return todo
