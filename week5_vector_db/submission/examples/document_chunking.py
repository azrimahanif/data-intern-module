#!/usr/bin/env python3
"""
Document Chunking and Embedding Example
Demonstrates how to chunk documents and create embeddings with metadata
"""

import os
import openai
import hashlib
from datetime import datetime
from typing import List, Dict, Any

class OpenAIEmbeddings:
    def __init__(self, api_key: str = None):
        """Initialize OpenAI client"""
        if api_key:
            openai.api_key = api_key
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
        
        if not openai.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.model = "text-embedding-ada-002"
        self.dimensions = 1536
    
    def create_embedding(self, text: str) -> List[float]:
        """Create a single embedding for text"""
        try:
            response = openai.Embedding.create(
                model=self.model,
                input=text
            )
            return response['data'][0]['embedding']
        except Exception as e:
            print(f"Error creating embedding: {e}")
            return None

class DocumentEmbedding:
    def __init__(self, embeddings_client: OpenAIEmbeddings):
        self.embeddings = embeddings_client
    
    def create_document_embedding(self, 
                                 text: str, 
                                 metadata: Dict[str, Any] = None,
                                 chunk_size: int = 1000,
                                 overlap: int = 200) -> List[Dict[str, Any]]:
        """
        Create embeddings for a document with chunking and metadata
        
        Args:
            text: Document text to embed
            metadata: Additional metadata for the document
            chunk_size: Maximum size of each text chunk
            overlap: Overlap between chunks for context preservation
        """
        # Chunk the text
        chunks = self._chunk_text(text, chunk_size, overlap)
        
        # Create embeddings for each chunk
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
                    'tokens_estimated': len(chunk.split()) * 1.3  # Rough estimate
                }
                chunk_embeddings.append(chunk_data)
                print(f"✅ Created embedding for chunk {i+1}/{len(chunks)}")
            else:
                print(f"❌ Failed to create embedding for chunk {i+1}")
        
        return chunk_embeddings
    
    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # If this isn't the last chunk, try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings
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

def main():
    """Main function to demonstrate document chunking and embedding"""
    
    print("📄 Document Chunking and Embedding Demo")
    print("=" * 60)
    
    try:
        # Initialize components
        embeddings = OpenAIEmbeddings()
        doc_embeddings = DocumentEmbedding(embeddings)
        
        print(f"✅ Initialized OpenAI client with model: {embeddings.model}")
        
        # Sample document
        document_text = """
        Artificial Intelligence (AI) is transforming industries across the globe. 
        Machine learning algorithms can now process vast amounts of data to identify 
        patterns and make predictions. Deep learning models have achieved remarkable 
        success in image recognition, natural language processing, and game playing.
        
        The field continues to evolve rapidly, with new architectures and techniques 
        being developed regularly. Companies are investing heavily in AI research 
        and development, recognizing its potential to drive innovation and efficiency.
        
        Natural Language Processing (NLP) has made significant strides in recent years. 
        Large language models can now understand context, generate human-like text, 
        and perform complex language tasks. These models are being used in chatbots, 
        content generation, translation services, and many other applications.
        
        Computer Vision is another area where AI has shown remarkable progress. 
        Modern systems can identify objects, recognize faces, analyze medical images, 
        and even drive autonomous vehicles. The accuracy and speed of these systems 
        continue to improve with advances in deep learning and neural networks.
        
        Reinforcement Learning represents a different approach to AI, where agents 
        learn through interaction with their environment. This approach has been 
        successful in game playing, robotics, and optimization problems. The key 
        insight is that agents can learn optimal strategies through trial and error.
        """
        
        # Document metadata
        metadata = {
            'source': 'AI Research Paper',
            'author': 'Data Science Team',
            'category': 'Technology',
            'tags': ['AI', 'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision'],
            'difficulty': 'intermediate',
            'last_updated': '2024-01-15'
        }
        
        print(f"\n📝 Document Information:")
        print(f"   Length: {len(document_text)} characters")
        print(f"   Estimated words: {len(document_text.split())}")
        print(f"   Metadata: {metadata}")
        
        # Create embeddings with different chunk sizes
        chunk_sizes = [150, 300, 500]
        
        for chunk_size in chunk_sizes:
            print(f"\n🔪 Chunking with size {chunk_size} (overlap 50):")
            print("-" * 50)
            
            chunk_embeddings = doc_embeddings.create_document_embedding(
                text=document_text,
                metadata=metadata,
                chunk_size=chunk_size,
                overlap=50
            )
            
            print(f"\n📊 Results for chunk size {chunk_size}:")
            print(f"   Total chunks: {len(chunk_embeddings)}")
            
            for chunk in chunk_embeddings:
                print(f"\n   Chunk {chunk['chunk_index'] + 1}:")
                print(f"     Text: {chunk['text'][:80]}...")
                print(f"     Length: {chunk['text_length']} chars")
                print(f"     Estimated tokens: {chunk['tokens_estimated']:.1f}")
                print(f"     Embedding dimensions: {len(chunk['embedding'])}")
                print(f"     ID: {chunk['id']}")
                print(f"     Created: {chunk['created_at']}")
        
        # Demonstrate chunking strategy
        print(f"\n🎯 Chunking Strategy Analysis:")
        print("-" * 50)
        
        optimal_chunk_size = 300
        optimal_overlap = 50
        
        print(f"   Optimal chunk size: {optimal_chunk_size} characters")
        print(f"   Optimal overlap: {optimal_overlap} characters")
        print(f"   Reasoning: Balances context preservation with embedding quality")
        
        # Show final recommendation
        print(f"\n💡 Recommendation:")
        print(f"   Use chunk size: {optimal_chunk_size} characters")
        print(f"   Use overlap: {optimal_overlap} characters")
        print(f"   This provides good balance between context and efficiency")
        
        print("\n🎉 Document chunking demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Set OPENAI_API_KEY environment variable")
        print("   2. Have sufficient OpenAI API credits")
        print("   3. Internet connection for API calls")

if __name__ == "__main__":
    main()
