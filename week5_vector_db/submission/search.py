"""
search.py
---------
Core search functions: semantic search, keyword search,
hybrid search, metadata filtering, reranking, and analytics.
"""

import time
from collections import defaultdict
from typing import Dict, Any, List
from sentence_transformers import SentenceTransformer
import chromadb

# ========================
# Embeddings with Caching
# ========================
_model = SentenceTransformer("all-MiniLM-L6-v2")
_embedding_cache: Dict[str, List[float]] = {}

def embed_texts(texts: List[str]):
    """Return embeddings with caching to avoid recomputation."""
    results = []
    for t in texts:
        if t in _embedding_cache:
            results.append(_embedding_cache[t])
        else:
            emb = _model.encode([t], convert_to_numpy=True)[0].tolist()
            _embedding_cache[t] = emb
            results.append(emb)
    return results

# ========================
# Vector DB Setup
# ========================
_client = chromadb.Client()
_collection = _client.get_or_create_collection("documents")

def get_vector_store():
    return _collection

def index_texts(texts, metadatas=None, ids=None, batch_size=2):
    """Add documents into vector database in batches."""
    vectordb = get_vector_store()
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_metas = metadatas[i:i+batch_size] if metadatas else None
        batch_ids = ids[i:i+batch_size] if ids else None
        embeddings = embed_texts(batch_texts)
        vectordb.add(
            documents=batch_texts,
            embeddings=embeddings,
            metadatas=batch_metas,
            ids=batch_ids
        )

def format_results(results):
    output = []
    for i, doc in enumerate(results["documents"][0]):
        output.append({
            "id": results["ids"][0][i],
            "text": doc,
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })
    return output

# ========================
# Analytics Logging
# ========================
search_logs = []

def log_search(query, results, runtime=None):
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "result_count": len(results),
        "top_result": results[0]["id"] if results else None,
        "runtime_ms": round(runtime * 1000, 2) if runtime else None
    }
    search_logs.append(entry)

def get_search_stats():
    query_freq = defaultdict(int)
    for log in search_logs:
        query_freq[log["query"]] += 1
    sorted_queries = sorted(query_freq.items(), key=lambda x: x[1], reverse=True)
    return {
        "total_queries": len(search_logs),
        "top_queries": sorted_queries[:5],
        "logs": search_logs
    }

# ========================
# Search Functions
# ========================
def semantic_search(query: str, top_k: int = 3, metadata_filter: Dict[str, Any] = None):
    start = time.time()
    vectordb = get_vector_store()
    query_emb = embed_texts([query])[0]
    results = vectordb.query(
        query_embeddings=[query_emb],
        n_results=top_k,
        where=metadata_filter if metadata_filter else {}
    )
    formatted = format_results(results)
    runtime = time.time() - start
    log_search(query, formatted, runtime)
    return formatted

def keyword_search(query: str, top_k: int = 3):
    vectordb = get_vector_store()
    results = vectordb.get(include=["documents", "metadatas", "ids"])
    
    matches = []
    for i, doc in enumerate(results["documents"]):
        if query.lower() in doc.lower():
            matches.append({
                "id": results["ids"][i],
                "text": doc,
                "metadata": results["metadatas"][i],
                "score": 1.0
            })
    return matches[:top_k]

def hybrid_search(query: str, top_k: int = 3, alpha: float = 0.5):
    start = time.time()
    vectordb = get_vector_store()
    query_emb = embed_texts([query])[0]
    results = vectordb.query(query_embeddings=[query_emb], n_results=top_k * 2)
    vector_results = format_results(results)

    keyword_hits = []
    for res in vector_results:
        if query.lower() in res["text"].lower():
            keyword_hits.append(res["id"])

    hybrid_results = []
    for res in vector_results:
        vector_score = 1 - res["distance"]
        keyword_score = 1.0 if res["id"] in keyword_hits else 0.0
        hybrid_score = alpha * vector_score + (1 - alpha) * keyword_score
        res["hybrid_score"] = hybrid_score
        hybrid_results.append(res)

    hybrid_results = sorted(hybrid_results, key=lambda x: x["hybrid_score"], reverse=True)[:top_k]
    runtime = time.time() - start
    log_search(query, hybrid_results, runtime)
    return hybrid_results
