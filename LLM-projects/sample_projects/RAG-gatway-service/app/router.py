from fastapi import APIRouter, HTTPException
from .schema import QueryRequest, QueryResponse
from .config import Config
from .topic_detector import TopicDetector
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()
config = Config()
topic_detector = TopicDetector(config.get_topic_descriptions())

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Process a query by detecting its topic and routing to the appropriate agent.
    """
    try:
        # Detect the topic using embeddings
        detected_topic, confidence = topic_detector.detect_topic(request.message)
        
        # Get the appropriate agent URL
        agent_url = config.get_agent_url(detected_topic)
        
        # Forward the request to the agent
        async with httpx.AsyncClient() as client:
            response = await client.post(
                agent_url,
                json={"message": request.message},
                timeout=float(os.getenv("REQUEST_TIMEOUT", "30.0"))
            )
            response.raise_for_status()
            agent_response = response.json()
            
            return QueryResponse(
                response=agent_response["response"],
                detected_topic=detected_topic,
                metadata={
                    "confidence": confidence,
                    "agent_metadata": agent_response.get("metadata")
                }
            )
            
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with agent: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) 