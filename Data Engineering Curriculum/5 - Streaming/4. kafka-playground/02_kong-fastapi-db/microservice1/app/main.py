from fastapi import FastAPI
from sqlmodel import SQLModel, Field
from contextlib import asynccontextmanager
import logging

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

app = FastAPI(lifespan=lifespan, root_path="/microservice1")


@app.post("/order-book")
async def order_book(book_order: BookOrder):

    return book_order


@app.post("/get-food")
async def get_food(food_name: str):

    return {"food_name": food_name}
