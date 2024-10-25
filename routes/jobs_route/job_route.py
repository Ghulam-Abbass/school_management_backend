import fastapi as _fastapi
from sqlalchemy.orm import Session
import services.auth_service.auth_services as _authservices
import services.jobs_service.job_services as _jobservice
import logging
from fastapi.responses import JSONResponse
from models.auth_model.User import User
import utils.functions as _functions
import config.smtplib as _email

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
    
    if auth.apply == True:
        return _functions.create_error_response("You already apply for job.")

    # Check for token validity
    if auth == "Unauthorized: Token has expired":
        return _functions.create_error_response("Unauthorized: Token has expired")
    if auth == "Unauthorized: Token is invalid":
        return _functions.create_error_response("Unauthorized: Token is invalid")

    # Get the teacher's user details
    user = await _authservices.get_user_by_id(db, teacher_id)
    if user is None:
        return JSONResponse(status_code=404, content={"success": False, "message": "User not found", "data": None})

    user.apply = True
    db.commit()

    # Create the job request
    request = _jobservice.create_teacher_job(db, teacher_id, auth.role)
    if request is None:
        return JSONResponse(status_code=404, content={"success": False, "message": "Something went wrong.", "data": None})

    # Notify headmasters
    headmasters = db.query(User).filter(User.role == "headmaster").all()
    for headmaster in headmasters:
        await _email.send_notification_email(
            headmaster.email,
            user.first_name,
            user.last_name,
            user.phone,
            user.email,
            user.address,
            user.age,
            user.education,
            user.gender,
            user.hobby,
            user.degree_year,
            user.bio,
            user.experience,
            user.skills,
            user.id
        )

    return {"success": True, "message": request, "data": None}


@job.get("/api/job/approve/{teacher_id}")
async def approve_application(
    teacher_id: int,
    db: Session = _fastapi.Depends(_authservices.get_db)
):
    user = db.query(User).filter(User.id == teacher_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    
    # Approve the application
    user.approved = True
    user.apply = True
    db.commit()

    # Send approval email
    await _email.send_teacher_email(user.email, "Congratulations 🎉", "Your job application has been approved.")
    
    return "Application approved successfully."


@job.get("/api/job/decline/{teacher_id}")
async def decline_application(
    teacher_id: int,
    db: Session = _fastapi.Depends(_authservices.get_db)
):
    user = db.query(User).filter(User.id == teacher_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    
    # Decline the application
    user.approved = False
    user.apply = False
    db.commit()

    # Send decline email
    await _email.send_teacher_email(user.email, "Sorry 😔", "We regret to inform you that your job application has been declined. Please try again later.")
    
    return "Application declined successfully."