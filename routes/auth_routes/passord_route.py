import fastapi as _fastapi
from sqlalchemy.orm import Session
import services.auth_services.auth_services as _authservices
import services.auth_services.password_services as _pwdservices
import logging
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks

logging.basicConfig(level=logging.DEBUG)

psw = _fastapi.APIRouter()

@psw.post("/api/forgot-password/")
def forgot_password(
    email: str = _fastapi.Form(..., description="Enter email"),
    db: Session = _fastapi.Depends(_authservices.get_db),
    background_tasks: BackgroundTasks = _fastapi.BackgroundTasks()
):
    response = _pwdservices.initiate_password_reset(email, db, background_tasks)
    if response == "User not found":
        data = {
            "success": False,
            "message": response,
            "data": None
        }
        return JSONResponse(status_code=422, content=data)
    return {
        "success": True,
        "message": response,
        "data": None
    }

@psw.get("/api/verify-code/")
def verify_code(token: str, db: Session = _fastapi.Depends(_authservices.get_db)):
    response = _pwdservices.check_code_valid(token, db)
    if response == False:
        return {
            "success": response,
            "message": "Not Matched",
            "data": None
        }
    return {
        "success": response,
            "message": "Matched Successfully.",
            "data": None
    }

@psw.post("/api/reset-password/")
def reset_password(
    code: str = _fastapi.Form(..., description="Enter code"),
    new_password: str = _fastapi.Form(..., description="Enter new password"),
    confirm_password: str = _fastapi.Form(..., description="Enter confirm password"),
    db: Session = _fastapi.Depends(_authservices.get_db)
):
    if new_password != confirm_password:
        response = {
            "success": False,
            "message": "Password not match",
            "data": None
        }
        return response

    data = _pwdservices.password_reset(code, new_password, db)
    return {
        "success": True,
        "message": data,
        "data": None
    }