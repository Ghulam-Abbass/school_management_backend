import db.database as _database
import models.User as _models
import sqlalchemy.orm as _orm
import schema.auth_schema as _schemas
import fastapi as _fastapi
import passlib.hash as _hash
import jwt
from json import JSONEncoder
import datetime as _dt
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from fastapi import HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from datetime import datetime

_JWT_SECRET = "schoolmanagmentsystem"

security = HTTPBearer()

class OptionalHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request):
        from fastapi import status
        try:
            r = await super().__call__(request)
            token = r.credentials
        except HTTPException as ex:
            assert ex.status_code == status.HTTP_403_FORBIDDEN, ex
            token = None
        return token

auth_scheme = OptionalHTTPBearer()

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, _dt.datetime):
            return obj.isoformat()
        return super().default(obj)

def _create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

async def create_user_db(firstName: str, lastName: str, email: str, phone: str, address: str, password: str, role: str, db: Session):
    
    hashed_password = _hash.bcrypt.hash(password)

    user_obj = _models.User(email=email, password=hashed_password, role=role, first_name=firstName, last_name=lastName, address=address, phone=phone, created_at=datetime.utcnow(), updated_at=None )

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj  

async def signup_user():
    response = {
            "success": True,
            "message": "User Register Successfully.",
            "data": None
        }
    return JSONResponse(status_code=201, content=response)
