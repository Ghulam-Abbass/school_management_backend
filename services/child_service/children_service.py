# services/child_service.py
from sqlalchemy.orm import Session
from models.children_model.Child import Child
from datetime import date
from typing import Optional
from datetime import datetime

def create_child(
    db: Session,
    parent_id: int,
    first_name: str,
    last_name: str,
    guardian_email: str,
    guardian_phone: str,
    address: str,
    child_class: str,
    section: str,
    birth_mark: Optional[str],
    health_issue: Optional[str],
    profile_image: str,
    signature: str,
    date_of_birth: date,
    age: int,
    gender: str,
    bio: Optional[str],
    hafiz: bool
):
    child = Child(
        parent_id=parent_id,
        first_name=first_name,
        last_name=last_name,
        guardian_email=guardian_email,
        guardian_phone=guardian_phone,
        address=address,
        child_class=child_class,
        section=section,
        birth_mark=birth_mark,
        health_issue=health_issue,
        profile_image=profile_image,
        signature=signature,
        date_of_birth=date_of_birth,
        age=age,
        gender=gender,
        bio=bio,
        hafiz=hafiz,
        created_at=datetime.utcnow(),
        updated_at=None
    )
    db.add(child)
    db.commit()
    db.refresh(child)
    return "User Add succssfully please wait for approve."
