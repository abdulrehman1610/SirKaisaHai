import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def utc_today_midnight() -> datetime:
    return utc_now().replace(hour=0, minute=0, second=0, microsecond=0)


class University(Base):
    __tablename__ = "universities"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)

    departments = relationship("Department", back_populates="university", cascade="all, delete-orphan")


class Department(Base):
    __tablename__ = "departments"

    id = Column(String, primary_key=True, default=generate_uuid)
    university_id = Column(String, ForeignKey("universities.id"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)

    university = relationship("University", back_populates="departments")
    professors = relationship("Professor", back_populates="department", cascade="all, delete-orphan")


class Professor(Base):
    __tablename__ = "professors"

    id = Column(String, primary_key=True, default=generate_uuid)
    department_id = Column(String, ForeignKey("departments.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    normalized_name = Column(String, nullable=False, unique=True, index=True)
    title = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    tags_json = Column(String, nullable=True, default="[]")  # Serialized list of tags
    ai_summary = Column(Text, nullable=True)
    created_by_user_id = Column(String, ForeignKey("verified_users.id"), nullable=True)

    department = relationship("Department", back_populates="professors")
    reviews = relationship("Review", back_populates="professor", cascade="all, delete-orphan")


class VerifiedUser(Base):
    __tablename__ = "verified_users"

    # STRICT PRIVACY PROMISE: Only keyed HMAC-SHA256 email_hash is stored! Plaintext email is NEVER saved.
    id = Column(String, primary_key=True, default=generate_uuid)
    email_hash = Column(String, unique=True, index=True, nullable=False)
    hash_version = Column(SmallInteger, nullable=False, default=2)
    session_token = Column(String, nullable=True, index=True)
    session_expires_at = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=True)
    verified_at = Column(DateTime, default=utc_now)


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        Index("ix_reviews_prof_created", "professor_id", "created_at"),
    )

    # STRICT PRIVACY PROMISE: Zero Foreign Keys back to VerifiedUser!
    id = Column(String, primary_key=True, default=generate_uuid)
    professor_id = Column(String, ForeignKey("professors.id"), nullable=False)
    course_code = Column(String, nullable=False, default="CS-101")
    course_title = Column(String, nullable=False, default="Course")

    rating_teaching = Column(Float, nullable=False, default=5.0)
    rating_grading = Column(Float, nullable=False, default=5.0)
    rating_workload = Column(Float, nullable=False, default=3.0)
    overall_score = Column(Float, nullable=False, default=4.5)

    comment = Column(Text, nullable=False)
    grade_received = Column(String, nullable=True)
    semester_taken = Column(String, nullable=False, default="Fall 2025")
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now)

    professor = relationship("Professor", back_populates="reviews")
    votes = relationship("ReviewVote", back_populates="review", cascade="all, delete-orphan")


class ReviewVote(Base):
    __tablename__ = "review_votes"
    __table_args__ = (
        UniqueConstraint("review_id", "voter_key", name="uq_review_votes_review_voter"),
    )

    # STRICT PRIVACY PROMISE: voter_key is HMAC(VOTE_SECRET, user_id:review_id) — no user_id stored!
    id = Column(String, primary_key=True, default=generate_uuid)
    review_id = Column(String, ForeignKey("reviews.id"), nullable=False, index=True)
    voter_key = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=utc_now)

    review = relationship("Review", back_populates="votes")


class TeacherSubmissionLog(Base):
    __tablename__ = "teacher_submission_logs"
    __table_args__ = (
        UniqueConstraint("user_id", "professor_id", name="uq_submission_user_prof"),
    )

    # Enforces "one review per student per teacher" without linking to review text
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("verified_users.id"), nullable=False, index=True)
    professor_id = Column(String, ForeignKey("professors.id"), nullable=False)
    submitted_at = Column(DateTime, default=utc_today_midnight)


class TeacherCreationLog(Base):
    __tablename__ = "teacher_creation_logs"

    # Audit log tracking which verified user_id added a new teacher (no plaintext email stored)
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("verified_users.id"), nullable=True)
    professor_id = Column(String, ForeignKey("professors.id"), nullable=False)
    teacher_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=utc_now)


class OTPChallenge(Base):
    __tablename__ = "otp_challenges"

    # Persistent OTP challenge: stores only identity_hash and code_hash (never plaintext email or code)
    id = Column(String, primary_key=True, default=generate_uuid)
    identity_hash = Column(String(64), nullable=False, index=True)
    code_hash = Column(String(64), nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    consumed_at = Column(DateTime, nullable=True)
    failed_attempts = Column(SmallInteger, nullable=False, default=0)
    created_at = Column(DateTime, default=utc_now)


class AuthAttempt(Base):
    __tablename__ = "auth_attempts"

    # Persistent sliding-window attempt log for OTP requests and failed verifications
    id = Column(String, primary_key=True, default=generate_uuid)
    identity_hash = Column(String(64), nullable=False, index=True)
    kind = Column(String(16), nullable=False)  # 'request' | 'verify_fail'
    created_at = Column(DateTime, default=utc_now, index=True)
