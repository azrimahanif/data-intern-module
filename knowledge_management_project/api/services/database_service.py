"""
Database Service
Connects to existing SQL database for metadata storage
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
import os
from datetime import datetime
import json

class DatabaseService:
    def __init__(self):
        """Initialize database connection"""
        self.database_url = os.getenv("DATABASE_URL")
        self.connection = None
        
        if not self.database_url:
            print("⚠️ Warning: DATABASE_URL not set. Database operations will fail.")
    
    def _get_connection(self):
        """Get database connection"""
        try:
            if not self.connection or self.connection.closed:
                self.connection = psycopg2.connect(self.database_url)
            return self.connection
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise Exception(f"Database connection failed: {str(e)}")
    
    def test_connection(self) -> Dict[str, Any]:
        """Test database connection"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            cursor.close()
            
            return {
                "status": "connected",
                "database": "PostgreSQL",
                "version": version[0] if version else "Unknown",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def create_tables(self) -> bool:
        """Create necessary tables if they don't exist"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Create documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    document_id VARCHAR(255) UNIQUE NOT NULL,
                    filename VARCHAR(255) NOT NULL,
                    content_type VARCHAR(100),
                    file_size BIGINT,
                    ai_analysis JSONB,
                    user_metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create document_metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS document_metadata (
                    id SERIAL PRIMARY KEY,
                    document_id VARCHAR(255) REFERENCES documents(document_id),
                    category VARCHAR(100),
                    tags TEXT[],
                    author VARCHAR(255),
                    department VARCHAR(100),
                    priority VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create search_logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_logs (
                    id SERIAL PRIMARY KEY,
                    query_text TEXT NOT NULL,
                    results_count INTEGER,
                    response_time_ms INTEGER,
                    user_id VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create document_analytics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS document_analytics (
                    id SERIAL PRIMARY KEY,
                    document_id VARCHAR(255) REFERENCES documents(document_id),
                    views_count INTEGER DEFAULT 0,
                    downloads_count INTEGER DEFAULT 0,
                    search_appearances INTEGER DEFAULT 0,
                    last_accessed TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            conn.commit()
            cursor.close()
            
            print("✅ Database tables created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    def store_document_metadata(
        self,
        document_id: str,
        filename: str,
        content_type: str,
        file_size: int,
        ai_analysis: Dict[str, Any],
        user_metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Store document metadata in database"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Insert into documents table
            cursor.execute("""
                INSERT INTO documents (document_id, filename, content_type, file_size, ai_analysis, user_metadata)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                document_id,
                filename,
                content_type,
                file_size,
                json.dumps(ai_analysis),
                json.dumps(user_metadata) if user_metadata else None
            ))
            
            db_id = cursor.fetchone()[0]
            
            # Insert into document_metadata table if AI analysis contains relevant info
            if ai_analysis.get('category') or ai_analysis.get('tags'):
                cursor.execute("""
                    INSERT INTO document_metadata (document_id, category, tags, author, department, priority)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (
                    document_id,
                    ai_analysis.get('category'),
                    ai_analysis.get('tags', []),
                    ai_analysis.get('author'),
                    ai_analysis.get('department'),
                    ai_analysis.get('priority', 'medium')
                ))
            
            # Insert into document_analytics table
            cursor.execute("""
                INSERT INTO document_analytics (document_id, views_count, downloads_count, search_appearances)
                VALUES (%s, 0, 0, 0);
            """, (document_id,))
            
            conn.commit()
            cursor.close()
            
            print(f"✅ Document metadata stored: {db_id}")
            return db_id
            
        except Exception as e:
            print(f"❌ Error storing document metadata: {e}")
            raise Exception(f"Failed to store document metadata: {str(e)}")
    
    def get_document_metadata(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get document metadata by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT d.*, dm.category, dm.tags, dm.author, dm.department, dm.priority
                FROM documents d
                LEFT JOIN document_metadata dm ON d.document_id = dm.document_id
                WHERE d.document_id = %s;
            """, (document_id,))
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return dict(result)
            return None
            
        except Exception as e:
            print(f"❌ Error getting document metadata: {e}")
            return None
    
    def list_documents(
        self,
        limit: int = 10,
        offset: int = 0,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List documents with optional filtering"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT d.*, dm.category, dm.tags, dm.author, dm.department, dm.priority
                FROM documents d
                LEFT JOIN document_metadata dm ON d.document_id = dm.document_id
            """
            
            params = []
            if category:
                query += " WHERE dm.category = %s"
                params.append(category)
            
            query += " ORDER BY d.created_at DESC LIMIT %s OFFSET %s;"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            
            return [dict(row) for row in results]
            
        except Exception as e:
            print(f"❌ Error listing documents: {e}")
            return []
    
    def log_search_query(self, query: str, results_count: int, user_id: Optional[str] = None) -> bool:
        """Log search query for analytics"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO search_logs (query_text, results_count, user_id)
                VALUES (%s, %s, %s);
            """, (query, results_count, user_id))
            
            conn.commit()
            cursor.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Error logging search query: {e}")
            return False
    
    def get_analytics_overview(self) -> Dict[str, Any]:
        """Get system overview analytics"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Total documents
            cursor.execute("SELECT COUNT(*) as total_documents FROM documents;")
            total_documents = cursor.fetchone()['total_documents']
            
            # Total searches
            cursor.execute("SELECT COUNT(*) as total_searches FROM search_logs;")
            total_searches = cursor.fetchone()['total_searches']
            
            # Documents by category
            cursor.execute("""
                SELECT dm.category, COUNT(*) as count
                FROM document_metadata dm
                GROUP BY dm.category
                ORDER BY count DESC;
            """)
            documents_by_category = [dict(row) for row in cursor.fetchall()]
            
            # Recent searches
            cursor.execute("""
                SELECT query_text, results_count, created_at
                FROM search_logs
                ORDER BY created_at DESC
                LIMIT 10;
            """)
            recent_searches = [dict(row) for row in cursor.fetchall()]
            
            cursor.close()
            
            return {
                "total_documents": total_documents,
                "total_searches": total_searches,
                "documents_by_category": documents_by_category,
                "recent_searches": recent_searches,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error getting analytics overview: {e}")
            return {"error": str(e)}
    
    def get_search_analytics(self) -> Dict[str, Any]:
        """Get search analytics"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Search volume by day
            cursor.execute("""
                SELECT DATE(created_at) as date, COUNT(*) as searches
                FROM search_logs
                WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY DATE(created_at)
                ORDER BY date;
            """)
            search_volume = [dict(row) for row in cursor.fetchall()]
            
            # Popular search queries
            cursor.execute("""
                SELECT query_text, COUNT(*) as count
                FROM search_logs
                GROUP BY query_text
                ORDER BY count DESC
                LIMIT 10;
            """)
            popular_queries = [dict(row) for row in cursor.fetchall()]
            
            # Average results per search
            cursor.execute("""
                SELECT AVG(results_count) as avg_results
                FROM search_logs;
            """)
            avg_results = cursor.fetchone()['avg_results']
            
            cursor.close()
            
            return {
                "search_volume": search_volume,
                "popular_queries": popular_queries,
                "average_results": float(avg_results) if avg_results else 0,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error getting search analytics: {e}")
            return {"error": str(e)}
    
    def get_document_analytics(self) -> Dict[str, Any]:
        """Get document analytics"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Document growth over time
            cursor.execute("""
                SELECT DATE(created_at) as date, COUNT(*) as documents
                FROM documents
                WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY DATE(created_at)
                ORDER BY date;
            """)
            document_growth = [dict(row) for row in cursor.fetchall()]
            
            # File type distribution
            cursor.execute("""
                SELECT content_type, COUNT(*) as count
                FROM documents
                GROUP BY content_type
                ORDER BY count DESC;
            """)
            file_types = [dict(row) for row in cursor.fetchall()]
            
            # Total file size
            cursor.execute("""
                SELECT SUM(file_size) as total_size
                FROM documents;
            """)
            total_size = cursor.fetchone()['total_size']
            
            cursor.close()
            
            return {
                "document_growth": document_growth,
                "file_types": file_types,
                "total_size": total_size or 0,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error getting document analytics: {e}")
            return {"error": str(e)}
    
    def delete_document(self, document_id: str) -> bool:
        """Delete document from database"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Delete from related tables first
            cursor.execute("DELETE FROM document_analytics WHERE document_id = %s;", (document_id,))
            cursor.execute("DELETE FROM document_metadata WHERE document_id = %s;", (document_id,))
            cursor.execute("DELETE FROM documents WHERE document_id = %s;", (document_id,))
            
            conn.commit()
            cursor.close()
            
            print(f"✅ Document deleted from database: {document_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting document: {e}")
            return False
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and not self.connection.closed:
            self.connection.close()
            print("✅ Database connection closed")
