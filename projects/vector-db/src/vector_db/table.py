from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np

from .embeddings import EmbeddingFunction
from .records import Record, TableMetadata
from .distances import DistanceMetric
from .indexes import (
    VectorIndex,
    BruteForceIndex,
    KDTreeIndex,
    IVFFlatIndex,
    LSHIndex,
    FullTextIndex,
    BTreeIndex,
)


class VectorTable:
    """
    Represents a collection (table) of vectors + metadata and associated indices.
    """

    def __init__(
        self,
        name: str,
        embedding: EmbeddingFunction,
        schema: Optional[Dict[str, type]] = None,
        text_fields: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ):
        self.metadata = TableMetadata(
            name=name,
            version=1,
            schema=schema or {},
            tags=tags or [],
        )
        self.embedding = embedding
        self._records: Dict[str, Record] = {}
        self._vector_indices: Dict[str, VectorIndex] = {}
        self._fts = FullTextIndex(fields=text_fields or ["text"])
        self._btree_indices: Dict[str, BTreeIndex] = {}

        # default brute-force index
        self.create_vector_index("default", index_type="bruteforce")

    # ---------- schema & metadata ----------

    def add_column(self, name: str, col_type: type) -> None:
        if name in self.metadata.schema:
            raise ValueError(f"Column {name} already exists")
        self.metadata.schema[name] = col_type

    def alter_column(self, name: str, new_type: type) -> None:
        if name not in self.metadata.schema:
            raise ValueError(f"Column {name} does not exist")
        self.metadata.schema[name] = new_type

    # ---------- index management ----------

    def create_vector_index(
        self,
        name: str,
        index_type: str = "bruteforce",
        metric: DistanceMetric = DistanceMetric.COSINE,
        **kwargs: Any,
    ) -> None:
        dim = self.embedding.dimension
        if index_type == "bruteforce":
            index = BruteForceIndex(dim, metric)
        elif index_type == "kdtree":
            index = KDTreeIndex(dim, metric)
        elif index_type == "ivfflat":
            index = IVFFlatIndex(dim, metric, **kwargs)
        elif index_type == "lsh":
            index = LSHIndex(dim, metric, **kwargs)
        else:
            raise ValueError(f"Unknown index_type: {index_type}")
        index.build_from(self._records.values())
        self._vector_indices[name] = index

    def create_btree_index(self, field: str) -> None:
        idx = BTreeIndex(field)
        idx.build_from(self._records.values())
        self._btree_indices[field] = idx

    def list_indices(self) -> List[str]:
        return list(self._vector_indices.keys())

    # ---------- CRUD ----------

    def _ensure_vector(self, vector: Optional[np.ndarray], payload: Dict[str, Any]) -> np.ndarray:
        if vector is not None:
            v = np.array(vector, dtype=np.float32)
            if v.shape[0] != self.embedding.dimension:
                raise ValueError(
                    f"Vector dimension {v.shape[0]} does not match table dim {self.embedding.dimension}"
                )
            return v
        text = payload.get("text")
        if not isinstance(text, str):
            raise ValueError("Either 'vector' must be provided or payload['text'] must be a string.")
        return self.embedding.embed(text)

    def add(
        self,
        payload: Dict[str, Any],
        vector: Optional[np.ndarray] = None,
        record_id: Optional[str] = None,
    ) -> Record:
        import uuid

        record_id = record_id or str(uuid.uuid4())
        vec = self._ensure_vector(vector, payload)
        rec = Record(id=record_id, vector=vec, payload=payload)
        if record_id in self._records:
            raise ValueError(f"Record with id {record_id} already exists")
        self._records[record_id] = rec

        self._fts.add(rec)
        for idx in self._vector_indices.values():
            idx.add(rec)
        for idx in self._btree_indices.values():
            idx.add(rec)

        return rec

    def delete(self, record_id: str) -> None:
        rec = self._records.pop(record_id, None)
        if not rec:
            return
        self._fts.remove(record_id)
        for idx in self._vector_indices.values():
            idx.remove(record_id)
        for idx in self._btree_indices.values():
            idx.remove(record_id)

    def update(
        self,
        record_id: str,
        payload: Optional[Dict[str, Any]] = None,
        vector: Optional[np.ndarray] = None,
    ) -> Record:
        if record_id not in self._records:
            raise KeyError(f"Record {record_id} not found")
        old = self._records[record_id]
        new_payload = payload if payload is not None else old.payload.copy()
        vec = self._ensure_vector(vector, new_payload) if vector is not None else old.vector
        rec = Record(id=record_id, vector=vec, payload=new_payload)
        self._records[record_id] = rec

        self._fts.update(rec)
        for idx in self._vector_indices.values():
            idx.update(rec)
        for idx in self._btree_indices.values():
            idx.update(rec)

        return rec

    def merge(self, record_id: str, patch: Dict[str, Any]) -> Record:
        if record_id not in self._records:
            raise KeyError(f"Record {record_id} not found")
        payload = self._records[record_id].payload.copy()
        payload.update(patch)
        return self.update(record_id, payload=payload)

    def upsert(
        self,
        record_id: str,
        payload: Dict[str, Any],
        vector: Optional[np.ndarray] = None,
    ) -> Record:
        if record_id in self._records:
            return self.update(record_id, payload=payload, vector=vector)
        return self.add(payload=payload, vector=vector, record_id=record_id)

    def all_records(self) -> Iterable[Record]:
        return self._records.values()

    # ---------- search APIs ----------

    def vector_search(
        self,
        query_vector: np.ndarray,
        k: int = 10,
        index_name: str = "default",
        metric: Optional[DistanceMetric] = None,
    ) -> List[Tuple[Record, float]]:
        if index_name not in self._vector_indices:
            raise KeyError(f"Index {index_name} not found")
        index = self._vector_indices[index_name]
        if metric is not None and metric != index.metric:
            raise ValueError(f"Index metric is {index.metric}, but {metric} requested")

        results = index.search(np.array(query_vector, dtype=np.float32), k=k)
        return [(self._records[rid], dist) for rid, dist in results if rid in self._records]

    def text_search(self, query: str, k: int = 10) -> List[Tuple[Record, float]]:
        results = self._fts.search(query, k=k)
        return [(self._records[rid], dist) for rid, dist in results if rid in self._records]

    def hybrid_search(
        self,
        text: str,
        k: int = 10,
        index_name: str = "default",
        alpha: float = 0.5,
        metric: DistanceMetric = DistanceMetric.COSINE,
    ) -> List[Tuple[Record, float]]:
        vec_query = self.embedding.embed(text)
        vec_results = {r.id: dist for r, dist in self.vector_search(vec_query, k=k * 3, index_name=index_name, metric=metric)}
        text_results = {r.id: dist for r, dist in self.text_search(text, k=k * 3)}

        ids = set(vec_results.keys()) | set(text_results.keys())
        if not ids:
            return []

        def normalize(d: Dict[str, float]) -> Dict[str, float]:
            if not d:
                return {}
            vals = np.array(list(d.values()), dtype=np.float32)
            mn, mx = float(vals.min()), float(vals.max())
            if mn == mx:
                return {rid: 0.5 for rid in d.keys()}
            return {rid: (val - mn) / (mx - mn) for rid, val in d.items()}

        vec_norm = normalize(vec_results)
        txt_norm = normalize(text_results)

        combined: List[Tuple[Record, float]] = []
        for rid in ids:
            dv = vec_norm.get(rid, 1.0)
            dt = txt_norm.get(rid, 1.0)
            score = alpha * dv + (1 - alpha) * dt
            combined.append((self._records[rid], score))

        combined.sort(key=lambda x: x[1])
        return combined[:k]
