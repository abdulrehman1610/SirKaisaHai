import pytest
from alembic import command
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models import Department, Professor, Review, University
from app.seed import OFFICIAL_DEPARTMENTS, reset_and_seed_database, upsert_reference_data
from app.services.identity import normalize_teacher_name
from tests.conftest import make_alembic_config


def test_alembic_upgrade_and_safe_seed_preserves_existing_data(tmp_path):
    db_file = tmp_path / "migration_test.db"
    db_url = f"sqlite:///{db_file.as_posix()}"
    cfg = make_alembic_config(db_url)
    command.upgrade(cfg, "head")

    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with SessionLocal() as db:
        upsert_reference_data(db=db)
        assert db.query(University).count() == 1
        assert db.query(Department).count() == len(OFFICIAL_DEPARTMENTS)

        # Create a professor and a review
        prof = Professor(
            id="prof-keep",
            department_id="dept-cs",
            name="Dr. Saved Teacher",
            normalized_name=normalize_teacher_name("Dr. Saved Teacher"),
            title="Professor",
        )
        db.add(prof)
        db.flush()
        db.add(
            Review(
                id="rev-keep",
                professor_id="prof-keep",
                course_code="CS-101",
                course_title="Intro",
                rating_teaching=5.0,
                rating_grading=4.5,
                rating_workload=3.0,
                overall_score=4.4,
                comment="Great lectures and fair exams.",
                semester_taken="Fall 2025",
            )
        )
        # Simulate missing dept-gd (which previously triggered a full DB wipe!)
        db.query(Department).filter(Department.id == "dept-gd").delete()
        db.commit()

        assert db.query(Department).filter(Department.id == "dept-gd").first() is None

        # Re-run safe seed: restores dept-gd AND keeps all reviews & professors intact
        upsert_reference_data(db=db)
        assert db.query(Department).filter(Department.id == "dept-gd").first() is not None
        assert db.query(Professor).filter(Professor.id == "prof-keep").first() is not None
        assert db.query(Review).filter(Review.id == "rev-keep").first() is not None

    insp = inspect(engine)
    assert "otp_challenges" in insp.get_table_names()
    assert "auth_attempts" in insp.get_table_names()
    engine.dispose()


def test_reset_refuses_without_confirm_and_in_production(db_session, monkeypatch):
    with pytest.raises(RuntimeError, match="confirmation"):
        reset_and_seed_database(confirm=False, db=db_session)

    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    with pytest.raises(RuntimeError, match="production"):
        reset_and_seed_database(confirm=True, db=db_session)
