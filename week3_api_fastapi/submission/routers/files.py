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