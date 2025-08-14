# Week 3: FastAPI Development - Excel Data Processing APIcd

## 🎯 Week Goals

Build a comprehensive FastAPI application that processes Excel files, stores data in a database, and provides RESTful API endpoints for data management. Learn to create production-ready APIs with file handling, data validation, and database integration.

### 📚 Learning Objectives

- **FastAPI Fundamentals**
  - Create RESTful API endpoints
  - Implement request/response models with Pydantic
  - Handle file uploads and processing
  - Add automatic API documentation

- **File Processing & Data Handling**
  - Process Excel files using pandas
  - Validate and clean data
  - Handle different file formats (.xlsx, .xls, .csv)
  - Implement error handling for file operations

- **Database Integration**
  - Connect APIs to SQLite/PostgreSQL using SQLAlchemy
  - Store processed Excel data in database
  - Implement CRUD operations for data management
  - Create database models and relationships

## 🏗️ Project: Employee Data Management API

You'll build an **Employee Data Management System** that:
1. Accepts Excel file uploads containing employee information
2. Processes and validates the data
3. Stores cleaned data in a database
4. Provides REST API endpoints for data operations
5. Generates reports and analytics

### 📊 Sample Data Structure
Your Excel files will contain employee data with columns:
- Employee ID, Name, Email, Department, Position, Salary, Hire Date, Status

## 📋 Step-by-Step Assignments

### Phase 1: Project Setup & Basic API (25 points)
- [ ] Set up FastAPI project structure
- [ ] Create basic "Hello World" endpoint
- [ ] Set up development environment with uvicorn
- [ ] Create Pydantic models for Employee data
- [ ] Implement basic CRUD endpoints (without database)

### Phase 2: File Upload & Processing (30 points)
- [ ] Create file upload endpoint for Excel files
- [ ] Implement Excel file processing with pandas
- [ ] Add data validation and cleaning logic
- [ ] Handle different file formats (.xlsx, .csv)
- [ ] Implement proper error handling for file operations

### Phase 3: Database Integration (25 points)
- [ ] Set up SQLAlchemy with SQLite database
- [ ] Create Employee database model
- [ ] Implement database CRUD operations
- [ ] Connect file processing to database storage
- [ ] Add database migration capabilities

### Phase 4: Advanced Features & Testing (20 points)
- [ ] Add data analytics endpoints (salary statistics, department counts)
- [ ] Implement data export functionality (Excel/CSV download)
- [ ] Write comprehensive API tests
- [ ] Add request/response logging
- [ ] Create API documentation and usage examples

## 📁 Required Project Structure

```
week3_api_fastapi/
├── README.md                           # This file
├── starter/                            # Provided starter files
│   ├── requirements.txt               # Python dependencies
│   ├── sample_employees.xlsx          # Sample Excel data
│   └── .env.example                   # Environment variables template
└── submission/
    ├── main.py                        # FastAPI application entry point
    ├── models/                        # Data models
    │   ├── __init__.py
    │   ├── employee.py               # Pydantic models
    │   └── database.py               # SQLAlchemy models
    ├── services/                      # Business logic
    │   ├── __init__.py
    │   ├── file_processor.py         # Excel processing logic
    │   └── employee_service.py       # Employee operations
    ├── routers/                       # API endpoints
    │   ├── __init__.py
    │   ├── employees.py              # Employee CRUD endpoints
    │   └── files.py                  # File upload endpoints
    ├── database/                      # Database configuration
    │   ├── __init__.py
    │   ├── connection.py             # Database setup
    │   └── crud.py                   # Database operations
    ├── tests/                         # API tests
    │   ├── __init__.py
    │   ├── test_employees.py
    │   └── test_file_upload.py
    ├── uploads/                       # Uploaded files storage
    ├── requirements.txt               # Dependencies
    ├── .env                          # Environment variables
    └── README.md                     # Project documentation
```

## 🚀 Step-by-Step Implementation Guide

> **Important**: Follow these steps exactly in order. Test each phase before moving to the next!

### 🔧 **Setup Phase: Environment & Tools**

#### Step 0.1: Install Required Tools
1. **Download and install Postman**: https://www.postman.com/downloads/
2. **Verify Python installation**: `python --version` (should be 3.9+)

#### Step 0.2: Project Setup
1. **Create virtual environment:**
   ```bash
   # Navigate to submission folder
   cd week3_api_fastapi/submission
   
   # Create virtual environment
   python -m venv venv
   
   # Activate it (Windows)
   venv\Scripts\activate
   
   # For Mac/Linux:
   # source venv/bin/activate
   ```

