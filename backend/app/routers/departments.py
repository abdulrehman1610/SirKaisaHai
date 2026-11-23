from typing import List
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.cache import departments_cache
from app.database import get_read_db
from app.models import Department
from app.schemas import DepartmentOut

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("", response_model=List[DepartmentOut])
def get_departments(response: Response, db: Session = Depends(get_read_db)):
    response.headers["Cache-Control"] = f"public, max-age={int(departments_cache.ttl_seconds)}"

    def _load() -> List[DepartmentOut]:
        depts = db.query(Department).all()
        return [
            DepartmentOut(
                id=d.id,
                universityId=d.university_id,
                name=d.name,
                code=d.code,
            )
            for d in depts
        ]

    return departments_cache.get_or_set(db, "all", _load)
