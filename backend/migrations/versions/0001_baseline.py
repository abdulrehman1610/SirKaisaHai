"""Baseline schema matching initial SirKaisaHai tables.

Revision ID: 0001_baseline
Revises: None
Create Date: 2026-11-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_baseline"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "universities",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), nullable=False),
        sa.Column("domain", sa.String(), nullable=False),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "verified_users",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("email_hash", sa.String(), nullable=False),
        sa.Column("session_token", sa.String(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("verified_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_verified_users_email_hash", "verified_users", ["email_hash"], unique=True)
    op.create_index("ix_verified_users_session_token", "verified_users", ["session_token"], unique=False)

    op.create_table(
        "departments",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("university_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["university_id"], ["universities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "professors",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("department_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.Column("tags_json", sa.String(), nullable=True),
        sa.Column("ai_summary", sa.Text(), nullable=True),
        sa.Column("created_by_user_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["verified_users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "reviews",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("professor_id", sa.String(), nullable=False),
        sa.Column("course_code", sa.String(), nullable=False),
        sa.Column("course_title", sa.String(), nullable=False),
        sa.Column("rating_teaching", sa.Float(), nullable=False),
        sa.Column("rating_grading", sa.Float(), nullable=False),
        sa.Column("rating_workload", sa.Float(), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("grade_received", sa.String(), nullable=True),
        sa.Column("semester_taken", sa.String(), nullable=False),
        sa.Column("helpful_count", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["professor_id"], ["professors.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "review_votes",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("review_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["review_id"], ["reviews.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["verified_users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "teacher_submission_logs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("professor_id", sa.String(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["verified_users.id"]),
        sa.ForeignKeyConstraint(["professor_id"], ["professors.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "teacher_creation_logs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("user_email", sa.String(), nullable=True),
        sa.Column("professor_id", sa.String(), nullable=False),
        sa.Column("teacher_name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["verified_users.id"]),
        sa.ForeignKeyConstraint(["professor_id"], ["professors.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("teacher_creation_logs")
    op.drop_table("teacher_submission_logs")
    op.drop_table("review_votes")
    op.drop_table("reviews")
    op.drop_table("professors")
    op.drop_table("departments")
    op.drop_index("ix_verified_users_session_token", table_name="verified_users")
    op.drop_index("ix_verified_users_email_hash", table_name="verified_users")
    op.drop_table("verified_users")
    op.drop_table("universities")
