import logging
import asyncio

from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, inspect
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, TopicPartition
from contextlib import asynccontextmanager

from app import settings
from app.utils import key_deserializer, value_deserializer
from app.db_config import engine
from app.debzium import debzium_startup_event
# Logging configuration
logging.basicConfig(level=logging.INFO)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


class BookOrder(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    user_id: int
    price: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting application")
    # Create a Producer Topic for Book Orders
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
        acks="all",
    )
    logging.info(f"KAFKA_BOOTSTRAP_SERVER: {settings.KAFKA_BOOTSTRAP_SERVER}")
    await producer.start()
    try:
        book_order = BookOrder(id=1, title="The Alchemist", user_id=1, price=10.0)
        await producer.send_and_wait(
            topic=settings.KAFKA_BOOK_ORDER_TOPIC,
            value=book_order.model_dump_json().encode('utf-8'),
            key=book_order.title.encode('utf-8'),
            headers=[("user_id", str(book_order.user_id).encode('utf-8'))]
        )
    finally:
        await producer.stop()
    
    logging.info(f"Created topic: {settings.KAFKA_BOOK_ORDER_TOPIC}")   
    
    create_db_and_tables()
    logging.info("Database and tables created")
    await debzium_startup_event()
    logging.info("Debezium connector registered")
    logging.info("Application started")
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/schema")
async def get_schema():
    inspector = inspect(engine)
    schema_details = {}

    for table_name in inspector.get_table_names(schema="public"):
        columns = inspector.get_columns(table_name, schema="public")
        schema_details[table_name] = [column["name"] for column in columns]

    return schema_details


@app.post("/order-book")
async def order_book(book_order: BookOrder):
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER,
        acks="all",
    )
    logging.info(f"KAFKA_BOOTSTRAP_SERVER: {settings.KAFKA_BOOTSTRAP_SERVER}")
    logging.info(f"Book order received: {
                 book_order.model_dump_json().encode('utf-8')}")

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
        # Start reading from the earliest offset if no offset is committed
        auto_offset_reset='latest',
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
        raise HTTPException(
            status_code=408, detail="No messages received within the timeout period")
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
