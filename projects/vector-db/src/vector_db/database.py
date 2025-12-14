from __future__ import annotations

from typing import Dict, List, Optional, Union

from .embeddings import EmbeddingFunction
from .table import VectorTable


class InMemoryVectorDB:
    """
    Top-level container for vector tables.

    - Manages connection lifecycle.
    - Manages tables.
    - Registers embedding functions.
    """

    def __init__(self, name: str = "default_db"):
        self.name = name
        self._connected: bool = False
        self._tables: Dict[str, VectorTable] = {}
        self._embeddings: Dict[str, EmbeddingFunction] = {}

    def connect(self) -> "InMemoryVectorDB":
        self._connected = True
        return self

    def close(self) -> None:
        self._connected = False

    def drop(self) -> None:
        """Drop all data in this in-memory DB."""
        self._tables.clear()
        self._embeddings.clear()
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    # ---- embeddings ----

    def register_embedding(self, name: str, embedding: EmbeddingFunction) -> None:
        self._embeddings[name] = embedding

    def get_embedding(self, name: str) -> EmbeddingFunction:
        if name not in self._embeddings:
            raise KeyError(f"Embedding {name} not registered")
        return self._embeddings[name]

    # ---- table management ----

    def create_table(
        self,
        name: str,
        embedding: Union[str, EmbeddingFunction],
        schema: Optional[dict] = None,
        text_fields: Optional[list[str]] = None,
        tags: Optional[list[str]] = None,
    ) -> VectorTable:
        if not self._connected:
            raise RuntimeError("Database is not connected. Call connect() first.")
        if name in self._tables:
            raise ValueError(f"Table {name} already exists")

        if isinstance(embedding, str):
            emb = self.get_embedding(embedding)
        else:
            emb = embedding

        table = VectorTable(
            name=name,
            embedding=emb,
            schema=schema,
            text_fields=text_fields,
            tags=tags,
        )
        self._tables[name] = table
        return table

    def open_table(self, name: str) -> VectorTable:
        if not self._connected:
            raise RuntimeError("Database is not connected. Call connect() first.")
        if name not in self._tables:
            raise KeyError(f"Table {name} not found")
        return self._tables[name]

    def drop_table(self, name: str) -> None:
        self._tables.pop(name, None)

    def list_tables(self) -> List[str]:
        return list(self._tables.keys())
