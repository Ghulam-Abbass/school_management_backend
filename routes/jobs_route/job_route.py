import fastapi as _fastapi
from sqlalchemy.orm import Session
import services.auth_service.auth_services as _authservices
import services.jobs_service.job_services as _jobservice
import logging
from fastapi.responses import JSONResponse
from models.auth_model.User import User
import utils.functions as _functions

logging.basicConfig(level=logging.DEBUG)

job = _fastapi.APIRouter()

@job.post("/api/teacher/job/{teacher_id}")
async def create_teacher_job(
    teacher_id: int,
    auth: User = _fastapi.Depends(_authservices.get_current_user),
    db: Session = _fastapi.Depends(_authservices.get_db)
):
    # Ensure the user has the 'teacher' role
    if auth.role != "teacher":
        return _functions.create_error_response("Only teachers can create job")
    
    if auth == "Unauthorized: Token has expired":
        return _functions.create_error_response("Unauthorized: Token has expired")

    if auth == "Unauthorized: Token is invalid":
        return _functions.create_error_response("Unauthorized: Token is invalid")
    
    user = await _authservices.get_user_by_id(db, teacher_id)
    
    if user is None:
        response = {
            "success": False,
            "message": "User not found",
            "data": None
        }
        return JSONResponse(status_code=404, content=response)

    request = _jobservice.create_teacher_job(
        db, teacher_id, auth.role
    )
    
    if request is None:
        response = {
            "success": False,
            "message": "Something went wrong.",
            "data": None
        }
        return JSONResponse(status_code=404, content=response)

    response = {
        "success": True,
        "message": request,
        "data": None
    }
    return response


@job.get("/api/staff/job")
async def create_staff_job():
    return "Get jobs"