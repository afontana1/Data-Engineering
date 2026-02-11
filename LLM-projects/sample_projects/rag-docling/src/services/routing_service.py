from typing import Literal
from pydantic import BaseModel, Field
from models.model_manager import get_model
import logging

logger = logging.getLogger(__name__)

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["vectorstore", "web_search"] = Field(
        description="Route to web search for recent events, vectorstore for indexed content"
    )
    explanation: str = Field(
        description="Explanation for why this datasource was chosen"
    )

class RoutingService:
    """Service for routing queries to appropriate data sources."""
    
    def __init__(self):
        self.model = get_model()
    
    def route_question(self, question: str) -> RouteQuery:
        """
        Route a question to the appropriate data source.
        
        Args:
            question: User's question
            
        Returns:
            RouteQuery with selected datasource and explanation
        """
        try:
            # Create routing prompt
            prompt = f"""You are an expert at routing questions to the most appropriate data source.

Question: {question}

Task: Determine whether this question should be answered using:
1. web_search: For questions about recent events, current information, or real-time data
2. vectorstore: For questions about general knowledge, concepts, or historical information

Consider:
1. Is this about a recent or current event?
2. Does this require up-to-date information?
3. Is this about general concepts or historical facts?

Provide:
1. A datasource choice ("web_search" or "vectorstore")
2. A brief explanation of your decision

Format your response as:
datasource: [choice]
explanation: [your explanation]"""

            # Get structured output from model
            llm_with_structured_output = self.model.with_structured_output(RouteQuery)
            result = llm_with_structured_output.invoke(prompt)
            
            logger.info(f"Routing result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in question routing: {str(e)}")
            # Default to vectorstore on error
            return RouteQuery(
                datasource="vectorstore",
                explanation=f"Defaulting to vectorstore due to error: {str(e)}"
            )
    
    def should_use_web_search(self, question: str, failed_vectorstore_attempts: int) -> bool:
        """
        Determine if we should fall back to web search after failed vectorstore attempts.
        
        Args:
            question: The question being processed
            failed_vectorstore_attempts: Number of failed vectorstore attempts
            
        Returns:
            Boolean indicating whether to use web search
        """
        try:
            prompt = f"""You are deciding whether to fall back to web search after {failed_vectorstore_attempts} failed attempts to find relevant information in the vectorstore.

Question: {question}

Consider:
1. Number of failed attempts: {failed_vectorstore_attempts}
2. Question type and likelihood of finding answer elsewhere
3. Cost/benefit of trying web search

Should we try web search now? Answer only 'yes' or 'no'."""

            response = str(self.model.invoke(prompt)).strip().lower()
            return response == "yes"
            
        except Exception as e:
            logger.error(f"Error in web search decision: {str(e)}")
            return failed_vectorstore_attempts >= 2  # Default fallback after 2 attempts