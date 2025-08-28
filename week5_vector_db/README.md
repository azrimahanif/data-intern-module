# Week 5: Vector Database Implementation

## 🎯 Week Goals

Implement vector databases for semantic search and similarity matching. Learn to store, index, and query high-dimensional vector embeddings for AI applications.

### 📚 Learning Objectives

- **Vector Database Fundamentals**
  - Understand vector embeddings and similarity search
  - Set up and configure vector databases (Pinecone/ChromaDB)
  - Implement efficient indexing strategies
  - Optimize query performance

- **Semantic Search Implementation**
  - Create embedding generation pipelines
  - Build semantic search functionality
  - Implement similarity scoring
  - Add filtering and metadata search

## 📋 Assignments

### Assignment 1: Vector Database Setup (40 points)
- [ ] Set up Pinecone or ChromaDB
- [ ] Create embedding generation pipeline
- [ ] Implement vector storage and indexing
- [ ] Build basic similarity search

### Assignment 2: Advanced Search Features (30 points)
- [ ] Add metadata filtering
- [ ] Implement hybrid search (vector + keyword)
- [ ] Create search result ranking
- [ ] Add search analytics

### Assignment 3: Performance Optimization (20 points)
- [ ] Optimize embedding generation
- [ ] Implement caching strategies
- [ ] Add query performance monitoring
- [ ] Scale vector database operations

### Assignment 4: Integration & Testing (10 points)
- [ ] Integrate with existing API
- [ ] Write comprehensive tests
- [ ] Create search interface
- [ ] Document search capabilities

## 🔑 **OpenAI Embeddings Implementation Guide**

### **Step 1: Setting Up OpenAI API**

1. **Get your API key:**
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new secret key
   - Store it securely (use environment variables)

2. **Install required packages:**
   ```bash
   pip install openai numpy pandas tiktoken
   ```

3. **Set up environment:**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   
   # Or set in PowerShell
   $env:OPENAI_API_KEY="your_api_key_here"
   ```

### **Step 2: Creating Embeddings with text-embedding-ada-002**

#### **Basic Embedding Generation**

```python
import openai
import numpy as np
from typing import List, Dict, Any

class OpenAIEmbeddings:
    def __init__(self, api_key: str = None):
        """Initialize OpenAI client"""
        if api_key:
            openai.api_key = api_key
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
        
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

# Usage example
if __name__ == "__main__":
    # Initialize embeddings
    embeddings = OpenAIEmbeddings()
    
    # Single text embedding
    text = "Hello, this is a sample text for embedding."
    embedding = embeddings.create_embedding(text)
    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    
    # Batch processing
    texts = [
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with multiple layers.",
        "Natural language processing helps computers understand text.",
        "Computer vision enables machines to interpret images."
    ]
    
    batch_embeddings = embeddings.create_batch_embeddings(texts)
    print(f"Created {len(batch_embeddings)} embeddings")
```

#### **Advanced Embedding with Metadata**

```python
import json
import hashlib
from datetime import datetime

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

# Usage example
if __name__ == "__main__":
    embeddings = OpenAIEmbeddings()
    doc_embeddings = DocumentEmbedding(embeddings)
    
    # Sample document
    document_text = """
    Artificial Intelligence (AI) is transforming industries across the globe. 
    Machine learning algorithms can now process vast amounts of data to identify 
    patterns and make predictions. Deep learning models have achieved remarkable 
    success in image recognition, natural language processing, and game playing.
    
    The field continues to evolve rapidly, with new architectures and techniques 
    being developed regularly. Companies are investing heavily in AI research 
    and development, recognizing its potential to drive innovation and efficiency.
    """
    
    # Document metadata
    metadata = {
        'source': 'AI Research Paper',
        'author': 'Data Science Team',
        'category': 'Technology',
        'tags': ['AI', 'Machine Learning', 'Deep Learning']
    }
    
    # Create embeddings with metadata
    chunk_embeddings = doc_embeddings.create_document_embedding(
        text=document_text,
        metadata=metadata,
        chunk_size=150,
        overlap=50
    )
    
    print(f"Created {len(chunk_embeddings)} chunks with embeddings")
    for chunk in chunk_embeddings:
        print(f"Chunk {chunk['chunk_index']}: {chunk['text'][:50]}...")
        print(f"  Embedding dimensions: {len(chunk['embedding'])}")
        print(f"  Metadata: {chunk['metadata']}")
```

### **Step 3: Storing and Retrieving Embeddings**

#### **Vector Database Integration (ChromaDB Example)**

```python
import chromadb
from chromadb.config import Settings

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
        
        # Generate IDs if not provided
        if not ids:
            ids = [f"doc_{i}" for i in range(len(texts))]
        
        # Ensure metadatas list matches texts
        if not metadatas:
            metadatas = [{} for _ in texts]
        
        try:
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Added {len(texts)} embeddings to collection")
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

