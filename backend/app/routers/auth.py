from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response, status
from sqlalchemy.orm import Session
from typing import Optional
from app.config import settings
from app.database import get_db
from app.limiter import limiter
from app.schemas import OTPRequest, OTPVerify, AuthResponse
from app.services.otp import request_otp_service, verify_otp_service, hash_email, consume_otp
from app.models import VerifiedUser, TeacherCreationLog, TeacherSubmissionLog, ReviewVote

router = APIRouter(prefix="/auth", tags=["Auth"])

# Cookie configuration
COOKIE_NAME = "skh_session"
IS_PRODUCTION = settings.ENVIRONMENT == "production"

@router.post("/request-otp", response_model=AuthResponse)
@limiter.limit("5/15minute")
def request_otp(request: Request, payload: OTPRequest):
    success, msg = request_otp_service(payload.email)
    if not success:
        return AuthResponse(success=False, message=msg)
    return AuthResponse(success=True, message=msg, email=payload.email)

import uuid

@router.post("/verify-otp", response_model=AuthResponse)
@limiter.limit("5/15minute")
def verify_otp(request: Request, payload: OTPVerify, response: Response, db: Session = Depends(get_db)):
    success, msg = verify_otp_service(payload.email, payload.code)
    if not success:
        return AuthResponse(success=False, message=msg)

    # STRICT PRIVACY: Hash student email with SHA-256
    e_hash = hash_email(payload.email)
    user = db.query(VerifiedUser).filter(VerifiedUser.email_hash == e_hash).first()
    
    if not user:
        user = VerifiedUser(
            email_hash=e_hash
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Generate a fresh, random, cryptographically unique session token
    session_token = f"skh-session-{uuid.uuid4()}"
    user.session_token = session_token
    db.commit()

    # ALWAYS destroy/burn the OTP immediately so it can NEVER be reused again
    consume_otp(payload.email)

    # Set httpOnly cookie — JavaScript cannot read this, only browser sends it automatically
    response.set_cookie(
        key=COOKIE_NAME,
        value=session_token,
        httponly=True,              # JavaScript CANNOT access this cookie
        secure=IS_PRODUCTION,       # HTTPS-only in production, allow HTTP in dev
        samesite="lax",             # Protects against CSRF while allowing normal navigation
        max_age=60 * 60 * 24 * 30,  # 30 days
        path="/",
    )

    return AuthResponse(
        success=True,
        message="Student email verified successfully!",
        token=None,  # NO token in response body anymore — it's in the cookie
        email=payload.email.strip().lower()
    )

@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    """Wipe session token in database and clear the session cookie"""
    token = request.cookies.get(COOKIE_NAME)
    if token:
        user = db.query(VerifiedUser).filter(VerifiedUser.session_token == token).first()
        if user:
            user.session_token = None
            db.commit()

    response.delete_cookie(
        key=COOKIE_NAME,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="lax",
        path="/",
    )
    return {"success": True, "message": "Logged out successfully. Previous session completely invalidated."}

@router.get("/me")
def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Check if user has an active, valid session token in database"""
    token = request.cookies.get(COOKIE_NAME)
    if not token or not token.startswith("skh-session-"):
        return {"authenticated": False}

    user = db.query(VerifiedUser).filter(VerifiedUser.session_token == token).first()
    if not user:
        return {"authenticated": False}

    return {
        "authenticated": True,
        "userId": user.id,
        "emailHash": user.email_hash
    }

@router.post("/reset-test-users")
def reset_test_users(
    x_admin_secret: Optional[str] = Header(default=None),
    db: Session = Depends(get_db)
):
    # Production protection: Only allow wiping if the correct admin secret key is provided
    if settings.ENVIRONMENT == "production":
        if not x_admin_secret or x_admin_secret != settings.ADMIN_SECRET_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized: Admin key required to reset data in production."
            )

    db.query(VerifiedUser).delete()
    db.query(TeacherCreationLog).delete()
    db.query(TeacherSubmissionLog).delete()
    db.query(ReviewVote).delete()
    db.commit()
    return {"success": True, "message": "All test users and logs cleared successfully!"}
