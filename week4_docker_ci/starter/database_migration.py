#!/usr/bin/env python3
"""
Database Migration Script
Helps migrate from SQLite to PostgreSQL for production deployment
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_to_postgresql():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Source SQLite database
    sqlite_url = "sqlite:///./employees.db"
    sqlite_engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
    
    # Target PostgreSQL database
    postgres_url = os.getenv("DATABASE_URL")
    if not postgres_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("Please set DATABASE_URL for PostgreSQL connection")
        return False
    
    try:
        postgres_engine = create_engine(postgres_url)
        
        # Test PostgreSQL connection
        with postgres_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ PostgreSQL connection successful")
        
        # Get data from SQLite
        with sqlite_engine.connect() as conn:
            # Get all employees
            result = conn.execute(text("SELECT * FROM employees"))
            employees = result.fetchall()
            print(f"📊 Found {len(employees)} employees in SQLite")
            
            # Get column names
            columns = [desc[0] for desc in result.description]
            print(f"📋 Columns: {', '.join(columns)}")
        
        # Insert into PostgreSQL
        if employees:
            with postgres_engine.connect() as conn:
                for employee in employees:
                    # Create INSERT statement
                    placeholders = ', '.join(['%s'] * len(columns))
                    columns_str = ', '.join(columns)
                    insert_sql = f"INSERT INTO employees ({columns_str}) VALUES ({placeholders})"
                    
                    try:
                        conn.execute(text(insert_sql), employee)
                        print(f"✅ Migrated employee: {employee[2]}")  # employee[2] is name
                    except Exception as e:
                        print(f"⚠️  Skipped employee {employee[2]}: {e}")
                
                conn.commit()
                print("✅ Migration completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_postgresql_tables():
    """Create tables in PostgreSQL if they don't exist"""
    
    postgres_url = os.getenv("DATABASE_URL")
    if not postgres_url:
        print("❌ DATABASE_URL not found")
        return False
    
    try:
        engine = create_engine(postgres_url)
        
        # Create employees table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            employee_id VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            department VARCHAR(50) NOT NULL,
            position VARCHAR(50) NOT NULL,
            salary DECIMAL(10,2) NOT NULL,
            hire_date TIMESTAMP NOT NULL,
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_employee_id ON employees(employee_id);
        CREATE INDEX IF NOT EXISTS idx_email ON employees(email);
        CREATE INDEX IF NOT EXISTS idx_department ON employees(department);
        """
        
        with engine.connect() as conn:
            conn.execute(text(create_table_sql))
            conn.commit()
            print("✅ PostgreSQL tables created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def main():
    """Main migration function"""
    print("🚀 Database Migration Tool")
    print("=" * 40)
    
    # Check if we're migrating to PostgreSQL
    if os.getenv("DATABASE_URL") and "postgresql" in os.getenv("DATABASE_URL"):
        print("📊 Detected PostgreSQL configuration")
        
        # Create tables first
        if create_postgresql_tables():
            # Then migrate data
            migrate_to_postgresql()
        else:
            print("❌ Cannot proceed without table creation")
    else:
        print("ℹ️  No PostgreSQL configuration found")
        print("Set DATABASE_URL to migrate data")

if __name__ == "__main__":
    main()
