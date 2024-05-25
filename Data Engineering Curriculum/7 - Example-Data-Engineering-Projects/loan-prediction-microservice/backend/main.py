import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes import router

app = FastAPI(
    title="Loan Prediction API",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(router, prefix="/v1/loan", tags=["loan"])

if __name__ == "__main__":
    server_attr = {"host": "0.0.0.0", "reload": True, "port": 8877, "workers": 4}
    uvicorn.run("main:app", **server_attr)
