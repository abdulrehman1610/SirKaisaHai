from typing import List, Optional, Set
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import case, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, get_current_user_optional
from app.limiter import limiter, user_or_ip_key
from app.models import Professor, Review, ReviewVote, TeacherSubmissionLog, VerifiedUser
from app.schemas import ReviewCreate, ReviewOut, VoteResponse
from app.services.identity import compute_voter_key, utc_day_floor
from app.services.profanity import check_profanity

router = APIRouter(prefix="/reviews", tags=["Teacher Reviews"])


def build_review_out(rev: Review, is_voted: bool = False) -> ReviewOut:
    # Truncate createdAt to minute precision to prevent sub-minute timing correlation
    created_minute = rev.created_at.replace(second=0, microsecond=0).isoformat()
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
        createdAt=created_minute,
    )


@router.get("", response_model=List[ReviewOut])
def get_reviews(
    professorId: Optional[str] = Query(default=None),
    user: Optional[VerifiedUser] = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    query = db.query(Review)

    if professorId:
        query = query.filter(Review.professor_id == professorId)

    reviews = query.order_by(Review.created_at.desc()).all()

    voted_review_ids: Set[str] = set()
    if user and reviews:
        voter_keys = [compute_voter_key(user.id, rev.id) for rev in reviews]
        voted_rows = (
            db.query(ReviewVote.review_id)
            .filter(ReviewVote.voter_key.in_(voter_keys))
            .all()
        )
        voted_review_ids = {row[0] for row in voted_rows}

    return [build_review_out(r, is_voted=(r.id in voted_review_ids)) for r in reviews]


@router.post("", response_model=ReviewOut)
@limiter.limit("10/hour", key_func=user_or_ip_key)
def submit_review(
    request: Request,
    payload: ReviewCreate,
    user: VerifiedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check profanity
    is_profane, _ = check_profanity(payload.comment)
    if is_profane:
        raise HTTPException(
            status_code=400,
            detail="Please keep feedback constructive and refrain from inappropriate language.",
        )

    prof = db.query(Professor).filter(Professor.id == payload.professorId).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Selected professor not found.")

    # Calculate overall score formula: (Teaching * 0.4 + Grading * 0.4 + (6 - Workload) * 0.2)
    overall_score = round(
        (payload.ratingTeaching * 0.4 + payload.ratingGrading * 0.4 + (6 - payload.ratingWorkload) * 0.2),
        1,
    )

    # ABSOLUTE PRIVACY: Review carries ZERO link to user identity.
    # Enforce 1-review-per-student-per-professor atomically via UNIQUE(user_id, professor_id).
    submission_log = TeacherSubmissionLog(
        user_id=user.id,
        professor_id=payload.professorId,
        submitted_at=utc_day_floor(),
    )
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
        helpful_count=0,
    )

    try:
        db.add(submission_log)
        db.add(new_review)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You have already published a review for {prof.name}. Each student can only review a teacher once.",
        )

    db.refresh(new_review)
    return build_review_out(new_review)


@router.post("/{review_id}/vote", response_model=VoteResponse)
@limiter.limit("60/hour", key_func=user_or_ip_key)
def vote_helpful(
    request: Request,
    review_id: str,
    user: VerifiedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rev = db.query(Review).filter(Review.id == review_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Review not found.")

    voter_key = compute_voter_key(user.id, review_id)
    try:
        db.add(ReviewVote(review_id=review_id, voter_key=voter_key))
        db.flush()
        db.execute(
            update(Review)
            .where(Review.id == review_id)
            .values(helpful_count=Review.helpful_count + 1)
        )
        db.commit()
    except IntegrityError:
        # Idempotent: student already voted helpful on this review
        db.rollback()

    current_count = db.query(Review.helpful_count).filter(Review.id == review_id).scalar() or 0
    return VoteResponse(success=True, voted=True, newCount=current_count)


@router.delete("/{review_id}/vote", response_model=VoteResponse)
@limiter.limit("60/hour", key_func=user_or_ip_key)
def unvote_helpful(
    request: Request,
    review_id: str,
    user: VerifiedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rev = db.query(Review).filter(Review.id == review_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Review not found.")

    voter_key = compute_voter_key(user.id, review_id)
    deleted = (
        db.query(ReviewVote)
        .filter(ReviewVote.review_id == review_id, ReviewVote.voter_key == voter_key)
        .delete(synchronize_session=False)
    )
    if deleted:
        db.execute(
            update(Review)
            .where(Review.id == review_id)
            .values(
                helpful_count=case(
                    (Review.helpful_count > 0, Review.helpful_count - 1),
                    else_=0,
                )
            )
        )
    db.commit()

    current_count = db.query(Review.helpful_count).filter(Review.id == review_id).scalar() or 0
    return VoteResponse(success=True, voted=False, newCount=current_count)
