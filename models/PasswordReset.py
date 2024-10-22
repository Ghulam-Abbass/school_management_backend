from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from db.database import Base



class PasswordReset(Base):
    __tablename__ = 'password_reset_table'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, index=True)
    expiry_date = Column(DateTime, default=datetime.utcnow() + timedelta(hours=1))

    # Foreign key to relate password resets to the user
    user_id = Column(Integer, ForeignKey('user_table.id'), nullable=False)

    # Relationship back to the User model
    user = relationship("User", back_populates="password_resets")
