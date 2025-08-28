# n8n Integration Guide for Vector Database

## 🔄 **What is n8n?**

n8n is a powerful workflow automation tool that allows you to connect different services and APIs to create automated business processes. It's perfect for integrating your vector database with real-world applications.

## 🚀 **Getting Started with n8n**

### **Step 1: Installation**

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

### **Step 2: Access n8n**
- Open browser: `http://localhost:5678`
- Create account and workspace

## 🔌 **Creating Vector Database API Endpoints**

To use your vector database with n8n, you'll need to create REST API endpoints.

### **FastAPI Integration Example**

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

## 📋 **n8n Workflow Examples**

### **Example 1: Automated Document Processing**

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

### **Example 2: Intelligent Customer Support**

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

### **Example 3: Content Recommendation Engine**

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

## ⚙️ **Advanced n8n Features**

### **Error Handling and Retries**

Configure your HTTP Request nodes with:
- **Retry on Failure:** 3 attempts
- **Retry Delay:** 5 seconds
- **Timeout:** 30 seconds

### **Data Validation**

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

### **Conditional Workflows**

Use **IF** nodes to create different paths:
- If similarity > 0.9: Send immediate response
- If similarity > 0.7: Send response with additional resources
- If similarity < 0.7: Escalate to human support

## 📊 **Monitoring and Analytics**

### **n8n Execution History**

- Monitor workflow success/failure rates
- Track execution times
- Identify bottlenecks

### **Custom Metrics**

Add logging nodes to track:
- Search query patterns
- Response quality scores
- User satisfaction metrics

## 🚀 **Production Deployment**

### **Docker Compose Setup**

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

### **Environment Variables**

Create `.env` file:
```bash
OPENAI_API_KEY=your_openai_key
N8N_PASSWORD=secure_password
VECTOR_DB_PATH=/app/data
```

## 💡 **Benefits of n8n Integration**

1. **Visual Workflow Design:** Drag-and-drop interface for complex workflows
2. **Real-time Processing:** Immediate response to events
3. **Scalability:** Handle multiple requests simultaneously
4. **Integration:** Connect with 200+ services (Slack, CRM, databases, etc.)
5. **Monitoring:** Built-in execution tracking and error handling
6. **Customization:** JavaScript code nodes for complex logic

## 🎯 **Use Cases for Vector DB + n8n**

- **Customer Support Automation:** Instant responses based on knowledge base
- **Content Recommendation:** Personalized suggestions for users
- **Document Classification:** Automatic categorization of incoming documents
- **Search Enhancement:** Improve search results with semantic understanding
- **Compliance Monitoring:** Track and analyze document content
- **Knowledge Management:** Build and maintain organizational knowledge bases

## 📚 **Additional Resources**

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community Workflows](https://n8n.io/workflows)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [n8n YouTube Channel](https://www.youtube.com/c/n8n-io)

## 🔧 **Troubleshooting Tips**

1. **API Connection Issues:**
   - Check if your FastAPI server is running
   - Verify the correct port (8000)
   - Test endpoints with Postman or curl

2. **Workflow Failures:**
   - Check n8n execution logs
   - Verify data format between nodes
   - Test individual nodes for errors

3. **Performance Issues:**
   - Monitor API response times
   - Check vector database performance
   - Optimize batch sizes for embeddings

4. **Authentication Problems:**
   - Verify API keys are correct
   - Check environment variables
   - Ensure proper CORS configuration

---

**Next Steps:** Start with simple workflows and gradually build complexity. Test thoroughly in development before deploying to production!
