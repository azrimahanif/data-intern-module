import hashlib
from datetime import datetime
from typing import List, Dict, Any
from submission.embeddings import OpenAIEmbeddings

class DocumentEmbedding:
    def __init__(self, embeddings_client: OpenAIEmbeddings):
        self.embeddings = embeddings_client
    
    def create_document_embedding(self, 
                                 text: str, 
                                 metadata: Dict[str, Any] = None,
                                 chunk_size: int = 1000,
                                 overlap: int = 200) -> List[Dict[str, Any]]:
        """Create embeddings for a document with chunking and metadata"""
        chunks = self._chunk_text(text, chunk_size, overlap)
        chunk_embeddings = []
        
        for i, chunk in enumerate(chunks):
            embedding = self.embeddings.create_embedding(chunk)
            
            if embedding:
                chunk_data = {
                    'id': self._generate_chunk_id(text, i),
                    'text': chunk,
                    'embedding': embedding,
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'metadata': metadata or {},
                    'created_at': datetime.utcnow().isoformat(),
                    'text_length': len(chunk),
                    'tokens_estimated': len(chunk.split()) * 1.3
                }
                chunk_embeddings.append(chunk_data)
        
        return chunk_embeddings
    
    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            if end < len(text):
                for i in range(end, max(start, end - 100), -1):
                    if text[i] in '.!?':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def _generate_chunk_id(self, text: str, chunk_index: int) -> str:
        """Generate unique ID for chunk"""
        content_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        return f"chunk_{chunk_index}_{content_hash}"
