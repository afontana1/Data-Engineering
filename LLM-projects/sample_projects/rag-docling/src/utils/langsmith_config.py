"""LangSmith configuration and utilities."""
import os
from langsmith import Client
from typing import Optional

def initialize_langsmith() -> Optional[Client]:
    """Initialize LangSmith client if environment variables are set.
    
    Returns:
        Optional[Client]: LangSmith client if configuration is valid, None otherwise
    """
    try:
        if os.getenv("LANGCHAIN_API_KEY"):
            client = Client()
            # Set the project name from environment variable or use default
            os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "docling-rag")
            return client
        return None
    except Exception as e:
        print(f"Error initializing LangSmith: {e}")
        return None

def is_langsmith_configured() -> bool:
    """Check if LangSmith is properly configured.
    
    Returns:
        bool: True if LangSmith is configured, False otherwise
    """
    required_vars = [
        "LANGCHAIN_API_KEY",
        "LANGCHAIN_TRACING_V2",
        "LANGCHAIN_ENDPOINT"
    ]
    return all(os.getenv(var) for var in required_vars) 