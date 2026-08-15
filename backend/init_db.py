import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app.models import University, Department, Professor, Review, VerifiedUser, ReviewVote, TeacherSubmissionLog, TeacherCreationLog
from app.seed import seed_database
from app.config import settings

def init_sql_database():
    print("=" * 60)
    print(f"  INITIALIZING SQL DATABASE")
    print(f"  Target DB URL: {settings.clean_database_url}")
    print("=" * 60)

    # 1. Create all SQL Tables
    print("[1/2] Creating SQL tables in database...")
    Base.metadata.create_all(bind=engine)
    print("  -> Tables created successfully: universities, departments, professors, reviews, verified_users, review_votes, teacher_submission_logs, teacher_creation_logs.")

    # 2. Seed Initial University Data
    print("[2/2] Checking & seeding initial data...")
    seed_database()
    print("  -> Initial data check complete!")

    print("=" * 60)
    print("  SQL DATABASE SETUP IS COMPLETE & READY!")
    print("=" * 60)

if __name__ == "__main__":
    init_sql_database()
