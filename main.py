from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from typing import List

app = FastAPI(title="File CRUD System", version="1.0.0")

# File storage directory
FILE_STORAGE = "files"

# Ensure storage directory exists
os.makedirs(FILE_STORAGE, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "File CRUD System is running"}

@app.get("/files")
async def list_files():
    """List all available files"""
    try:
        files = []
        for filename in os.listdir(FILE_STORAGE):
            file_path = os.path.join(FILE_STORAGE, filename)
            if os.path.isfile(file_path):
                file_info = {
                    "name": filename,
                    "size": os.path.getsize(file_path),
                    "modified": os.path.getmtime(file_path)
                }
                files.append(file_info)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

@app.post("/files")
async def upload_file(file: UploadFile = File(...)):
    """Upload a new file"""
    try:
        file_path = os.path.join(FILE_STORAGE, file.filename)
        
        # Check if file already exists
        if os.path.exists(file_path):
            raise HTTPException(status_code=400, detail="File already exists")
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "size": os.path.getsize(file_path)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.get("/files/{filename}")
async def download_file(filename: str):
    """Download a file"""
    file_path = os.path.join(FILE_STORAGE, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.put("/files/{filename}")
async def update_file(filename: str, file: UploadFile = File(...)):
    """Update an existing file"""
    try:
        file_path = os.path.join(FILE_STORAGE, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Save the updated file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "message": "File updated successfully",
            "filename": filename,
            "size": os.path.getsize(file_path)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating file: {str(e)}")

@app.delete("/files/{filename}")
async def delete_file(filename: str):
    """Delete a file"""
    file_path = os.path.join(FILE_STORAGE, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        os.remove(file_path)
        return {"message": "File deleted successfully", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)