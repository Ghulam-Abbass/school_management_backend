from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from db.database import Base



class Job(Base):
    __tablename__ = 'job_table'

    job_id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String(100), unique=True, index=True)
    user_id = Column(Integer, ForeignKey('user_table.id'))

    # Define the one-to-one relationship
    user = relationship("User", back_populates="job")
