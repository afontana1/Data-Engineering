from typing import List

from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import BaseModel, Extra
from ollama import Client, AsyncClient


class CustomOllamaEmbeddings(BaseModel, Embeddings):
    """CustomOllamaEmbeddings embedding model.

    Example:
        .. code-block:: python

            from langchain_ollama import CustomOllamaEmbeddings

            model = CustomOllamaEmbeddings(model="llama3", base_url="http://localhost:11434")
            embedder.embed_query("what is the place that jonathan worked at?")
    """

    model: str
    """Model name to use."""

    base_url: str
    """Base URL for the Ollama service."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""
        embedded_docs = []
        client = Client(host=self.base_url)
        for doc in texts:
            embedded_docs.append(list(client.embeddings(self.model, doc)["embedding"]))
        return embedded_docs

    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""
        return self.embed_documents([text])[0]

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""
        embedded_docs = []
        async_client = AsyncClient(host=self.base_url)
        for doc in texts:
            embedded_docs.append(
                list((await async_client.embeddings(self.model, doc))["embedding"])
            )
        return embedded_docs

    async def aembed_query(self, text: str) -> List[float]:
        """Embed query text."""
        return (await self.aembed_documents([text]))[0]
