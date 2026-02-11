# main.py
from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from sqlmodel import Field, SQLModel, select
from typing import Optional, AsyncGenerator

from app import settings
from app.deps import LoginForAccessTokenDep, DBSessionDep, TodoProducerDep, GetCurrentUserDep
from app.db_eng import engine

from __generated__.schemas import todo_pb2


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)
    user_id: Optional[int] = Field(index=True)

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Become GenEng and make the world a better place."
            }
        }


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables.")
    create_db_and_tables()
    print("Tables created")
    yield


app = FastAPI(lifespan=lifespan, root_path="/todo-service")

@app.get("/")
def read_root(request: Request, user_data: GetCurrentUserDep):
    # print header received from the request
    print(request.headers)
    print
    return {"Hello": "World"}

@app.post("/auth/login", tags=["Wrapper Auth"])
def login_for_access_token(form_data: LoginForAccessTokenDep):
    return form_data


@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo, producer: TodoProducerDep, session: DBSessionDep, user_data: GetCurrentUserDep) -> Todo:

    todo.user_id = user_data["id"]

    session.add(todo)
    session.commit()
    session.refresh(todo)

    todo_protbuf = todo_pb2.Todo(id=todo.id, content=todo.content)
    try:
        # Produce message
        await producer.send_and_wait(topic=settings.KAFKA_TODO_TOPIC,
                                     value=todo_protbuf,
                                     key=str(user_data["email"])
                                     )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail="Error while producing message to Kafka")

    return todo


@app.get("/todos/", response_model=list[Todo])
def read_todos(session: DBSessionDep, user_data: GetCurrentUserDep):
    todos = session.exec(select(Todo).where(
        Todo.user_id == user_data["id"])).all()
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, session: DBSessionDep, user_data: GetCurrentUserDep):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int, session: DBSessionDep, user_data: GetCurrentUserDep):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return todo
