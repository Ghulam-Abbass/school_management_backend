import models.User as _user
import fastapi as _fastapi
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from random import choice
from string import ascii_letters, digits
import models.PasswordReset as _password
from config.smtplib import send_reset_password_email
import random

def initiate_password_reset(email: str, db: Session, background_tasks: _fastapi.BackgroundTasks):
    user = db.query(_user.User).filter(_user.User.email == email).first()
    if user:
        code = random.randint(1000, 9999)
        expiry_date = datetime.now() + timedelta(hours=1)
        reset_request = _password.PasswordReset(user_id=user.id, code=str(code), expiry_date=expiry_date)
        
        db.add(reset_request)
        db.commit()
        
        # Send the 4-digit code to the user's email using background task
        background_tasks.add_task(send_reset_password_email, to_email=user.email, code=code)

        return "Code successfully sent to your email."
    return "User not found"

def check_code_valid(code: str, db: Session):
    reset_request = db.query(_password.PasswordReset).filter(
        _password.PasswordReset.code == code,
        _password.PasswordReset.expiry_date >= datetime.now()
    ).first()
    return reset_request is not None
