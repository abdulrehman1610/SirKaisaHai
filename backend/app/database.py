from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from app.config import settings

db_url = settings.clean_database_url
is_sqlite = db_url.startswith("sqlite")

if is_sqlite:
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        echo=False,
    )
else:
    # Use pool_recycle instead of per-request pool_pre_ping to avoid an extra
    # SELECT 1 round-trip to remote PostgreSQL on every single API call.
    engine = create_engine(
        db_url,
        pool_size=5,
        max_overflow=10,
        pool_recycle=180,
        pool_pre_ping=False,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_read_db(db: Session = Depends(get_db)):
    """
    Read-only session using AUTOCOMMIT on PostgreSQL so GET endpoints pay
    1 network round-trip (SELECT) instead of 3 (BEGIN + SELECT + ROLLBACK).
    Depends on get_db so test overrides of get_db continue to work automatically.
    """
    bind = db.get_bind()
    if bind.dialect.name == "postgresql":
        ro_db = Session(
            bind=bind.execution_options(isolation_level="AUTOCOMMIT"),
            autoflush=False,
            expire_on_commit=False,
        )
        try:
            yield ro_db
        finally:
            ro_db.close()
    else:
        yield db
