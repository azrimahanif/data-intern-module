import pandas as pd
from datetime import datetime, timedelta
import random

# Sample employee data
employees = [
    {'employee_id': 'EMP001', 'name': 'John Smith', 'email': 'john.smith@company.com', 'department': 'Engineering', 'position': 'Senior Developer', 'salary': 75000, 'hire_date': '2022-01-15', 'status': 'active'},
    {'employee_id': 'EMP002', 'name': 'Sarah Johnson', 'email': 'sarah.johnson@company.com', 'department': 'Marketing', 'position': 'Marketing Manager', 'salary': 65000, 'hire_date': '2021-06-20', 'status': 'active'},
    {'employee_id': 'EMP003', 'name': 'Mike Davis', 'email': 'mike.davis@company.com', 'department': 'Sales', 'position': 'Sales Representative', 'salary': 50000, 'hire_date': '2023-03-10', 'status': 'active'},
    {'employee_id': 'EMP004', 'name': 'Emily Brown', 'email': 'emily.brown@company.com', 'department': 'HR', 'position': 'HR Specialist', 'salary': 55000, 'hire_date': '2022-08-05', 'status': 'active'},
    {'employee_id': 'EMP005', 'name': 'David Wilson', 'email': 'david.wilson@company.com', 'department': 'Engineering', 'position': 'Junior Developer', 'salary': 60000, 'hire_date': '2023-01-12', 'status': 'active'},
    {'employee_id': 'EMP006', 'name': 'Lisa Anderson', 'email': 'lisa.anderson@company.com', 'department': 'Finance', 'position': 'Financial Analyst', 'salary': 70000, 'hire_date': '2021-11-30', 'status': 'inactive'},
    {'employee_id': 'EMP007', 'name': 'Tom Garcia', 'email': 'tom.garcia@company.com', 'department': 'Operations', 'position': 'Operations Manager', 'salary': 80000, 'hire_date': '2020-09-15', 'status': 'active'},
    {'employee_id': 'EMP008', 'name': 'Jennifer Lee', 'email': 'jennifer.lee@company.com', 'department': 'Engineering', 'position': 'DevOps Engineer', 'salary': 85000, 'hire_date': '2022-04-01', 'status': 'active'},
    {'employee_id': 'EMP009', 'name': 'Robert Taylor', 'email': 'robert.taylor@company.com', 'department': 'Sales', 'position': 'Sales Manager', 'salary': 90000, 'hire_date': '2019-12-10', 'status': 'active'},
    {'employee_id': 'EMP010', 'name': 'Amanda Clark', 'email': 'amanda.clark@company.com', 'department': 'Marketing', 'position': 'Content Specialist', 'salary': 45000, 'hire_date': '2023-05-20', 'status': 'active'}
]

# Create DataFrame
df = pd.DataFrame(employees)

# Save to Excel
df.to_excel('sample_employees.xlsx', index=False)
print('Sample Excel file created: sample_employees.xlsx')

# Also save as CSV for testing
df.to_csv('sample_employees.csv', index=False)
print('Sample CSV file created: sample_employees.csv')