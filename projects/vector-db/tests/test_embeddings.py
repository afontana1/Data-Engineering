import numpy as np
import pytest

from vector_db.embeddings import CallableEmbedding, HashEmbedding


def test_callable_embedding_wraps_function_and_validates_dim():
    def emb(text: str):
        return [len(text), 0.0]

    wrapper = CallableEmbedding(emb, dim=2)
    vec = wrapper.embed("hi")
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (2,)
    assert vec.dtype == np.float32
    with pytest.raises(ValueError):
        bad = CallableEmbedding(emb, dim=3)
        bad.embed("hi")


def test_hash_embedding_normalizes_and_counts_tokens():
    emb = HashEmbedding(dim=8)
    vec = emb.embed("foo bar foo")
    assert vec.shape == (8,)
    assert np.isclose(np.linalg.norm(vec), 1.0)
    # Two occurrences of 'foo' should land in same bucket and have larger magnitude than singletons
    foo_bucket = abs(hash("foo")) % 8
    bar_bucket = abs(hash("bar")) % 8
    assert vec[foo_bucket] > vec[bar_bucket]
