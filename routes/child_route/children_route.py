# routes/child_route.py
import fastapi as _fastapi
from sqlalchemy.orm import Session
import services.auth_service.auth_services as _authservices
from models.auth_model.User import User
import services.child_service.children_service as _childService
import utils.functions as _functions
import config.smtplib as _email
from typing import Optional
from fastapi.responses import JSONResponse
from datetime import datetime

child = _fastapi.APIRouter()

@child.post("/api/child/{parent_id}")
async def add_child(
    parent_id: int,
    first_name: str = _fastapi.Form(..., description="Enter first name"),
    last_name: str = _fastapi.Form(..., description="Enter last name"),
    guardian_email: str = _fastapi.Form(..., description="Enter guardian email"),
    guardian_phone: str = _fastapi.Form(..., description="Enter guardian phone"),
    address: str = _fastapi.Form(..., description="Enter address"),
    child_class: str = _fastapi.Form(..., description="Enter class"),
    section: str = _fastapi.Form(..., description="Select section"),
    birth_mark: Optional[str] = _fastapi.Form(None, description="Enter birth mark"),
    health_issue: Optional[str] = _fastapi.Form(None, description="Enter health issue"),
    profile_image: _fastapi.UploadFile = _fastapi.File(..., description="Upload profile image"),
    signature: _fastapi.UploadFile = _fastapi.File(..., description="Upload signature image"),
    date_of_birth: str = _fastapi.Form(..., description="yyyy-mm-dd"),
    age: int = _fastapi.Form(..., description="Enter age"),
    gender: str = _fastapi.Form(..., description="Select gender"),
    bio: Optional[str] = _fastapi.Form(None, description="About you"),
    hafiz: bool = _fastapi.Form(False),
    auth: User = _fastapi.Depends(_authservices.get_current_user),
    db: Session = _fastapi.Depends(_authservices.get_db)
):
    if auth.role != "parent":
        return _functions.create_error_response("Only parents can add a child")
    
    if auth == "Invalid email or password":
        return _functions.create_error_response("Invalid email or password")

    if auth == "Unauthorized: Token has expired":
        return _functions.create_error_response("Unauthorized: Token has expired")

    if auth == "Unauthorized: Token is invalid":
        return _functions.create_error_response("Unauthorized: Token is invalid")
    
    user = await _authservices.get_user_by_id(db, parent_id)
    
    if user is None:
        response = {
            "success": False,
            "message": "Parent not found",
            "data": None
        }
        return JSONResponse(status_code=404, content=response)

    profile_image_url = None
    if profile_image:
        profile_image_url = await _functions.upload_image(profile_image)

    signature_image_url = None
    if signature:
        signature_image_url = await _functions.upload_image(signature)

    dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()

    new_child = _childService.create_child(
        db=db,
        parent_id=parent_id,
        first_name=first_name,
        last_name=last_name,
        guardian_email=guardian_email,
        guardian_phone=guardian_phone,
        address=address,
        child_class=child_class,
        section=section,
        birth_mark=birth_mark,
        health_issue=health_issue,
        profile_image=profile_image_url,
        signature=signature_image_url,
        date_of_birth=dob,
        age=age,
        gender=gender,
        bio=bio,
        hafiz=hafiz
    )

    if new_child is None:
        response = {
            "success": False,
            "message": "Something went wrong.",
            "data": None
        }
        return JSONResponse(status_code=404, content=response)

    response = {
        "success": False,
        "message": new_child,
        "data": None
    }
    return response


@child.post("/api/{parent_id}/child/{child_id}")
async def update_child(
    parent_id: int,
    child_id: int,
    first_name: str = _fastapi.Form(None, description="Enter first name"),
    last_name: str = _fastapi.Form(None, description="Enter last name"),
    guardian_email: str = _fastapi.Form(None, description="Enter guardian email"),
    guardian_phone: str = _fastapi.Form(None, description="Enter guardian phone"),
    address: str = _fastapi.Form(None, description="Enter address"),
    child_class: str = _fastapi.Form(None, description="Enter class"),
    section: str = _fastapi.Form(None, description="Select section"),
    birth_mark: Optional[str] = _fastapi.Form(None, description="Enter birth mark"),
    health_issue: Optional[str] = _fastapi.Form(None, description="Enter health issue"),
    profile_image: _fastapi.UploadFile = _fastapi.File(None, description="Upload profile image"),
    signature: _fastapi.UploadFile = _fastapi.File(None, description="Upload signature image"),
    date_of_birth: str = _fastapi.Form(None, description="yyyy-mm-dd"),
    age: int = _fastapi.Form(None, description="Enter age"),
    gender: str = _fastapi.Form(None, description="Select gender"),
    bio: Optional[str] = _fastapi.Form(None, description="About you"),
    hafiz: bool = _fastapi.Form(False),
    auth: User = _fastapi.Depends(_authservices.get_current_user),
    db: Session = _fastapi.Depends(_authservices.get_db)
):
    if auth.role != "parent":
        return _functions.create_error_response("Only parents can add a child")
    
    if auth == "Invalid email or password":
        return _functions.create_error_response("Invalid email or password")

    if auth == "Unauthorized: Token has expired":
        return _functions.create_error_response("Unauthorized: Token has expired")

    if auth == "Unauthorized: Token is invalid":
        return _functions.create_error_response("Unauthorized: Token is invalid")
    
    user = await _authservices.get_user_by_id(db, parent_id)
    child = await _childService.get_child_by_id(db, child_id)
    
    if user is None:
        response = {
            "success": False,
            "message": "Parent not found",
            "data": None
        }
        return JSONResponse(status_code=404, content=response)

    profile_image_url = None
    if profile_image:
        profile_image_url = await _functions.upload_image(profile_image)

    signature_image_url = None
    if signature:
        signature_image_url = await _functions.upload_image(signature)

    dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()

    new_child = _childService.create_child(
        db=db,
        parent_id=parent_id,
        first_name=first_name,
        last_name=last_name,
        guardian_email=guardian_email,
        guardian_phone=guardian_phone,
        address=address,
        child_class=child_class,
        section=section,
        birth_mark=birth_mark,
        health_issue=health_issue,
        profile_image=profile_image_url,
        signature=signature_image_url,
        date_of_birth=dob,
        age=age,
        gender=gender,
        bio=bio,
        hafiz=hafiz
    )

    if new_child is None:
        response = {
            "success": False,
            "message": "Something went wrong.",
            "data": None
        }
        return JSONResponse(status_code=404, content=response)

    response = {
        "success": False,
        "message": new_child,
        "data": None
    }
    return response
