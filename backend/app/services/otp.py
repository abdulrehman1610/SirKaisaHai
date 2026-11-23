import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.config import settings
from app.models import AuthAttempt, OTPChallenge
from app.services.email_service import send_otp_email
from app.services.identity import (
    email_identity_hash,
    normalize_email,
    otp_code_hash,
    utc_now,
)

LOCKOUT_WINDOW_SECONDS = 900  # 15 minutes
MAX_REQUEST_ATTEMPTS = 5      # 5 OTP requests / 15 min per identity
MAX_VERIFY_ATTEMPTS = 5       # 5 failed OTP verifications / 15 min per identity
PURGE_AFTER_HOURS = 24


def hash_email(email: str) -> str:
    """Backward-compatible wrapper returning keyed HMAC-SHA256 identity hash."""
    return email_identity_hash(email)


def send_real_email(to_email: str, otp_code: str) -> bool:
    """Delegates to the branded SirKaisaHai HTML OTP email dispatcher."""
    return send_otp_email(to_email, otp_code)


def _purge_stale_auth_records(db: Session, now: datetime) -> None:
    """Remove expired challenges and attempt records older than 24 hours."""
    cutoff = now - timedelta(hours=PURGE_AFTER_HOURS)
    db.query(OTPChallenge).filter(OTPChallenge.expires_at < cutoff).delete(synchronize_session=False)
    db.query(AuthAttempt).filter(AuthAttempt.created_at < cutoff).delete(synchronize_session=False)


def _check_identity_rate_limit(
    db: Session,
    identity_hash: str,
    kind: str,
    max_limit: int,
    now: datetime,
) -> Tuple[bool, int, int]:
    """
    Checks persistent auth_attempts in the last 15 minutes.
    Returns (is_blocked, remaining_seconds, recent_count).
    """
    window_start = now - timedelta(seconds=LOCKOUT_WINDOW_SECONDS)
    recent_rows = (
        db.query(AuthAttempt.created_at)
        .filter(
            AuthAttempt.identity_hash == identity_hash,
            AuthAttempt.kind == kind,
            AuthAttempt.created_at >= window_start,
        )
        .order_by(AuthAttempt.created_at.asc())
        .all()
    )
    count = len(recent_rows)
    if count >= max_limit:
        oldest = recent_rows[0][0]
        elapsed = (now - oldest).total_seconds()
        remaining = max(1, int(LOCKOUT_WINDOW_SECONDS - elapsed))
        return True, remaining, count
    return False, 0, count


def request_otp_service(db: Session, email: str) -> Tuple[bool, str, int]:
    """
    Generates and persists a hashed 6-digit OTP challenge.
    Returns (success, message, http_status_code).
    """
    email_clean = normalize_email(email)
    if not email_clean.endswith("@superior.edu.pk"):
        return False, "Only Superior University student emails (@superior.edu.pk) are permitted.", 400

    now = utc_now()
    identity_hash = email_identity_hash(email_clean)

    _purge_stale_auth_records(db, now)

    is_blocked, remaining_sec, _ = _check_identity_rate_limit(
        db, identity_hash, "request", MAX_REQUEST_ATTEMPTS, now
    )
    if is_blocked:
        mins = max(1, (remaining_sec + 59) // 60)
        return (
            False,
            f"Too many verification requests. Please wait about {mins} minute(s) and try again.",
            429,
        )

    # Invalidate any previously active unconsumed challenge for this identity
    db.query(OTPChallenge).filter(
        OTPChallenge.identity_hash == identity_hash,
        OTPChallenge.consumed_at.is_(None),
    ).update({"consumed_at": now}, synchronize_session=False)

    # Generate cryptographically secure 6-digit OTP (zero-padded)
    otp_code = f"{secrets.randbelow(1_000_000):06d}"
    expires_at = now + timedelta(seconds=settings.OTP_TTL_SECONDS)

    challenge = OTPChallenge(
        identity_hash=identity_hash,
        code_hash=otp_code_hash(identity_hash, otp_code),
        expires_at=expires_at,
        consumed_at=None,
        failed_attempts=0,
        created_at=now,
    )
    db.add(challenge)
    db.add(AuthAttempt(identity_hash=identity_hash, kind="request", created_at=now))
    db.commit()

    # Print plaintext OTP ONLY in local development (never in production logs)
    if not settings.is_production:
        print("\n=======================================================")
        print(f"  [DEV OTP GENERATED] Email: {email_clean}")
        print(f"  [DEV OTP CODE]      {otp_code}")
        print("=======================================================\n")

    send_real_email(email_clean, otp_code)

    # Generic non-enumerating response (does not leak prior verification status)
    msg = "If this Superior University address is valid, a 6-digit verification code has been sent. Please check your inbox and Spam/Junk folder."
    return True, msg, 200


def verify_otp_service(db: Session, email: str, code: str) -> Tuple[bool, str, int, Optional[OTPChallenge]]:
    """
    Validates OTP against persistent hashed challenge using constant-time comparison.
    Returns (success, message, http_status_code, matched_challenge).
    Caller marks matched_challenge.consumed_at inside its commit transaction.
    """
    email_clean = normalize_email(email)
    code_clean = code.strip()
    now = utc_now()
    identity_hash = email_identity_hash(email_clean)

    is_blocked, remaining_sec, recent_fails = _check_identity_rate_limit(
        db, identity_hash, "verify_fail", MAX_VERIFY_ATTEMPTS, now
    )
    if is_blocked:
        mins = max(1, (remaining_sec + 59) // 60)
        return (
            False,
            f"Too many failed verification attempts. Locked out for about {mins} minute(s) for security.",
            429,
            None,
        )

    challenge = (
        db.query(OTPChallenge)
        .filter(
            OTPChallenge.identity_hash == identity_hash,
            OTPChallenge.consumed_at.is_(None),
        )
        .order_by(OTPChallenge.created_at.desc())
        .first()
    )

    if challenge is not None:
        if now > challenge.expires_at:
            challenge.consumed_at = now
            db.commit()
            return False, "Verification code expired. Please request a new code.", 400, None

        expected_hash = otp_code_hash(identity_hash, code_clean)
        if hmac.compare_digest(challenge.code_hash, expected_hash):
            # Clear prior failed attempts in window on success
            window_start = now - timedelta(seconds=LOCKOUT_WINDOW_SECONDS)
            db.query(AuthAttempt).filter(
                AuthAttempt.identity_hash == identity_hash,
                AuthAttempt.kind == "verify_fail",
                AuthAttempt.created_at >= window_start,
            ).delete(synchronize_session=False)
            return True, "Success", 200, challenge

        challenge.failed_attempts = (challenge.failed_attempts or 0) + 1

    # Record failed verification attempt persistently
    db.add(AuthAttempt(identity_hash=identity_hash, kind="verify_fail", created_at=now))
    db.commit()

    attempts_left = MAX_VERIFY_ATTEMPTS - (recent_fails + 1)
    if attempts_left > 0:
        return (
            False,
            f"Invalid verification code. ({attempts_left} attempt(s) remaining before 15-min lockout)",
            400,
            None,
        )
    return (
        False,
        "Invalid verification code. Maximum attempts reached. Locked out for 15 minutes.",
        429,
        None,
    )
