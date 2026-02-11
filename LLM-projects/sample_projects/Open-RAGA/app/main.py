from fastapi import FastAPI, HTTPException
from .assistant import ChatManager
from .models.schemas import ChatInput, ChatOutput
from typing import Optional
from dotenv import load_dotenv
import os
from pathlib import Path
import logging
import traceback
import uvicorn
import time
from fastapi.middleware.cors import CORSMiddleware
import yaml
from .settings import MODEL_CONFIG_PATH,EMBD_MODEL_DIR,DOCS_PATH,VECTOR_STORE_PATH
from .src.llm.llm_factory import CHATLLMFactory
from .src.embedder.embedder_factory import EMBFactory
from .src.vector_database.vector_db_factory import VECTORDBFactory


print("=== Starting the app ===")



# Load environment variables
load_dotenv()

# Uvicorn logger
logger = logging.getLogger("uvicorn")

# Global variables to be initialized in startup
llm = None
embedder_pipe = None
vector_db = None
manager = None

# Nvidia API key
NVIDIA_NVC_API_KEY = os.getenv('NVIDIA_LLM_API')



# load config
def load_config(config_path=MODEL_CONFIG_PATH):
    
    """
    Loads a YAML configuration file safely from the given path.

    Args:
        filename (str): YAML filename.
        config_dir (str): Path to the directory containing the YAML config.

    Returns:
        dict: Parsed YAML config.
    """
  
    with open(MODEL_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)






# FastAPI app initialization
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    global llm, embedder_pipe, vector_db, manager

    try:
        start_time = time.perf_counter()

        # Load model config
        model_config = load_config()
        chat_llm_args = model_config['chat_llm_args']
        chat_llm_args['api_key'] = NVIDIA_NVC_API_KEY
        db_args = model_config['db_args']
        db_args['vector_store_path'] = VECTOR_STORE_PATH
        db_args['docs_path'] = DOCS_PATH
        embedder_args = model_config['embedder_args']
        embedder_args['model_path'] = EMBD_MODEL_DIR

        # Create pipelines
        llm_pipe = CHATLLMFactory.create_chat_model_pipeline(chat_llm_args['type'], **chat_llm_args)
        embedder_pipe = EMBFactory.create_embedder_model_pipeline(embedder_args['type'], **embedder_args)
        db_args['embedding_model'] = await embedder_pipe.load_model()
        vector_db_pipe = VECTORDBFactory.create_vector_db_pipeline(db_args['type'], **db_args)

        # Async load LLM and vector DB
        llm = await llm_pipe.load_model()
        elapsed = (time.perf_counter() - start_time) * 1000
        logger.info(f"⚡ Latency (llm initialization): {elapsed:.2f} ms")

        start_time = time.perf_counter()
        vector_db = await vector_db_pipe.load_faiss_db()
        elapsed = (time.perf_counter() - start_time) * 1000
        logger.info(f"⚡ Latency (vector initialization): {elapsed:.2f} ms")

        # Initialize ChatManager
        manager = ChatManager(llm, vector_db.as_retriever())

        # Vector DB test
        _ = vector_db.as_retriever().invoke("startup test")

        logger.info("✅ All components initialized successfully.")

    except Exception as e:
        logger.error("❌ Error during startup: %s", traceback.format_exc())
        raise RuntimeError("Startup initialization failed.")


@app.get("/")
def health_check():
    return {'health': 'ok'}


@app.post("/chat", response_model=ChatOutput)
async def get_response(request: ChatInput):
    global manager

    try:
        logger.info(f"📥 Received query: {request.query}")
        logger.info(f"📚 Context: {request.last_3_turn}")

        start_time = time.perf_counter()
        response = await manager.run(request.query, request.last_3_turn)
        elapsed = (time.perf_counter() - start_time) * 1000

        logger.info(f"⚡ Latency (model response): {elapsed:.2f} ms")
        logger.info(f"📤 Returning response: {response}")

        return {'response': response}

    except Exception as e:
        logger.error("❌ Error processing request: %s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

