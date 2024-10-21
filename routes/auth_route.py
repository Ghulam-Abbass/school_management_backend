import fastapi as _fastapi
import schema.auth_schema as _authschema
from sqlalchemy.orm import Session
import services.auth_services as _authservices
import logging
from models.User import User
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.DEBUG)

auth = _fastapi.APIRouter()

@auth.post("/auth/signup")
async def signup_user(
    first_name: str = _fastapi.Form(..., description="Enter firstName"),
    last_name: str = _fastapi.Form(..., description="Enter lastName"),
    email: str = _fastapi.Form(..., description="Enter email"),
    phone: str = _fastapi.Form(..., description="Enter phone"),
    address: str = _fastapi.Form(..., description="Enter address"),
    password: str = _fastapi.Form(..., description="Enter password"),
    role: str = _fastapi.Form(..., description="Enter role"),
    db: Session = _fastapi.Depends(_authservices.get_db)
):
    if not email:
        response = {
            "success": False,
            "message": "Email is required.",
            "data": None
        }
        return JSONResponse(status_code=422, content=response)
    
    if not first_name:
        response = {
            "success": False,
            "message": "FirstName is required.",
            "data": None
        }
        return JSONResponse(status_code=422, content=response)
    if not last_name:
        response = {
            "success": False,
            "message": "LastName is required.",
            "data": None
        }
        return JSONResponse(status_code=422, content=response)
    if not phone:
        response = {
            "success": False,
            "message": "Phone is required.",
            "data": None
        }
        return JSONResponse(status_code=422, content=response)
    if not address:
        response = {
            "success": False,
            "message": "Address is required.",
            "data": None
        }
        return JSONResponse(status_code=422, content=response)
    
    if not password:
        response = {
            "success": False,
            "message": "Password is required.",
            "data": None
        }
        return JSONResponse(status_code=422, content=response)
    
    if not role:
        response = {
            "success": False,
            "message": "Role is required.",
            "data": None
        }
        return JSONResponse(status_code=422, content=response)

    db_user = await _authservices.get_user_by_email(email=email, db=db)

    if db_user:
        response = {
            "success": False,
            "message": "User already exists.",
            "data": None
        }
        return JSONResponse(status_code=409, content=response)
    
    user = await _authservices.create_user_db(firstName=first_name, lastName=last_name, address=address, phone=phone, email=email, password=password, role=role, db=db)

    return await _authservices.signup_user()
