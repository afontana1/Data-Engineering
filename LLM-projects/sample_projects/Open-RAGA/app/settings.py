from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# this settings.py file contains all path needed for different modules

MODEL_CONFIG_PATH = BASE_DIR / "app"  / "config" /  "prod" / "model_config.yaml"
DOCS_PATH = BASE_DIR /  "app" /"data" / "preprocessed" 
EMBD_MODEL_DIR = BASE_DIR / "app" / "src" / "embedder" / "model_checkpoints" 
VECTOR_STORE_PATH = BASE_DIR / "app" / "data" / "vector_db" / "knowledge_base" 
PROMPT_TEMPLATES_PATH = BASE_DIR / "app" / "generation" / "prompt_templates.yaml"

