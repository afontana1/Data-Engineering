from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from .distances import DistanceMetric
from .records import Record
from .table import VectorTable


class Query:
    """
    Chainable query builder for a VectorTable.
    """

    def __init__(self, table: VectorTable):
        self._table = table
        self._where_preds: List[Callable[[Record], bool]] = []
        self._selected_fields: Optional[List[str]] = None
        self._limit: Optional[int] = None
        self._offset: int = 0
        self._rerank_fn: Optional[Callable[[Record, float], float]] = None

        self._vector_query: Optional[np.ndarray] = None
        self._text_query: Optional[str] = None
        self._k: int = 10
        self._index_name: str = "default"
        self._metric: DistanceMetric = DistanceMetric.COSINE
        self._hybrid_alpha: Optional[float] = None

    def select(self, fields: Sequence[str]) -> "Query":
        self._selected_fields = list(fields)
        return self

    def where(self, predicate: Callable[[Record], bool]) -> "Query":
        self._where_preds.append(predicate)
        return self

    def filter(self, **field_equals: Any) -> "Query":
        def pred(rec: Record) -> bool:
            return all(rec.payload.get(k) == v for k, v in field_equals.items())

        self._where_preds.append(pred)
        return self

    def limit(self, limit: int) -> "Query":
        self._limit = limit
        return self

    def offset(self, offset: int) -> "Query":
        self._offset = offset
        return self

    def rerank(self, fn: Callable[[Record, float], float]) -> "Query":
        self._rerank_fn = fn
        return self

    def metric(self, metric: DistanceMetric) -> "Query":
        self._metric = metric
        return self

    def use_index(self, index_name: str) -> "Query":
        self._index_name = index_name
        return self

    def vector_search(self, vec: np.ndarray, k: int = 10) -> "Query":
        self._vector_query = np.array(vec, dtype=np.float32)
        self._k = k
        self._hybrid_alpha = None
        return self

    def text_search(self, text: str, k: int = 10) -> "Query":
        self._text_query = text
        self._k = k
        self._hybrid_alpha = None
        return self

    def hybrid(self, text: str, k: int = 10, alpha: float = 0.5) -> "Query":
        self._text_query = text
        self._k = k
        self._hybrid_alpha = alpha
        return self

    def _apply_where(self, items: List[Tuple[Record, float]]) -> List[Tuple[Record, float]]:
        if not self._where_preds:
            return items
        out: List[Tuple[Record, float]] = []
        for rec, dist in items:
            if all(pred(rec) for pred in self._where_preds):
                out.append((rec, dist))
        return out

    def _apply_rerank(self, items: List[Tuple[Record, float]]) -> List[Tuple[Record, float]]:
        if not self._rerank_fn:
            return items
        reranked = [(rec, self._rerank_fn(rec, dist)) for rec, dist in items]
        reranked.sort(key=lambda x: x[1])
        return reranked

    def _apply_limit_offset(self, items: List[Tuple[Record, float]]) -> List[Tuple[Record, float]]:
        start = self._offset
        end = None if self._limit is None else (start + self._limit)
        return items[start:end]

    def _project(self, rec: Record) -> Dict[str, Any]:
        if not self._selected_fields:
            return {"id": rec.id, "vector": rec.vector, **rec.payload}
        out: Dict[str, Any] = {"id": rec.id}
        for f in self._selected_fields:
            if f == "vector":
                out["vector"] = rec.vector
            elif f in rec.payload:
                out[f] = rec.payload[f]
        return out

    def execute(self) -> List[Dict[str, Any]]:
        if self._hybrid_alpha is not None and self._text_query is not None:
            results = self._table.hybrid_search(
                text=self._text_query,
                k=self._k,
                index_name=self._index_name,
                alpha=self._hybrid_alpha,
                metric=self._metric,
            )
        elif self._vector_query is not None:
            results = self._table.vector_search(
                query_vector=self._vector_query,
                k=self._k,
                index_name=self._index_name,
                metric=self._metric,
            )
        elif self._text_query is not None:
            results = self._table.text_search(self._text_query, k=self._k)
        else:
            results = [(rec, 0.0) for rec in self._table.all_records()]

        items = self._apply_where(results)
        items = self._apply_rerank(items)
        items = self._apply_limit_offset(items)
        return [self._project(rec) for rec, _ in items]
