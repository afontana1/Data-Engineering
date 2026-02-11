from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router import router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="RAG Gateway",
    description="A gateway service for routing queries to topic-specific RAG agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=eval(os.getenv("CORS_ORIGINS", '["*"]')),
    allow_credentials=True,
    allow_methods=eval(os.getenv("CORS_METHODS", '["*"]')),
    allow_headers=eval(os.getenv("CORS_HEADERS", '["*"]')),
)

# Include the router
app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    } 