from datetime import timedelta
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app
from app.models import OTPChallenge
from app.services.identity import utc_now


def test_otp_persists_across_client_instances_and_never_stores_plaintext(client, db_session):
    email = "bscs-f23-010@superior.edu.pk"
    r1 = client.post("/api/auth/request-otp", json={"email": email})
    assert r1.status_code == 200
    code = client.captured_otps[email]
    assert len(code) == 6 and code.isdigit()

    # Verify DB stores only hashed code and identity_hash (never plaintext email or code)
    ch = db_session.query(OTPChallenge).first()
    assert ch is not None
    assert ch.code_hash != code
    assert email not in ch.identity_hash
    assert code not in ch.code_hash

    # Simulate a second worker / fresh client instance verifying the same persisted challenge
    with TestClient(app) as worker2:
        r2 = worker2.post("/api/auth/verify-otp", json={"email": email, "code": code})
        assert r2.status_code == 200
        assert r2.json()["success"] is True

        # Replaying the burned OTP must fail
        r3 = worker2.post("/api/auth/verify-otp", json={"email": email, "code": code})
        assert r3.status_code == 400


def test_new_otp_invalidates_previous_and_expired_otp_fails(client, db_session):
    email = "bsai-f23-022@superior.edu.pk"
    client.post("/api/auth/request-otp", json={"email": email})
    first_code = client.captured_otps[email]

    client.post("/api/auth/request-otp", json={"email": email})
    second_code = client.captured_otps[email]

    if first_code != second_code:
        r_old = client.post("/api/auth/verify-otp", json={"email": email, "code": first_code})
        assert r_old.status_code == 400

    # Force expiration of active challenge
    active = (
        db_session.query(OTPChallenge)
        .filter(OTPChallenge.consumed_at.is_(None))
        .first()
    )
    assert active is not None
    active.expires_at = utc_now() - timedelta(seconds=5)
    db_session.commit()

    r_exp = client.post("/api/auth/verify-otp", json={"email": email, "code": second_code})
    assert r_exp.status_code == 400
    assert "expired" in r_exp.json()["message"].lower()


def test_per_email_and_per_ip_rate_limits_behind_proxy(client):
    # 5 OTP requests from different IPs for the SAME email -> 6th hits per-email 429
    email = "bsds-f23-001@superior.edu.pk"
    for i in range(5):
        r = client.post(
            "/api/auth/request-otp",
            json={"email": email},
            headers={"X-Forwarded-For": f"203.0.113.{i + 1}"},
        )
        assert r.status_code == 200

    r6 = client.post(
        "/api/auth/request-otp",
        json={"email": email},
        headers={"X-Forwarded-For": "203.0.113.99"},
    )
    assert r6.status_code == 429

    # Different email on a different X-Forwarded-For IP still succeeds (independent IP bucket)
    r_other = client.post(
        "/api/auth/request-otp",
        json={"email": "bsds-f23-002@superior.edu.pk"},
        headers={"X-Forwarded-For": "198.51.100.77"},
    )
    assert r_other.status_code == 200


def test_production_mode_does_not_print_otp_or_email(client, monkeypatch, capsys):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    email = "bsit-f23-055@superior.edu.pk"
    r = client.post(
        "/api/auth/request-otp",
        json={"email": email},
        headers={"X-Forwarded-For": "198.51.100.88"},
    )
    assert r.status_code == 200
    code = client.captured_otps[email]
    captured = capsys.readouterr()
    assert code not in captured.out
    assert email not in captured.out
