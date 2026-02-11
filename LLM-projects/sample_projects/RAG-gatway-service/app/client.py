import httpx
import os
from typing import Dict, Any
from .schema import QueryRequest, QueryResponse

class AgentClient:
    def __init__(self):
        self.timeout = float(os.getenv("AGENT_TIMEOUT", "30.0"))
        self.client = httpx.AsyncClient(timeout=self.timeout)

    async def query_agent(self, url: str, request: QueryRequest) -> QueryResponse:
        """Send a query to an agent service."""
        try:
            response = await self.client.post(
                url,
                json=request.model_dump(),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return QueryResponse(**response.json())
        except httpx.HTTPError as e:
            raise Exception(f"Error querying agent at {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error while querying agent: {str(e)}")

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose() 