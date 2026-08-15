import os
from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "SirKaisaHai Backend"
    ENVIRONMENT: str = "development"  # "development" or "production"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "sirkaisahai-super-secret-key-for-development-only"
    ADMIN_SECRET_KEY: str = "sirkaisahai-admin-dev-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    DATABASE_URL: str = "sqlite:///./sirkaisahai.db"
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "https://sirkaisahai.vercel.app"
    ]
    
    # SMTP / Real Email Settings
    SMTP_SERVER: str = ""  # e.g., smtp.resend.com or smtp.gmail.com
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_SENDER_EMAIL: str = "noreply@sirkaisahai.com"

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
