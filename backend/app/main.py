from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.config import settings
from app.database import engine, Base, get_db
from app.limiter import limiter
from app.routers import auth, departments, professors, reviews
from app.seed import seed_database

# Create DB tables if they do not exist
Base.metadata.create_all(bind=engine)

# Auto migrate columns if missing in existing database
try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE professors ADD COLUMN created_by_user_id VARCHAR"))
        conn.commit()
except Exception:
    pass  # Column already exists or table freshly created

try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE verified_users ADD COLUMN session_token VARCHAR"))
        conn.commit()
except Exception:
    pass  # Column already exists or table freshly created

# Auto seed database with Superior Uni Teachers if empty
try:
    seed_database()
except Exception as e:
    print(f"[Seed Note] Seeding check: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.ENVIRONMENT != "production" else None,
    docs_url=f"{settings.API_V1_STR}/docs" if settings.ENVIRONMENT != "production" else None
)

# Attach slowapi rate limiter to app state
app.state.limiter = limiter

from fastapi.responses import JSONResponse
from fastapi import Request

@app.exception_handler(RateLimitExceeded)
def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Too many attempts. You have been temporarily locked out for 15 minutes for security. Please try again later.",
            "error": "rate_limit_exceeded"
        },
        headers={"Retry-After": "900"}
    )

# CORS middleware for frontend communication (restricted to allowed origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(departments.router, prefix=settings.API_V1_STR)
app.include_router(professors.router, prefix=settings.API_V1_STR)
app.include_router(reviews.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database health check failed: {str(e)}"
        )
