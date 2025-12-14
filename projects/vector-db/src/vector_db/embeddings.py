from __future__ import annotations

from typing import Protocol, Callable, Sequence, Union

import numpy as np


class EmbeddingFunction(Protocol):
    """Interface for embedding functions."""

    @property
    def dimension(self) -> int:
        ...

    def embed(self, text: str) -> np.ndarray:
        ...


class CallableEmbedding:
    """
    Wrap a plain function into an EmbeddingFunction.

    func: (text: str) -> np.ndarray or Sequence[float]
    dim: embedding dimension
    """

    def __init__(self, func: Callable[[str], Union[np.ndarray, Sequence[float]]], dim: int):
        self._func = func
        self._dim = dim

    @property
    def dimension(self) -> int:
        return self._dim

    def embed(self, text: str) -> np.ndarray:
        v = self._func(text)
        if not isinstance(v, np.ndarray):
            v = np.array(v, dtype=np.float32)
        if v.shape[0] != self._dim:
            raise ValueError(f"Expected embedding dimension {self._dim}, got {v.shape[0]}")
        return v.astype(np.float32)


class HashEmbedding(EmbeddingFunction):
    """
    Toy embedding for demos: hash tokens into a fixed-size vector.

    DO NOT use in production; this is just to keep the project self-contained.
    """

    def __init__(self, dim: int = 64):
        self._dim = dim

    @property
    def dimension(self) -> int:
        return self._dim

    def embed(self, text: str) -> np.ndarray:
        vec = np.zeros(self._dim, dtype=np.float32)
        for token in text.split():
            h = hash(token)
            idx = abs(h) % self._dim
            vec[idx] += 1.0
        norm = float(np.linalg.norm(vec))
        if norm > 0:
            vec /= norm
        return vec
