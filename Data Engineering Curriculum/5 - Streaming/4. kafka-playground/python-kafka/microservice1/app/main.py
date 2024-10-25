from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, TopicPartition
from contextlib import asynccontextmanager
import logging
import asyncio

from app import settings
from app.topic import startup_topic_event
from app.utils import key_deserializer, value_deserializer

# Logging configuration
logging.basicConfig(level=logging.INFO)


class BookOrder(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str
    user_id: int
    price: float

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting application")    
    # THIS WILL FAIL DUE TO BROKER VERSION COMPAITIBILITY
    # ERROR: IncompatibleBrokerVersion: Kafka broker does not support the 'CreateTopicsRequest_v0' Kafka protocol.
    # asyncio.create_task(startup_topic_event())
    logging.info("Application started")
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/order-book")
async def order_book(book_order: BookOrder):
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
        acks="all",
    )
    logging.info(f"KAFKA_BOOTSTRAP_SERVER: {settings.KAFKA_BOOTSTRAP_SERVER}")
    logging.info(f"Book order received: {book_order.model_dump_json().encode('utf-8')}")

    await producer.start()

    try:
        await producer.send_and_wait(
            topic=settings.KAFKA_BOOK_ORDER_TOPIC,
            value=book_order.model_dump_json().encode('utf-8'),
            key=book_order.title.encode('utf-8'),
            headers=[("user_id", str(book_order.user_id).encode('utf-8'))]
        )
    finally:
        await producer.stop()

    return book_order

@app.get("/consumer")
async def consume_messages():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_BOOK_ORDER_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_CONSUMER_BOOK_GROUD_ID,
        key_deserializer=key_deserializer,
        value_deserializer=value_deserializer,
        auto_offset_reset='latest',  # Start reading from the earliest offset if no offset is committed
    )
    await consumer.start()

    try:
        # Fetch a single message with a timeout
        msg = await asyncio.wait_for(consumer.getone(), timeout=10.0)
        tp = TopicPartition(msg.topic, msg.partition)

        # Current position
        position = await consumer.position(tp)
        logging.info(f"Current position: {position}")
        
        # Committed offset
        committed = await consumer.committed(tp)
        logging.info(f"Committed offset: {committed}")

        logging.info(
            "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
                msg.topic, msg.partition, msg.offset, msg.key, msg.value,
                msg.timestamp)
        )
        return {"raw_message": msg, "offset": msg.offset, "key": msg.key, "value": msg.value}
    except asyncio.TimeoutError:
        logging.warning("No messages received within the timeout period")
        raise HTTPException(status_code=408, detail="No messages received within the timeout period")
    finally:
        logging.info("Finally Stopping consumer")
        await consumer.stop()
        
@app.post("/get-food")
async def get_food(food_name: str):
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
        acks="all",
    )
    logging.info(f"KAFKA_BOOTSTRAP_SERVER: {settings.KAFKA_BOOTSTRAP_SERVER}")
    logging.info(f"Food order received: {food_name}")
    
    await producer.start()
    
    try:
        await producer.send_and_wait(
            topic=settings.KAFKA_FOOD_ORDER_TOPIC,
            value=food_name.encode('utf-8'),
            key=food_name.encode('utf-8'),
        )
    finally:
        await producer.stop()

    return {"food_name": food_name}