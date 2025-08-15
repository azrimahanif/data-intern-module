from typing import List, Optional
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.database import Employee as EmployeeORM
from models.employee import EmployeeCreate, EmployeeUpdate

def create_employee(emp: EmployeeCreate, db: Session):
    db_emp = EmployeeORM(**emp.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def create_employee_if_not_exists(data: dict) -> EmployeeORM:
    db: Session = SessionLocal()
    try:
        existing = db.query(EmployeeORM).filter(
            (EmployeeORM.employee_id == data['employee_id']) | (EmployeeORM.email == data['email'])
        ).first()
        if existing:
            return existing
        emp = EmployeeORM(**data)
        db.add(emp)
        db.commit()
        db.refresh(emp)
        return emp
    finally:
        db.close()

def get_employee(emp_id: int) -> Optional[EmployeeORM]:
    db: Session = SessionLocal()
    try:
        return db.query(EmployeeORM).filter(EmployeeORM.id == emp_id).first()
    finally:
        db.close()

def list_employees(skip: int = 0, limit: int = 100) -> List[EmployeeORM]:
    db: Session = SessionLocal()
    try:
        return db.query(EmployeeORM).offset(skip).limit(limit).all()
    finally:
        db.close()

def update_employee(emp_id: int, payload: EmployeeUpdate) -> Optional[EmployeeORM]:
    db: Session = SessionLocal()
    try:
        emp = db.query(EmployeeORM).filter(EmployeeORM.id == emp_id).first()
        if not emp:
            return None
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(emp, key, value)
        db.commit()
        db.refresh(emp)
        return emp
    finally:
        db.close()

def delete_employee(emp_id: int) -> bool:
    db: Session = SessionLocal()
    try:
        emp = db.query(EmployeeORM).filter(EmployeeORM.id == emp_id).first()
        if not emp:
            return False
        db.delete(emp)
        db.commit()
        return True
    finally:
        db.close()