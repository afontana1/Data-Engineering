import streamlit as st
from typing import Annotated, Sequence, Literal, Dict, Any, List
from typing_extensions import TypedDict
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from models.vectorstore import get_vectorstore
from langchain.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
import logging

from services.grading_service import GradingService
from services.routing_service import RoutingService
from services.web_search_service import WebSearchService
from models.model_manager import get_model, AVAILABLE_MODELS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize memory saver
memory = MemorySaver()

# Initialize services
grading_service = GradingService()
routing_service = RoutingService()
web_search_service = WebSearchService()

class GraphState(TypedDict):
    """State maintained between steps."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_question: str
    documents: List[Dict[str, Any]]
    generation: str
    failed_retrievals: int
    source: str

def initialize_state(question: str) -> GraphState:
    """Initialize the graph state with a question."""
    return {
        "messages": [],
        "current_question": question,
        "documents": [],
        "generation": "",
        "failed_retrievals": 0,
        "source": ""
    }

def route_question(state: GraphState) -> Dict[str, Any]:
    """Route the question to appropriate data source."""
    question = state["current_question"]
    try:
        route = routing_service.route_question(question)
        logger.info(f"Routing question to: {route.datasource} ({route.explanation})")
        
        return {
            **state,
            "source": route.datasource,
            "next": route.datasource  # Add next step for the graph
        }
    except Exception as e:
        logger.error(f"Error in routing: {str(e)}")
        return {
            **state,
            "source": "vectorstore",  # Default to vectorstore on error
            "next": "vectorstore",
            "generation": f"Error in routing: {str(e)}"
        }

def retrieve_from_vectorstore(state: GraphState) -> Dict[str, Any]:
    """Retrieve documents from vectorstore."""
    logger.info("Retrieving from vectorstore")
    question = state["current_question"]
    
    try:
        # Get documents from vectorstore
        vectorstore = get_vectorstore()
        raw_documents = vectorstore.similarity_search(question, k=3)
        
        # Convert Document objects to dictionaries
        documents = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "source": "vectorstore"
            }
            for doc in raw_documents
        ]
        
        return {
            **state,  # Include all existing state
            "documents": documents
        }
    except Exception as e:
        logger.error(f"Error retrieving from vectorstore: {str(e)}")
        return {
            **state,
            "documents": [],
            "generation": f"Error retrieving documents: {str(e)}"
        }

def web_search(state: GraphState) -> Dict[str, Any]:
    """Perform web search."""
    logger.info("Performing web search")
    question = state["current_question"]
    
    try:
        # Get web search results
        results = web_search_service.search(question)
        
        # Convert results to consistent format
        documents = [
            {
                "content": result.get("content", ""),
                "metadata": {"source": "web_search", **result.get("metadata", {})},
                "source": "web_search"
            }
            for result in results
        ]
        
        # If we also have vectorstore results, combine them
        if state.get("documents"):
            documents.extend(state["documents"])
        
        return {
            **state,  # Include all existing state
            "documents": documents
        }
    except Exception as e:
        logger.error(f"Error in web search: {str(e)}")
        return {
            **state,
            "documents": [],
            "generation": f"Error performing web search: {str(e)}"
        }

def grade_documents(state: GraphState) -> Dict[str, Any]:
    """Grade retrieved documents and decide next step."""
    documents = state["documents"]
    question = state["current_question"]
    
    try:
        # Grade documents
        grade = grading_service.grade_documents(question, documents)
        logger.info(f"Document relevance: {grade}")
        
        # Increment failed retrievals if documents are not relevant
        failed_retrievals = state.get("failed_retrievals", 0)
        if grade.binary_score == "no":
            failed_retrievals += 1
        
        # Determine next step
        next_step = "generate"
        if grade.binary_score == "no":
            if state["source"] == "vectorstore" and routing_service.should_use_web_search(
                question, failed_retrievals
            ):
                next_step = "web_search"
            else:
                next_step = "rewrite"
        
        return {
            **state,
            "failed_retrievals": failed_retrievals,
            "next": next_step,
            "grade_explanation": grade.explanation
        }
    except Exception as e:
        logger.error(f"Error in document grading: {str(e)}")
        return {
            **state,
            "next": "generate",  # Default to generate on error
            "generation": f"Error in document grading: {str(e)}"
        }

def rewrite_question(state: GraphState) -> Dict[str, Any]:
    """Rewrite the question for better retrieval."""
    question = state["current_question"]
    failed_retrievals = state["failed_retrievals"]
    
    try:
        # Get rewritten question
        rewritten = grading_service.suggest_rewrite(question, failed_retrievals)
        
        return {
            **state,  # Include all existing state
            "current_question": rewritten
        }
    except Exception as e:
        logger.error(f"Error rewriting question: {str(e)}")
        return {
            **state,
            "generation": f"Error rewriting question: {str(e)}"
        }

def generate_response(state: GraphState) -> Dict[str, Any]:
    """Generate response using retrieved documents."""
    model = get_model()
    question = state["current_question"]
    documents = state["documents"]
    
    try:
        # Create context from documents
        context = "\n\n".join(
            f"Document {i+1}:\n{doc['content']}"
            for i, doc in enumerate(documents)
        )
        
        # Create system message
        system_message = SystemMessage(content=f"""You are a helpful AI assistant that answers questions based on the provided documents.
        Always cite your sources and be honest if you're not sure about something.
        If using web search results, mention that the information comes from the web.
        
        Here are the relevant documents:
        {context}""")
        
        # Create messages
        messages = [
            system_message,
            HumanMessage(content=question)
        ]
        
        # Generate response
        response = model.invoke(messages)
        
        # Add source information
        sources = [doc.get("source", "unknown") for doc in documents]
        if "web_search" in sources:
            response.content += "\n\n(Information from web search results)"
        
        return {
            **state,  # Include all existing state
            "generation": response.content,
            "messages": state["messages"] + [AIMessage(content=response.content)]
        }
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        error_msg = "I encountered an error generating a response. Please try again."
        return {
            **state,
            "generation": error_msg,
            "messages": state["messages"] + [AIMessage(content=error_msg)]
        }

def create_chat_graph():
    """Create the chat graph with adaptive RAG."""
    # Initialize graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("route_question", route_question)
    workflow.add_node("vectorstore", retrieve_from_vectorstore)
    workflow.add_node("web_search", web_search)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("rewrite", rewrite_question)
    workflow.add_node("generate", generate_response)
    
    # Add edges
    workflow.set_entry_point("route_question")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "route_question",
        lambda x: x["next"],  # Use the next field from state
        {
            "vectorstore": "vectorstore",
            "web_search": "web_search"
        }
    )
    
    workflow.add_edge("vectorstore", "grade_documents")
    workflow.add_edge("web_search", "grade_documents")
    
    workflow.add_conditional_edges(
        "grade_documents",
        lambda x: x["next"],  # Use the next field from state
        {
            "generate": "generate",
            "rewrite": "rewrite",
            "web_search": "web_search"
        }
    )
    
    workflow.add_edge("rewrite", "vectorstore")
    workflow.add_edge("generate", END)
    
    return workflow.compile(checkpointer=memory)

def process_question(question: str) -> Dict[str, Any]:
    """Process a question through the graph."""
    graph = create_chat_graph()
    initial_state = initialize_state(question)
    
    # Create configuration for the memory checkpointer
    config = {
        "configurable": {
            "thread_id": st.session_state.get("chat_id", "default"),
            "checkpoint_ns": "chat_history",
            "checkpoint_id": f"chat_{st.session_state.get('chat_id', 'default')}"
        }
    }
    
    result = graph.invoke(initial_state, config=config)
    return result