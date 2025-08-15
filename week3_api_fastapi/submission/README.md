# Week3 Api Fastapi Submission

## 📁 Submission Contents

This folder contains your Week3 Api Fastapi assignments.

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

1. Create and activate a virtual environment:
        python -m venv venv
        # activate (Windows PowerShell)
        venv\Scripts\activate
2. Install dependencies:
        pip install -r requirements.txt
3. Start API server:
        uvicorn main:app --reload
4. The server will be running at:
        http://Localhost:8000
5. Upload Excel File
6. View Stored data

## 📊 Results Summary

1. Excel file successfully uploaded to the API.
2. Data stored in employees.db (SQLite database).
        /employees/ lists all employees.

3. CRUD operations tested:
        Create → Add a new employee
        Read → List or get employee details
        Update → Modify employee information
        Delete → Remove an employee

## 🎯 Learning Outcomes

1. How to build an API with FastAPI.
2. How to read and process Excel files using pandas.
3. How to store data in a database using SQLAlchemy.
4. How to validate data using Pydantic.
5. How to test APIs with Swagger UI.