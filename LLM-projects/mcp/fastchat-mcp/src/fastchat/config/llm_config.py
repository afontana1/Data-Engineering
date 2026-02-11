import os
from ..app.chat.features.llm_provider import LLMProvider


class ConfigLLM:
    DEFAULT_PROVIDER: LLMProvider = LLMProvider.OPENAI
    DEFAULT_HISTORY_LEN: int = 20


class ConfigGPT:
    MODEL_PRICE = {
        "gpt-3.5-turbo": {
            "input": 0.5 / 1000000,
            "output": 1.5 / 1000000,
        },
        "gpt-4o-mini": {
            "input": 0.15 / 1000000,
            "output": 0.60 / 1000000,
        },
        "gpt-5-mini": {
            "input": 0.25 / 1000000,
            "output": 2.00 / 1000000,
        },
        "gpt-5-nano": {
            "input": 0.05 / 1000000,
            "output": 0.40 / 1000000,
        },
    }
    """Price by one tokens from each model"""

    # DEFAULT_MODEL_NAME = "gpt-4o-mini"
    DEFAULT_MODEL_NAME = "gpt-5-nano"
    """GPT model that will be used"""

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    """OpenAI Api Key"""
