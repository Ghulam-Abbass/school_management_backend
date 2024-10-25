import models.job_model.Job as _job
from sqlalchemy.orm import Session

def create_teacher_job(db: Session, user_id: int, job_name: str):

    if job_name != "teacher":
        return "Only teacher can apply"

    job_request = _job.Job(user_id=user_id, job_name=job_name)
    
    db.add(job_request)
    db.commit()

    return "Job created successfully please wait for the confirmation"