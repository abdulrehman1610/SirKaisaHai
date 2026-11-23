from typing import List, Optional
from pydantic import BaseModel, Field


# University Schemas
class UniversityOut(BaseModel):
    id: str
    name: str
    shortName: str
    domain: str
    logoUrl: Optional[str] = None

    class Config:
        from_attributes = True


# Department Schemas
class DepartmentOut(BaseModel):
    id: str
    universityId: str
    name: str
    code: str

    class Config:
        from_attributes = True


# Professor (Teacher) Schemas
class ProfessorCreate(BaseModel):
    name: str = Field(..., min_length=3)
    departmentId: str
    title: Optional[str] = "Lecturer"
    tags: Optional[List[str]] = ["New Faculty"]
    # Deprecated: accepted for backward compatibility only; ignored by backend
    userEmail: Optional[str] = None


class ProfessorOut(BaseModel):
    id: str
    departmentId: str
    departmentName: str
    name: str
    title: str
    avatarUrl: Optional[str] = None
    avgTeaching: float
    avgGrading: float
    avgWorkload: float
    overallRating: float
    totalReviews: int
    aiSummary: Optional[str] = None
    tags: List[str]

    class Config:
        from_attributes = True


# Review Schemas
class ReviewCreate(BaseModel):
    professorId: str
    courseCode: Optional[str] = "CS-101"
    courseTitle: Optional[str] = "General Course"
    ratingTeaching: float = Field(..., ge=1.0, le=5.0)
    ratingGrading: float = Field(..., ge=1.0, le=5.0)
    ratingWorkload: float = Field(..., ge=1.0, le=5.0)
    comment: str = Field(..., min_length=5, max_length=500)
    gradeReceived: Optional[str] = "A"
    semesterTaken: Optional[str] = "Fall 2025"
    # Deprecated: accepted for backward compatibility only; ignored by backend
    userEmail: Optional[str] = None


class ReviewOut(BaseModel):
    id: str
    professorId: str
    professorName: str
    courseCode: str
    courseTitle: str
    ratingTeaching: float
    ratingGrading: float
    ratingWorkload: float
    overallScore: float
    comment: str
    gradeReceived: Optional[str] = None
    semesterTaken: str
    helpfulCount: int
    isHelpfulVoted: Optional[bool] = False
    createdAt: str

    class Config:
        from_attributes = True


class VoteResponse(BaseModel):
    success: bool
    voted: bool
    newCount: int


# Search Result Schema
class SearchResultItem(BaseModel):
    id: str
    type: str = "professor"
    title: str
    subtitle: str
    department: str
    rating: float
    reviewCount: int
    url: str


# Auth Schemas
class OTPRequest(BaseModel):
    email: str


class OTPVerify(BaseModel):
    email: str
    code: str


class AuthResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    email: Optional[str] = None
