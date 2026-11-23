from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_read_db
from app.limiter import limiter
from app.routers import auth, departments, professors, reviews

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if not settings.is_production else None,
    docs_url=f"{settings.API_V1_STR}/docs" if not settings.is_production else None,
)

# Attach slowapi rate limiter to app state
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    path = request.url.path
    if "/auth/" in path:
        msg = "Too many verification attempts. You have been temporarily locked out for 15 minutes for security."
        retry_after = "900"
    elif "/professors" in path:
        msg = "Daily limit reached for adding new teachers (5 per day). Please try again tomorrow."
        retry_after = "86400"
    elif "/vote" in path:
        msg = "You are voting too quickly. Please wait a bit before trying again."
        retry_after = "3600"
    elif "/reviews" in path:
        msg = "Review submission limit reached (10 per hour). Please wait before submitting more reviews."
        retry_after = "3600"
    else:
        msg = "Too many requests. Please slow down and try again later."
        retry_after = "900"

    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "message": msg,
            "detail": msg,
            "error": "rate_limit_exceeded",
        },
        headers={"Retry-After": retry_after},
    )


# CORS middleware for frontend communication (restricted to configured origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
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
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
def health_check(db: Session = Depends(get_read_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "environment": settings.ENVIRONMENT,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database health check failed: {str(e)}",
        )