# Complete workflow example
def complete_embedding_workflow():
    """Complete example of creating, storing, and retrieving embeddings"""
    
    # 1. Initialize components
    embeddings_client = OpenAIEmbeddings()
    vector_db = VectorDatabase()
    
    # 2. Create collection
    vector_db.create_collection("ai_documents")
    
    # 3. Sample documents
    documents = [
        "Machine learning algorithms can identify patterns in data.",
        "Deep learning uses neural networks for complex tasks.",
        "Natural language processing enables text understanding.",
        "Computer vision helps machines interpret images.",
        "Reinforcement learning optimizes decision-making processes."
    ]
    
    # 4. Create embeddings
    print("🔄 Creating embeddings...")
    document_embeddings = embeddings_client.create_batch_embeddings(documents)
    
    # 5. Prepare metadata
    metadatas = [
        {"category": "ML", "difficulty": "beginner"},
        {"category": "DL", "difficulty": "intermediate"},
        {"category": "NLP", "difficulty": "intermediate"},
        {"category": "CV", "difficulty": "intermediate"},
        {"category": "RL", "difficulty": "advanced"}
    ]
    
    # 6. Store in vector database
    print("💾 Storing embeddings...")
    vector_db.add_embeddings(
        texts=documents,
        embeddings=document_embeddings,
        metadatas=metadatas
    )
    
    # 7. Search for similar content
    print("🔍 Searching for similar content...")
    query = "How do machines learn from data?"
    query_embedding = embeddings_client.create_embedding(query)
    
    if query_embedding:
        results = vector_db.search_similar(query_embedding, n_results=3)
        
        print("\n📊 Search Results:")
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0], 
            results['metadatas'][0], 
            results['distances'][0]
        )):
            print(f"\n{i+1}. Document: {doc}")
            print(f"   Metadata: {metadata}")
            print(f"   Similarity Score: {1 - distance:.3f}")
    
    # 8. Collection information
    print(f"\n📈 Collection Info: {vector_db.get_collection_info()}")

if __name__ == "__main__":
    complete_embedding_workflow()
```

### **Step 4: Best Practices and Optimization**

#### **Performance Tips**

1. **Batch Processing:**
   - Use batch API calls (up to 100 texts per request)
   - Implement rate limiting to avoid API throttling
   - Cache embeddings for repeated queries

2. **Text Preprocessing:**
   - Clean and normalize text before embedding
   - Remove unnecessary whitespace and special characters
   - Consider text length limits (8K tokens for ada-002)

3. **Error Handling:**
   - Implement retry logic for failed API calls
   - Handle rate limiting gracefully
   - Log errors for debugging

4. **Cost Optimization:**
   - Monitor API usage and costs
   - Cache embeddings when possible
   - Use appropriate chunk sizes to minimize API calls

#### **Security Considerations**

1. **API Key Management:**
   - Never hardcode API keys
   - Use environment variables or secure key management
   - Rotate keys regularly

2. **Data Privacy:**
   - Be aware of what data you're sending to OpenAI
   - Consider data residency requirements
   - Implement data retention policies

## 🔄 **n8n Integration Guide**

### **What is n8n?**

n8n is a powerful workflow automation tool that allows you to connect different services and APIs to create automated business processes. It's perfect for integrating your vector database with real-world applications.

### **Step 1: Setting Up n8n**

1. **Install n8n:**
   ```bash
   # Using npm
   npm install n8n -g
   
   # Using Docker
   docker run -it --rm \
     --name n8n \
     -p 5678:5678 \
     -v ~/.n8n:/home/node/.n8n \
     n8nio/n8n
   ```

2. **Access n8n:**
   - Open browser: `http://localhost:5678`
   - Create account and workspace

### **Step 2: Creating Vector Database API Endpoints**

To use your vector database with n8n, you'll need to create REST API endpoints. Here's how:

#### **FastAPI Integration Example**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn

app = FastAPI(title="Vector Database API", version="1.0.0")

# Data models
class SearchQuery(BaseModel):
    text: str
    n_results: int = 5
    filters: Optional[Dict[str, Any]] = None