2. **Install required packages:**
   ```bash
   # Copy from starter folder or install directly
   pip install fastapi uvicorn sqlalchemy pandas openpyxl python-multipart python-dotenv pytest httpx
   ```

3. **Create project structure** (see required folder structure above)

4. **Copy environment file:**
   ```bash
   # Copy from starter/env_example.txt to .env
   # Edit .env with your database settings
   ```

### Phase 1: Basic FastAPI Setup & Testing (25 points)

#### Step 1.1: Create Basic FastAPI App
Create `submission/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Employee Data Management API",
    description="API for processing Excel files and managing employee data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Employee Data Management API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Step 1.2: Test Basic Setup
1. **Start the server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open Postman and test:**
   - **GET** `http://localhost:8000/` 
     - Should return: `{"message": "Employee Data Management API", "version": "1.0.0"}`
   - **GET** `http://localhost:8000/health`
     - Should return: `{"status": "healthy"}`

3. **Check automatic docs:**
   - Visit: `http://localhost:8000/docs`
   - You should see interactive API documentation

#### Step 1.3: Create Pydantic Models
Create `submission/models/employee.py`:
```python
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional
from enum import Enum

class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"

class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    department: str
    position: str
    salary: float
    hire_date: datetime
    status: EmployeeStatus = EmployeeStatus.ACTIVE

class EmployeeCreate(EmployeeBase):
    @validator('salary')
    def salary_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Salary must be positive')
        return v

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    status: Optional[EmployeeStatus] = None

class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Phase 2: File Upload & Processing (30 points)

#### Step 2.1: File Upload Endpoint
Create `submission/routers/files.py`:
```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import pandas as pd
import os
from services.file_processor import FileProcessor

router = APIRouter(prefix="/files", tags=["files"])
file_processor = FileProcessor()

