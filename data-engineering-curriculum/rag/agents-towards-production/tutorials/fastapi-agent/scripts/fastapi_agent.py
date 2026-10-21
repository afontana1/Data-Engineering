from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
import os
import asyncio

# Define our simple agent class
class SimpleAgent:
    def __init__(self, name="FastAPI Agent"):
        self.name = name
    
    def generate_response(self, query):
        """Generate a synchronous response to a user query"""
        return f"Agent {self.name} received: '{query}'\nResponse: This is a simulated agent response."
    
    async def generate_response_stream(self, query):
        """Generate a streaming response to a user query"""
        prefix = f"Agent {self.name} thinking about: '{query}'\n"
        response = "This is a simulated agent response that streams token by token."
        
        # Yield the prefix as a single chunk
        yield prefix
        
        # Stream the response token by token with small delays
        for token in response.split():
            await asyncio.sleep(0.1)  # Simulate thinking time
            yield token + " "

# Define request and response models
class QueryRequest(BaseModel):
    query: str
    context: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "query": "What is FastAPI?",
                "context": "I'm a beginner programmer."
            }
        }

class QueryResponse(BaseModel):
    response: str
    
    class Config:
        schema_extra = {
            "example": {
                "response": "FastAPI is a modern, high-performance web framework for building APIs with Python."
            }
        }

# Initialize FastAPI app
app = FastAPI(
    title="Agent API",
    description="A simple API that serves an AI agent",
    version="0.1.0"
)

# Create an instance of our agent
agent = SimpleAgent()

# Health check endpoint
@app.get("/health")
def health_check():
    """Check if the API is running"""
    return {"status": "ok", "message": "API is operational"}

# Create a synchronous endpoint for the agent
@app.post("/agent", response_model=QueryResponse)
def query_agent(request: QueryRequest):
    """Get a response from the agent"""
    response = agent.generate_response(request.query)
    return QueryResponse(response=response)

# Create a streaming endpoint for the agent
@app.post("/agent/stream")
async def stream_agent(request: QueryRequest):
    """Stream a response from the agent token by token"""
    
    async def event_generator():
        async for token in agent.generate_response_stream(request.query):
            # Format as a JSON object
            data = json.dumps({"token": token})
            yield f"data: {data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    ) 