import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.cache import professors_cache
from app.database import get_db, get_read_db
from app.dependencies import get_current_user
from app.limiter import limiter, user_or_ip_key
from app.models import Department, Professor, Review, TeacherCreationLog, VerifiedUser
from app.schemas import ProfessorCreate, ProfessorOut, SearchResultItem
from app.services.identity import normalize_teacher_name

router = APIRouter(prefix="/professors", tags=["Professors / Teachers"])


def _row_to_professor_out(
    prof: Professor,
    dept_name: Optional[str],
    total_reviews: int,
    avg_teaching: Optional[float],
    avg_grading: Optional[float],
    avg_workload: Optional[float],
    overall_rating: Optional[float],
) -> ProfessorOut:
    if total_reviews > 0:
        t_avg = round(float(avg_teaching or 0.0), 1)
        g_avg = round(float(avg_grading or 0.0), 1)
        w_avg = round(float(avg_workload or 0.0), 1)
        o_avg = round(float(overall_rating or 0.0), 1)
    else:
        t_avg = 5.0
        g_avg = 5.0
        w_avg = 3.0
        o_avg = 5.0

    tags = json.loads(prof.tags_json) if prof.tags_json else []

    return ProfessorOut(
        id=prof.id,
        departmentId=prof.department_id,
        departmentName=dept_name or "Department",
        name=prof.name,
        title=prof.title,
        avatarUrl=prof.avatar_url,
        avgTeaching=t_avg,
        avgGrading=g_avg,
        avgWorkload=w_avg,
        overallRating=o_avg,
        totalReviews=int(total_reviews),
        aiSummary=prof.ai_summary,
        tags=tags,
    )


def _query_professors_aggregated(
    db: Session,
    department_id: Optional[str] = None,
    q: Optional[str] = None,
    prof_id: Optional[str] = None,
) -> List[ProfessorOut]:
    """Single SQL LEFT JOIN + GROUP BY query — eliminates N+1 review & department queries."""
    query = (
        db.query(
            Professor,
            Department.name.label("dept_name"),
            func.count(Review.id).label("total_reviews"),
            func.avg(Review.rating_teaching).label("avg_teaching"),
            func.avg(Review.rating_grading).label("avg_grading"),
            func.avg(Review.rating_workload).label("avg_workload"),
            func.avg(Review.overall_score).label("overall_rating"),
        )
        .join(Department, Professor.department_id == Department.id)
        .outerjoin(Review, Review.professor_id == Professor.id)
    )

    if prof_id:
        query = query.filter(Professor.id == prof_id)

    if department_id and department_id != "all":
        query = query.filter(Professor.department_id == department_id)

    if q and q.strip():
        search = f"%{q.strip().lower()}%"
        query = query.filter(
            (Professor.name.ilike(search)) | (Professor.title.ilike(search))
        )

    rows = query.group_by(Professor.id, Department.name).all()
    return [
        _row_to_professor_out(
            prof=row[0],
            dept_name=row[1],
            total_reviews=row[2] or 0,
            avg_teaching=row[3],
            avg_grading=row[4],
            avg_workload=row[5],
            overall_rating=row[6],
        )
        for row in rows
    ]


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
    db: Session = Depends(get_read_db),
):
    cache_key = f"list:{departmentId or 'all'}:{(q or '').strip().lower()}"
    return professors_cache.get_or_set(
        db,
        cache_key,
        lambda: _query_professors_aggregated(db, department_id=departmentId, q=q),
    )


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
    professors_cache.invalidate_all(db)
    return _row_to_professor_out(
        prof=new_prof,
        dept_name=dept.name,
        total_reviews=0,
        avg_teaching=None,
        avg_grading=None,
        avg_workload=None,
        overall_rating=None,
    )


@router.get("/search/all", response_model=List[SearchResultItem])
def search_catalog(
    q: Optional[str] = Query(default=""),
    departmentId: Optional[str] = Query(default="all"),
    db: Session = Depends(get_read_db),
):
    cache_key = f"search:{departmentId or 'all'}:{(q or '').strip().lower()}"

    def _load() -> List[SearchResultItem]:
        prof_dtos = _query_professors_aggregated(db, department_id=departmentId, q=q)
        return [
            SearchResultItem(
                id=p.id,
                type="professor",
                title=p.name,
                subtitle=p.title,
                department=p.departmentName,
                rating=p.overallRating,
                reviewCount=p.totalReviews,
                url=f"/professor/{p.id}",
            )
            for p in prof_dtos
        ]

    return professors_cache.get_or_set(db, cache_key, _load)


@router.get("/{prof_id}", response_model=ProfessorOut)
def get_professor_by_id(prof_id: str, db: Session = Depends(get_read_db)):
    def _load() -> ProfessorOut:
        results = _query_professors_aggregated(db, prof_id=prof_id)
        if not results:
            raise HTTPException(status_code=404, detail="Professor not found")
        return results[0]

    return professors_cache.get_or_set(db, f"id:{prof_id}", _load)
