"""Add DB-level unique constraints, normalized professor name, and hot query indexes.

Revision ID: 0005_constraints_and_indexes
Revises: 0004_review_votes_voter_key
Create Date: 2026-11-23
"""
from typing import Dict, List, Sequence, Tuple, Union

from alembic import op
import sqlalchemy as sa

from app.services.identity import normalize_teacher_name

revision: str = "0005_constraints_and_indexes"
down_revision: Union[str, None] = "0004_review_votes_voter_key"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("professors") as batch_op:
        batch_op.add_column(sa.Column("normalized_name", sa.String(), nullable=True))

    # Backfill normalized_name and fail clearly if existing duplicates collide
    bind = op.get_bind()
    rows = bind.execute(sa.text("SELECT id, name FROM professors")).fetchall()
    seen: Dict[str, List[Tuple[str, str]]] = {}
    for prof_id, prof_name in rows:
        norm = normalize_teacher_name(prof_name or "")
        seen.setdefault(norm, []).append((prof_id, prof_name))

    collisions = {norm: items for norm, items in seen.items() if len(items) > 1}
    if collisions:
        details = "; ".join(f"'{k}': {v}" for k, v in collisions.items())
        raise RuntimeError(
            f"Cannot enforce UNIQUE(professors.normalized_name); resolve duplicate teachers first: {details}"
        )

    for prof_id, prof_name in rows:
        norm = normalize_teacher_name(prof_name or "")
        bind.execute(
            sa.text("UPDATE professors SET normalized_name = :norm WHERE id = :pid"),
            {"norm": norm, "pid": prof_id},
        )

    with op.batch_alter_table("professors") as batch_op:
        batch_op.alter_column("normalized_name", existing_type=sa.String(), nullable=False)
        batch_op.create_index("ix_professors_normalized_name", ["normalized_name"], unique=True)
        batch_op.create_index("ix_professors_department_id", ["department_id"], unique=False)

    with op.batch_alter_table("teacher_submission_logs") as batch_op:
        batch_op.create_index("ix_teacher_submission_logs_user_id", ["user_id"], unique=False)
        batch_op.create_unique_constraint("uq_submission_user_prof", ["user_id", "professor_id"])

    op.create_index("ix_reviews_prof_created", "reviews", ["professor_id", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_reviews_prof_created", table_name="reviews")

    with op.batch_alter_table("teacher_submission_logs") as batch_op:
        batch_op.drop_constraint("uq_submission_user_prof", type_="unique")
        batch_op.drop_index("ix_teacher_submission_logs_user_id")

    with op.batch_alter_table("professors") as batch_op:
        batch_op.drop_index("ix_professors_department_id")
        batch_op.drop_index("ix_professors_normalized_name")
        batch_op.drop_column("normalized_name")
