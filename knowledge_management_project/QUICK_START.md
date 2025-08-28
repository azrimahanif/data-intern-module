# 🚀 **Quick Start Guide - Knowledge Management System**

## ⚡ **Get Running in 5 Minutes**

### **1. Setup Environment**
```bash
# Copy environment template
cp env_template.txt .env

# Edit .env with your actual credentials
# You'll need:
# - OpenAI API key
# - Qdrant connection details
# - Database connection string
# - n8n webhook tokens
# - AI agent credentials
```

### **2. Install Dependencies**
```bash
cd api
pip install -r requirements.txt
```

### **3. Test Connections**
```bash
# Start the API server
uvicorn main:app --reload

# In another terminal, test health check
curl http://localhost:8000/health
```

### **4. Upload Your First Document**
```bash
# Test document upload
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf"
```

### **5. Search Documents**
```bash
# Test search functionality
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "your search term", "limit": 5}'
```

## 🔧 **What You Need to Configure**

### **Required Services:**
1. **OpenAI API Key** - For embeddings
2. **Qdrant Instance** - [https://qdrant.aafiyat2u.net/](https://qdrant.aafiyat2u.net/)
3. **n8n Instance** - [https://n8n.aafiyat2u.net](https://n8n.aafiyat2u.net)
4. **SQL Database** - PostgreSQL (provided)
5. **AI Agent** - (provided)

### **Environment Variables:**
```bash
# Core API Keys
OPENAI_API_KEY=sk-...
QDRANT_API_KEY=your_qdrant_key
DATABASE_URL=postgresql://...

# n8n Integration
N8N_WEBHOOK_TOKEN=your_webhook_token
N8N_API_KEY=your_api_key

# AI Agent
AI_AGENT_URL=your_ai_agent_url
AI_AGENT_API_KEY=your_ai_agent_key
```

## 📁 **Project Structure Overview**

```
knowledge_management_project/
├── api/                    # FastAPI server
│   ├── main.py            # Main application
│   ├── services/          # Service connections
│   └── requirements.txt   # Python dependencies
├── n8n_workflows/         # n8n workflow files
├── looker_studio/         # Dashboard configs
├── ai_agent/              # AI agent configs
└── README.md              # Full documentation
```

## 🎯 **Week 1 Goals (First 5 Days)**

### **Day 1: Connect to Services**
- ✅ Test Qdrant connection
- ✅ Test database connection
- ✅ Test n8n connection
- ✅ Test AI agent connection

### **Day 2: Basic API**
- ✅ Start FastAPI server
- ✅ Test health endpoint
- ✅ Verify all services connected

### **Day 3: Document Upload**
- ✅ Implement file upload
- ✅ Test with sample PDF
- ✅ Verify storage in Qdrant

### **Day 4: Search Functionality**
- ✅ Implement vector search
- ✅ Test search queries
- ✅ Verify results

### **Day 5: Integration Test**
- ✅ End-to-end document flow
- ✅ Search and retrieval
- ✅ Basic error handling

## 🚨 **Common Issues & Solutions**

### **Connection Errors:**
```bash
# Qdrant connection failed
# Solution: Check QDRANT_URL and QDRANT_API_KEY in .env

# Database connection failed
# Solution: Verify DATABASE_URL format and credentials

# n8n connection failed
# Solution: Check N8N_BASE_URL and webhook tokens
```

### **OpenAI API Errors:**
```bash
# API key invalid
# Solution: Get new key from OpenAI platform

# Rate limit exceeded
# Solution: Wait or upgrade plan

# Model not found
# Solution: Verify text-embedding-ada-002 is available
```

### **File Upload Issues:**
```bash
# File too large
# Solution: Check MAX_FILE_SIZE in .env

# Unsupported file type
# Solution: Use PDF, DOC, DOCX, TXT, MD, CSV, XLSX, XLS
```

## 📊 **Testing Your Setup**

### **Health Check Response:**
```json
{
  "overall_status": "healthy",
  "services": {
    "qdrant": {"status": "connected"},
    "database": {"status": "connected"},
    "n8n": {"status": "connected"},
    "ai_agent": {"status": "connected"}
  }
}
```

### **Successful Document Upload:**
```json
{
  "message": "Document processed successfully",
  "document_id": "uuid-here",
  "ai_analysis": {
    "category": "technical",
    "tags": ["api", "documentation"],
    "priority": "medium"
  }
}
```

### **Successful Search:**
```json
{
  "query": "your search term",
  "results": [
    {
      "id": "doc-id",
      "score": 0.95,
      "content": "Document content...",
      "metadata": {...}
    }
  ]
}
```

## 🔗 **Useful Links**

- **API Documentation:** http://localhost:8000/docs
- **Qdrant:** [https://qdrant.aafiyat2u.net/](https://qdrant.aafiyat2u.net/)
- **n8n:** [https://n8n.aafiyat2u.net](https://n8n.aafiyat2u.net)
- **OpenAI:** [https://platform.openai.com/](https://platform.openai.com/)

## 🆘 **Need Help?**

1. **Check the logs** - Look for error messages
2. **Verify environment** - Ensure all variables are set
3. **Test connections** - Use the health endpoint
4. **Check documentation** - Review README.md
5. **Ask for support** - Contact your mentor

---

**Ready to build something amazing? Let's go! 🚀**
