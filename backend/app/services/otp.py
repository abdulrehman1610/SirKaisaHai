import hashlib
import time
import random
from typing import Tuple, Dict
from app.config import settings

# In-memory store for OTPs: email -> (otp_code, timestamp_expiry)
otp_store: Dict[str, Tuple[str, float]] = {}

# Per-Email rate limiting & lockout trackers: email -> list of attempt timestamps
request_attempts: Dict[str, list] = {}
verify_attempts: Dict[str, list] = {}

LOCKOUT_WINDOW_SECONDS = 900  # 15 minutes
MAX_REQUEST_ATTEMPTS = 5      # 5 OTP requests / 15 min per email
MAX_VERIFY_ATTEMPTS = 5       # 5 Failed OTP code attempts / 15 min per email

def is_rate_limited(tracker: Dict[str, list], email: str, max_limit: int) -> Tuple[bool, int]:
    """Checks if email exceeded max_limit attempts in the last 15 minutes. Returns (is_blocked, remaining_seconds)."""
    now = time.time()
    attempts = tracker.get(email, [])
    # Filter attempts within the 15 min sliding window
    recent = [t for t in attempts if now - t < LOCKOUT_WINDOW_SECONDS]
    tracker[email] = recent

    if len(recent) >= max_limit:
        oldest = recent[0]
        remaining = int(LOCKOUT_WINDOW_SECONDS - (now - oldest))
        return True, max(remaining, 1)

    return False, 0

def record_attempt(tracker: Dict[str, list], email: str):
    """Records an attempt timestamp for this email"""
    tracker.setdefault(email, []).append(time.time())

def hash_email(email: str) -> str:
    cleaned = email.strip().lower()
    return hashlib.sha256(cleaned.encode("utf-8")).hexdigest()

from app.services.email_service import send_otp_email

def send_real_email(to_email: str, otp_code: str) -> bool:
    """Delegates to the branded SirKaisaHai HTML OTP email dispatcher"""
    return send_otp_email(to_email, otp_code)

def request_otp_service(email: str) -> Tuple[bool, str]:
    email_clean = email.strip().lower()
    if not email_clean.endswith("@superior.edu.pk"):
        return False, "Only Superior University student emails (@superior.edu.pk) are permitted."

    # 1. PER-EMAIL RATE LIMIT CHECK (5 requests / 15 min)
    is_blocked, remaining_sec = is_rate_limited(request_attempts, email_clean, MAX_REQUEST_ATTEMPTS)
    if is_blocked:
        mins = max(1, remaining_sec // 60)
        return False, f"Too many OTP requests for {email_clean}. Locked out for {mins} more minutes. Please try again later."

    # Record this OTP request attempt
    record_attempt(request_attempts, email_clean)

    # Generate real random 6-digit OTP code
    otp_code = str(random.randint(100000, 999999))
    expiry = time.time() + 600  # 10 minutes expiry

    otp_store[email_clean] = (otp_code, expiry)

    # Print to console for instant developer visibility
    print(f"\n=======================================================")
    print(f"  [OTP GENERATED] Email: {email_clean}")
    print(f"  [OTP CODE]      👉 {otp_code} 👈")
    print(f"=======================================================\n")

    # Try sending real email if SMTP configured
    email_sent = send_real_email(email_clean, otp_code)

    if email_sent:
        msg = f"OTP verification code sent to {email_clean}. Please check your inbox!"
    else:
        msg = f"OTP code generated for {email_clean}. Check terminal output or enter your code!"

    return True, msg

def verify_otp_service(email: str, code: str) -> Tuple[bool, str]:
    """Validates OTP with strict per-email brute-force protection and lockout."""
    email_clean = email.strip().lower()
    code_clean = code.strip()

    # 1. PER-EMAIL BRUTE-FORCE LOCKOUT CHECK (5 failed attempts / 15 min)
    is_blocked, remaining_sec = is_rate_limited(verify_attempts, email_clean, MAX_VERIFY_ATTEMPTS)
    if is_blocked:
        mins = max(1, remaining_sec // 60)
        return False, f"Too many failed verification attempts for this email. Locked out for {mins} more minutes for security."

    if email_clean in otp_store:
        stored_code, expiry = otp_store[email_clean]
        if time.time() > expiry:
            del otp_store[email_clean]  # Clean up expired OTP
            return False, "OTP code expired. Please request a new code."
        if stored_code == code_clean:
            # Successful verify: clear failed attempts for this email
            verify_attempts.pop(email_clean, None)
            return True, "Success"

    # Record failed attempt towards lockout threshold
    record_attempt(verify_attempts, email_clean)
    attempts_left = MAX_VERIFY_ATTEMPTS - len(verify_attempts.get(email_clean, []))
    if attempts_left > 0:
        return False, f"Invalid verification code. ({attempts_left} attempts remaining before 15-min lockout)"
    else:
        return False, "Invalid verification code. Maximum attempts reached. Account locked out for 15 minutes."

def consume_otp(email: str):
    """Remove OTP from store after successful DB commit. Safe to call even if already consumed."""
    email_clean = email.strip().lower()
    otp_store.pop(email_clean, None)

