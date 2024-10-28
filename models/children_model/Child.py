# models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Date, ForeignKey
from sqlalchemy_utils import URLType
from db.database import Base  # Import the Base from the db module
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship

# Example model
class Child(Base):
    __tablename__ = 'child_table'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    guardian_phone = Column(String(50))
    guardian_email = Column(String(100),unique=True)
    address = Column(String(225))
    child_class = Column(String(50))
    section = Column(String(50))
    birth_mark = Column(String(225), nullable=True)
    health_issue = Column(String(225), nullable=True)
    profile_image = Column(String(255))
    signature = Column(String(255))
    date_of_birth = Column(Date)
    age = Column(Integer)
    gender = Column(String(50))
    bio = Column(String(500), nullable=True)
    approved = Column(Boolean, default=False, nullable=True)
    hafiz = Column(Boolean, default=False, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=None, onupdate=datetime.utcnow)

    parent_id = Column(Integer, ForeignKey('user_table.id'), nullable=False)

    user = relationship("User", back_populates="childrens")