import models.auth_models.User as _user
import fastapi as _fastapi
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models.auth_models.PasswordReset as _password
import passlib.hash as _hash
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

def password_reset(code: str, new_password: str, db: Session):
    reset_request = db.query( _password.PasswordReset).filter(
         _password.PasswordReset.code == code,
         _password.PasswordReset.expiry_date >= datetime.now()
    ).first()
    if reset_request:
        hash_password = _hash.bcrypt.hash(new_password)
        user = db.query(_user.User).get(reset_request.user_id)
        user.password = hash_password
        db.delete(reset_request)
        db.commit()
        return "Password reset successfully."
    
    return "Invalid token or token expired"
