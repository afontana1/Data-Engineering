from fastapi import FastAPI

app = FastAPI(root_path="/service2")


@app.get("/")
def read_root():
    return {"Hello": "Microservice2"}
