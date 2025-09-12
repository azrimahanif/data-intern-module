from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn

app = FastAPI(title="Vector Database API", version="1.0.0")

# ==========================
# Data models
# ==========================
class SearchQuery(BaseModel):
    text: str
    n_results: int = 5
    filters: Optional[Dict[str, Any]] = None

class DocumentInput(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    documents: List[str]
    metadatas: List[Dict[str, Any]]
    distances: List[float]
    similarity_scores: List[float]

# ==========================
# Fake in-memory DB (for testing)
# ==========================
documents_db = []
metadatas_db = []

def fake_embedding(text: str) -> List[float]:
    """Very simple fake embedding (length of text)"""
    return [len(text)]

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Simple similarity: inverse of absolute difference"""
    return 1 / (1 + abs(v1[0] - v2[0]))

# ==========================
# API Endpoints
# ==========================
@app.post("/documents", response_model=Dict[str, str])
async def add_document(document: DocumentInput):
    """Add a new document to the fake vector database"""
    try:
        documents_db.append(document.text)
        metadatas_db.append(document.metadata or {})
        return {"message": "Document added successfully", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=SearchResult)
async def search_documents(query: SearchQuery):
    """Search for similar documents (simple fake search)"""
    try:
        if not documents_db:
            raise HTTPException(status_code=404, detail="No documents in database")

        query_emb = fake_embedding(query.text)

        sims = [cosine_similarity(query_emb, fake_embedding(doc)) for doc in documents_db]
        ranked = sorted(
            list(zip(documents_db, metadatas_db, sims)),
            key=lambda x: x[2],
            reverse=True
        )[:query.n_results]

        docs, metas, scores = zip(*ranked)
        distances = [1 - s for s in scores]

        return SearchResult(
            documents=list(docs),
            metadatas=list(metas),
            distances=distances,
            similarity_scores=list(scores)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "vector-database-api"}

# ==========================
# Run server
# ==========================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

