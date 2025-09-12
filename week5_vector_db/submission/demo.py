"""
demo.py
-------
Demo for Assignment 3: Performance optimization.
"""

from submission.search import (
    index_texts,
    semantic_search,
    semantic_search_with_filter,
    hybrid_search,
    rerank_results,
    get_search_stats
)

if __name__ == "__main__":
    # Example docs
    docs = [
        "Python is a popular programming language.",
        "Machine learning enables computers to learn from data.",
        "Vector databases store embeddings for semantic search.",
        "OpenAI develops advanced AI models.",
        "Deep learning is a subset of machine learning.",
        "ChromaDB and Pinecone are popular vector databases.",
    ]
    ids = [f"doc{i+1}" for i in range(len(docs))]
    metadatas = [
        {"category": "programming"},
        {"category": "ml"},
        {"category": "db"},
        {"category": "ai"},
        {"category": "ml"},
        {"category": "db"},
    ]

    # Index with batching
    index_texts(docs, metadatas, ids, batch_size=2)

    print("\n=== Normal Search ===")
    results = semantic_search("What is a vector database?", top_k=3)
    for r in results:
        print(r)

    print("\n=== Hybrid Search ===")
    results = hybrid_search("machine learning", top_k=3)
    for r in results:
        print(r)

    print("\n=== Reranked Results ===")
    base_results = semantic_search("AI models", top_k=3)
    reranked = rerank_results("AI models", base_results)
    for r in reranked:
        print(r)

    print("\n=== Analytics & Performance ===")
    stats = get_search_stats()
    print(stats)


