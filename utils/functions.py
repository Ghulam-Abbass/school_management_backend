from fastapi.responses import JSONResponse
import fastapi as _fastapi
import os
import shutil
from typing import Optional

def create_error_response(message: str, data: dict = None, status_code: int = 401) -> JSONResponse:
    response = {
        "success": False,
        "message": message,
        "data": data
    }
    return JSONResponse(status_code=status_code, content=response)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_PDF_EXTENSION = {'pdf'}

def is_image_file(filename: str) -> bool:
    extension = filename.split(".")[-1].lower()
    return extension in ALLOWED_EXTENSIONS

def is_pdf_file(filename: str) -> bool:
    """Check if the file has a .pdf extension."""
    extension = filename.split(".")[-1].lower()
    return extension in ALLOWED_PDF_EXTENSION

async def upload_image(image: _fastapi.UploadFile) -> str:
    upload_dir = "uploads/"
    os.makedirs(upload_dir, exist_ok=True)

    if not is_image_file(image.filename):
        raise _fastapi.HTTPException(status_code=400, detail="Invalid image file type.")
    
    file_location = os.path.join(upload_dir, image.filename.replace(" ", "-"))
    
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(image.file, file_object)
    except Exception as e:
        raise _fastapi.HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")
    
    return file_location

async def upload_file(file: _fastapi.UploadFile, file_type: str) -> str:
    """Upload a file to the server. Supports 'cv' as file_type for PDFs."""
    # Define the directory for CV uploads
    if file_type == "cv":
        upload_dir = "uploads/cvs/"
    else:
        raise _fastapi.HTTPException(status_code=400, detail="Unsupported file type.")
    
    # Ensure the directory exists
    os.makedirs(upload_dir, exist_ok=True)

    # Validate if the uploaded file is a PDF
    if not is_pdf_file(file.filename):
        raise _fastapi.HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    # Create the file path (replace spaces to avoid issues)
    file_location = os.path.join(upload_dir, file.filename.replace(" ", "-"))
    
    try:
        # Save the file to the specified location
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        raise _fastapi.HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    
    return file_location
