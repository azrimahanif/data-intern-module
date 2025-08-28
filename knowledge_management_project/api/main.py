"""
AI-Powered Knowledge Management System
Main FastAPI application
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import services
from services.qdrant_service import QdrantService
from services.database_service import DatabaseService
from services.n8n_service import N8nService
from services.ai_service import AIService

# Initialize FastAPI app
app = FastAPI(
    title="Knowledge Management API",
    description="AI-powered knowledge management system with vector search",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
qdrant_service = QdrantService()
database_service = DatabaseService()
n8n_service = N8nService()
ai_service = AIService()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI-Powered Knowledge Management System",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint - test all service connections"""
    try:
        # Test Qdrant connection
        qdrant_status = qdrant_service.test_connection()
        
        # Test database connection
        db_status = database_service.test_connection()
        
        # Test n8n connection
        n8n_status = n8n_service.test_connection()
        
        # Test AI service connection
        ai_status = ai_service.test_connection()
        
        # Determine overall status
        all_healthy = all([
            qdrant_status.get("status") == "connected",
            db_status.get("status") == "connected",
            n8n_status.get("status") == "connected",
            ai_status.get("status") == "connected"
        ])
        
        return {
            "overall_status": "healthy" if all_healthy else "unhealthy",
            "services": {
                "qdrant": qdrant_status,
                "database": db_status,
                "n8n": n8n_status,
                "ai_agent": ai_status
            },
            "timestamp": "2024-01-15T10:00:00Z"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    metadata: Optional[Dict[str, Any]] = None
):
    """Upload and process a document"""
    try:
        # Validate file type
        allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file.content_type} not supported. Allowed: {allowed_types}"
            )
        
        # Read file content
        content = await file.read()
        
        # Process document with AI agent
        ai_analysis = ai_service.analyze_document(content, file.filename)
        
        # Create OpenAI embedding
        embedding = ai_service.create_embedding(content.decode('utf-8'))
        
        # Store in Qdrant
        document_id = qdrant_service.add_document(
            content=content.decode('utf-8'),
            embedding=embedding,
            metadata={
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": len(content),
                **ai_analysis,
                **(metadata or {})
            }
        )
        
        # Store metadata in SQL database
        db_document_id = database_service.store_document_metadata(
            document_id=document_id,
            filename=file.filename,
            content_type=file.content_type,
            file_size=len(content),
            ai_analysis=ai_analysis,
            user_metadata=metadata
        )
        
        # Trigger n8n workflow for document processing
        n8n_service.trigger_document_processing({
            "document_id": document_id,
            "filename": file.filename,
            "status": "processed"
        })
        
        return {
            "message": "Document processed successfully",
            "document_id": document_id,
            "database_id": db_document_id,
            "ai_analysis": ai_analysis,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")

@app.post("/search")
async def search_documents(
    query: str,
    limit: int = 5,
    filters: Optional[Dict[str, Any]] = None
):
    """Search documents using vector similarity"""
    try:
        # Create query embedding
        query_embedding = ai_service.create_embedding(query)
        
        # Search Qdrant
        search_results = qdrant_service.search_similar(
            query_embedding=query_embedding,
            limit=limit,
            filters=filters
        )
        
        # Enhance results with database metadata
        enhanced_results = []
        for result in search_results:
            metadata = database_service.get_document_metadata(result.id)
            enhanced_results.append({
                "id": result.id,
                "score": result.score,
                "content": result.payload.get("text", "")[:200] + "...",
                "metadata": metadata,
                "payload": result.payload
            })
        
        # Log search analytics
        database_service.log_search_query(query, len(enhanced_results))
        
        # Trigger n8n workflow for search analytics
        n8n_service.trigger_search_analytics({
            "query": query,
            "results_count": len(enhanced_results),
            "timestamp": "2024-01-15T10:00:00Z"
        })
        
        return {
            "query": query,
            "results": enhanced_results,
            "total_results": len(enhanced_results),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/documents")
async def list_documents(
    limit: int = 10,
    offset: int = 0,
    category: Optional[str] = None
):
    """List all documents with optional filtering"""
    try:
        documents = database_service.list_documents(
            limit=limit,
            offset=offset,
            category=category
        )
        
        return {
            "documents": documents,
            "total": len(documents),
            "limit": limit,
            "offset": offset,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")

@app.get("/documents/{document_id}")
async def get_document(document_id: str):
    """Get document details by ID"""
    try:
        # Get from Qdrant
        qdrant_doc = qdrant_service.get_document(document_id)
        
        # Get metadata from database
        metadata = database_service.get_document_metadata(document_id)
        
        if not qdrant_doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "id": document_id,
            "content": qdrant_doc.payload.get("text", ""),
            "metadata": metadata,
            "payload": qdrant_doc.payload,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document: {str(e)}")

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document"""
    try:
        # Delete from Qdrant
        qdrant_service.delete_document(document_id)
        
        # Delete from database
        database_service.delete_document(document_id)
        
        return {
            "message": "Document deleted successfully",
            "document_id": document_id,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

@app.get("/analytics/overview")
async def get_analytics_overview():
    """Get system overview analytics"""
    try:
        analytics = database_service.get_analytics_overview()
        
        return {
            "analytics": analytics,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

@app.get("/analytics/search")
async def get_search_analytics():
    """Get search analytics"""
    try:
        search_analytics = database_service.get_search_analytics()
        
        return {
            "search_analytics": search_analytics,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get search analytics: {str(e)}")

@app.get("/analytics/documents")
async def get_document_analytics():
    """Get document analytics"""
    try:
        document_analytics = database_service.get_document_analytics()
        
        return {
            "document_analytics": document_analytics,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document analytics: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
