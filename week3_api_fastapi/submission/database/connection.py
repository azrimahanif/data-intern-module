from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL (SQLite for development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./employees.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()