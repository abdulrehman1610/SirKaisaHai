import hashlib
import hmac
import re
from datetime import datetime, time as dt_time, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.config import settings

_HONORIFIC_PATTERN = re.compile(
    r"^(?:(?:dr|prof|engr|sir|ma'am|maam|mr|mrs|ms|miss|doctor|professor)[\.\s]+)+",
    flags=re.IGNORECASE,
)


def normalize_email(email: str) -> str:
    return email.strip().lower()


def email_identity_hash(email: str, secret: Optional[str] = None) -> str:
    """Keyed HMAC-SHA256 identity hash for student emails."""
    key = (secret if secret is not None else settings.EMAIL_HASH_SECRET).encode("utf-8")
    msg = normalize_email(email).encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def legacy_email_hash(email: str) -> str:
    """Unsalted SHA-256 hash retained only for lazy migration of pre-HMAC users."""
    return hashlib.sha256(normalize_email(email).encode("utf-8")).hexdigest()


def otp_code_hash(identity_hash: str, code: str, secret: Optional[str] = None) -> str:
    """Keyed HMAC-SHA256 hash of a 6-digit OTP bound to an email identity hash."""
    key = (secret if secret is not None else settings.EMAIL_HASH_SECRET).encode("utf-8")
    msg = f"{identity_hash}:{code.strip()}".encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def compute_voter_key(user_id: str, review_id: str, secret: Optional[str] = None) -> str:
    """Unlinkable per-review HMAC voter key so DB cannot group a student's votes."""
    key = (secret if secret is not None else settings.VOTE_SECRET).encode("utf-8")
    msg = f"{user_id}:{review_id}".encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def mask_email(email: str) -> str:
    """Mask local-part of an email for safe display (e.g. bs***45@superior.edu.pk)."""
    cleaned = normalize_email(email)
    if "@" not in cleaned:
        return "***"
    local, domain = cleaned.split("@", 1)
    if len(local) <= 4:
        masked_local = local[0] + "***" if local else "***"
    else:
        masked_local = f"{local[:2]}***{local[-2:]}"
    return f"{masked_local}@{domain}"


def normalize_teacher_name(name: str) -> str:
    """Strip stacked honorific prefixes, lowercase, and collapse internal whitespace."""
    cleaned = re.sub(r"\s+", " ", name.strip()).lower()
    cleaned = _HONORIFIC_PATTERN.sub("", cleaned).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def _get_session_timezone():
    try:
        return ZoneInfo(settings.SESSION_TIMEZONE)
    except (ZoneInfoNotFoundError, KeyError):
        return timezone(timedelta(hours=settings.SESSION_UTC_OFFSET_HOURS))


def utc_now() -> datetime:
    """Timezone-naive UTC timestamp without calling deprecated datetime.utcnow()."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def compute_session_expiry(now_utc: Optional[datetime] = None) -> datetime:
    """
    Compute session expiration as naive UTC datetime.
    When SESSION_EXPIRE_END_OF_DAY is True (default), expires at midnight (00:00:00 next day)
    in SESSION_TIMEZONE (Asia/Karachi, UTC+5), so each session lasts only for that calendar day.
    """
    base_utc = now_utc or utc_now()
    if not settings.SESSION_EXPIRE_END_OF_DAY:
        return base_utc + timedelta(days=settings.SESSION_TTL_DAYS)

    tz = _get_session_timezone()
    aware_utc = base_utc.replace(tzinfo=timezone.utc)
    local_now = aware_utc.astimezone(tz)
    next_local_midnight = datetime.combine(
        local_now.date() + timedelta(days=1),
        dt_time(0, 0, 0),
        tzinfo=tz,
    )
    return next_local_midnight.astimezone(timezone.utc).replace(tzinfo=None)


def utc_day_floor(dt: Optional[datetime] = None) -> datetime:
    """Truncate a UTC datetime to day precision (00:00:00) to prevent timing correlation."""
    base = dt or utc_now()
    return base.replace(hour=0, minute=0, second=0, microsecond=0)
