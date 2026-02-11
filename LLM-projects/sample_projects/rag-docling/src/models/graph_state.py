from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    """
    Represents the state of our adaptive RAG graph.
    
    Attributes:
        messages: Conversation messages
        current_question: Current question being processed
        documents: Retrieved documents
        generation: Generated response
        failed_retrievals: Number of failed retrieval attempts
        source: Selected data source (vectorstore or web_search)
        hallucination_check: Result of hallucination check
        answer_check: Result of answer relevance check
    """
    messages: List[BaseMessage]
    current_question: str
    documents: Optional[List[Dict[str, Any]]]
    generation: Optional[str]
    failed_retrievals: int
    source: Optional[str]
    hallucination_check: Optional[Dict[str, Any]]
    answer_check: Optional[Dict[str, Any]] 