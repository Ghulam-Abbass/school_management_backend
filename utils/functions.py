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

def is_image_file(filename: str) -> bool:
    extension = filename.split(".")[-1].lower()
    return extension in ALLOWED_EXTENSIONS

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
