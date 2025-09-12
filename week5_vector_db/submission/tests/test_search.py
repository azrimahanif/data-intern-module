# tests/test_search.py
import pytest
from submission.search import (
    index_texts,
    semantic_search,
    semantic_search_with_filter,
    hybrid_search,
    rerank_results,
    get_search_stats
)

@pytest.fixture(scope="module", autouse=True)
def setup_data():
    """Index contoh dokumen untuk semua test"""
    docs = [
        "Python is a popular programming language.",
        "Machine learning enables computers to learn from data.",
        "Vector databases store embeddings for semantic search.",
        "OpenAI develops advanced AI models.",
        "Deep learning is a subset of machine learning.",
    ]
    ids = [f"doc{i+1}" for i in range(len(docs))]
    metadatas = [
        {"category": "programming"},
        {"category": "ml"},
        {"category": "db"},
        {"category": "ai"},
        {"category": "ml"},
    ]
    index_texts(docs, metadatas, ids)


def test_semantic_search():
    results = semantic_search("What is a vector database?", top_k=2)
    assert len(results) > 0
    assert "vector" in results[0]["text"].lower()


def test_filter_search():
    results = semantic_search_with_filter("machine learning", {"category": "ml"}, top_k=2)
    assert all(r["metadata"]["category"] == "ml" for r in results)


def test_hybrid_search():
    results = hybrid_search("AI models", top_k=2)
    assert len(results) > 0
    assert any("AI" in r["text"] or "ai" in r["text"].lower() for r in results)


def test_rerank_results():
    results = semantic_search("machine learning", top_k=3)
    reranked = rerank_results("machine learning", results)
    assert "rerank_score" in reranked[0]


def test_analytics_stats():
    stats = get_search_stats()
    assert "total_queries" in stats
    assert isinstance(stats["total_queries"], int)
