# vector_db.py
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from chromadb.errors import NotFoundError

class VectorDatabase:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = None

    def create_collection(self, name: str, metadata: Dict[str, Any] = None):
        try:
            # default metadata kalau kosong
            if not metadata:
                metadata = {"description": f"Collection for {name}"}
            self.collection = self.client.create_collection(name=name, metadata=metadata)
        except Exception:
            # kalau collection dah wujud, just get
            self.collection = self.client.get_collection(name=name)

    def add_embeddings(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]] = None,
        ids: List[str] = None
    ):
        if not self.collection:
            raise ValueError("No collection created")
        if not ids:
            ids = [f"doc_{i}" for i in range(len(texts))]
        if not metadatas:
            metadatas = [{} for _ in texts]
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def search_similar(self, query_embedding: List[float], n_results: int = 5, where: Optional[Dict[str, Any]] = None):
        if not self.collection:
            raise ValueError("No collection created")
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )

    def get_info(self):
        if not self.collection:
            return {}
        return {
            "name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata
        }
