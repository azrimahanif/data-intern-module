"""
n8n Service
Connects to existing n8n instance at https://n8n.aafiyat2u.net
"""

import requests
from typing import Dict, Any, Optional
import os
from datetime import datetime
import json

class N8nService:
    def __init__(self):
        """Initialize n8n service connection"""
        self.base_url = os.getenv("N8N_BASE_URL", "https://n8n.aafiyat2u.net")
        self.webhook_token = os.getenv("N8N_WEBHOOK_TOKEN")
        self.api_key = os.getenv("N8N_API_KEY")
        
        # Headers for API requests
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "KnowledgeManagementSystem/1.0"
        }
        
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def test_connection(self) -> Dict[str, Any]:
        """Test connection to n8n instance"""
        try:
            # Try to access n8n health endpoint or main page
            response = requests.get(
                f"{self.base_url}/healthz",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "status": "connected",
                    "url": self.base_url,
                    "response_time": response.elapsed.total_seconds(),
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                # Try alternative endpoint
                response = requests.get(
                    self.base_url,
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    return {
                        "status": "connected",
                        "url": self.base_url,
                        "response_time": response.elapsed.total_seconds(),
                        "timestamp": datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        "status": "error",
                        "url": self.base_url,
                        "status_code": response.status_code,
                        "error": "Could not connect to n8n instance",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "url": self.base_url,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def trigger_document_processing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger n8n workflow for document processing"""
        try:
            if not self.webhook_token:
                print("⚠️ Warning: N8N_WEBHOOK_TOKEN not set. Cannot trigger workflow.")
                return {"status": "error", "message": "Webhook token not configured"}
            
            webhook_url = f"{self.base_url}/webhook/document-processing"
            
            payload = {
                "trigger": "document_processing",
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "knowledge_management_system"
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code in [200, 201, 202]:
                print(f"✅ Document processing workflow triggered successfully")
                return {
                    "status": "success",
                    "workflow": "document_processing",
                    "response": response.json() if response.content else None,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                print(f"❌ Failed to trigger document processing workflow: {response.status_code}")
                return {
                    "status": "error",
                    "workflow": "document_processing",
                    "status_code": response.status_code,
                    "error": response.text,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            print(f"❌ Error triggering document processing workflow: {e}")
            return {
                "status": "error",
                "workflow": "document_processing",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def trigger_search_analytics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger n8n workflow for search analytics"""
        try:
            if not self.webhook_token:
                print("⚠️ Warning: N8N_WEBHOOK_TOKEN not set. Cannot trigger workflow.")
                return {"status": "error", "message": "Webhook token not configured"}
            
            webhook_url = f"{self.base_url}/webhook/search-analytics"
            
            payload = {
                "trigger": "search_analytics",
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "knowledge_management_system"
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code in [200, 201, 202]:
                print(f"✅ Search analytics workflow triggered successfully")
                return {
                    "status": "success",
                    "workflow": "search_analytics",
                    "response": response.json() if response.content else None,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                print(f"❌ Failed to trigger search analytics workflow: {response.status_code}")
                return {
                    "status": "error",
                    "workflow": "search_analytics",
                    "status_code": response.status_code,
                    "error": response.text,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            print(f"❌ Error triggering search analytics workflow: {e}")
            return {
                "status": "error",
                "workflow": "search_analytics",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def trigger_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger n8n workflow for notifications"""
        try:
            if not self.webhook_token:
                print("⚠️ Warning: N8N_WEBHOOK_TOKEN not set. Cannot trigger workflow.")
                return {"status": "error", "message": "Webhook token not configured"}
            
            webhook_url = f"{self.base_url}/webhook/notifications"
            
            payload = {
                "trigger": "notification",
                "data": notification_data,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "knowledge_management_system"
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code in [200, 201, 202]:
                print(f"✅ Notification workflow triggered successfully")
                return {
                    "status": "success",
                    "workflow": "notification",
                    "response": response.json() if response.content else None,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                print(f"❌ Failed to trigger notification workflow: {response.status_code}")
                return {
                    "status": "error",
                    "workflow": "notification",
                    "status_code": response.status_code,
                    "error": response.text,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            print(f"❌ Error triggering notification workflow: {e}")
            return {
                "status": "error",
                "workflow": "notification",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a specific workflow"""
        try:
            if not self.api_key:
                print("⚠️ Warning: N8N_API_KEY not set. Cannot get workflow status.")
                return {"status": "error", "message": "API key not configured"}
            
            response = requests.get(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                workflow_data = response.json()
                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "workflow_name": workflow_data.get("name", "Unknown"),
                    "active": workflow_data.get("active", False),
                    "last_execution": workflow_data.get("lastExecutedAt"),
                    "execution_count": workflow_data.get("executionCount", 0),
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "workflow_id": workflow_id,
                    "status_code": response.status_code,
                    "error": response.text,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def list_workflows(self) -> Dict[str, Any]:
        """List all available workflows"""
        try:
            if not self.api_key:
                print("⚠️ Warning: N8N_API_KEY not set. Cannot list workflows.")
                return {"status": "error", "message": "API key not configured"}
            
            response = requests.get(
                f"{self.base_url}/api/v1/workflows",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                workflows = response.json()
                return {
                    "status": "success",
                    "total_workflows": len(workflows),
                    "workflows": [
                        {
                            "id": w.get("id"),
                            "name": w.get("name"),
                            "active": w.get("active", False),
                            "last_execution": w.get("lastExecutedAt"),
                            "execution_count": w.get("executionCount", 0)
                        }
                        for w in workflows
                    ],
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "status_code": response.status_code,
                    "error": response.text,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def execute_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific workflow with data"""
        try:
            if not self.api_key:
                print("⚠️ Warning: N8N_API_KEY not set. Cannot execute workflow.")
                return {"status": "error", "message": "API key not configured"}
            
            response = requests.post(
                f"{self.base_url}/api/v1/workflows/{workflow_id}/execute",
                json=data,
                headers=self.headers,
                timeout=60
            )
            
            if response.status_code in [200, 201, 202]:
                execution_data = response.json()
                return {
                    "status": "success",
                    "workflow_id": workflow_id,
                    "execution_id": execution_data.get("executionId"),
                    "response": execution_data,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "workflow_id": workflow_id,
                    "status_code": response.status_code,
                    "error": response.text,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def get_execution_logs(self, execution_id: str) -> Dict[str, Any]:
        """Get execution logs for a specific workflow execution"""
        try:
            if not self.api_key:
                print("⚠️ Warning: N8N_API_KEY not set. Cannot get execution logs.")
                return {"status": "error", "message": "API key not configured"}
            
            response = requests.get(
                f"{self.base_url}/api/v1/executions/{execution_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                execution_data = response.json()
                return {
                    "status": "success",
                    "execution_id": execution_id,
                    "workflow_id": execution_data.get("workflowId"),
                    "status": execution_data.get("status"),
                    "started_at": execution_data.get("startedAt"),
                    "finished_at": execution_data.get("finishedAt"),
                    "data": execution_data.get("data"),
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "execution_id": execution_id,
                    "status_code": response.status_code,
                    "error": response.text,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            return {
                "status": "error",
                "execution_id": execution_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
