from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

class QueryRequest(BaseModel):
    topic: str
    message: str

class QueryResponse(BaseModel):
    response: str
    metadata: dict = {}

@app.post("/query")
async def query(request: QueryRequest):
    agent_type = os.getenv("AGENT_TYPE", "fallback")
    
    # Mock responses based on agent type
    responses = {
        "password_reset": {
            "response": "To reset your password, please visit the password reset page and follow the instructions.",
            "metadata": {"confidence": 0.95}
        },
        "billing": {
            "response": "For billing inquiries, please contact our support team at billing@example.com",
            "metadata": {"confidence": 0.90}
        },
        "fallback": {
            "response": "I'm not sure about that. Please contact our support team for assistance.",
            "metadata": {"confidence": 0.80}
        }
    }
    
    return responses.get(agent_type, responses["fallback"]) 