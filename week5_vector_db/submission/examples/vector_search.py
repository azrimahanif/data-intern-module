#!/usr/bin/env python3
"""
Vector Search Example
Demonstrates how to store embeddings in ChromaDB and perform similarity search
"""

import os
import openai
import chromadb
from chromadb.config import Settings
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
    
    def create_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts"""
        all_embeddings = []
        
        for i, text in enumerate(texts):
            embedding = self.create_embedding(text)
            if embedding:
                all_embeddings.append(embedding)
                print(f"✅ Created embedding {i+1}/{len(texts)}")
            else:
                all_embeddings.append(None)
                print(f"❌ Failed embedding {i+1}/{len(texts)}")
        
        return all_embeddings

class VectorDatabase:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB client"""
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = None
    
    def create_collection(self, name: str, metadata: Dict[str, Any] = None):
        """Create a new collection for embeddings"""
        try:
            self.collection = self.client.create_collection(
                name=name,
                metadata=metadata or {"description": "Document embeddings collection"}
            )
            print(f"✅ Created collection: {name}")
        except Exception as e:
            print(f"Collection {name} already exists, using existing one")
            self.collection = self.client.get_collection(name=name)
    
    def add_embeddings(self, 
                       texts: List[str], 
                       embeddings: List[List[float]], 
                       metadatas: List[Dict[str, Any]] = None,
                       ids: List[str] = None):
        """Add embeddings to the collection"""
        if not self.collection:
            raise ValueError("No collection selected. Call create_collection first.")
        
        # Filter out None embeddings
        valid_indices = [i for i, emb in enumerate(embeddings) if emb is not None]
        valid_texts = [texts[i] for i in valid_indices]
        valid_embeddings = [embeddings[i] for i in valid_indices]
        valid_metadatas = [metadatas[i] for i in valid_indices] if metadatas else [{} for _ in valid_indices]
        
        # Generate IDs if not provided
        if not ids:
            ids = [f"doc_{i}" for i in valid_indices]
        else:
            ids = [ids[i] for i in valid_indices]
        
        try:
            self.collection.add(
                embeddings=valid_embeddings,
                documents=valid_texts,
                metadatas=valid_metadatas,
                ids=ids
            )
            print(f"✅ Added {len(valid_texts)} embeddings to collection")
        except Exception as e:
            print(f"❌ Error adding embeddings: {e}")
    
    def search_similar(self, 
                      query_embedding: List[float], 
                      n_results: int = 5,
                      where: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search for similar embeddings"""
        if not self.collection:
            raise ValueError("No collection selected. Call create_collection first.")
        
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where
            )
            return results
        except Exception as e:
            print(f"❌ Error searching: {e}")
            return None
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the current collection"""
        if not self.collection:
            return {"error": "No collection selected"}
        
        return {
            "name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata
        }

def complete_embedding_workflow():
    """Complete example of creating, storing, and retrieving embeddings"""
    
    print("🚀 Complete Vector Search Workflow")
    print("=" * 60)
    
    try:
        # 1. Initialize components
        print("🔧 Initializing components...")
        embeddings_client = OpenAIEmbeddings()
        vector_db = VectorDatabase()
        
        # 2. Create collection
        print("\n📁 Creating collection...")
        vector_db.create_collection("ai_documents", {
            "description": "AI and Machine Learning documents",
            "created_by": "Intern Demo",
            "version": "1.0"
        })
        
        # 3. Sample documents
        documents = [
            "Machine learning algorithms can identify patterns in data and make predictions based on historical information.",
            "Deep learning uses neural networks with multiple layers to process complex data structures and learn hierarchical representations.",
            "Natural language processing enables computers to understand, interpret, and generate human language in a meaningful way.",
            "Computer vision helps machines interpret and analyze visual information from the world, including images and videos.",
            "Reinforcement learning optimizes decision-making processes by allowing agents to learn through trial and error.",
            "Supervised learning trains models using labeled data to make predictions on new, unseen data.",
            "Unsupervised learning discovers hidden patterns in data without predefined labels or categories.",
            "Transfer learning leverages knowledge from one domain to improve performance in related domains.",
            "Neural networks are computational models inspired by biological neural networks in the human brain.",
            "Convolutional neural networks are particularly effective for processing grid-like data such as images."
        ]
        
        # 4. Create embeddings
        print("\n🔄 Creating embeddings...")
        document_embeddings = embeddings_client.create_batch_embeddings(documents)
        
        # 5. Prepare metadata
        metadatas = [
            {"category": "ML", "difficulty": "beginner", "topic": "fundamentals"},
            {"category": "DL", "difficulty": "intermediate", "topic": "neural_networks"},
            {"category": "NLP", "difficulty": "intermediate", "topic": "language_processing"},
            {"category": "CV", "difficulty": "intermediate", "topic": "image_processing"},
            {"category": "RL", "difficulty": "advanced", "topic": "decision_making"},
            {"category": "ML", "difficulty": "beginner", "topic": "supervised_learning"},
            {"category": "ML", "difficulty": "intermediate", "topic": "unsupervised_learning"},
            {"category": "ML", "difficulty": "intermediate", "topic": "transfer_learning"},
            {"category": "DL", "difficulty": "beginner", "topic": "neural_networks"},
            {"category": "DL", "difficulty": "intermediate", "topic": "cnn"}
        ]
        
        # 6. Store in vector database
        print("\n💾 Storing embeddings...")
        vector_db.add_embeddings(
            texts=documents,
            embeddings=document_embeddings,
            metadatas=metadatas
        )
        
        # 7. Collection information
        print(f"\n📈 Collection Info: {vector_db.get_collection_info()}")
        
        # 8. Search for similar content
        print("\n🔍 Performing similarity searches...")
        
        # Search queries
        search_queries = [
            "How do machines learn from data?",
            "What are neural networks?",
            "How does computer vision work?",
            "Explain deep learning concepts",
            "What is natural language processing?"
        ]
        
        for i, query in enumerate(search_queries, 1):
            print(f"\n🔍 Search {i}: '{query}'")
            print("-" * 50)
            
            query_embedding = embeddings_client.create_embedding(query)
            
            if query_embedding:
                results = vector_db.search_similar(query_embedding, n_results=3)
                
                if results and results['documents']:
                    print(f"📊 Top 3 Results:")
                    for j, (doc, metadata, distance) in enumerate(zip(
                        results['documents'][0], 
                        results['metadatas'][0], 
                        results['distances'][0]
                    )):
                        similarity_score = 1 - distance
                        print(f"\n   {j+1}. Similarity: {similarity_score:.3f}")
                        print(f"      Document: {doc[:80]}...")
                        print(f"      Category: {metadata.get('category', 'N/A')}")
                        print(f"      Difficulty: {metadata.get('difficulty', 'N/A')}")
                        print(f"      Topic: {metadata.get('topic', 'N/A')}")
                else:
                    print("❌ No search results found")
            else:
                print("❌ Failed to create query embedding")
        
        # 9. Filtered search example
        print("\n🎯 Filtered Search Example:")
        print("-" * 50)
        
        # Search only for beginner-level content
        beginner_query = "What is machine learning?"
        beginner_embedding = embeddings_client.create_embedding(beginner_query)
        
        if beginner_embedding:
            filtered_results = vector_db.search_similar(
                beginner_embedding, 
                n_results=5,
                where={"difficulty": "beginner"}
            )
            
            if filtered_results and filtered_results['documents']:
                print(f"🔍 Beginner-level results for: '{beginner_query}'")
                for j, (doc, metadata, distance) in enumerate(zip(
                    filtered_results['documents'][0], 
                    filtered_results['metadatas'][0], 
                    filtered_results['distances'][0]
                )):
                    similarity_score = 1 - distance
                    print(f"\n   {j+1}. Similarity: {similarity_score:.3f}")
                    print(f"      Document: {doc[:80]}...")
                    print(f"      Category: {metadata.get('category', 'N/A')}")
        
        print("\n🎉 Vector search workflow completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during workflow: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Set OPENAI_API_KEY environment variable")
        print("   2. Have sufficient OpenAI API credits")
        print("   3. Internet connection for API calls")
        print("   4. Installed chromadb: pip install chromadb")

if __name__ == "__main__":
    complete_embedding_workflow()
