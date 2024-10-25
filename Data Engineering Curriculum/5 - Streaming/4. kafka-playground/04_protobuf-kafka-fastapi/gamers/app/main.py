from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
import logging

from app import person_pb2


logging.basicConfig(level=logging.INFO)

KAFKA_BROKER = "broker:19092"
KAFKA_TOPIC = "gamers"
KAFKA_CONSUMER_GROUP_ID = "gamers-consumer-group"


class GamePlayersRegistration(SQLModel):
    player_name: str
    age: int
    email: str
    phone_number: str


async def consume():
    # Milestone: CONSUMER INTIALIZE
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER
    )

    await consumer.start()
    try:
        async for msg in consumer:
            new_person = person_pb2.Person()
            new_person.ParseFromString(msg.value)
            logging.info(f"Deserialized data: {new_person}")

            # logging.info(
            #     "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
            #         msg.topic, msg.partition, msg.offset, msg.key, msg.value,
            #         msg.timestamp)
            # )
    finally:
        await consumer.stop()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting consumer")
    asyncio.create_task(consume())
    yield
    print("Stopping consumer")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def hello():
    # Create a new Person message
    person = person_pb2.Person()
    person.name = "John Doe"
    person.id = 1234
    person.email = "johndoe@example.com"

    # Serialize the message to a byte string
    serialized_person = person.SerializeToString()
    print(f"Serialized data: {serialized_person}")

    # Deserialize the byte string back into a Person message
    new_person = person_pb2.Person()
    new_person.ParseFromString(serialized_person)
    print(f"Deserialized data: {new_person}")
    print(f"Name: {new_person.name}, ID: {
          new_person.id}, Email: {new_person.email}")
    return {"Hello": "World"}


@app.post("/register-player")
async def register_new_player(player_data: GamePlayersRegistration):

    person = person_pb2.Person()
    person.name = player_data.player_name
    person.id = player_data.age
    person.email = player_data.email

    serialized_person = person.SerializeToString()

    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)

    await producer.start()

    try:
        await producer.send_and_wait(KAFKA_TOPIC, serialized_person)
    finally:
        await producer.stop()

    return player_data.model_dump_json()
