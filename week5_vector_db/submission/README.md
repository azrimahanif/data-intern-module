# Week5 Vector Db Submission

## 📁 Submission Contents

This folder contains your Week5 Vector Db assignments.

### Required Files
- [ ] Add your required files here
- [ ] Based on the weekly requirements
- [ ] Check the main README.md for details

### Submission Checklist
- [ ] All requirements completed
- [ ] Code quality standards met
- [ ] Documentation is complete
- [ ] Tests are passing
- [ ] Ready for review

## 🚀 How to Run

1. Activate virtual environment
    - .venv\Scripts\activate 

2. Install dependencies
    - pip install -r requirements.txt

3. Run demo script
    - python -m submission.demo

4. Run API server (for Postman/browser)
    - uvicorn submission.api:app --reload
    - Open http://127.0.0.1:8000/docs


## 📊 Results Summary

1. Indexing & Embedding: Successfully converted documents into embeddings using sentence-transformers.

2. Search: Implemented normal search, filter-based search, hybrid search (keyword + semantic), and reranking; all returned results with similarity scores.

3. Analytics: Captured query logs, top queries, and execution runtime in milliseconds.

4. API: All endpoints (/index, /search, /analytics) are accessible through Swagger UI and Postman.

5. Testing: All unit tests (FastAPI TestClient + function tests) passed without errors.


## 🎯 Learning Outcomes

1. Understood how vector databases (ChromaDB, Pinecone) store embeddings for semantic search.

2. Learned how to use SentenceTransformers to generate text embeddings.

3. Gained experience implementing a search pipeline with normal, hybrid, and rerank strategies.

4. Learned how to capture and analyze search analytics (logs, query frequency, runtime).

5. Built and exposed FastAPI endpoints, tested using Swagger UI and Postman.

6. Practiced automated testing with pytest and FastAPI’s TestClient.

7. Improved skills in managing projects with virtual environments and requirements.txt.
