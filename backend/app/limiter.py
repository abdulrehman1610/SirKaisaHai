import hashlib
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

COOKIE_NAME = "skh_session"


def _is_trusted_proxy(remote_host: str) -> bool:
    trusted = settings.TRUSTED_PROXY_IPS.strip()
    if not trusted:
        return False
    if trusted == "*":
        return True
    allowed = {ip.strip() for ip in trusted.split(",") if ip.strip()}
    return remote_host in allowed


def get_client_ip(request: Request) -> str:
    """Resolve real client IP from X-Forwarded-For when behind a trusted proxy."""
    direct_ip = request.client.host if request.client and request.client.host else get_remote_address(request)
    if _is_trusted_proxy(direct_ip):
        xff = request.headers.get("x-forwarded-for")
        if xff:
            first_ip = xff.split(",")[0].strip()
            if first_ip:
                return first_ip
    return direct_ip or "127.0.0.1"


def user_or_ip_key(request: Request) -> str:
    """Key write rate limits by hashed session token when logged in, falling back to client IP."""
    token = request.cookies.get(COOKIE_NAME)
    if token and token.startswith("skh-session-"):
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()[:16]
        return f"tok:{digest}"
    return f"ip:{get_client_ip(request)}"


limiter = Limiter(
    key_func=get_client_ip,
    storage_uri=settings.RATELIMIT_STORAGE_URI,
)
