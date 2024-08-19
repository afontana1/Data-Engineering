import os

REDIS_HOST = os.environ.get("REDIS_HOST", "172.20.0.20")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
SCRIPT_NAME = os.environ.get("SCRIPT_NAME", "get_loan_features")
MODEL_NAME = os.environ.get("MODEL_NAME", "loan_model")
