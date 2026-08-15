from fastapi import APIRouter, Depends, HTTPException, Query, Header, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Review, Professor, ReviewVote, TeacherSubmissionLog, VerifiedUser
from app.schemas import ReviewCreate, ReviewOut
from app.services.profanity import check_profanity
from app.services.otp import hash_email

router = APIRouter(prefix="/reviews", tags=["Teacher Reviews"])

def build_review_out(rev: Review, is_voted: bool = False) -> ReviewOut:
    return ReviewOut(
        id=rev.id,
        professorId=rev.professor_id,
        professorName=rev.professor.name if rev.professor else "Professor",
        courseCode=rev.course_code,
        courseTitle=rev.course_title,
        ratingTeaching=rev.rating_teaching,
        ratingGrading=rev.rating_grading,
        ratingWorkload=rev.rating_workload,
        overallScore=rev.overall_score,
        comment=rev.comment,
        gradeReceived=rev.grade_received,
        semesterTaken=rev.semester_taken,
        helpfulCount=rev.helpful_count,
        isHelpfulVoted=is_voted,
        createdAt=rev.created_at.isoformat()
    )

@router.get("", response_model=List[ReviewOut])
def get_reviews(
    professorId: Optional[str] = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Review)

    if professorId:
        query = query.filter(Review.professor_id == professorId)

    reviews = query.order_by(Review.created_at.desc()).all()
    return [build_review_out(r) for r in reviews]

@router.post("", response_model=ReviewOut)
def submit_review(
    request: Request,
    payload: ReviewCreate,
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db)
):
    # Check profanity
    is_profane, flagged = check_profanity(payload.comment)
    if is_profane:
        raise HTTPException(
            status_code=400,
            detail="Please keep feedback constructive and refrain from inappropriate language."
        )

    prof = db.query(Professor).filter(Professor.id == payload.professorId).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Selected professor not found.")

    # RESOLVE user from session cookie (reliable even after page refresh)
    user = None
    cookie_name = "skh_session"
    token = request.cookies.get(cookie_name)
    if token and token.startswith("skh-session-"):
        user = db.query(VerifiedUser).filter(VerifiedUser.session_token == token).first()

    # Fallback: also try frontend-sent email if cookie lookup fails
    if not user and payload.userEmail:
        e_hash = hash_email(payload.userEmail)
        user = db.query(VerifiedUser).filter(VerifiedUser.email_hash == e_hash).first()

    # ENFORCE ONE REVIEW PER STUDENT PER TEACHER
    if user:
        existing_submission = db.query(TeacherSubmissionLog).filter(
            TeacherSubmissionLog.user_id == user.id,
            TeacherSubmissionLog.professor_id == payload.professorId
        ).first()

        if existing_submission:
            raise HTTPException(
                status_code=400,
                detail=f"You have already published a review for {prof.name}. Each student can only review a teacher once."
            )

    # Calculate overall score formula: (Teaching * 0.4 + Grading * 0.4 + (6 - Workload) * 0.2)
    overall_score = round(
        (payload.ratingTeaching * 0.4 + payload.ratingGrading * 0.4 + (6 - payload.ratingWorkload) * 0.2),
        1
    )

    # ABSOLUTE PRIVACY: Save review with NO link to user identity
    new_review = Review(
        professor_id=payload.professorId,
        course_code=payload.courseCode or "CS-101",
        course_title=payload.courseTitle or "Course",
        rating_teaching=payload.ratingTeaching,
        rating_grading=payload.ratingGrading,
        rating_workload=payload.ratingWorkload,
        overall_score=overall_score,
        comment=payload.comment.strip(),
        grade_received=payload.gradeReceived,
        semester_taken=payload.semesterTaken or "Fall 2025",
        helpful_count=0
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    # Log submission to enforce one-review-per-teacher rule without linking to review text
    if user:
        submission_log = TeacherSubmissionLog(
            user_id=user.id,
            professor_id=payload.professorId
        )
        db.add(submission_log)
        db.commit()

    return build_review_out(new_review)

@router.post("/{review_id}/vote")
def vote_helpful(review_id: str, db: Session = Depends(get_db)):
    rev = db.query(Review).filter(Review.id == review_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Review not found.")

    rev.helpful_count += 1
    db.commit()
    db.refresh(rev)

    return {"success": True, "newCount": rev.helpful_count}
