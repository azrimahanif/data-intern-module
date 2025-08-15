from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import files, employees  # <— tambah import router

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

# Daftarkan semua router supaya endpoint aktif
app.include_router(files.router)
app.include_router(employees.router)

@app.get("/")
async def root():
    return {"message": "Employee Data Management API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
