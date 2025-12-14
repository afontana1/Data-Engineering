from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

import numpy as np

from .base import VectorIndex
from ..distances import DistanceMetric
from ..records import Record


class LSHIndex(VectorIndex):
    """
    Locality Sensitive Hashing for cosine similarity via random hyperplanes.

    This is an approximate nearest-neighbor index.
    """

    def __init__(
        self,
        dim: int,
        metric: DistanceMetric = DistanceMetric.COSINE,
        n_planes: int = 16,
    ):
        if metric != DistanceMetric.COSINE:
            raise ValueError("LSHIndex here is implemented for cosine distance only.")
        super().__init__(dim, metric)
        self.n_planes = n_planes
        self.planes = np.random.randn(n_planes, dim).astype(np.float32)
        self.buckets: Dict[int, Dict[str, np.ndarray]] = {}

    def _hash(self, v: np.ndarray) -> int:
        signs = (self.planes @ v) >= 0
        h = 0
        for bit in signs:
            h = (h << 1) | int(bool(bit))
        return h

    def build_from(self, records: Iterable[Record]) -> None:
        self.buckets = {}
        for r in records:
            self.add(r)

    def add(self, record: Record) -> None:
        h = self._hash(record.vector.astype(np.float32))
        self.buckets.setdefault(h, {})[record.id] = record.vector.astype(np.float32)

    def remove(self, record_id: str) -> None:
        for bucket in self.buckets.values():
            bucket.pop(record_id, None)

    def update(self, record: Record) -> None:
        self.remove(record.id)
        self.add(record)

    def search(self, query: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        query = query.astype(np.float32)
        h = self._hash(query)
        candidates = self.buckets.get(h, {})
        if len(candidates) < k:
            candidates = {rid: v for bucket in self.buckets.values() for rid, v in bucket.items()}
        results: List[Tuple[str, float]] = []
        for rid, vec in candidates.items():
            d = self._dist(query, vec)
            results.append((rid, d))
        results.sort(key=lambda x: x[1])
        return results[:k]
