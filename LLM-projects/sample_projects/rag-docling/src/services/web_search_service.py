from typing import List, Dict, Any
from langchain_community.tools.tavily_search import TavilySearchResults
import logging

logger = logging.getLogger(__name__)

class WebSearchService:
    """Service for performing web searches using Tavily."""
    
    def __init__(self):
        self.search_tool = TavilySearchResults(k=3)
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform a web search for the given query.
        
        Args:
            query: Search query
            
        Returns:
            List of search results with content and metadata
        """
        try:
            logger.info(f"Performing web search for: {query}")
            results = self.search_tool.invoke({"query": query})
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content": result["content"],
                    "metadata": {
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "source": "web_search"
                    }
                })
            
            logger.info(f"Found {len(formatted_results)} web search results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in web search: {str(e)}")
            return []  # Return empty list on error
    
    def combine_results(self, web_results: List[Dict[str, Any]], 
                       vectorstore_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Combine and deduplicate results from web search and vectorstore.
        
        Args:
            web_results: Results from web search
            vectorstore_results: Results from vectorstore
            
        Returns:
            Combined and deduplicated results
        """
        try:
            # Add source to vectorstore results if not present
            for result in vectorstore_results:
                if "metadata" not in result:
                    result["metadata"] = {}
                result["metadata"]["source"] = "vectorstore"
            
            # Combine results
            all_results = web_results + vectorstore_results
            
            # Simple deduplication based on content
            seen_content = set()
            unique_results = []
            
            for result in all_results:
                content = result["content"]
                if content not in seen_content:
                    seen_content.add(content)
                    unique_results.append(result)
            
            logger.info(f"Combined {len(web_results)} web results and {len(vectorstore_results)} vectorstore results into {len(unique_results)} unique results")
            return unique_results
            
        except Exception as e:
            logger.error(f"Error combining results: {str(e)}")
            return all_results  # Return all results without deduplication on error 