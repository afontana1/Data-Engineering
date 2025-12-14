"""
vector_db: simple in-memory vector database with indices and query builder.
"""

from .distances import DistanceMetric
from .embeddings import EmbeddingFunction, CallableEmbedding, HashEmbedding
from .records import Record, TableMetadata
from .table import VectorTable
from .query import Query
from .database import InMemoryVectorDB

__all__ = [
    "DistanceMetric",
    "EmbeddingFunction",
    "CallableEmbedding",
    "HashEmbedding",
    "Record",
    "TableMetadata",
    "VectorTable",
    "Query",
    "InMemoryVectorDB",
]
