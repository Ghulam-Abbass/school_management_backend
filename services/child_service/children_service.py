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
    return "Child Add succssfully please wait for approve."


def update_child(
    db: Session,
    child_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    guardian_email: Optional[str] = None,
    guardian_phone: Optional[str] = None,
    address: Optional[str] = None,
    child_class: Optional[str] = None,
    section: Optional[str] = None,
    birth_mark: Optional[str] = None,
    health_issue: Optional[str] = None,
    profile_image: Optional[str] = None,
    signature: Optional[str] = None,
    date_of_birth: Optional[datetime] = None,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    bio: Optional[str] = None,
    hafiz: Optional[bool] = None
):
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise ValueError("Child not found")

    if first_name is not None:
        child.first_name = first_name
    if last_name is not None:
        child.last_name = last_name
    if guardian_email is not None:
        child.guardian_email = guardian_email
    if guardian_phone is not None:
        child.guardian_phone = guardian_phone
    if address is not None:
        child.address = address
    if child_class is not None:
        child.child_class = child_class
    if section is not None:
        child.section = section
    if birth_mark is not None:
        child.birth_mark = birth_mark
    if health_issue is not None:
        child.health_issue = health_issue
    if profile_image is not None:
        child.profile_image = profile_image
    if signature is not None:
        child.signature = signature
    if date_of_birth is not None:
        child.date_of_birth = date_of_birth
    if age is not None:
        child.age = age
    if gender is not None:
        child.gender = gender
    if bio is not None:
        child.bio = bio
    if hafiz is not None:
        child.hafiz = hafiz

    child.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(child)

    if child.approved == True:
        return "Child updated successfully"
    else:
        return "Child updated successfully. Please wait for approval."