@router.post("/upload-excel")
async def upload_excel_file(file: UploadFile = File(...)):
    """Upload and process Excel file containing employee data"""
    
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Only Excel and CSV files are allowed")
    
    try:
        # Save uploaded file
        file_path = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process file
        result = await file_processor.process_file(file_path)
        
        return {
            "filename": file.filename,
            "message": "File processed successfully",
            "processed_records": result["processed_count"],
            "errors": result["errors"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
```

#### Step 2.2: File Processing Service
Create `submission/services/file_processor.py`:
```python
import pandas as pd
from typing import Dict, List, Any
from models.employee import EmployeeCreate
from datetime import datetime

class FileProcessor:
    
    def __init__(self):
        self.required_columns = [
            'employee_id', 'name', 'email', 'department', 
            'position', 'salary', 'hire_date', 'status'
        ]
    
    async def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process Excel/CSV file and return processed data"""
        
        try:
            # Read file based on extension
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            
            # Validate columns
            missing_columns = set(self.required_columns) - set(df.columns)
            if missing_columns:
                return {
                    "processed_count": 0,
                    "errors": [f"Missing required columns: {missing_columns}"]
                }
            
            # Clean and validate data
            cleaned_data, errors = self._clean_data(df)
            
            # TODO: Save to database (will implement in Phase 3)
            
            return {
                "processed_count": len(cleaned_data),
                "errors": errors,
                "data": cleaned_data
            }
            
        except Exception as e:
            return {
                "processed_count": 0,
                "errors": [f"Error reading file: {str(e)}"]
            }
    
    def _clean_data(self, df: pd.DataFrame) -> tuple[List[Dict], List[str]]:
        """Clean and validate dataframe data"""
        cleaned_data = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Convert hire_date to datetime
                hire_date = pd.to_datetime(row['hire_date'])
                
                # Create employee data
                employee_data = {
                    'employee_id': str(row['employee_id']),
                    'name': str(row['name']).strip(),
                    'email': str(row['email']).strip().lower(),
                    'department': str(row['department']).strip(),
                    'position': str(row['position']).strip(),
                    'salary': float(row['salary']),
                    'hire_date': hire_date,
                    'status': str(row['status']).lower()
                }
                
                # Validate with Pydantic
                employee = EmployeeCreate(**employee_data)
                cleaned_data.append(employee.dict())
                
            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")
        
        return cleaned_data, errors
```

### Phase 3: Database Integration & Testing (25 points)

#### Step 3.1: Setup Local Database
1. **Create .env file** (copy from starter/env_example.txt):
   ```bash
   DATABASE_URL=sqlite:///./employees.db
   DEBUG=True
   ```

2. **Create database models** `submission/models/database.py`:
   ```python
   from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.sql import func
   from models.employee import EmployeeStatus

   Base = declarative_base()

   class Employee(Base):
       __tablename__ = "employees"
       
       id = Column(Integer, primary_key=True, index=True)
       employee_id = Column(String, unique=True, index=True)
       name = Column(String, index=True)
       email = Column(String, unique=True, index=True)
       department = Column(String, index=True)
       position = Column(String)
       salary = Column(Float)
       hire_date = Column(DateTime)
       status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
       created_at = Column(DateTime, server_default=func.now())
       updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
   ```

#### Step 3.2: Database Connection Setup
Create `submission/database/connection.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL (SQLite for development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./employees.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### Step 3.3: Create CRUD Operations
Create `submission/database/crud.py`:
```python
from sqlalchemy.orm import Session
from models.database import Employee
from models.employee import EmployeeCreate, EmployeeUpdate
from typing import List, Optional

def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).offset(skip).limit(limit).all()

def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        update_data = employee_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_employee, field, value)
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee
```

#### Step 3.4: Test Database Connection
1. **Restart your FastAPI server**
2. **Check if database file is created**: Look for `employees.db` in your submission folder
3. **Test database in Postman**: You should be able to create employees through your API now

### Phase 4: Complete CRUD Endpoints & Testing (20 points)

#### Step 4.1: Create Employee CRUD Endpoints
Create `submission/routers/employees.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from database.connection import get_db
from database import crud

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db=db, employee=employee)

@router.get("/", response_model=List[EmployeeResponse])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_employees(db, skip=skip, limit=limit)

@router.get("/{employee_id}", response_model=EmployeeResponse)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = crud.update_employee(db, employee_id=employee_id, employee_update=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.delete_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}
```

#### Step 4.2: Update main.py to include routers
Update `submission/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import employees, files

app = FastAPI(
    title="Employee Data Management API",
    description="API for processing Excel files and managing employee data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(employees.router)
app.include_router(files.router)

@app.get("/")
async def root():
    return {"message": "Employee Data Management API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🧪 **Complete API Testing with Postman**

### **Step-by-Step Testing Instructions**

#### **1. Start Your API Server**
```bash
# From submission/ directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### **2. Test Basic Endpoints**
**✅ Test 1: Health Check**
- **Method**: GET
- **URL**: `http://localhost:8000/health`
- **Expected**: `{"status": "healthy"}`

**✅ Test 2: API Info**
- **Method**: GET  
- **URL**: `http://localhost:8000/`
- **Expected**: `{"message": "Employee Data Management API", "version": "1.0.0"}`

#### **3. Test Employee CRUD Operations**

**✅ Test 3: Create Employee**
- **Method**: POST
- **URL**: `http://localhost:8000/employees/`
- **Headers**: `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "employee_id": "EMP001",
  "name": "John Smith",
  "email": "john.smith@company.com",
  "department": "Engineering",
  "position": "Senior Developer",
  "salary": 75000,
  "hire_date": "2022-01-15T00:00:00",
  "status": "active"
}
```
- **Expected**: Returns created employee with ID and timestamps

**✅ Test 4: Get All Employees**
- **Method**: GET
- **URL**: `http://localhost:8000/employees/`
- **Expected**: Array of all employees

**✅ Test 5: Get Specific Employee**
- **Method**: GET
- **URL**: `http://localhost:8000/employees/1`
- **Expected**: Single employee data

**✅ Test 6: Update Employee**
- **Method**: PUT
- **URL**: `http://localhost:8000/employees/1`
- **Headers**: `Content-Type: application/json`
- **Body** (raw JSON):
```json
{
  "salary": 80000,
  "position": "Lead Developer"
}
```
- **Expected**: Updated employee data

**✅ Test 7: Delete Employee**
- **Method**: DELETE
- **URL**: `http://localhost:8000/employees/1`
- **Expected**: `{"message": "Employee deleted successfully"}`

#### **4. Test File Upload**

**✅ Test 8: Upload Excel File**
- **Method**: POST
- **URL**: `http://localhost:8000/files/upload-excel`
- **Body**: form-data
  - **Key**: `file` (type: File)
  - **Value**: Select the `sample_employees.xlsx` from starter folder
- **Expected**: 
```json
{
  "filename": "sample_employees.xlsx",
  "message": "File processed successfully",
  "processed_records": 10,
  "errors": []
}
```

**✅ Test 9: Verify File Data Was Saved**
- **Method**: GET
- **URL**: `http://localhost:8000/employees/`
- **Expected**: Should now contain employees from the Excel file

#### **5. Test Error Handling**

**✅ Test 10: Invalid Employee Data**
- **Method**: POST
- **URL**: `http://localhost:8000/employees/`
- **Body**: 
```json
{
  "employee_id": "EMP999",
  "name": "Test User",
  "email": "invalid-email",
  "salary": -1000
}
```
- **Expected**: Validation errors

**✅ Test 11: Employee Not Found**
- **Method**: GET
- **URL**: `http://localhost:8000/employees/999`
- **Expected**: 404 error with "Employee not found"

### **Postman Collection Setup**
1. **Create New Collection**: "Employee API Tests"
2. **Add Environment**: 
   - Variable: `base_url`
   - Value: `http://localhost:8000`
3. **Save All Tests**: Save each test above as requests in your collection
4. **Export Collection**: Save as JSON for submission

### **Database Verification**
After testing, check your database:
1. **SQLite Browser** (optional): Download and open `employees.db` file
2. **Command Line**: 
```bash
sqlite3 employees.db
.tables
SELECT * FROM employees;
```

## 🎯 Evaluation Criteria

### Technical Requirements (80 points)
- **Phase 1**: Basic FastAPI setup with Pydantic models (25 points)
- **Phase 2**: File upload and Excel processing functionality (30 points)
- **Phase 3**: Database integration with SQLAlchemy (25 points)

### Code Quality (20 points)
- Clean, readable code with proper structure
- Proper error handling and validation
- Comprehensive testing
- Good documentation

### Bonus Features (10 extra points)
- Advanced analytics endpoints
- Data export functionality
- Authentication/authorization
- Docker containerization

## 📝 Submission Instructions

### Due Date
**Friday, 5:00 PM**

### Submission Checklist
- [ ] **All 4 phases completed and working**
- [ ] **Code follows the required project structure**
- [ ] **All 11 Postman tests passing**
- [ ] **Sample Excel file processing works**
- [ ] **Database operations functional (SQLite file created)**
- [ ] **Postman collection exported as JSON**
- [ ] **README.md with setup and usage instructions**
- [ ] **Requirements.txt with all dependencies**
- [ ] **Screenshots of successful Postman tests**

### Running Your Application
```bash
# From submission/ directory
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation
Once running, visit:
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## 📋 **Implementation Checklist**

Before testing, ensure you have completed:

### **Phase 1 Checklist** ✅
- [ ] Created basic FastAPI app in `main.py`
- [ ] Added health and root endpoints
- [ ] Created Pydantic models in `models/employee.py`
- [ ] Tested basic endpoints in Postman

### **Phase 2 Checklist** ✅
- [ ] Created file upload router in `routers/files.py`
- [ ] Implemented file processing service in `services/file_processor.py`
- [ ] Added Excel/CSV reading with pandas
- [ ] Tested file upload in Postman

### **Phase 3 Checklist** ✅
- [ ] Created database models in `models/database.py`
- [ ] Set up database connection in `database/connection.py`
- [ ] Implemented CRUD operations in `database/crud.py`
- [ ] Verified database file creation

### **Phase 4 Checklist** ✅
- [ ] Created employee router in `routers/employees.py`
- [ ] Added all CRUD endpoints
- [ ] Updated main.py to include routers
- [ ] Completed all 11 Postman tests above

## 📚 Suggested Resources

### FastAPI Learning
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI File Uploads](https://fastapi.tiangolo.com/tutorial/request-files/)

### Database & ORM
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [SQLAlchemy with FastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/)

### Data Processing
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)

### Testing
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest Documentation](https://docs.pytest.org/)

## 💡 Tips for Success

1. **Start Small**: Begin with Phase 1 and test each endpoint before moving on
2. **Use the Docs**: FastAPI auto-generates interactive documentation
3. **Test Early**: Use the `/docs` endpoint to test your API as you build
4. **Handle Errors**: Implement proper error handling for file uploads and data validation
5. **Validate Data**: Use Pydantic models to ensure data integrity
6. **Structure Code**: Follow the provided project structure for better organization

## 🔧 Troubleshooting

### Common Issues
- **Import Errors**: Ensure all `__init__.py` files are created
- **Database Errors**: Check DATABASE_URL in `.env` file
- **File Upload Issues**: Verify file permissions and upload directory exists
- **Validation Errors**: Check Pydantic model definitions match data

### Debug Mode
Run with debug information:
```bash
uvicorn main:app --reload --log-level debug
```

---

**Focus**: Building a complete, production-ready API that demonstrates file processing, data validation, database operations, and RESTful design principles. 