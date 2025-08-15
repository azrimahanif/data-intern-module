import requests
import os

BASE_URL = "http://localhost:8000"

def upload_excel():
    print("\n=== 1. Upload Excel ===")
    file_path = os.path.join("starter", "sample_employees.xlsx")
    files = {"file": open(file_path, "rb")}
    r = requests.post(f"{BASE_URL}/files/upload-excel", files=files)
    print(r.status_code, r.json())

def list_employees():
    print("\n=== 2. List Employees ===")
    r = requests.get(f"{BASE_URL}/employees/")
    print(r.status_code, r.json())
    return r.json()

def create_employee():
    print("\n=== 3. Create Employee ===")
    payload = {
        "employee_id": "T123",
        "name": "Test User",
        "email": "test.user@example.com",
        "department": "QA",
        "position": "Tester",
        "salary": 50000,
        "hire_date": "2023-01-01T00:00:00",
        "status": "active"
    }
    r = requests.post(f"{BASE_URL}/employees/", json=payload)
    print(r.status_code, r.json())
    return r.json().get("id")

def update_employee(emp_id):
    print("\n=== 4. Update Employee ===")
    payload = {
        "name": "Test User Updated",
        "salary": 55000
    }
    r = requests.put(f"{BASE_URL}/employees/{emp_id}", json=payload)
    print(r.status_code, r.json())

def delete_employee(emp_id):
    print("\n=== 5. Delete Employee ===")
    r = requests.delete(f"{BASE_URL}/employees/{emp_id}")
    print(r.status_code, r.json())

if __name__ == "__main__":
    # 1. Upload Excel
    upload_excel()

    # 2. List employees
    employees = list_employees()

    # 3. Create new employee
    emp_id = create_employee()

    # 4. Update that employee
    update_employee(emp_id)
    list_employees()

    # 5. Delete that employee
    delete_employee(emp_id)
    list_employees()
