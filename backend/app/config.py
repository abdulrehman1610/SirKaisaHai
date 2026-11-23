import json
import os
from typing import List, Literal, Optional, Union
from pydantic import model_validator
from pydantic_settings import BaseSettings

_DEV_EMAIL_HASH_SECRET = "dev-only-email-hash-secret-change-in-production"
_DEV_VOTE_SECRET = "dev-only-vote-secret-change-in-production"
_DEV_ADMIN_SECRET = "sirkaisahai-admin-dev-key"
_INSECURE_PLACEHOLDERS = {
    "",
    _DEV_EMAIL_HASH_SECRET,
    _DEV_VOTE_SECRET,
    _DEV_ADMIN_SECRET,
    "your_secure_random_salt_here",
    "change-me-to-at-least-32-random-bytes-in-production",
}


class Settings(BaseSettings):
    PROJECT_NAME: str = "SirKaisaHai Backend"
    ENVIRONMENT: str = "development"  # "development" or "production"
    API_V1_STR: str = "/api"

    # Legacy JWT settings (kept until PF-5 cleanup)
    SECRET_KEY: str = "sirkaisahai-super-secret-key-for-development-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # Cryptographic & Admin Secrets
    EMAIL_HASH_SECRET: str = _DEV_EMAIL_HASH_SECRET
    SECRET_SALT: Optional[str] = None  # Legacy env alias for EMAIL_HASH_SECRET
    VOTE_SECRET: str = _DEV_VOTE_SECRET
    ADMIN_SECRET_KEY: str = _DEV_ADMIN_SECRET

    # Database
    DATABASE_URL: str = "sqlite:///./sirkaisahai.db"

    # CORS (supports comma-separated string or JSON list in env)
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "https://sirkaisahai.vercel.app",
    ]

    # Cookie & Session policy
    COOKIE_SECURE: Optional[bool] = None
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"
    COOKIE_DOMAIN: Optional[str] = None
    SESSION_EXPIRE_END_OF_DAY: bool = True
    SESSION_TIMEZONE: str = "Asia/Karachi"
    SESSION_UTC_OFFSET_HOURS: int = 5
    SESSION_TTL_DAYS: int = 1
    OTP_TTL_SECONDS: int = 600

    # Rate limiting & Proxy trust
    RATELIMIT_STORAGE_URI: str = "memory://"
    TRUSTED_PROXY_IPS: str = "*"

    # SMTP / Real Email Settings
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_SENDER_EMAIL: str = "noreply@sirkaisahai.com"

    @model_validator(mode="after")
    def _normalize_and_validate(self) -> "Settings":
        # Legacy SECRET_SALT alias fallback for one release
        if (
            self.EMAIL_HASH_SECRET == _DEV_EMAIL_HASH_SECRET
            and self.SECRET_SALT
            and self.SECRET_SALT.strip()
        ):
            self.EMAIL_HASH_SECRET = self.SECRET_SALT.strip()

        # Normalize COOKIE_DOMAIN empty string -> None
        if self.COOKIE_DOMAIN is not None and not self.COOKIE_DOMAIN.strip():
            self.COOKIE_DOMAIN = None

        # Normalize CORS_ORIGINS into a clean list
        if isinstance(self.CORS_ORIGINS, str):
            raw = self.CORS_ORIGINS.strip()
            if raw.startswith("["):
                self.CORS_ORIGINS = [str(o).strip() for o in json.loads(raw) if str(o).strip()]
            else:
                self.CORS_ORIGINS = [o.strip() for o in raw.split(",") if o.strip()]

        if self.ENVIRONMENT.lower() == "production":
            errors: List[str] = []
            for name, val in [
                ("EMAIL_HASH_SECRET", self.EMAIL_HASH_SECRET),
                ("VOTE_SECRET", self.VOTE_SECRET),
                ("ADMIN_SECRET_KEY", self.ADMIN_SECRET_KEY),
            ]:
                if not val or val in _INSECURE_PLACEHOLDERS or len(val) < 32:
                    errors.append(f"{name} must be set to a random secret of at least 32 characters in production")

            if "*" in self.CORS_ORIGINS:
                errors.append("CORS_ORIGINS must not contain '*' when allow_credentials=True in production")

            if errors:
                raise ValueError("Invalid production configuration:\n- " + "\n- ".join(errors))

        return self

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @property
    def effective_cookie_secure(self) -> bool:
        if self.COOKIE_SECURE is not None:
            return self.COOKIE_SECURE
        return self.is_production

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def clean_database_url(self) -> str:
        # SQLAlchemy requires postgresql:// instead of legacy postgres:// (often supplied by Supabase/Render)
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
