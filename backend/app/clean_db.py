import sys

from app.config import settings
from app.database import SessionLocal
from app.models import (
    AuthAttempt,
    OTPChallenge,
    ReviewVote,
    TeacherCreationLog,
    TeacherSubmissionLog,
    VerifiedUser,
)


def clean_test_users() -> None:
    if settings.is_production:
        raise RuntimeError("Refusing to wipe test users when ENVIRONMENT=production.")

    db = SessionLocal()
    try:
        db.query(OTPChallenge).delete()
        db.query(AuthAttempt).delete()
        db.query(ReviewVote).delete()
        db.query(TeacherCreationLog).delete()
        db.query(TeacherSubmissionLog).delete()
        db.query(VerifiedUser).delete()
        db.commit()
        print("All test users, OTP challenges, attempts, votes, and logs wiped cleanly!")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    try:
        clean_test_users()
    except RuntimeError as err:
        print(f"[ERROR] {err}", file=sys.stderr)
        raise SystemExit(1)
