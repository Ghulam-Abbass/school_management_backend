from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from db.database import Base



class Password(Base):
    __tablename__ = 'password_reset_table'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, index=True)
    expiry_date = Column(DateTime, default=datetime.utcnow() + timedelta(hours=1))
