#!/usr/bin/env python3
"""
Basic OpenAI Embeddings Example
Demonstrates how to create embeddings using OpenAI's text-embedding-ada-002 model
"""

import os
import openai
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
        self.dimensions = 1536  # Ada-002 produces 1536-dimensional vectors
    
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
    
    def create_batch_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Create embeddings for multiple texts in batches"""
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                response = openai.Embedding.create(
                    model=self.model,
                    input=batch
                )
                batch_embeddings = [item['embedding'] for item in response['data']]
                all_embeddings.extend(batch_embeddings)
                print(f"Processed batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
            except Exception as e:
                print(f"Error processing batch {i//batch_size + 1}: {e}")
                # Add None for failed embeddings
                all_embeddings.extend([None] * len(batch))
        
        return all_embeddings
    
    def get_embedding_dimensions(self) -> int:
        """Get the dimensionality of embeddings"""
        return self.dimensions

def main():
    """Main function to demonstrate basic embedding functionality"""
    
    print("🚀 OpenAI Embeddings Demo")
    print("=" * 50)
    
    try:
        # Initialize embeddings client
        embeddings = OpenAIEmbeddings()
        print(f"✅ Initialized OpenAI client with model: {embeddings.model}")
        print(f"📏 Embedding dimensions: {embeddings.dimensions}")
        
        # Single text embedding
        print("\n📝 Single Text Embedding:")
        print("-" * 30)
        
        text = "Hello, this is a sample text for embedding."
        print(f"Input text: {text}")
        
        embedding = embeddings.create_embedding(text)
        if embedding:
            print(f"✅ Embedding created successfully!")
            print(f"   Dimensions: {len(embedding)}")
            print(f"   First 5 values: {embedding[:5]}")
            print(f"   Last 5 values: {embedding[-5:]}")
            print(f"   Data type: {type(embedding[0])}")
        else:
            print("❌ Failed to create embedding")
        
        # Batch processing
        print("\n📚 Batch Embedding Processing:")
        print("-" * 30)
        
        texts = [
            "Machine learning is a subset of artificial intelligence.",
            "Deep learning uses neural networks with multiple layers.",
            "Natural language processing helps computers understand text.",
            "Computer vision enables machines to interpret images.",
            "Reinforcement learning optimizes decision-making processes."
        ]
        
        print(f"Processing {len(texts)} texts...")
        batch_embeddings = embeddings.create_batch_embeddings(texts)
        
        print(f"\n✅ Created {len(batch_embeddings)} embeddings")
        
        # Display results
        for i, (text, embedding) in enumerate(zip(texts, batch_embeddings)):
            if embedding:
                print(f"\n{i+1}. Text: {text[:50]}...")
                print(f"   Embedding: {len(embedding)} dimensions")
                print(f"   Sample values: {embedding[:3]}...")
            else:
                print(f"\n{i+1}. Text: {text[:50]}...")
                print(f"   ❌ Embedding failed")
        
        # Embedding analysis
        print("\n🔍 Embedding Analysis:")
        print("-" * 30)
        
        if all(batch_embeddings):
            # Calculate some basic statistics
            all_values = [val for emb in batch_embeddings for val in emb if emb]
            if all_values:
                import numpy as np
                values_array = np.array(all_values)
                print(f"   Total values: {len(values_array)}")
                print(f"   Mean: {values_array.mean():.6f}")
                print(f"   Std: {values_array.std():.6f}")
                print(f"   Min: {values_array.min():.6f}")
                print(f"   Max: {values_array.max():.6f}")
                print(f"   Range: {values_array.max() - values_array.min():.6f}")
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Set OPENAI_API_KEY environment variable")
        print("   2. Have sufficient OpenAI API credits")
        print("   3. Internet connection for API calls")

if __name__ == "__main__":
    main()
