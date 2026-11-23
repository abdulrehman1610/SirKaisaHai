import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.limiter import limiter, user_or_ip_key
from app.models import Department, Professor, Review, TeacherCreationLog, VerifiedUser
from app.schemas import ProfessorCreate, ProfessorOut, SearchResultItem
from app.services.identity import normalize_teacher_name

router = APIRouter(prefix="/professors", tags=["Professors / Teachers"])


def build_professor_out(prof: Professor, db: Session) -> ProfessorOut:
    reviews = db.query(Review).filter(Review.professor_id == prof.id).all()
    total_reviews = len(reviews)

    if total_reviews > 0:
        avg_teaching = round(sum(r.rating_teaching for r in reviews) / total_reviews, 1)
        avg_grading = round(sum(r.rating_grading for r in reviews) / total_reviews, 1)
        avg_workload = round(sum(r.rating_workload for r in reviews) / total_reviews, 1)
        overall_rating = round(sum(r.overall_score for r in reviews) / total_reviews, 1)
    else:
        avg_teaching = 5.0
        avg_grading = 5.0
        avg_workload = 3.0
        overall_rating = 5.0

    tags = json.loads(prof.tags_json) if prof.tags_json else []

    return ProfessorOut(
        id=prof.id,
        departmentId=prof.department_id,
        departmentName=prof.department.name if prof.department else "Department",
        name=prof.name,
        title=prof.title,
        avatarUrl=prof.avatar_url,
        avgTeaching=avg_teaching,
        avgGrading=avg_grading,
        avgWorkload=avg_workload,
        overallRating=overall_rating,
        totalReviews=total_reviews,
        aiSummary=prof.ai_summary,
        tags=tags,
    )


def _raise_duplicate_professor(existing: Professor, db: Session) -> None:
    existing_dept = db.query(Department).filter(Department.id == existing.department_id).first()
    dept_label = existing_dept.name if existing_dept else "another department"
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=(
            f"A teacher with the name '{existing.name}' already exists in the {dept_label} department "
            f"(id: {existing.id})."
        ),
    )


@router.get("", response_model=List[ProfessorOut])
def get_professors(
    departmentId: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Professor)

    if departmentId and departmentId != "all":
        query = query.filter(Professor.department_id == departmentId)

    if q:
        search = f"%{q.strip().lower()}%"
        query = query.filter(
            (Professor.name.ilike(search)) | (Professor.title.ilike(search))
        )

    profs = query.all()
    return [build_professor_out(p, db) for p in profs]


@router.post("", response_model=ProfessorOut)
@limiter.limit("5/day", key_func=user_or_ip_key)
def create_professor(
    request: Request,
    payload: ProfessorCreate,
    user: VerifiedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    dept = db.query(Department).filter(Department.id == payload.departmentId).first()
    if not dept:
        raise HTTPException(status_code=400, detail="Department not found.")

    raw_name = payload.name.strip()
    norm_new_name = normalize_teacher_name(raw_name)
    if len(norm_new_name) < 2:
        raise HTTPException(status_code=400, detail="Please enter the professor's full name.")

    # Fast indexed university-wide duplicate check
    existing = db.query(Professor).filter(Professor.normalized_name == norm_new_name).first()
    if existing:
        _raise_duplicate_professor(existing, db)

    tags = payload.tags if payload.tags else ["New Faculty"]
    new_prof = Professor(
        department_id=payload.departmentId,
        name=raw_name,
        normalized_name=norm_new_name,
        title=payload.title or "Lecturer",
        tags_json=json.dumps(tags),
        ai_summary=f"{raw_name} is a faculty member in the {dept.name} department.",
        created_by_user_id=user.id,
    )

    try:
        db.add(new_prof)
        db.flush()

        # Audit log tracks only verified user_id (never plaintext email)
        db.add(
            TeacherCreationLog(
                professor_id=new_prof.id,
                teacher_name=raw_name,
                user_id=user.id,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        existing_after_race = (
            db.query(Professor).filter(Professor.normalized_name == norm_new_name).first()
        )
        if existing_after_race:
            _raise_duplicate_professor(existing_after_race, db)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Teacher already exists.")

    db.refresh(new_prof)
    return build_professor_out(new_prof, db)


@router.get("/search/all", response_model=List[SearchResultItem])
def search_catalog(
    q: Optional[str] = Query(default=""),
    departmentId: Optional[str] = Query(default="all"),
    db: Session = Depends(get_db),
):
    query = db.query(Professor)

    if departmentId and departmentId != "all":
        query = query.filter(Professor.department_id == departmentId)

    if q and q.strip():
        search = f"%{q.strip().lower()}%"
        query = query.filter(
            (Professor.name.ilike(search)) | (Professor.title.ilike(search))
        )

    profs = query.all()
    results = []

    for p in profs:
        prof_dto = build_professor_out(p, db)
        results.append(
            SearchResultItem(
                id=p.id,
                type="professor",
                title=p.name,
                subtitle=p.title,
                department=prof_dto.departmentName,
                rating=prof_dto.overallRating,
                reviewCount=prof_dto.totalReviews,
                url=f"/professor/{p.id}",
            )
        )

    return results


@router.get("/{prof_id}", response_model=ProfessorOut)
def get_professor_by_id(prof_id: str, db: Session = Depends(get_db)):
    prof = db.query(Professor).filter(Professor.id == prof_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")
    return build_professor_out(prof, db)
