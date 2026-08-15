import json
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal, engine, Base
from app.models import University, Department, Professor, Review, VerifiedUser, TeacherCreationLog, TeacherSubmissionLog, ReviewVote

# The 7 Official Computing Departments of Superior University
OFFICIAL_DEPARTMENTS = [
    {"id": "dept-cs", "name": "Computer Science", "code": "CS"},
    {"id": "dept-se", "name": "Software Engineering", "code": "SE"},
    {"id": "dept-cys", "name": "Cyber Security", "code": "CYS"},
    {"id": "dept-ds", "name": "Data Science", "code": "DS"},
    {"id": "dept-ai", "name": "Artificial Intelligence", "code": "AI"},
    {"id": "dept-it", "name": "Information Technology", "code": "IT"},
    {"id": "dept-iot", "name": "Internet of Things", "code": "IoT"},
]

def reset_and_seed_database():
    """Completely wipes tables and seeds the official Superior University departments."""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        print("\n[DB RESET] Clearing all old reviews, teachers, logs, and departments...")
        
        # 1. Delete dependent tables first
        db.query(ReviewVote).delete()
        db.query(Review).delete()
        db.query(TeacherCreationLog).delete()
        db.query(TeacherSubmissionLog).delete()
        db.query(Professor).delete()
        db.query(Department).delete()
        db.query(University).delete()
        db.commit()

        print("[DB SEED] Creating University & Official Departments...")

        # 2. Add Superior University
        uni = University(
            id="uni-superior",
            name="Superior University",
            short_name="Superior",
            domain="superior.edu.pk",
            logo_url="https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=100&auto=format&fit=crop&q=80"
        )
        db.add(uni)

        # 3. Add the 7 Official Departments
        for d in OFFICIAL_DEPARTMENTS:
            dept = Department(
                id=d["id"],
                university_id="uni-superior",
                name=d["name"],
                code=d["code"]
            )
            db.add(dept)

        db.commit()
        print("[SUCCESS] Database reset cleanly! 7 official departments seeded successfully:")
        for d in OFFICIAL_DEPARTMENTS:
            print(f"  ✓ {d['name']} ({d['code']})")
        print("\nAll temporary faculty and test reviews have been cleared. Ready for real data!\n")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to reset and seed database: {e}")
    finally:
        db.close()

def seed_database():
    """Auto-seed and ensure the official 7 departments are active."""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        # Check if the new IoT department exists
        has_new_depts = db.query(Department).filter(Department.id == "dept-iot").first()
        if has_new_depts:
            return

        reset_and_seed_database()
    except Exception as e:
        print(f"[Seed Note] Check: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_and_seed_database()
