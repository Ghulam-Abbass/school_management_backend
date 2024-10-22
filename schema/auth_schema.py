from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional 

class _UserBase(BaseModel):
    email: str

class UserSignin(_UserBase):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    role: str
    profile_image:  Optional[str]
    cover_image:  Optional[str]
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes=True  

    @classmethod
    def from_orm(cls, obj):
        # Convert datetime to ISO format
        return cls(
            id=obj.id,
            first_name=obj.first_name,
            last_name=obj.last_name,
            email=obj.email,
            address=obj.address,
            phone=obj.phone,
            role=obj.role,
            profile_image= obj.profile_image,
            cover_image= obj.cover_image,
            created_at=obj.created_at.isoformat() if obj.created_at else None,
            updated_at=obj.updated_at.isoformat() if obj.updated_at else None
        )  
