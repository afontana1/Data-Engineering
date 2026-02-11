from semantic_router import Route
from typing import Dict, Any, List, Union, Optional
from langchain_core.language_models.llms import LLM

from dummy_llm import DummyLLM


class ExtendedRoute(Route):
    """This class extends the Route class to include a dummy llm for testing purposes."""
    responses: Optional[List[str]]
    langchain_llm: Optional[Union[DummyLLM, LLM]]

    def __init__(self, config: Dict[str, Any]):
        # initialize parent
        super().__init__(**config)

        # extract relevance data from config
        self.responses = config.get('responses', [])
        if self.responses:
            # initialize dummy llm with pre-defined responses
            self.langchain_llm = DummyLLM(responses=self.responses)
