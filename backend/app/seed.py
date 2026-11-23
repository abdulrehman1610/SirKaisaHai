import argparse
import sys
from typing import Optional
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models import (
    AuthAttempt,
    Department,
    OTPChallenge,
    Professor,
    Review,
    ReviewVote,
    TeacherCreationLog,
    TeacherSubmissionLog,
    University,
)

# The 8 Official Computing Departments of Superior University
OFFICIAL_DEPARTMENTS = [
    {"id": "dept-cs", "name": "Computer Science", "code": "CS"},
    {"id": "dept-se", "name": "Software Engineering", "code": "SE"},
    {"id": "dept-cys", "name": "Cyber Security", "code": "CYS"},
    {"id": "dept-ds", "name": "Data Science", "code": "DS"},
    {"id": "dept-ai", "name": "Artificial Intelligence", "code": "AI"},
    {"id": "dept-it", "name": "Information Technology", "code": "IT"},
    {"id": "dept-iot", "name": "Internet of Things", "code": "IoT"},
    {"id": "dept-gd", "name": "Game Design", "code": "GD"},
]

SUPERIOR_UNIVERSITY = {
    "id": "uni-superior",
    "name": "Superior University",
    "short_name": "Superior",
    "domain": "superior.edu.pk",
    "logo_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=100&auto=format&fit=crop&q=80",
}


def upsert_reference_data(db: Optional[Session] = None) -> None:
    """
    Idempotently inserts or updates Superior University and its 8 official Computing departments.
    NEVER deletes professors, reviews, users, or logs.
    """
    owns_session = db is None
    session = db if db is not None else SessionLocal()

    try:
        uni = session.query(University).filter(University.id == SUPERIOR_UNIVERSITY["id"]).first()
        if uni is None:
            session.add(University(**SUPERIOR_UNIVERSITY))
        else:
            uni.name = SUPERIOR_UNIVERSITY["name"]
            uni.short_name = SUPERIOR_UNIVERSITY["short_name"]
            uni.domain = SUPERIOR_UNIVERSITY["domain"]
            uni.logo_url = SUPERIOR_UNIVERSITY["logo_url"]
        session.flush()

        for dept_data in OFFICIAL_DEPARTMENTS:
            dept = session.query(Department).filter(Department.id == dept_data["id"]).first()
            if dept is None:
                session.add(
                    Department(
                        id=dept_data["id"],
                        university_id=SUPERIOR_UNIVERSITY["id"],
                        name=dept_data["name"],
                        code=dept_data["code"],
                    )
                )
            else:
                dept.university_id = SUPERIOR_UNIVERSITY["id"]
                dept.name = dept_data["name"]
                dept.code = dept_data["code"]

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        if owns_session:
            session.close()


def seed_database(db: Optional[Session] = None) -> None:
    """Safe alias for upsert_reference_data()."""
    upsert_reference_data(db=db)


def reset_and_seed_database(confirm: bool = False, db: Optional[Session] = None) -> None:
    """
    Explicit destructive reset for local development only.
    Refuses to run when ENVIRONMENT=production or without confirm=True.
    """
    if settings.is_production:
        raise RuntimeError("Refusing to reset database when ENVIRONMENT=production.")
    if not confirm:
        raise RuntimeError("Destructive reset requires explicit confirmation (confirm=True / --confirm).")

    owns_session = db is None
    session = db if db is not None else SessionLocal()

    try:
        session.query(OTPChallenge).delete()
        session.query(AuthAttempt).delete()
        session.query(ReviewVote).delete()
        session.query(Review).delete()
        session.query(TeacherCreationLog).delete()
        session.query(TeacherSubmissionLog).delete()
        session.query(Professor).delete()
        session.query(Department).delete()
        session.query(University).delete()
        session.commit()

        upsert_reference_data(db=session)
    except Exception:
        session.rollback()
        raise
    finally:
        if owns_session:
            session.close()


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Seed SirKaisaHai reference data.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Wipe all data before seeding (blocked in production; requires --confirm).",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Confirm destructive --reset operation.",
    )
    args = parser.parse_args(argv)

    try:
        if args.reset:
            reset_and_seed_database(confirm=args.confirm)
            print("[SUCCESS] Database wiped and reference data re-seeded.")
        else:
            upsert_reference_data()
            print("[SUCCESS] Reference data upserted safely (1 university, 8 departments).")
        return 0
    except RuntimeError as err:
        print(f"[ERROR] {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