class DocumentInput(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    documents: List[str]
    metadatas: List[Dict[str, Any]]
    distances: List[float]
    similarity_scores: List[float]

# Initialize your components
embeddings_client = OpenAIEmbeddings()
vector_db = VectorDatabase()
vector_db.create_collection("n8n_documents")

@app.post("/documents", response_model=Dict[str, str])
async def add_document(document: DocumentInput):
    """Add a new document to the vector database"""
    try:
        # Create embedding
        embedding = embeddings_client.create_embedding(document.text)
        if not embedding:
            raise HTTPException(status_code=500, detail="Failed to create embedding")
        
        # Add to vector database
        vector_db.add_embeddings(
            texts=[document.text],
            embeddings=[embedding],
            metadatas=[document.metadata or {}]
        )
        
        return {"message": "Document added successfully", "status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=SearchResult)
async def search_documents(query: SearchQuery):
    """Search for similar documents"""
    try:
        # Create query embedding
        query_embedding = embeddings_client.create_embedding(query.text)
        if not query_embedding:
            raise HTTPException(status_code=500, detail="Failed to create query embedding")
        
        # Search vector database
        results = vector_db.search_similar(
            query_embedding, 
            n_results=query.n_results,
            where=query.filters
        )
        
        if not results:
            raise HTTPException(status_code=500, detail="Search failed")
        
        # Calculate similarity scores
        similarity_scores = [1 - distance for distance in results['distances'][0]]
        
        return SearchResult(
            documents=results['documents'][0],
            metadatas=results['metadatas'][0],
            distances=results['distances'][0],
            similarity_scores=similarity_scores
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "vector-database-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### **Step 3: n8n Workflow Examples**

#### **Example 1: Automated Document Processing**

This workflow automatically processes incoming documents and adds them to your vector database:

```
📧 Email Trigger → 📄 Extract Text → 🤖 Create Embedding → 💾 Store in Vector DB → 📧 Send Confirmation
```

**n8n Node Configuration:**

1. **Email Trigger Node:**
   - Configure to watch for new emails
   - Extract email body and attachments

2. **Code Node (Text Extraction):**
   ```javascript
   // Extract text from email body and attachments
   const emailBody = $input.first().json.body;
   const attachments = $input.first().json.attachments || [];
   
   let allText = emailBody;
   
   // Process attachments (PDF, Word docs, etc.)
   for (const attachment of attachments) {
     if (attachment.mimeType.includes('text')) {
       allText += '\n' + attachment.content;
     }
   }
   
   return [{ text: allText, emailId: $input.first().json.id }];
   ```

3. **HTTP Request Node (Add to Vector DB):**
   - Method: POST
   - URL: `http://localhost:8000/documents`
   - Body: 
     ```json
     {
       "text": "{{ $json.text }}",
       "metadata": {
         "source": "email",
         "emailId": "{{ $json.emailId }}",
         "timestamp": "{{ $now }}"
       }
     }
     ```

4. **Email Node (Confirmation):**
   - Send confirmation email to sender

#### **Example 2: Intelligent Customer Support**

This workflow uses your vector database to provide intelligent responses to customer inquiries:

```
💬 Customer Message → 🔍 Search Knowledge Base → 🤖 Generate Response → 💬 Send Reply
```

**n8n Node Configuration:**

1. **Webhook Node:**
   - Receives customer messages from your website/chat system

2. **HTTP Request Node (Search Vector DB):**
   - Method: POST
   - URL: `http://localhost:8000/search`
   - Body:
     ```json
     {
       "text": "{{ $json.message }}",
       "n_results": 3,
       "filters": {
         "category": "support"
       }
     }
     ```

3. **Code Node (Process Results):**
   ```javascript
   const searchResults = $input.first().json;
   const customerMessage = $('Webhook').first().json.message;
   
   // Find the most relevant result
   const bestMatch = searchResults.documents[0];
   const similarity = searchResults.similarity_scores[0];
   
   let response;
   if (similarity > 0.8) {
     response = `Based on our knowledge base: ${bestMatch}`;
   } else {
     response = "I'll need to research this further. Let me get back to you.";
   }
   
   return [{
     response: response,
     similarity: similarity,
     customerMessage: customerMessage
   }];
   ```

4. **HTTP Request Node (Send Response):**
   - Send the response back to your customer support system

#### **Example 3: Content Recommendation Engine**

This workflow recommends relevant content based on user behavior:

```
👤 User Activity → 🔍 Find Similar Content → 📊 Rank Results → 📧 Send Recommendations
```

**n8n Node Configuration:**

1. **Database Node:**
   - Query user activity/reading history

2. **HTTP Request Node (Search Vector DB):**
   - Method: POST
   - URL: `http://localhost:8000/search`
   - Body:
     ```json
     {
       "text": "{{ $json.userInterests }}",
       "n_results": 10,
       "filters": {
         "difficulty": "{{ $json.userLevel }}"
       }
     }
     ```

3. **Code Node (Rank and Filter):**
   ```javascript
   const results = $input.first().json;
   const userPreferences = $('Database').first().json;
   
   // Filter and rank results
   const recommendations = results.documents
     .map((doc, index) => ({
       content: doc,
       metadata: results.metadatas[index],
       score: results.similarity_scores[index]
     }))
     .filter(item => item.score > 0.7)
     .sort((a, b) => b.score - a.score)
     .slice(0, 5);
   
   return [{
     userId: userPreferences.userId,
     recommendations: recommendations
   }];
   ```

4. **Email Node (Send Recommendations):**
   - Send personalized content recommendations

### **Step 4: Advanced n8n Features**

#### **Error Handling and Retries**

Configure your HTTP Request nodes with:
- **Retry on Failure:** 3 attempts
- **Retry Delay:** 5 seconds
- **Timeout:** 30 seconds

#### **Data Validation**

Use n8n's **Set** node to validate and transform data:
```javascript
// Validate search query
if (!$input.first().json.text || $input.first().json.text.length < 3) {
  throw new Error("Search query must be at least 3 characters long");
}

// Transform data
return [{
  processedText: $input.first().json.text.trim().toLowerCase(),
  timestamp: new Date().toISOString()
}];
```

#### **Conditional Workflows**

Use **IF** nodes to create different paths:
- If similarity > 0.9: Send immediate response
- If similarity > 0.7: Send response with additional resources
- If similarity < 0.7: Escalate to human support

### **Step 5: Monitoring and Analytics**

#### **n8n Execution History**

- Monitor workflow success/failure rates
- Track execution times
- Identify bottlenecks

#### **Custom Metrics**

Add logging nodes to track:
- Search query patterns
- Response quality scores
- User satisfaction metrics

### **Step 6: Production Deployment**

#### **Docker Compose Setup**

```yaml
version: '3.8'
services:
  vector-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
  
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
    volumes:
      - ~/.n8n:/home/node/.n8n
```

#### **Environment Variables**

Create `.env` file:
```bash
OPENAI_API_KEY=your_openai_key
N8N_PASSWORD=secure_password
VECTOR_DB_PATH=/app/data
```

### **Benefits of n8n Integration**

1. **Visual Workflow Design:** Drag-and-drop interface for complex workflows
2. **Real-time Processing:** Immediate response to events
3. **Scalability:** Handle multiple requests simultaneously
4. **Integration:** Connect with 200+ services (Slack, CRM, databases, etc.)
5. **Monitoring:** Built-in execution tracking and error handling
6. **Customization:** JavaScript code nodes for complex logic

### **Use Cases for Vector DB + n8n**

- **Customer Support Automation:** Instant responses based on knowledge base
- **Content Recommendation:** Personalized suggestions for users
- **Document Classification:** Automatic categorization of incoming documents
- **Search Enhancement:** Improve search results with semantic understanding
- **Compliance Monitoring:** Track and analyze document content
- **Knowledge Management:** Build and maintain organizational knowledge bases

## 📁 Folder Checklist

```
week5_vector_db/
├── README.md                    # This file
└── submission/
    ├── vector_db.py            # Vector database operations
    ├── embeddings.py           # Embedding generation with OpenAI
    ├── search.py               # Search functionality
    ├── config.py               # Database configuration
    ├── tests/                  # Test suite
    ├── examples/               # Working examples
    │   ├── basic_embeddings.py
    │   ├── document_chunking.py
    │   └── vector_search.py
    ├── n8n_integration/        # n8n workflow examples
    │   ├── api_server.py       # FastAPI server for n8n
    │   ├── workflows/          # n8n workflow JSON files
    │   └── docker-compose.yml  # Production setup
    └── README.md               # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Week 4 completion
- Python 3.9+
- Pinecone account or ChromaDB setup
- OpenAI API key
- n8n (optional, for workflow automation)

### Setup Instructions

1. **Install required packages**
   ```bash
   pip install openai pinecone-client chromadb numpy pandas tiktoken fastapi uvicorn
   ```

2. **Set up API keys**
   - Configure OpenAI API key
   - Set up Pinecone/ChromaDB credentials
   - Create `.env` file for environment variables

3. **Run the examples**
   ```bash
   cd submission/examples
   python basic_embeddings.py
   python document_chunking.py
   python vector_search.py
   ```

4. **Start the API server**
   ```bash
   cd submission/n8n_integration
   python api_server.py
   ```

5. **Import n8n workflows**
   - Open n8n at http://localhost:5678
   - Import workflow JSON files from `n8n_integration/workflows/`

## 📝 Submission Instructions

### Due Date
**Friday, 5:00 PM**

### Submission Format
- Vector database implementation
- Search functionality code
- Performance benchmarks
- Integration documentation
- Working examples with OpenAI embeddings
- n8n workflow examples (optional but recommended)

## 📚 Suggested Resources

- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Vector Database Guide](https://www.pinecone.io/learn/vector-database/)
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/embeddings/use-cases)
- [n8n Documentation](https://docs.n8n.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [n8n Community Workflows](https://n8n.io/workflows)

---

**Focus**: Building efficient semantic search capabilities for AI-powered applications using OpenAI's powerful embedding models, with practical integration into business workflows using n8n. 