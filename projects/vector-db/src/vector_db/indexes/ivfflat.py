from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

import numpy as np

from .base import VectorIndex
from ..distances import DistanceMetric
from ..records import Record


class IVFFlatIndex(VectorIndex):
    """
    Very simple IVF-Flat index.

    - Trains centroids with Lloyd iterations (k-means-like).
    - Assigns vectors to nearest centroid (inverted lists).
    - Searches only n_probe closest centroid lists.
    """

    def __init__(
        self,
        dim: int,
        metric: DistanceMetric = DistanceMetric.COSINE,
        n_lists: int = 10,
        n_probe: int = 3,
        max_train_iters: int = 10,
    ):
        super().__init__(dim, metric)
        self.n_lists = n_lists
        self.n_probe = n_probe
        self.max_train_iters = max_train_iters
        self.centroids: np.ndarray | None = None
        self.inverted_lists: Dict[int, Dict[str, np.ndarray]] = {i: {} for i in range(n_lists)}

    def build_from(self, records: Iterable[Record]) -> None:
        recs = list(records)
        if not recs:
            self.centroids = None
            self.inverted_lists = {i: {} for i in range(self.n_lists)}
            return

        X = np.stack([r.vector.astype(np.float32) for r in recs])
        n = X.shape[0]
        if n < self.n_lists:
            self.n_lists = n
        indices = np.random.choice(n, self.n_lists, replace=False)
        centroids = X[indices].copy()

        for _ in range(self.max_train_iters):
            assignments = self._assign_to_centroids(X, centroids)
            for i in range(self.n_lists):
                mask = assignments == i
                if not np.any(mask):
                    continue
                centroids[i] = X[mask].mean(axis=0)

        self.centroids = centroids
        self.inverted_lists = {i: {} for i in range(self.n_lists)}
        for r in recs:
            cid = int(self._assign_to_centroids(r.vector[None, :], self.centroids)[0])
            self.inverted_lists[cid][r.id] = r.vector.astype(np.float32)

    def _assign_to_centroids(self, X: np.ndarray, centroids: np.ndarray) -> np.ndarray:
        dists = np.sum((X[:, None, :] - centroids[None, :, :]) ** 2, axis=2)
        return np.argmin(dists, axis=1)

    def add(self, record: Record) -> None:
        if self.centroids is None:
            self.centroids = record.vector.astype(np.float32)[None, :]
            self.n_lists = 1
            self.inverted_lists = {0: {record.id: record.vector.astype(np.float32)}}
            return
        cid = int(self._assign_to_centroids(record.vector[None, :], self.centroids)[0])
        self.inverted_lists.setdefault(cid, {})[record.id] = record.vector.astype(np.float32)

    def remove(self, record_id: str) -> None:
        for bucket in self.inverted_lists.values():
            bucket.pop(record_id, None)

    def update(self, record: Record) -> None:
        self.remove(record.id)
        self.add(record)

    def search(self, query: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        if self.centroids is None:
            return []
        query = query.astype(np.float32)
        dists_centroids = np.sum((self.centroids - query[None, :]) ** 2, axis=1)
        probe_ids = np.argsort(dists_centroids)[: self.n_probe]
        results: List[Tuple[str, float]] = []
        for cid in probe_ids:
            for rid, vec in self.inverted_lists.get(int(cid), {}).items():
                d = self._dist(query, vec)
                results.append((rid, d))
        results.sort(key=lambda x: x[1])
        return results[:k]
