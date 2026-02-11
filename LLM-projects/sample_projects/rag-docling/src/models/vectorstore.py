from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import streamlit as st
import os
import tempfile
import logging
import atexit
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global client instance
_client = None
_temp_dir = None

def cleanup_qdrant():
    """Cleanup function to remove temporary directory and close client."""
    global _client, _temp_dir
    if _client is not None:
        try:
            _client.close()
        except Exception as e:
            logger.warning(f"Error closing Qdrant client: {e}")
        _client = None
    
    if _temp_dir and os.path.exists(_temp_dir):
        try:
            shutil.rmtree(_temp_dir)
            logger.info(f"Cleaned up temporary directory: {_temp_dir}")
        except Exception as e:
            logger.warning(f"Error cleaning up temporary directory: {e}")
        _temp_dir = None

# Register cleanup function
atexit.register(cleanup_qdrant)

@st.cache_resource
def get_vectorstore():
    """Initialize or get the Qdrant vector store."""
    
    # Check for API key
    openai_key = st.session_state.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("OpenAI API key is required for embeddings. Please enter it in the sidebar.")
    
    global _client, _temp_dir
    
    # Create a unique temporary directory for this session
    if _temp_dir is None:
        _temp_dir = tempfile.mkdtemp(prefix="qdrant_")
        logger.info(f"Created temporary directory for Qdrant: {_temp_dir}")
    
    # Initialize client if not exists
    if _client is None:
        try:
            _client = QdrantClient(
                path=_temp_dir,
                prefer_grpc=True
            )
            
            # Initialize collection if it doesn't exist
            collections = _client.get_collections().collections
            if not any(collection.name == "documents" for collection in collections):
                _client.create_collection(
                    collection_name="documents",
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
                logger.info("Created new Qdrant collection: documents")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {str(e)}")
            raise
    
    # Create embeddings with API key
    embedding_model = OpenAIEmbeddings(
        openai_api_key=openai_key
    )
    
    return QdrantVectorStore(
        client=_client,
        collection_name="documents",
        embedding=embedding_model,
    ) 