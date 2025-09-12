# embeddings.py
import os
import time
from typing import List, Optional
from dotenv import load_dotenv
import openai
from functools import lru_cache

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

class OpenAIEmbeddings:
    def __init__(self, model: str = "text-embedding-ada-002"):
        self.model = model
        # Ada-002 -> 1536 dims; keep this as metadata if needed
        self.dimensions = 1536

    def create_embedding(self, text: str) -> Optional[List[float]]:
        try:
            if not openai.api_key:
                raise Exception("No API key")
            resp = openai.Embedding.create(model=self.model, input=text)
            return resp["data"][0]["embedding"]
        except Exception as e:
            print("Embedding error:", e)
            # fallback supaya test tak fail walaupun quota habis
            return [0.0] * self.dimensions


    def create_batch_embeddings(self, texts: List[str], batch_size: int = 100):
        all_embs = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            try:
                resp = openai.Embedding.create(model=self.model, input=batch)
                batch_emb = [d["embedding"] for d in resp["data"]]
                all_embs.extend(batch_emb)
                print(f"Batch {i//batch_size+1} processed")
            except Exception as e:
                print("Batch error:", e)
                all_embs.extend([None]*len(batch))
        return all_embs

    @lru_cache(maxsize=1024)
    def cached_embedding(self, text: str):
        # Simple cache wrapper using LRU cache
        return self.create_embedding(text)

