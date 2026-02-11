import streamlit as st
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_env_variables():
    """Load environment variables from .env file."""
    # Try to load from .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    if os.path.exists(env_path):
        logger.info(f"Found .env file at {env_path}")
        load_dotenv(env_path)
        # Debug: Print loaded keys (masked)
        openai_key = os.getenv("OPENAI_API_KEY", "")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        logger.info(f"OpenAI key loaded: {'✓' if openai_key else '✗'}")
        logger.info(f"Anthropic key loaded: {'✓' if anthropic_key else '✗'}")
        return True
    logger.info("No .env file found")
    return False

def initialize_session_state():
    """Initialize session state variables."""
    # Load environment variables first
    env_loaded = load_env_variables()
    logger.info(f"Environment variables loaded: {env_loaded}")
    
    # Initialize basic state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = []
    
    if "model_name" not in st.session_state:
        st.session_state.model_name = "GPT-4o"
    
    if "document_structures" not in st.session_state:
        st.session_state.document_structures = {}
    
    # Initialize API keys from environment variables
    api_keys = {
        "openai_api_key": {
            "env_key": "OPENAI_API_KEY",
            "purpose": "embeddings and chat model"
        },
        "anthropic_api_key": {
            "env_key": "ANTHROPIC_API_KEY",
            "purpose": "chat model"
        }
    }
    
    # Load API keys from environment
    for session_key, config in api_keys.items():
        if session_key not in st.session_state:
            api_key = os.getenv(config["env_key"], "")
            if api_key:
                st.session_state[session_key] = api_key
                st.session_state.api_key_source = "env"
                # Ensure the environment variable is set
                os.environ[config["env_key"]] = api_key
                logger.info(f"Loaded {session_key} from environment")
            else:
                st.session_state[session_key] = ""
                st.session_state.api_key_source = "user"
                logger.info(f"No {session_key} found in environment")
        else:
            logger.info(f"{session_key} already in session state")