import db.database as _database
import models.auth_model.User as _models
import sqlalchemy.orm as _orm
import schema.auth_schema.auth_schema as _schemas
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

async def authenticate_user(email: str, password: str, db=_orm.Session):
    user = await get_user_by_email(email=email, db=db)
    if not user:
        return None
    if not _hash.bcrypt.verify(password, user.password):
        return "wrong password"
    
    return user

async def create_token_login(user: _models.User):
    user_schema_obj = _schemas.UserSignin.from_orm(user)
    user_dict = user_schema_obj.dict()

    token_expiration = _dt.datetime.utcnow() + _dt.timedelta(days=1)

    token = jwt.encode(user_dict, _JWT_SECRET, json_encoder=CustomJSONEncoder)
    response = {
        "success": True,
        "message": "User Login Successfully.",
        "data":
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": token_expiration.isoformat(),
                "role": user.role,
                "profile_image": user.profile_image,
                "cover_image": user.cover_image,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
        }
    return response

async def get_user(token=_fastapi.Depends(auth_scheme), db=_fastapi.Depends(get_db)):

    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        user = await get_user_by_id(user_id=payload["id"], db=db)
        if not user:
            return "Invalid email or password"          
        print("User data attributes:", user)
        # Prepare the response
        user_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "address": user.address,
            "phone": user.phone,
            "role": user.role,
            "profile_image": user.profile_image,
            "cover_image": user.cover_image,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
        
        return user_data
    except jwt.ExpiredSignatureError:
        return "Unauthorized: Token has expired"
    except jwt.InvalidTokenError:
        return "Unauthorized: Token is invalid" 
 

 # view user

async def get_user_by_id(db: Session, user_id: int):
    user = db.query(_models.User).filter(_models.User.id == user_id).first()
    
    if not user:
        return None
    
    return user

def update_profile(
    db: Session, 
    user_id: int, 
    first_name: str, 
    last_name: str, 
    phone: str, 
    address: str,
    profile_image_url: str = None,
    cover_image_url: str = None
):
    user = db.query(_models.User).filter(_models.User.id == user_id).first()

    if user is None:
        return None


    if first_name:
        setattr(user, "first_name", first_name)
    if last_name:
        setattr(user, "last_name", last_name)
    if phone:
        setattr(user, "phone", phone)
    if address:
        setattr(user, "address", address)
    if profile_image_url:
        setattr(user, "profile_image", profile_image_url)
    if cover_image_url:
        setattr(user, "cover_image", cover_image_url)

    # Set the updated_at timestamp
    setattr(user, "updated_at", datetime.utcnow())

    # Commit changes to the database
    db.commit()
    db.refresh(user)

    # Return updated user data
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "address": user.address,
        "phone": user.phone,
        "role": user.role,
        "profile_image": user.profile_image,
        "cover_image": user.cover_image,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }
    
    return user_data

def update_teacher_profile(
    db: Session, 
    user_id: int, 
    first_name: str, 
    last_name: str, 
    phone: str, 
    address: str,
    profile_image_url: str = None,
    cover_image_url: str = None,
    cv_file_url: str = None,
    date_of_birth: str = None,
    age: int = None,
    experience: float = None,
    work_at_place: str = None,
    education: str = None,
    degree_year: int = None,
    skills: str = None,
    hobby: str = None,
    gender: str = None
):
    user = db.query(_models.User).filter(_models.User.id == user_id).first()

    if user is None:
        return None

    # Update the base fields
    if first_name:
        setattr(user, "first_name", first_name)
    if last_name:
        setattr(user, "last_name", last_name)
    if phone:
        setattr(user, "phone", phone)
    if address:
        setattr(user, "address", address)
    if profile_image_url:
        setattr(user, "profile_image", profile_image_url)
    if cover_image_url:
        setattr(user, "cover_image", cover_image_url)

    if cv_file_url:
        setattr(user, "cv", cv_file_url)
    if date_of_birth:
        setattr(user, "date_of_birth", date_of_birth)
    if age:
        setattr(user, "age", age)
    if experience:
        setattr(user, "experience", experience)
    if work_at_place:
        setattr(user, "work_at_place", work_at_place)
    if education:
        setattr(user, "education", education)
    if degree_year:
        setattr(user, "degree_year", degree_year)
    if skills:
        setattr(user, "skills", skills)
    if hobby:
        setattr(user, "hobby", hobby)
    if gender:
        setattr(user, "gender", gender)

    setattr(user, "updated_at", datetime.utcnow())

    db.commit()
    db.refresh(user)

    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "address": user.address,
        "phone": user.phone,
        "role": user.role,
        "profile_image": user.profile_image,
        "cover_image": user.cover_image,
        "cv": user.cv,
        "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
        "age": user.age,
        "approved": user.approved,
        "experience": user.experience,
        "work_at_place": user.work_at_place,
        "education": user.education,
        "degree_year": user.degree_year,
        "skills": user.skills,
        "hobby": user.hobby,
        "gender": user.gender,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }
    
    return user_data


async def get_current_user(token=_fastapi.Depends(auth_scheme), db=_fastapi.Depends(get_db)):
    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        user = await get_user_by_id(user_id=payload["id"], db=db)
        if not user:
            return "Invalid email or password" 
        
        return user
    except jwt.ExpiredSignatureError:
        return "Unauthorized: Token has expired"
    except jwt.InvalidTokenError:
        return "Unauthorized: Token is invalid"  
    

async def logout_user(token: str):
    try:
        jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
        return "User Logout Successfully."
    except jwt.ExpiredSignatureError:
        return "Unauthorized: Token has expired"
    except jwt.InvalidTokenError:
        return "Unauthorized: Invalid token"
  

