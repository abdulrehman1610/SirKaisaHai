"""Add verified_users.hash_version & session_expires_at; drop teacher_creation_logs.user_email.

Revision ID: 0002_session_expiry_and_hash_version
Revises: 0001_baseline
Create Date: 2026-11-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_session_expiry_and_hash_version"
down_revision: Union[str, None] = "0001_baseline"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("verified_users") as batch_op:
        batch_op.add_column(
            sa.Column("hash_version", sa.SmallInteger(), nullable=False, server_default="1")
        )
        batch_op.add_column(sa.Column("session_expires_at", sa.DateTime(), nullable=True))

    # Wipe plaintext email data before dropping the column
    op.execute(sa.text("UPDATE teacher_creation_logs SET user_email = NULL"))
    with op.batch_alter_table("teacher_creation_logs") as batch_op:
        batch_op.drop_column("user_email")


def downgrade() -> None:
    with op.batch_alter_table("teacher_creation_logs") as batch_op:
        batch_op.add_column(sa.Column("user_email", sa.String(), nullable=True))

    with op.batch_alter_table("verified_users") as batch_op:
        batch_op.drop_column("session_expires_at")
        batch_op.drop_column("hash_version")
