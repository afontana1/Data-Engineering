import numpy as np

from vector_db.indexes import BruteForceIndex, KDTreeIndex, IVFFlatIndex, LSHIndex
from vector_db.distances import DistanceMetric
from vector_db.records import Record


def make_records(n: int = 5, dim: int = 3):
    recs = []
    rng = np.random.default_rng(0)
    for i in range(n):
        vec = rng.normal(size=dim).astype(np.float32)
        recs.append(Record(id=str(i), vector=vec, payload={}))
    return recs


def test_bruteforce_index_search_orders_by_distance():
    idx = BruteForceIndex(dim=3, metric=DistanceMetric.EUCLIDEAN)
    recs = make_records(3, dim=3)
    idx.build_from(recs)
    query = recs[0].vector
    results = idx.search(query, k=3)
    assert results[0][0] == recs[0].id
    assert len(results) == 3


def test_kdtree_build_and_search_matches_bruteforce_small_set():
    recs = make_records(6, dim=2)
    bf = BruteForceIndex(dim=2, metric=DistanceMetric.EUCLIDEAN)
    bf.build_from(recs)

    kd = KDTreeIndex(dim=2, metric=DistanceMetric.EUCLIDEAN)
    kd.build_from(recs)

    query = recs[1].vector
    got_kd = kd.search(query, k=3)
    got_bf = bf.search(query, k=3)
    assert [r for r, _ in got_kd] == [r for r, _ in got_bf]


def test_ivfflat_build_and_search_returns_results():
    recs = make_records(12, dim=4)
    idx = IVFFlatIndex(dim=4, metric=DistanceMetric.COSINE, n_lists=4, n_probe=2, max_train_iters=3)
    idx.build_from(recs)
    query = recs[0].vector
    results = idx.search(query, k=5)
    assert len(results) > 0


def test_lsh_index_exact_bucket_matches():
    idx = LSHIndex(dim=3, metric=DistanceMetric.COSINE, n_planes=8)
    rec = Record(id="a", vector=np.ones(3, dtype=np.float32), payload={})
    idx.build_from([rec])
    # Same vector should hash to same bucket and be returned
    results = idx.search(np.ones(3, dtype=np.float32), k=1)
    assert results[0][0] == "a"
