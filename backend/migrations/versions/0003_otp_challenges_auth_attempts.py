"""Add persistent otp_challenges and auth_attempts tables.

Revision ID: 0003_otp_challenges_auth_attempts
Revises: 0002_session_expiry_and_hash_version
Create Date: 2026-11-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_otp_and_auth_attempts"
down_revision: Union[str, None] = "0002_session_and_hash_ver"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "otp_challenges",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("identity_hash", sa.String(length=64), nullable=False),
        sa.Column("code_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("consumed_at", sa.DateTime(), nullable=True),
        sa.Column("failed_attempts", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_otp_challenges_identity_hash", "otp_challenges", ["identity_hash"], unique=False)
    op.create_index("ix_otp_challenges_expires_at", "otp_challenges", ["expires_at"], unique=False)

    op.create_table(
        "auth_attempts",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("identity_hash", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_auth_attempts_identity_hash", "auth_attempts", ["identity_hash"], unique=False)
    op.create_index("ix_auth_attempts_created_at", "auth_attempts", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_auth_attempts_created_at", table_name="auth_attempts")
    op.drop_index("ix_auth_attempts_identity_hash", table_name="auth_attempts")
    op.drop_table("auth_attempts")

    op.drop_index("ix_otp_challenges_expires_at", table_name="otp_challenges")
    op.drop_index("ix_otp_challenges_identity_hash", table_name="otp_challenges")
    op.drop_table("otp_challenges")
