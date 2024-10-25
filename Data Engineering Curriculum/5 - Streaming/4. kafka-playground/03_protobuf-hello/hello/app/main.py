from fastapi import FastAPI
from sqlmodel import SQLModel, Field
from contextlib import asynccontextmanager
import logging
from app import person_pb2
# Logging configuration
logging.basicConfig(level=logging.INFO)


class BookOrder(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str
    user_id: int
    price: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application started")
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def hi():
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


@app.post("/order-book")
async def order_book(book_order: BookOrder):

    return book_order


@app.post("/get-food")
async def get_food(food_name: str):

    return {"food_name": food_name}
