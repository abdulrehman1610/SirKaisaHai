from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.database import get_db, get_read_db
from app.models import VerifiedUser
from app.services.identity import utc_now

COOKIE_NAME = "skh_session"


def _resolve_verified_user(request: Request, db: Session) -> Optional[VerifiedUser]:
    """
    Resolve the authenticated VerifiedUser from the httpOnly skh_session cookie.
    Enforces server-side session expiration (end-of-day) and clears expired tokens.
    """
    token = request.cookies.get(COOKIE_NAME)
    if not token or not token.startswith("skh-session-"):
        return None

    user = db.query(VerifiedUser).filter(VerifiedUser.session_token == token).first()
    if not user:
        return None

    if user.session_expires_at is not None and utc_now() >= user.session_expires_at:
        db.execute(
            update(VerifiedUser)
            .where(VerifiedUser.id == user.id)
            .values(session_token=None, session_expires_at=None)
        )
        if db.in_transaction():
            db.commit()
        return None

    return user


def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_read_db),
) -> Optional[VerifiedUser]:
    return _resolve_verified_user(request, db)


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> VerifiedUser:
    """Require a valid, non-expired verified student session."""
    user = _resolve_verified_user(request, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Verify your student email to continue.",
        )
    return user
