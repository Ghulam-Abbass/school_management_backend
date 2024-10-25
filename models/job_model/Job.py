from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from db.database import Base



class Job(Base):
    __tablename__ = 'job_table'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_name = Column(String(100))
    user_id = Column(Integer, ForeignKey('user_table.id'))

    # Define the one-to-one relationship
    user = relationship("User", back_populates="job")
