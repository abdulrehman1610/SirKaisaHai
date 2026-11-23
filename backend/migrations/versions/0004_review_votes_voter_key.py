"""Replace review_votes.user_id with unlinkable voter_key and unique constraint.

Revision ID: 0004_review_votes_voter_key
Revises: 0003_otp_challenges_auth_attempts
Create Date: 2026-11-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_review_votes_voter_key"
down_revision: Union[str, None] = "0003_otp_and_auth_attempts"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Clear legacy rows (if any) before replacing user_id with unlinkable HMAC voter_key
    op.execute(sa.text("DELETE FROM review_votes"))
    with op.batch_alter_table("review_votes") as batch_op:
        batch_op.drop_column("user_id")
        batch_op.add_column(sa.Column("voter_key", sa.String(length=64), nullable=False))
        batch_op.create_index("ix_review_votes_review_id", ["review_id"], unique=False)
        batch_op.create_unique_constraint("uq_review_votes_review_voter", ["review_id", "voter_key"])


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM review_votes"))
    with op.batch_alter_table("review_votes") as batch_op:
        batch_op.drop_constraint("uq_review_votes_review_voter", type_="unique")
        batch_op.drop_index("ix_review_votes_review_id")
        batch_op.drop_column("voter_key")
        batch_op.add_column(sa.Column("user_id", sa.String(), nullable=False))
        batch_op.create_foreign_key("fk_review_votes_user_id", "verified_users", ["user_id"], ["id"])
