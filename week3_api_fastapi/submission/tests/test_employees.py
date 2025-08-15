from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"

def test_crud_employee():
    payload = {
        "employee_id": "TEST01",
        "name": "Test User",
        "email": "test.user@example.com",
        "department": "QA",
        "position": "Tester",
        "salary": 50000,
        "hire_date": "2023-01-01T00:00:00",
        "status": "active"
    }
    # Create
    r = client.post("/employees/", json=payload)
    assert r.status_code == 200
    emp_id = r.json()["id"]
    # Read
    r = client.get(f"/employees/{emp_id}")
    assert r.status_code == 200
    # Update
    r = client.put(f"/employees/{emp_id}", json={"position": "Senior Tester"})
    assert r.status_code == 200
    assert r.json()["position"] == "Senior Tester"
    # Delete
    r = client.delete(f"/employees/{emp_id}")
    assert r.status_code == 200
    assert r.json()["detail"] == "deleted"
