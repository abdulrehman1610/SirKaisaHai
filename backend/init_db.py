import os
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config

# Ensure backend directory is on sys.path
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.config import settings
from app.seed import upsert_reference_data


def init_sql_database() -> None:
    print("=" * 60)
    print("  INITIALIZING SQL DATABASE (Alembic + Safe Upsert Seed)")
    print(f"  Environment: {settings.ENVIRONMENT}")
    print("=" * 60)

    alembic_cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(BACKEND_DIR / "migrations"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.clean_database_url)

    print("[1/2] Running Alembic migrations (upgrade head)...")
    command.upgrade(alembic_cfg, "head")
    print("  -> Migrations applied successfully.")

    print("[2/2] Upserting reference university & department data...")
    upsert_reference_data()
    print("  -> Reference data upserted cleanly (existing data preserved).")

    print("=" * 60)
    print("  SQL DATABASE SETUP IS COMPLETE & READY!")
    print("=" * 60)


if __name__ == "__main__":
    init_sql_database()
