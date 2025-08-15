from fastapi.testclient import TestClient
from main import app
import io
import pandas as pd

client = TestClient(app)

def test_file_upload():
    df = pd.DataFrame([
        {
            "employee_id": "FX001",
            "name": "File X",
            "email": "file.x@example.com",
            "department": "Ops",
            "position": "Operator",
            "salary": 40000,
            "hire_date": "2023-02-01",
            "status": "active",
        }
    ])
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    buf.seek(0)
    files = {"file": ("test_upload.xlsx", buf, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    r = client.post("/files/upload-excel", files=files)
    assert r.status_code == 200
    assert "processed_records" in r.json()