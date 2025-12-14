from __future__ import annotations

from vector_db import (
    InMemoryVectorDB,
    HashEmbedding,
    Query,
)


def main() -> None:
    db = InMemoryVectorDB("demo").connect()

    # register an embedding implementation
    db.register_embedding("hash-64", HashEmbedding(dim=64))

    # create a table
    articles = db.create_table(
        name="articles",
        embedding="hash-64",
        schema={"title": str, "text": str, "category": str},
        text_fields=["title", "text"],
        tags=["demo"],
    )

    # insert some records
    articles.add({"title": "Intro to vectors", "text": "Vectors in linear algebra", "category": "math"})
    articles.add({"title": "Intro to graphs", "text": "Graph algorithms and shortest paths", "category": "cs"})
    articles.add({"title": "Neural networks", "text": "Deep learning with vectors and matrices", "category": "ml"})

    # additional indices
    articles.create_vector_index("ivf", index_type="ivfflat", n_lists=4, n_probe=2)
    articles.create_vector_index("lsh", index_type="lsh", n_planes=12)

    query_text = "vectors and matrices"
    q_vec = articles.embedding.embed(query_text)

    q = (
        Query(articles)
        .where(lambda r: r.payload.get("category") != "cs")
        .vector_search(q_vec, k=5)
        .use_index("ivf")
        .limit(5)
    )

    results = q.execute()
    for row in results:
        print(row["id"], row.get("title"), row.get("category"))


if __name__ == "__main__":
    main()
