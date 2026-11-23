import os
import sys
from pathlib import Path
from typing import Dict

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("EMAIL_HASH_SECRET", "test-email-hash-secret-0123456789abcdef0123456789abcdef")
os.environ.setdefault("VOTE_SECRET", "test-vote-secret-0123456789abcdef0123456789abcdef")
os.environ.setdefault("ADMIN_SECRET_KEY", "test-admin-secret-0123456789abcdef0123456789abcdef")
os.environ.setdefault("RATELIMIT_STORAGE_URI", "memory://")

from app.database import get_db
from app.limiter import limiter
from app.main import app
from app.seed import upsert_reference_data
from app.services import otp as otp_service


def make_alembic_config(db_url: str) -> Config:
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "migrations"))
    cfg.set_main_option("sqlalchemy.url", db_url)
    return cfg


@pytest.fixture()
def db_engine(tmp_path):
    db_file = tmp_path / "test_sirkaisahai.db"
    db_url = f"sqlite:///{db_file.as_posix()}"
    cfg = make_alembic_config(db_url)
    command.upgrade(cfg, "head")

    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionTesting()
    try:
        upsert_reference_data(db=db)
    finally:
        db.close()

    yield engine, SessionTesting, db_url
    engine.dispose()


@pytest.fixture()
def db_session(db_engine):
    _, SessionTesting, _ = db_engine
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_engine, monkeypatch):
    _, SessionTesting, _ = db_engine

    def override_get_db():
        db = SessionTesting()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    limiter.reset()

    captured_otps: Dict[str, str] = {}

    def fake_send_email(to_email: str, otp_code: str) -> bool:
        captured_otps[to_email.strip().lower()] = otp_code
        return True

    monkeypatch.setattr(otp_service, "send_real_email", fake_send_email)

    with TestClient(app) as tc:
        tc.captured_otps = captured_otps  # type: ignore[attr-defined]
        yield tc

    app.dependency_overrides.clear()
    limiter.reset()


def verify_student(client: TestClient, email: str, forwarded_for: str = "198.51.100.10") -> str:
    headers = {"X-Forwarded-For": forwarded_for}
    r1 = client.post("/api/auth/request-otp", json={"email": email}, headers=headers)
    assert r1.status_code == 200, r1.text
    code = client.captured_otps[email.strip().lower()]  # type: ignore[attr-defined]
    r2 = client.post("/api/auth/verify-otp", json={"email": email, "code": code}, headers=headers)
    assert r2.status_code == 200, r2.text
    assert r2.json()["success"] is True
    cookie = r2.cookies.get("skh_session")
    assert cookie and cookie.startswith("skh-session-")
    return cookie
