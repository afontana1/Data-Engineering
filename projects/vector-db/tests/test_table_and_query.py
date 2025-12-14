import numpy as np
import pytest

from vector_db import InMemoryVectorDB, HashEmbedding, Query
from vector_db.distances import DistanceMetric


def setup_table():
    db = InMemoryVectorDB("test").connect()
    db.register_embedding("hash", HashEmbedding(dim=16))
    table = db.create_table(
        name="docs",
        embedding="hash",
        schema={"title": str, "text": str, "category": str, "views": int},
        text_fields=["title", "text"],
    )
    return table


def test_add_and_vector_dimension_validation():
    table = setup_table()
    # Missing vector and non-string text should fail
    with pytest.raises(ValueError):
        table.add({"title": "x", "text": None})
    # Wrong dimension vector fails
    with pytest.raises(ValueError):
        table.add({"title": "x", "text": "hello"}, vector=np.zeros(8))
    rec = table.add({"title": "hello", "text": "world"}, vector=np.zeros(16))
    assert rec.id in [r.id for r in table.all_records()]


def test_upsert_and_update_paths():
    table = setup_table()
    rec = table.upsert("1", {"title": "a", "text": "b"}, vector=np.ones(16))
    assert rec.payload["title"] == "a"
    updated = table.upsert("1", {"title": "c", "text": "d"}, vector=np.ones(16) * 2)
    assert updated.payload["title"] == "c"
    assert np.allclose(updated.vector, np.ones(16) * 2)


def test_delete_and_indices_sync():
    table = setup_table()
    rec1 = table.add({"title": "t1", "text": "hello world", "views": 5}, vector=np.ones(16))
    rec2 = table.add({"title": "t2", "text": "another doc", "views": 10}, vector=np.ones(16) * 2)
    table.create_btree_index("views")
    # ensure indices built
    assert table.list_indices()

    table.delete(rec1.id)
    # rec1 should not appear in searches
    vec_results = table.vector_search(np.ones(16), k=5)
    ids = [r.id for r, _ in vec_results]
    assert rec1.id not in ids
    text_results = table.text_search("hello", k=5)
    ids = [r.id for r, _ in text_results]
    assert rec1.id not in ids


def test_hybrid_and_query_builder():
    table = setup_table()
    rec1 = table.add({"title": "cats", "text": "cats are great", "category": "pets"}, vector=np.ones(16))
    rec2 = table.add({"title": "dogs", "text": "dogs are loyal", "category": "pets"}, vector=np.ones(16) * 2)

    # hybrid search should return something
    combined = table.hybrid_search("cats", k=2, alpha=0.5)
    assert len(combined) == 2

    # Query builder chaining
    q = (
        Query(table)
        .filter(category="pets")
        .vector_search(rec1.vector, k=2)
        .use_index("default")
        .metric(DistanceMetric.COSINE)
        .limit(1)
    )
    results = q.execute()
    assert len(results) == 1
    assert results[0]["category"] == "pets"


def test_query_offset_and_projection():
    table = setup_table()
    for i in range(5):
        table.add({"title": f"t{i}", "text": "hello world", "category": "c"}, vector=np.ones(16) * i)
    q = Query(table).text_search("hello", k=10).offset(2).limit(2).select(["title"])
    rows = q.execute()
    assert len(rows) == 2
    for row in rows:
        assert set(row.keys()) == {"id", "title"}
