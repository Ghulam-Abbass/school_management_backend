# models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Date
from sqlalchemy_utils import URLType
from db.database import Base  # Import the Base from the db module
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship

# Example model
class User(Base):
    __tablename__ = 'user_table'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(50))
    email = Column(String(100),unique=True)
    address = Column(String(225))
    password = Column(String(225))
    role = Column(String(50))
    profile_image = Column(String(255), nullable=True)
    cover_image = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.utcnow)

    cv = Column(String(255), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    approved = Column(Boolean, default=False, nullable=True)
    experience = Column(Float, nullable=True)
    work_at_place = Column(String(100), nullable=True)
    education = Column(String(100), nullable=True)
    degree_year = Column(Integer, nullable=True)
    skills = Column(String(255), nullable=True)
    hobby = Column(String(255), nullable=True)
    gender = Column(String(50), nullable=True)

    password_resets = relationship("PasswordReset", back_populates="user", cascade="all, delete-orphan")