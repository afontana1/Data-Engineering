import numpy as np

from vector_db.distances import DistanceMetric, DISTANCE_FUNCS


def test_cosine_distance_basic():
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    dist = DISTANCE_FUNCS[DistanceMetric.COSINE](a, b)
    assert dist == 1.0


def test_cosine_distance_zero_norm_returns_one():
    a = np.zeros(3)
    b = np.array([1.0, 2.0, 3.0])
    dist = DISTANCE_FUNCS[DistanceMetric.COSINE](a, b)
    assert dist == 1.0


def test_euclidean_distance_matches_numpy():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 6.0, 3.0])
    dist = DISTANCE_FUNCS[DistanceMetric.EUCLIDEAN](a, b)
    assert np.isclose(dist, np.linalg.norm(a - b))


def test_dot_distance_negates_dot_product():
    a = np.array([1.0, 2.0])
    b = np.array([-2.0, 0.5])
    dist = DISTANCE_FUNCS[DistanceMetric.DOT](a, b)
    assert dist == -float(np.dot(a, b))
