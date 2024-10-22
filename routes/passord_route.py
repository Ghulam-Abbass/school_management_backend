import fastapi as _fastapi
from sqlalchemy.orm import Session
import services.auth_services as _authservices
import services.password_services as _pwdservices
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
            "messages": "Not Matched",
            "data": None
        }
    return {
        "success": response,
            "messages": "Matched Successfully.",
            "data": None
    }