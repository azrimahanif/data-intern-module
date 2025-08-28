"""
Qdrant Vector Database Service
Connects to existing Qdrant instance at https://qdrant.aafiyat2u.net/
"""

import qdrant_client
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Any, Optional
import os
import uuid
from datetime import datetime

class QdrantService:
    def __init__(self):
        """Initialize Qdrant client connection"""
        self.qdrant_url = os.getenv("QDRANT_URL", "https://qdrant.aafiyat2u.net/")
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = "knowledge_base"
        
        # Initialize client
        if self.api_key:
            self.client = qdrant_client.QdrantClient(
                url=self.qdrant_url,
                api_key=self.api_key
            )
        else:
            self.client = qdrant_client.QdrantClient(url=self.qdrant_url)
        
        # Ensure collection exists
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=1536,  # OpenAI text-embedding-ada-002 dimension
                        distance=Distance.COSINE
                    )
                )
                print(f"✅ Created collection: {self.collection_name}")
            else:
                print(f"✅ Using existing collection: {self.collection_name}")
                
        except Exception as e:
            print(f"⚠️ Warning: Could not ensure collection exists: {e}")
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to Qdrant instance"""
        try:
            collections = self.client.get_collections()
            return {
                "status": "connected",
                "url": self.qdrant_url,
                "collections_count": len(collections.collections),
                "collection_names": [col.name for col in collections.collections],
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "url": self.qdrant_url,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def add_document(self, content: str, embedding: List[float], metadata: Dict[str, Any]) -> str:
        """Add a document with embedding to Qdrant"""
        try:
            # Generate unique document ID
            document_id = str(uuid.uuid4())
            
            # Prepare point for Qdrant
            point = PointStruct(
                id=document_id,
                vector=embedding,
                payload={
                    "text": content,
                    "metadata": metadata,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
            )
            
            # Add to collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            print(f"✅ Document added to Qdrant: {document_id}")
            return document_id
            
        except Exception as e:
            print(f"❌ Error adding document to Qdrant: {e}")
            raise Exception(f"Failed to add document to Qdrant: {str(e)}")
    
    def search_similar(
        self, 
        query_embedding: List[float], 
        limit: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Search for similar documents using vector similarity"""
        try:
            # Build filter if provided
            qdrant_filter = None
            if filters:
                qdrant_filter = self._build_filter(filters)
            
            # Perform search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                query_filter=qdrant_filter,
                with_payload=True,
                with_vectors=False
            )
            
            print(f"✅ Search completed: {len(search_results)} results")
            return search_results
            
        except Exception as e:
            print(f"❌ Error searching Qdrant: {e}")
            raise Exception(f"Search failed: {str(e)}")
    
    def _build_filter(self, filters: Dict[str, Any]) -> Filter:
        """Build Qdrant filter from dictionary"""
        conditions = []
        
        for key, value in filters.items():
            if isinstance(value, str):
                conditions.append(
                    FieldCondition(
                        key=f"metadata.{key}",
                        match=MatchValue(value=value)
                    )
                )
            elif isinstance(value, list):
                # Handle list filters (e.g., tags)
                for item in value:
                    conditions.append(
                        FieldCondition(
                            key=f"metadata.{key}",
                            match=MatchValue(value=item)
                        )
                    )
        
        return Filter(must=conditions)
    
    def get_document(self, document_id: str) -> Optional[Any]:
        """Get a specific document by ID"""
        try:
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[document_id],
                with_payload=True,
                with_vectors=False
            )
            
            if result:
                return result[0]
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving document: {e}")
            return None
    
    def update_document(self, document_id: str, metadata: Dict[str, Any]) -> bool:
        """Update document metadata"""
        try:
            # Get existing document
            existing_doc = self.get_document(document_id)
            if not existing_doc:
                return False
            
            # Update payload
            updated_payload = existing_doc.payload.copy()
            updated_payload["metadata"].update(metadata)
            updated_payload["updated_at"] = datetime.utcnow().isoformat()
            
            # Update in Qdrant
            point = PointStruct(
                id=document_id,
                vector=existing_doc.vector,
                payload=updated_payload
            )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            print(f"✅ Document updated: {document_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating document: {e}")
            return False
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document from Qdrant"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[document_id]
            )
            
            print(f"✅ Document deleted: {document_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting document: {e}")
            return False
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            collection_stats = self.client.get_collection(self.collection_name)
            
            return {
                "name": collection_info.name,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "points_count": collection_stats.points_count,
                "segments_count": collection_stats.segments_count,
                "status": "active"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }
    
    def clear_collection(self) -> bool:
        """Clear all documents from collection (use with caution!)"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector="*"
            )
            
            print(f"⚠️ Collection cleared: {self.collection_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error clearing collection: {e}")
            return False
