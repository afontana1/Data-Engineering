from pydantic import BaseModel
from typing import Optional, Dict, Any

class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    message: str

class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    response: str
    detected_topic: str
    metadata: Optional[Dict[str, Any]] = None 