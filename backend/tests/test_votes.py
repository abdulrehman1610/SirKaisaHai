from sqlalchemy import inspect

from app.models import Professor, Review
from app.services.identity import normalize_teacher_name
from tests.conftest import verify_student


def _seed_review(db_session):
    prof = Professor(
        id="prof-v",
        department_id="dept-cs",
        name="Dr. Vote Test",
        normalized_name=normalize_teacher_name("Dr. Vote Test"),
        title="Lecturer",
    )
    rev = Review(
        id="rev-v",
        professor_id="prof-v",
        course_code="CS-201",
        course_title="DSA",
        rating_teaching=4.5,
        rating_grading=4.5,
        rating_workload=3.0,
        overall_score=4.2,
        comment="Solid course structure and clear slides.",
        semester_taken="Fall 2025",
        helpful_count=0,
    )
    db_session.add_all([prof, rev])
    db_session.commit()
    return rev


def test_review_votes_table_has_no_user_id_column(db_engine):
    engine, _, _ = db_engine
    cols = {c["name"] for c in inspect(engine).get_columns("review_votes")}
    assert "user_id" not in cols
    assert "voter_key" in cols


def test_helpful_votes_require_auth_are_idempotent_and_toggleable(client, db_session):
    _seed_review(db_session)

    # Unauthenticated POST & DELETE -> 401
    assert client.post("/api/reviews/rev-v/vote").status_code == 401
    assert client.delete("/api/reviews/rev-v/vote").status_code == 401

    # Anonymous GET shows isHelpfulVoted=False
    anon_list = client.get("/api/reviews?professorId=prof-v").json()
    assert anon_list[0]["isHelpfulVoted"] is False
    assert anon_list[0]["helpfulCount"] == 0

    # Student 1 votes repeatedly -> idempotent, count increments by exactly 1
    verify_student(client, "voter1@superior.edu.pk", forwarded_for="203.0.113.10")
    for _ in range(5):
        r = client.post("/api/reviews/rev-v/vote")
        assert r.status_code == 200
        assert r.json() == {"success": True, "voted": True, "newCount": 1}

    # GET reflects isHelpfulVoted=True for Student 1
    s1_list = client.get("/api/reviews?professorId=prof-v").json()
    assert s1_list[0]["isHelpfulVoted"] is True
    assert s1_list[0]["helpfulCount"] == 1

    # Student 2 votes -> count becomes 2
    client.cookies.clear()
    verify_student(client, "voter2@superior.edu.pk", forwarded_for="203.0.113.11")
    r2 = client.post("/api/reviews/rev-v/vote")
    assert r2.status_code == 200
    assert r2.json() == {"success": True, "voted": True, "newCount": 2}

    # Student 2 unvotes -> count becomes 1; repeating DELETE stays 1 (idempotent)
    d1 = client.delete("/api/reviews/rev-v/vote")
    assert d1.status_code == 200
    assert d1.json() == {"success": True, "voted": False, "newCount": 1}

    d2 = client.delete("/api/reviews/rev-v/vote")
    assert d2.status_code == 200
    assert d2.json() == {"success": True, "voted": False, "newCount": 1}

    s2_list = client.get("/api/reviews?professorId=prof-v").json()
    assert s2_list[0]["isHelpfulVoted"] is False
