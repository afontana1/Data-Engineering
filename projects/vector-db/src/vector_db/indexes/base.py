from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List, Tuple

import numpy as np

from ..distances import DistanceMetric, DISTANCE_FUNCS
from ..records import Record


class VectorIndex(ABC):
    """Abstract base class for vector indices."""

    def __init__(self, dim: int, metric: DistanceMetric = DistanceMetric.COSINE):
        self.dim = dim
        self.metric = metric
        self._dist = DISTANCE_FUNCS[metric]

    @abstractmethod
    def build_from(self, records: Iterable[Record]) -> None:
        """(Re)build index from existing records."""
        ...

    @abstractmethod
    def add(self, record: Record) -> None:
        ...

    @abstractmethod
    def remove(self, record_id: str) -> None:
        ...

    @abstractmethod
    def update(self, record: Record) -> None:
        ...

    @abstractmethod
    def search(self, query: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        """
        Return list of (record_id, distance) pairs, sorted by distance ascending.
        """
        ...
