from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np

from .base import VectorIndex
from ..distances import DistanceMetric
from ..records import Record


class _KDNode:
    __slots__ = ("point", "record_id", "left", "right", "axis")

    def __init__(self, point: np.ndarray, record_id: str, axis: int):
        self.point = point
        self.record_id = record_id
        self.left: Optional["_KDNode"] = None
        self.right: Optional["_KDNode"] = None
        self.axis = axis


class KDTreeIndex(VectorIndex):
    """
    Simple KD-tree for exact nearest neighbors in moderate dimensions.

    This implementation supports euclidean distance only.
    """

    def __init__(self, dim: int, metric: DistanceMetric = DistanceMetric.EUCLIDEAN):
        if metric is not DistanceMetric.EUCLIDEAN:
            raise ValueError("KDTreeIndex supports only euclidean distance.")
        super().__init__(dim, metric)
        self.root: Optional[_KDNode] = None
        self._records: Dict[str, np.ndarray] = {}

    def build_from(self, records: Iterable[Record]) -> None:
        self._records = {r.id: r.vector.astype(np.float32) for r in records}
        points = [(rid, vec) for rid, vec in self._records.items()]
        self.root = self._build(points, depth=0)

    def _build(self, items: List[Tuple[str, np.ndarray]], depth: int) -> Optional[_KDNode]:
        if not items:
            return None
        axis = depth % self.dim
        items.sort(key=lambda x: x[1][axis])
        mid = len(items) // 2
        rid, point = items[mid]
        node = _KDNode(point, rid, axis)
        node.left = self._build(items[:mid], depth + 1)
        node.right = self._build(items[mid + 1 :], depth + 1)
        return node

    def add(self, record: Record) -> None:
        self._records[record.id] = record.vector.astype(np.float32)
        self.build_from([Record(rid, v) for rid, v in self._records.items()])

    def remove(self, record_id: str) -> None:
        if record_id in self._records:
            del self._records[record_id]
            self.build_from([Record(rid, v) for rid, v in self._records.items()])

    def update(self, record: Record) -> None:
        self.add(record)

    def search(self, query: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        if self.root is None:
            return []
        query = query.astype(np.float32)
        best: List[Tuple[str, float]] = []

        def visit(node: Optional[_KDNode], depth: int = 0) -> None:
            nonlocal best
            if node is None:
                return
            d = self._dist(query, node.point)
            best.append((node.record_id, d))
            best.sort(key=lambda x: x[1])
            if len(best) > k:
                best.pop()

            axis = node.axis
            diff = query[axis] - node.point[axis]
            first, second = (node.left, node.right) if diff < 0 else (node.right, node.left)
            visit(first, depth + 1)
            if len(best) < k or abs(diff) < best[-1][1]:
                visit(second, depth + 1)

        visit(self.root, 0)
        best.sort(key=lambda x: x[1])
        return best[:k]
