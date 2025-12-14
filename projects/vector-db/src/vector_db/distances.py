from __future__ import annotations

from enum import Enum
from typing import Callable, Dict

import numpy as np


class DistanceMetric(str, Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT = "dot"


def _cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0.0:
        return 1.0
    return 1.0 - float(np.dot(a, b) / denom)


def _euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    diff = a - b
    return float(np.sqrt(np.dot(diff, diff)))


def _dot_distance(a: np.ndarray, b: np.ndarray) -> float:
    # Treat negative dot as a "distance" so lower is better.
    return float(-np.dot(a, b))


DISTANCE_FUNCS: Dict[DistanceMetric, Callable[[np.ndarray, np.ndarray], float]] = {
    DistanceMetric.COSINE: _cosine_distance,
    DistanceMetric.EUCLIDEAN: _euclidean_distance,
    DistanceMetric.DOT: _dot_distance,
}
