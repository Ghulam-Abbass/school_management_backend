import models.auth_model.User as _user
import models.job_model.Job as _job
import fastapi as _fastapi
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

def create_teacher_job(db: Session, teacher_id: int, job_name: str):

    if job_name != "teacher":
        return "Only teacher can apply"

    job_request = _job.Job(user_id=teacher_id, job_name=job_name)
    
    db.add(job_request)
    db.commit()

    return "Job created successfully please wait for the confirmation"