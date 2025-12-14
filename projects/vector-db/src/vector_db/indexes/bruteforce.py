from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

import numpy as np

from .base import VectorIndex
from ..distances import DistanceMetric
from ..records import Record


class BruteForceIndex(VectorIndex):
    """Linear scan index. Simple but robust baseline."""

    def __init__(self, dim: int, metric: DistanceMetric = DistanceMetric.COSINE):
        super().__init__(dim, metric)
        self._vectors: Dict[str, np.ndarray] = {}

    def build_from(self, records: Iterable[Record]) -> None:
        self._vectors = {r.id: r.vector.astype(np.float32) for r in records}

    def add(self, record: Record) -> None:
        self._vectors[record.id] = record.vector.astype(np.float32)

    def remove(self, record_id: str) -> None:
        self._vectors.pop(record_id, None)

    def update(self, record: Record) -> None:
        self._vectors[record.id] = record.vector.astype(np.float32)

    def search(self, query: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        query = query.astype(np.float32)
        results: List[Tuple[str, float]] = []
        for rid, vec in self._vectors.items():
            d = self._dist(query, vec)
            results.append((rid, d))
        results.sort(key=lambda x: x[1])
        return results[:k]
