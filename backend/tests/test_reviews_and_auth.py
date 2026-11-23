from datetime import timedelta

from app.limiter import limiter
from app.models import Professor, Review, TeacherSubmissionLog, VerifiedUser
from app.services.identity import normalize_teacher_name, utc_now
from tests.conftest import verify_student


def _seed_prof(db_session, pid="prof-1", name="Dr. Ali Khan", dept="dept-cs"):
    prof = Professor(
        id=pid,
        department_id=dept,
        name=name,
        normalized_name=normalize_teacher_name(name),
        title="Assistant Professor",
    )
    db_session.add(prof)
    db_session.commit()
    return prof


def test_unauthenticated_and_user_email_spoofed_reviews_rejected(client, db_session):
    _seed_prof(db_session)

    # T1: No cookie -> 401
    r1 = client.post(
        "/api/reviews",
        json={
            "professorId": "prof-1",
            "ratingTeaching": 4.5,
            "ratingGrading": 4.0,
            "ratingWorkload": 3.0,
            "comment": "Trying to post without authenticating.",
        },
    )
    assert r1.status_code == 401
    assert db_session.query(Review).count() == 0
    assert db_session.query(TeacherSubmissionLog).count() == 0

    # Even if a verified user exists, passing userEmail without cookie -> 401
    verify_student(client, "victim@superior.edu.pk")
    client.cookies.clear()
    r2 = client.post(
        "/api/reviews",
        json={
            "professorId": "prof-1",
            "ratingTeaching": 2.0,
            "ratingGrading": 2.0,
            "ratingWorkload": 5.0,
            "comment": "Impersonation attempt using userEmail field.",
            "userEmail": "victim@superior.edu.pk",
        },
    )
    assert r2.status_code == 401
    assert db_session.query(Review).count() == 0


def test_review_submission_dedup_timing_and_logout_expiry(client, db_session):
    _seed_prof(db_session)
    verify_student(client, "student1@superior.edu.pk")

    # T3: Valid first review -> 200
    r1 = client.post(
        "/api/reviews",
        json={
            "professorId": "prof-1",
            "ratingTeaching": 5.0,
            "ratingGrading": 4.0,
            "ratingWorkload": 2.0,
            "comment": "Clear lectures, fair exams, manageable workload.",
        },
    )
    assert r1.status_code == 200
    body = r1.json()
    # Minute precision check (seconds == 00)
    assert body["createdAt"].endswith(":00")
    assert db_session.query(Review).count() == 1

    # Day precision check on teacher_submission_logs.submitted_at
    log = db_session.query(TeacherSubmissionLog).first()
    assert log is not None
    assert (log.submitted_at.hour, log.submitted_at.minute, log.submitted_at.second) == (0, 0, 0)

    # T4: Duplicate review same professor -> 409 Conflict, review count stays 1
    r2 = client.post(
        "/api/reviews",
        json={
            "professorId": "prof-1",
            "ratingTeaching": 3.0,
            "ratingGrading": 3.0,
            "ratingWorkload": 3.0,
            "comment": "Second attempt for the same teacher.",
        },
    )
    assert r2.status_code == 409
    assert db_session.query(Review).count() == 1

    # Expired session rejected and token cleared
    user = db_session.query(VerifiedUser).first()
    old_token = user.session_token
    user.session_expires_at = utc_now() - timedelta(minutes=1)
    db_session.commit()

    me_exp = client.get("/api/auth/me")
    assert me_exp.json()["authenticated"] is False
    db_session.expire_all()
    assert db_session.query(VerifiedUser).filter(VerifiedUser.id == user.id).first().session_token is None

    # Re-verify, then logout immediately finishes the session (even if old cookie is replayed)
    new_token = verify_student(client, "student1@superior.edu.pk")
    assert new_token != old_token
    out = client.post("/api/auth/logout")
    assert out.status_code == 200
    assert client.get("/api/auth/me").json()["authenticated"] is False

    # Replay the logged-out cookie manually -> rejected with 401
    client.cookies.set("skh_session", new_token)
    r_replay = client.post(
        "/api/reviews",
        json={
            "professorId": "prof-1",
            "ratingTeaching": 4.0,
            "ratingGrading": 4.0,
            "ratingWorkload": 3.0,
            "comment": "Replaying cookie after logout should fail.",
        },
    )
    assert r_replay.status_code == 401


def test_duplicate_professor_409_and_write_rate_limits(client, db_session):
    verify_student(client, "creator@superior.edu.pk")

    p1 = client.post(
        "/api/professors",
        json={"name": "Dr. Ali Khan", "departmentId": "dept-cs", "title": "Professor"},
    )
    assert p1.status_code == 200

    # Normalized duplicate across departments -> 409 with existing id & department
    p_dup = client.post(
        "/api/professors",
        json={"name": "  Prof.  Ali   Khan ", "departmentId": "dept-se", "title": "Lecturer"},
    )
    assert p_dup.status_code == 409
    assert p1.json()["id"] in p_dup.json()["detail"]

    # Reset limiter to cleanly verify exact 5/day professor creation quota
    limiter.reset()
    for idx in range(1, 6):
        r = client.post(
            "/api/professors",
            json={"name": f"Teacher Number {idx}", "departmentId": "dept-cs"},
        )
        assert r.status_code == 200
    r_lim = client.post(
        "/api/professors",
        json={"name": "Teacher Number 6", "departmentId": "dept-cs"},
    )
    assert r_lim.status_code == 429
    assert "5 per day" in r_lim.json()["detail"]

    # Review hourly limit: 10/hour -> 11th returns 429 with review-specific message
    limiter.reset()
    for idx in range(11):
        pid = f"prof-rate-{idx}"
        _seed_prof(db_session, pid=pid, name=f"Rate Prof {idx}")
        resp = client.post(
            "/api/reviews",
            json={
                "professorId": pid,
                "ratingTeaching": 4.0,
                "ratingGrading": 4.0,
                "ratingWorkload": 3.0,
                "comment": f"Constructive review number {idx} for rate limit check.",
            },
        )
        if idx < 10:
            assert resp.status_code == 200
        else:
            assert resp.status_code == 429
            assert "10 per hour" in resp.json()["detail"]
