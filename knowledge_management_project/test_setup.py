#!/usr/bin/env python3
"""
Test Setup Script
Run this to verify your Knowledge Management System setup
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test if all required environment variables are set"""
    print("🔍 Testing Environment Variables...")
    
    required_vars = [
        'OPENAI_API_KEY',
        'QDRANT_URL', 
        'QDRANT_API_KEY',
        'DATABASE_URL',
        'N8N_BASE_URL',
        'N8N_WEBHOOK_TOKEN',
        'AI_AGENT_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            print(f"❌ {var}: Not set")
        else:
            print(f"✅ {var}: Set")
    
    if missing_vars:
        print(f"\n⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with the required values.")
        return False
    
    print("✅ All environment variables are set!")
    return True

def test_openai():
    """Test OpenAI API connection"""
    print("\n🤖 Testing OpenAI API...")
    
    try:
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Test with a simple embedding
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input="test"
        )
        
        if response and 'data' in response:
            embedding = response['data'][0]['embedding']
            print(f"✅ OpenAI API working! Embedding dimensions: {len(embedding)}")
            return True
        else:
            print("❌ OpenAI API response invalid")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        return False

def test_qdrant():
    """Test Qdrant connection"""
    print("\n🗄️ Testing Qdrant Connection...")
    
    try:
        qdrant_url = os.getenv('QDRANT_URL')
        response = requests.get(f"{qdrant_url}/collections", timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Qdrant connection successful!")
            return True
        else:
            print(f"❌ Qdrant connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Qdrant test failed: {e}")
        return False

def test_n8n():
    """Test n8n connection"""
    print("\n🔄 Testing n8n Connection...")
    
    try:
        n8n_url = os.getenv('N8N_BASE_URL')
        response = requests.get(n8n_url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ n8n connection successful!")
            return True
        else:
            print(f"❌ n8n connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ n8n test failed: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n💾 Testing Database Connection...")
    
    try:
        import psycopg2
        database_url = os.getenv('DATABASE_URL')
        
        # Test connection
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        
        print(f"✅ Database connection successful! PostgreSQL version: {version[0]}")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_ai_agent():
    """Test AI agent connection"""
    print("\n🧠 Testing AI Agent Connection...")
    
    try:
        ai_agent_url = os.getenv('AI_AGENT_URL')
        if not ai_agent_url:
            print("⚠️ AI_AGENT_URL not set, skipping test")
            return True
            
        response = requests.get(ai_agent_url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ AI Agent connection successful!")
            return True
        else:
            print(f"❌ AI Agent connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI Agent test failed: {e}")
        return False

def test_api_server():
    """Test if the API server is running"""
    print("\n🚀 Testing API Server...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        
        if response.status_code == 200:
            print("✅ API server is running!")
            return True
        else:
            print(f"❌ API server returned status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ API server is not running. Start it with: uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ API server test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Knowledge Management System - Setup Test")
    print("=" * 50)
    
    # Test environment variables
    if not test_environment():
        print("\n❌ Environment setup incomplete. Please fix missing variables.")
        return
    
    # Test individual services
    tests = [
        test_openai,
        test_qdrant,
        test_n8n,
        test_database,
        test_ai_agent
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    # Test API server (optional)
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Start the API server: uvicorn main:app --reload")
        print("2. Test document upload")
        print("3. Test search functionality")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("- Verify API keys and URLs")
        print("- Check network connectivity")
        print("- Ensure services are running")
    
    # Test API server if other tests passed
    if passed == total:
        print("\n" + "=" * 50)
        test_api_server()

if __name__ == "__main__":
    main()
