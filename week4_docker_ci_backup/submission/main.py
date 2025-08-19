from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from routers import files, employees

# Database
from database.config import Base, engine
from models import employee  # penting untuk register model

# Ensure tables are created at startup
Base.metadata.create_all(bind=engine)

# Init app
app = FastAPI(
    title="Employee Data Management API",
    description="API for processing Excel files and managing employee data",
    version="1.0.0"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow semua origin (boleh ketatkan nanti)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers registration
app.include_router(files.router)
app.include_router(employees.router)

# Health + root
@app.get("/")
async def root():
    return {
        "message": "Employee Data Management API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
