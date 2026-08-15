import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

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
    department_id = Column(String, ForeignKey("departments.id"), nullable=False)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    tags_json = Column(String, nullable=True, default="[]")  # Serialized list of tags
    ai_summary = Column(Text, nullable=True)
    created_by_user_id = Column(String, ForeignKey("verified_users.id"), nullable=True)

    department = relationship("Department", back_populates="professors")
    reviews = relationship("Review", back_populates="professor", cascade="all, delete-orphan")

class VerifiedUser(Base):
    __tablename__ = "verified_users"

    # STRICT PRIVACY PROMISE: Only SHA-256 email_hash is stored! Plain text email is NEVER saved.
    id = Column(String, primary_key=True, default=generate_uuid)
    email_hash = Column(String, unique=True, index=True, nullable=False)
    session_token = Column(String, nullable=True, index=True)
    is_verified = Column(Boolean, default=True)
    verified_at = Column(DateTime, default=datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"

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
    created_at = Column(DateTime, default=datetime.utcnow)

    professor = relationship("Professor", back_populates="reviews")
    votes = relationship("ReviewVote", back_populates="review", cascade="all, delete-orphan")

class ReviewVote(Base):
    __tablename__ = "review_votes"

    id = Column(String, primary_key=True, default=generate_uuid)
    review_id = Column(String, ForeignKey("reviews.id"), nullable=False)
    user_id = Column(String, ForeignKey("verified_users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("Review", back_populates="votes")

class TeacherSubmissionLog(Base):
    __tablename__ = "teacher_submission_logs"

    # Enforces "one review per student per teacher" without linking to review text
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("verified_users.id"), nullable=False)
    professor_id = Column(String, ForeignKey("professors.id"), nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

class TeacherCreationLog(Base):
    __tablename__ = "teacher_creation_logs"

    # ONLY SECURITY EXCEPTION: Audit log tracking which verified student added a new teacher
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("verified_users.id"), nullable=True)
    user_email = Column(String, nullable=True)
    professor_id = Column(String, ForeignKey("professors.id"), nullable=False)
    teacher_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
