from datetime import datetime, timedelta
import pytest
from sqlalchemy import inspect

from app.config import Settings
from app.models import Professor, TeacherSubmissionLog, VerifiedUser
from app.services.identity import (
    compute_session_expiry,
    email_identity_hash,
    legacy_email_hash,
    normalize_teacher_name,
)
from tests.conftest import verify_student


def test_production_settings_reject_weak_or_default_secrets_and_wildcard_cors():
    with pytest.raises(ValueError, match="EMAIL_HASH_SECRET"):
        Settings(
            _env_file=None,
            ENVIRONMENT="production",
            EMAIL_HASH_SECRET="short",
            VOTE_SECRET="v" * 40,
            ADMIN_SECRET_KEY="a" * 40,
            CORS_ORIGINS="https://sirkaisahai.vercel.app",
        )

    with pytest.raises(ValueError, match="CORS_ORIGINS"):
        Settings(
            _env_file=None,
            ENVIRONMENT="production",
            EMAIL_HASH_SECRET="e" * 40,
            VOTE_SECRET="v" * 40,
            ADMIN_SECRET_KEY="a" * 40,
            CORS_ORIGINS="https://sirkaisahai.vercel.app,*",
        )

    ok = Settings(
        _env_file=None,
        ENVIRONMENT="production",
        EMAIL_HASH_SECRET="e" * 40,
        VOTE_SECRET="v" * 40,
        ADMIN_SECRET_KEY="a" * 40,
        CORS_ORIGINS="https://sirkaisahai.vercel.app,https://example.com",
    )
    assert ok.effective_cookie_secure is True
    assert ok.cors_origins_list == ["https://sirkaisahai.vercel.app", "https://example.com"]


def test_hmac_differs_from_legacy_and_lazy_migrates_preserving_user_id(client, db_session):
    email = "bsse-f22-099@superior.edu.pk"
    assert email_identity_hash(email) != legacy_email_hash(email)

    # Seed a legacy v1 user with an existing submission log
    legacy_user = VerifiedUser(
        id="legacy-user-1",
        email_hash=legacy_email_hash(email),
        hash_version=1,
    )
    prof = Professor(
        id="prof-legacy",
        department_id="dept-cs",
        name="Dr. Legacy Prof",
        normalized_name=normalize_teacher_name("Dr. Legacy Prof"),
        title="Professor",
    )
    db_session.add_all([legacy_user, prof])
    db_session.flush()
    db_session.add(TeacherSubmissionLog(user_id="legacy-user-1", professor_id="prof-legacy"))
    db_session.commit()

    # Verify via OTP -> upgrades hash in place without changing user.id
    verify_student(client, email)

    db_session.expire_all()
    migrated = db_session.query(VerifiedUser).filter(VerifiedUser.id == "legacy-user-1").first()
    assert migrated is not None
    assert migrated.email_hash == email_identity_hash(email)
    assert migrated.hash_version == 2
    assert db_session.query(VerifiedUser).count() == 1

    # Duplicate review is still blocked because user.id was preserved!
    resp = client.post(
        "/api/reviews",
        json={
            "professorId": "prof-legacy",
            "ratingTeaching": 4.0,
            "ratingGrading": 4.0,
            "ratingWorkload": 3.0,
            "comment": "Trying to review a second time after migration.",
        },
    )
    assert resp.status_code == 409


def test_teacher_creation_logs_has_no_user_email_column(db_engine):
    engine, _, _ = db_engine
    cols = {c["name"] for c in inspect(engine).get_columns("teacher_creation_logs")}
    assert "user_email" not in cols
    assert "user_id" in cols


def test_end_of_day_session_expiry_calculation():
    # 2026-11-23 10:00 UTC == 2026-11-23 15:00 PKT (UTC+5)
    # End of day PKT is 2026-11-24 00:00 PKT == 2026-11-23 19:00 UTC
    now_utc = datetime(2026, 11, 23, 10, 0, 0)
    exp = compute_session_expiry(now_utc)
    assert exp == datetime(2026, 11, 23, 19, 0, 0)

    # Just after PKT midnight: 2026-11-23 19:05 UTC == 2026-11-24 00:05 PKT
    # Should expire at 2026-11-25 00:00 PKT == 2026-11-24 19:00 UTC
    early_morning_pkt_in_utc = datetime(2026, 11, 23, 19, 5, 0)
    exp2 = compute_session_expiry(early_morning_pkt_in_utc)
    assert exp2 == datetime(2026, 11, 24, 19, 0, 0)
    assert exp2 > early_morning_pkt_in_utc
    assert (exp2 - early_morning_pkt_in_utc) < timedelta(hours=24)
