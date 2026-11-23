import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.dependencies import COOKIE_NAME, get_current_user_optional
from app.limiter import limiter
from app.models import (
    AuthAttempt,
    OTPChallenge,
    ReviewVote,
    TeacherCreationLog,
    TeacherSubmissionLog,
    VerifiedUser,
)
from app.schemas import AuthResponse, OTPRequest, OTPVerify
from app.services.identity import (
    compute_session_expiry,
    email_identity_hash,
    legacy_email_hash,
    mask_email,
    normalize_email,
    utc_now,
)
from app.services.otp import request_otp_service, verify_otp_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/request-otp", response_model=AuthResponse)
@limiter.limit("5/15minute")
def request_otp(request: Request, payload: OTPRequest, db: Session = Depends(get_db)):
    success, msg, status_code = request_otp_service(db, payload.email)
    if not success:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": msg, "detail": msg},
        )
    return AuthResponse(success=True, message=msg, email=mask_email(payload.email))


@router.post("/verify-otp", response_model=AuthResponse)
@limiter.limit("5/15minute")
def verify_otp(
    request: Request,
    payload: OTPVerify,
    response: Response,
    db: Session = Depends(get_db),
):
    success, msg, status_code, challenge = verify_otp_service(db, payload.email, payload.code)
    if not success or challenge is None:
        return JSONResponse(
            status_code=status_code,
            content={"success": False, "message": msg, "detail": msg},
        )

    now = utc_now()
    e_hash = email_identity_hash(payload.email)
    user = db.query(VerifiedUser).filter(VerifiedUser.email_hash == e_hash).first()

    # Lazy migration: upgrade legacy unsalted SHA-256 users in place preserving user.id & submission logs
    if not user:
        leg_hash = legacy_email_hash(payload.email)
        legacy_user = db.query(VerifiedUser).filter(VerifiedUser.email_hash == leg_hash).first()
        if legacy_user:
            legacy_user.email_hash = e_hash
            legacy_user.hash_version = 2
            user = legacy_user

    if not user:
        user = VerifiedUser(email_hash=e_hash, hash_version=2)
        db.add(user)
        db.flush()

    # Fresh session token valid strictly until end of this calendar day (Asia/Karachi)
    session_token = f"skh-session-{uuid.uuid4()}"
    expires_at = compute_session_expiry(now)
    user.session_token = session_token
    user.session_expires_at = expires_at

    # Burn OTP challenge atomically in the same transaction
    challenge.consumed_at = now
    db.commit()
    db.refresh(user)

    max_age_seconds = max(60, int((expires_at - now).total_seconds()))

    response.set_cookie(
        key=COOKIE_NAME,
        value=session_token,
        httponly=True,
        secure=settings.effective_cookie_secure,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        max_age=max_age_seconds,
        path="/",
    )

    return AuthResponse(
        success=True,
        message="Student email verified successfully!",
        token=None,
        email=mask_email(normalize_email(payload.email)),
    )


@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    """Immediately invalidate session token in database and clear the session cookie."""
    token = request.cookies.get(COOKIE_NAME)
    if token:
        user = db.query(VerifiedUser).filter(VerifiedUser.session_token == token).first()
        if user:
            user.session_token = None
            user.session_expires_at = None
            db.commit()

    response.delete_cookie(
        key=COOKIE_NAME,
        httponly=True,
        secure=settings.effective_cookie_secure,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        path="/",
    )
    return {"success": True, "message": "Logged out successfully. Session immediately invalidated."}


@router.get("/me")
def get_current_user_session(
    user: Optional[VerifiedUser] = Depends(get_current_user_optional),
):
    """Check if caller holds an active, non-expired session token in database."""
    if not user:
        return {"authenticated": False}

    return {
        "authenticated": True,
        "userId": user.id,
        "emailHash": user.email_hash,
        "expiresAt": user.session_expires_at.isoformat() if user.session_expires_at else None,
    }


@router.post("/reset-test-users")
def reset_test_users(
    x_admin_secret: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
):
    if settings.is_production:
        if not x_admin_secret or x_admin_secret != settings.ADMIN_SECRET_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: Admin key required to reset data in production.",
            )

    db.query(OTPChallenge).delete()
    db.query(AuthAttempt).delete()
    db.query(ReviewVote).delete()
    db.query(TeacherCreationLog).delete()
    db.query(TeacherSubmissionLog).delete()
    db.query(VerifiedUser).delete()
    db.commit()
    return {"success": True, "message": "All test users and logs cleared successfully!"}
