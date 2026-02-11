from abc import abstractmethod
from typing import Any, Dict, List, Optional, Protocol, TypedDict


class EmbeddingOptions(TypedDict, total=False):
    model: str
    dimensions: int


class Prompts:
    messages: List[Any]


class LLMOptions(TypedDict, total=False):
    # TODO: Rip this into LLMOptions for consistency
    model: str
    llm_params: Dict[str, Any]
    embedding_params: Optional[EmbeddingOptions]


class LanguageModel(Protocol):
    def __init__(self, **opts: LLMOptions): ...

    @abstractmethod
    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    def get_response_sync(
        self,
        messages: Prompts,
    ) -> Optional[str]: ...

    def get_embedding(self, text: str) -> List[float]: ...
