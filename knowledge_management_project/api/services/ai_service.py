"""
AI Service
Connects to existing AI agent and OpenAI for embeddings and analysis
"""

import openai
import requests
from typing import List, Dict, Any, Optional
import os
from datetime import datetime
import json

class AIService:
    def __init__(self):
        """Initialize AI service connections"""
        # OpenAI configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # AI Agent configuration
        self.ai_agent_url = os.getenv("AI_AGENT_URL")
        self.ai_agent_api_key = os.getenv("AI_AGENT_API_KEY")
        
        # OpenAI model configuration
        self.embedding_model = "text-embedding-ada-002"
        self.embedding_dimensions = 1536
        
        # AI Agent headers
        self.ai_headers = {
            "Content-Type": "application/json",
            "User-Agent": "KnowledgeManagementSystem/1.0"
        }
        
        if self.ai_agent_api_key:
            self.ai_headers["Authorization"] = f"Bearer {self.ai_agent_api_key}"
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connections to AI services"""
        results = {
            "openai": {"status": "unknown"},
            "ai_agent": {"status": "unknown"},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Test OpenAI connection
        try:
            if self.openai_api_key:
                # Try to create a simple embedding
                test_embedding = self.create_embedding("test")
                if test_embedding and len(test_embedding) == self.embedding_dimensions:
                    results["openai"] = {
                        "status": "connected",
                        "model": self.embedding_model,
                        "dimensions": self.embedding_dimensions
                    }
                else:
                    results["openai"] = {
                        "status": "error",
                        "error": "Failed to create test embedding"
                    }
            else:
                results["openai"] = {
                    "status": "error",
                    "error": "OpenAI API key not configured"
                }
        except Exception as e:
            results["openai"] = {
                "status": "error",
                "error": str(e)
            }
        
        # Test AI Agent connection
        try:
            if self.ai_agent_url:
                response = requests.get(
                    f"{self.ai_agent_url}/health",
                    headers=self.ai_headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    results["ai_agent"] = {
                        "status": "connected",
                        "url": self.ai_agent_url,
                        "response_time": response.elapsed.total_seconds()
                    }
                else:
                    # Try alternative endpoint
                    response = requests.get(
                        self.ai_agent_url,
                        headers=self.ai_headers,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        results["ai_agent"] = {
                            "status": "connected",
                            "url": self.ai_agent_url,
                            "response_time": response.elapsed.total_seconds()
                        }
                    else:
                        results["ai_agent"] = {
                            "status": "error",
                            "url": self.ai_agent_url,
                            "status_code": response.status_code,
                            "error": "Could not connect to AI agent"
                        }
            else:
                results["ai_agent"] = {
                    "status": "error",
                    "error": "AI Agent URL not configured"
                }
        except Exception as e:
            results["ai_agent"] = {
                "status": "error",
                "url": self.ai_agent_url,
                "error": str(e)
            }
        
        return results
    
    def create_embedding(self, text: str) -> Optional[List[float]]:
        """Create OpenAI embedding for text"""
        try:
            if not self.openai_api_key:
                print("⚠️ Warning: OPENAI_API_KEY not set. Cannot create embeddings.")
                return None
            
            response = openai.Embedding.create(
                model=self.embedding_model,
                input=text
            )
            
            embedding = response['data'][0]['embedding']
            print(f"✅ Created embedding: {len(embedding)} dimensions")
            return embedding
            
        except Exception as e:
            print(f"❌ Error creating OpenAI embedding: {e}")
            return None
    
    def create_batch_embeddings(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Create embeddings for multiple texts"""
        try:
            if not self.openai_api_key:
                print("⚠️ Warning: OPENAI_API_KEY not set. Cannot create embeddings.")
                return [None] * len(texts)
            
            embeddings = []
            batch_size = 100  # OpenAI batch limit
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                try:
                    response = openai.Embedding.create(
                        model=self.embedding_model,
                        input=batch
                    )
                    
                    batch_embeddings = [item['embedding'] for item in response['data']]
                    embeddings.extend(batch_embeddings)
                    
                    print(f"✅ Processed batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
                    
                except Exception as e:
                    print(f"❌ Error processing batch {i//batch_size + 1}: {e}")
                    embeddings.extend([None] * len(batch))
            
            return embeddings
            
        except Exception as e:
            print(f"❌ Error creating batch embeddings: {e}")
            return [None] * len(texts)
    
    def analyze_document(self, content: bytes, filename: str) -> Dict[str, Any]:
        """Analyze document content using AI agent"""
        try:
            if not self.ai_agent_url:
                print("⚠️ Warning: AI_AGENT_URL not set. Using basic analysis.")
                return self._basic_document_analysis(content, filename)
            
            # Prepare content for AI agent
            if isinstance(content, bytes):
                text_content = content.decode('utf-8', errors='ignore')
            else:
                text_content = str(content)
            
            # Send to AI agent for analysis
            payload = {
                "action": "analyze_document",
                "content": text_content,
                "filename": filename,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            response = requests.post(
                f"{self.ai_agent_url}/analyze",
                json=payload,
                headers=self.ai_headers,
                timeout=60
            )
            
            if response.status_code == 200:
                analysis = response.json()
                print(f"✅ AI analysis completed for: {filename}")
                return analysis
            else:
                print(f"⚠️ AI agent analysis failed, using basic analysis: {response.status_code}")
                return self._basic_document_analysis(content, filename)
                
        except Exception as e:
            print(f"❌ Error in AI analysis: {e}, using basic analysis")
            return self._basic_document_analysis(content, filename)
    
    def _basic_document_analysis(self, content: bytes, filename: str) -> Dict[str, Any]:
        """Basic document analysis when AI agent is not available"""
        try:
            if isinstance(content, bytes):
                text_content = content.decode('utf-8', errors='ignore')
            else:
                text_content = str(content)
            
            # Basic content analysis
            words = text_content.split()
            sentences = text_content.split('.')
            paragraphs = text_content.split('\n\n')
            
            # Determine category based on filename and content
            category = self._determine_category(filename, text_content)
            
            # Extract basic tags
            tags = self._extract_basic_tags(text_content)
            
            # Estimate priority
            priority = self._estimate_priority(text_content, filename)
            
            return {
                "category": category,
                "tags": tags,
                "priority": priority,
                "word_count": len(words),
                "sentence_count": len(sentences),
                "paragraph_count": len(paragraphs),
                "content_summary": text_content[:200] + "..." if len(text_content) > 200 else text_content,
                "analysis_method": "basic",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error in basic analysis: {e}")
            return {
                "category": "unknown",
                "tags": [],
                "priority": "medium",
                "analysis_method": "basic",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _determine_category(self, filename: str, content: str) -> str:
        """Determine document category based on filename and content"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # File extension based categories
        if filename.endswith(('.pdf', '.doc', '.docx')):
            if any(word in content_lower for word in ['report', 'analysis', 'study']):
                return "reports"
            elif any(word in content_lower for word in ['policy', 'procedure', 'guideline']):
                return "policies"
            elif any(word in content_lower for word in ['contract', 'agreement', 'legal']):
                return "legal"
            else:
                return "documents"
        
        elif filename.endswith(('.txt', '.md')):
            if any(word in content_lower for word in ['readme', 'guide', 'manual']):
                return "documentation"
            else:
                return "text"
        
        elif filename.endswith(('.csv', '.xlsx', '.xls')):
            return "data"
        
        # Content based categories
        if any(word in content_lower for word in ['technical', 'engineering', 'code']):
            return "technical"
        elif any(word in content_lower for word in ['financial', 'budget', 'expense']):
            return "financial"
        elif any(word in content_lower for word in ['hr', 'human resources', 'employee']):
            return "hr"
        elif any(word in content_lower for word in ['marketing', 'campaign', 'advertisement']):
            return "marketing"
        
        return "general"
    
    def _extract_basic_tags(self, content: str) -> List[str]:
        """Extract basic tags from content"""
        content_lower = content.lower()
        tags = []
        
        # Common business terms
        business_terms = [
            'strategy', 'planning', 'analysis', 'research', 'development',
            'management', 'leadership', 'innovation', 'technology', 'digital',
            'customer', 'service', 'quality', 'efficiency', 'productivity'
        ]
        
        for term in business_terms:
            if term in content_lower:
                tags.append(term)
        
        # Add file-specific tags
        if 'api' in content_lower or 'endpoint' in content_lower:
            tags.append('api')
        if 'database' in content_lower or 'sql' in content_lower:
            tags.append('database')
        if 'security' in content_lower or 'authentication' in content_lower:
            tags.append('security')
        
        return tags[:5]  # Limit to 5 tags
    
    def _estimate_priority(self, content: str, filename: str) -> str:
        """Estimate document priority"""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        # High priority indicators
        high_priority_words = ['urgent', 'critical', 'emergency', 'immediate', 'asap']
        if any(word in content_lower for word in high_priority_words):
            return "high"
        
        # Medium priority indicators
        medium_priority_words = ['important', 'priority', 'deadline', 'due']
        if any(word in content_lower for word in medium_priority_words):
            return "medium"
        
        # Check filename for priority indicators
        if any(word in filename_lower for word in ['urgent', 'critical', 'important']):
            return "high"
        
        return "medium"
    
    def enhance_search_query(self, query: str) -> Dict[str, Any]:
        """Enhance search query using AI agent"""
        try:
            if not self.ai_agent_url:
                print("⚠️ Warning: AI_AGENT_URL not set. Using basic query enhancement.")
                return self._basic_query_enhancement(query)
            
            payload = {
                "action": "enhance_search_query",
                "query": query,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            response = requests.post(
                f"{self.ai_agent_url}/enhance",
                json=payload,
                headers=self.ai_headers,
                timeout=30
            )
            
            if response.status_code == 200:
                enhancement = response.json()
                print(f"✅ Query enhancement completed")
                return enhancement
            else:
                print(f"⚠️ AI query enhancement failed, using basic enhancement: {response.status_code}")
                return self._basic_query_enhancement(query)
                
        except Exception as e:
            print(f"❌ Error in AI query enhancement: {e}, using basic enhancement")
            return self._basic_query_enhancement(query)
    
    def _basic_query_enhancement(self, query: str) -> Dict[str, Any]:
        """Basic query enhancement when AI agent is not available"""
        try:
            # Simple query expansion
            expanded_terms = []
            query_lower = query.lower()
            
            # Add synonyms for common terms
            synonyms = {
                'document': ['file', 'paper', 'report'],
                'search': ['find', 'lookup', 'query'],
                'analysis': ['study', 'review', 'examination'],
                'data': ['information', 'facts', 'details']
            }
            
            for term, syns in synonyms.items():
                if term in query_lower:
                    expanded_terms.extend(syns)
            
            # Remove duplicates and limit
            expanded_terms = list(set(expanded_terms))[:3]
            
            return {
                "original_query": query,
                "enhanced_query": query,
                "expanded_terms": expanded_terms,
                "suggestions": expanded_terms,
                "enhancement_method": "basic",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "original_query": query,
                "enhanced_query": query,
                "expanded_terms": [],
                "suggestions": [],
                "enhancement_method": "basic",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_embedding_dimensions(self) -> int:
        """Get embedding dimensions for the current model"""
        return self.embedding_dimensions
    
    def get_embedding_model(self) -> str:
        """Get current embedding model name"""
        return self.embedding_model
