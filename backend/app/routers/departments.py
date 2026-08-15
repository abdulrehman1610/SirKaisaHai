from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Department
from app.schemas import DepartmentOut

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("", response_model=List[DepartmentOut])
def get_departments(db: Session = Depends(get_db)):
    depts = db.query(Department).all()
    return [
        DepartmentOut(
            id=d.id,
            universityId=d.university_id,
            name=d.name,
            code=d.code
        )
        for d in depts
    ]
