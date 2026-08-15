# SirKaisaHai — Production Readiness & Deployment Guide
### Complete step-by-step roadmap to transition from local development to production

---

## Overview

This guide outlines every technical step, security check, and hosting configuration required to take **SirKaisaHai** live for students at Superior University (and beyond) with zero downtime, robust security, and 100% adherence to free/low-cost tier hosting.

---

## Summary Checklist

- [ ] **1. Security Hardening:** Restrict CORS, disable wipe endpoints, generate 256-bit secrets, add rate limiting.
- [ ] **2. Database Migration:** Replace SQLite with managed PostgreSQL (Supabase/Neon/Railway).
- [ ] **3. Email Delivery:** Configure transactional SMTP (Resend/Brevo/Gmail) & persist OTP state.
- [ ] **4. Backend Deployment:** Dockerize FastAPI and deploy to Railway / Render / Fly.io.
- [ ] **5. Frontend Deployment:** Build Vue 3 bundle and deploy to Vercel / Netlify with SPA rewrites.
- [ ] **6. Domain & SSL:** Hook up custom domain and enable automatic HTTPS.
- [ ] **7. Monitoring & Backups:** Add `/health` checks, automated uptime alerts, and daily DB snapshots.

---

## Phase 1: Security Hardening & Code Cleanup

### 1.1 Disable / Protect Test Wipe Endpoints
In [backend/app/routers/auth.py](file:///d:/Experiments%20with%20AI/sirkaisahai/backend/app/routers/auth.py), the `/reset-test-users` endpoint is currently public. In production, an attacker could wipe all student verification records.

**Action:** Guard the endpoint with an admin key or disable it when `ENVIRONMENT=production`:
```python
from app.config import settings

@router.post("/reset-test-users")
def reset_test_users(
    admin_key: Optional[str] = Header(default=None),
    db: Session = Depends(get_db)
):
    if settings.ENVIRONMENT == "production":
        if not admin_key or admin_key != settings.ADMIN_SECRET_KEY:
            raise HTTPException(status_code=403, detail="Unauthorized in production.")
    
    db.query(VerifiedUser).delete()
    db.query(TeacherCreationLog).delete()
    db.query(TeacherSubmissionLog).delete()
    db.query(ReviewVote).delete()
    db.commit()
    return {"success": True, "message": "All test users and logs cleared successfully!"}
```

### 1.2 Restrict CORS Origins
In [backend/app/main.py](file:///d:/Experiments%20with%20AI/sirkaisahai/backend/app/main.py), change wildcard `allow_origins=["*"]` to read strictly from settings:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # E.g. ["https://sirkaisahai.vercel.app", "https://sirkaisahai.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
```

### 1.3 Generate Cryptographically Secure Secret Keys
Never use the default development string. Generate a 32-byte secret:
```bash
# In your terminal
python -c "import secrets; print(secrets.token_hex(32))"
```
Place this value in your production environment as `SECRET_KEY`.

### 1.4 Rate Limiting on OTP and Review Submissions
Install `slowapi` to prevent malicious email bombing or review flooding:
```bash
pip install slowapi
```
Add limits (e.g., max 3 OTP requests/hour per email, max 5 reviews/hour per IP).

---

## Phase 2: PostgreSQL Database Migration

SQLite is not suitable for production because:
1. Ephemeral containers on platforms like Railway/Render wipe local `.db` files upon redeployment.
2. Concurrent writes lock the file and cause 500 errors during traffic spikes.

### 2.1 Set Up Managed PostgreSQL (Free Tier)
Choose one of the following free-tier managed databases:
* **Supabase:** 500 MB free PostgreSQL + automatic daily backups ([supabase.com](https://supabase.com))
* **Neon.tech:** Serverless PostgreSQL with generous free tier ([neon.tech](https://neon.tech))
* **Railway PostgreSQL:** 1-click plugin included in free/hobby plans ([railway.app](https://railway.app))

### 2.2 Update Backend Dependencies
Add PostgreSQL drivers to [backend/requirements.txt](file:///d:/Experiments%20with%20AI/sirkaisahai/backend/requirements.txt):
```txt
psycopg2-binary>=2.9.9
asyncpg>=0.29.0
```

### 2.3 Configure Database URL
In your production `.env` (or cloud dashboard):
```ini
DATABASE_URL="postgresql://username:password@db.xxxx.supabase.co:5432/postgres"
```

In [backend/app/database.py](file:///d:/Experiments%20with%20AI/sirkaisahai/backend/app/database.py), handle SQLite vs Postgres connection args cleanly:
```python
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)
```

---

## Phase 3: Transactional Email & OTP Delivery

### 3.1 Choose an SMTP / Email Provider
* **Resend** (Recommended): 3,000 emails/month free ([resend.com](https://resend.com)). Super fast and 100% inbox delivery rate.
* **Brevo (Sendinblue):** 300 emails/day free.
* **Gmail SMTP:** Free for testing/small batches (requires Gmail 2FA "App Password").

### 3.2 Production `.env` for SMTP
```ini
SMTP_SERVER="smtp.resend.com"
SMTP_PORT=587
SMTP_USER="resend"
SMTP_PASSWORD="re_your_api_key_here"
SMTP_SENDER_EMAIL="verify@yourdomain.com"
```

### 3.3 Persist OTP State in Database
Currently, `otp_store` is an in-memory Python dictionary. If the backend scales to 2+ worker processes or restarts, pending OTP codes are lost.
* **Fix:** Store OTP codes either in a short-lived `otp_verifications` database table with a `expires_at` column, or sign the OTP into a temporary JWT sent to the client.

---

## Phase 4: Dockerization & Backend Deployment

### 4.1 Create `Dockerfile` in `backend/`
Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install build dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4.2 Create `backend/.dockerignore`
```dockerignore
__pycache__
*.pyc
*.pyo
*.db
.env
.venv
```

### 4.3 Deploy Backend to Railway / Render

#### Option A: Railway (Fastest)
1. Push your code to GitHub.
2. Log into [railway.app](https://railway.app) and create a **New Project from GitHub Repo**.
3. Set the Root Directory to `/backend`.
4. Add a **PostgreSQL** database service from Railway's menu.
5. Under **Variables**, add:
   * `PROJECT_NAME="SirKaisaHai"`
   * `DATABASE_URL=${{Postgres.DATABASE_URL}}`
   * `SECRET_KEY=your_generated_secret_key`
   * `CORS_ORIGINS=["https://sirkaisahai.vercel.app", "http://localhost:5173"]`
   * `SMTP_SERVER=smtp.resend.com`
   * `SMTP_PORT=587`
   * `SMTP_USER=resend`
   * `SMTP_PASSWORD=re_xxxxxx`
   * `SMTP_SENDER_EMAIL=verify@sirkaisahai.com`
6. Railway will automatically build and assign a live URL: `https://backend-production-xxxx.up.railway.app`.

---

## Phase 5: Frontend Build & SPA Deployment

### 5.1 Configure Production API Base URL
In `sirkaisahai_first/`, create `.env.production`:
```ini
VITE_API_BASE_URL="https://backend-production-xxxx.up.railway.app/api"
```

### 5.2 Configure SPA Rewrites (Prevent 404 on Refresh)
When using Vue Router HTML5 History mode, direct refreshes on `/professor/prof-1` or `/search` will 404 unless rewrites redirect all requests to `index.html`.

Create `sirkaisahai_first/vercel.json`:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### 5.3 Deploy Frontend to Vercel (100% Free)
1. Go to [vercel.com](https://vercel.com) and click **Add New Project**.
2. Select your GitHub repository.
3. Set the **Root Directory** to `sirkaisahai_first`.
4. Framework Preset will auto-detect **Vite**.
5. Under **Environment Variables**, set:
   * `VITE_API_BASE_URL` = `https://backend-production-xxxx.up.railway.app/api`
6. Click **Deploy**. Vercel will build and assign `https://sirkaisahai.vercel.app`.

---

## Phase 6: Production Smoke Test Flow

Run through this full checklist on your live URL to verify everything works:

```mermaid
flowchart TD
    Step1[1. Open live Vercel URL] --> Step2[2. Verify page loads & initial teachers render from Postgres]
    Step2 --> Step3[3. Click Verify Email & enter @superior.edu.pk email]
    Step3 --> Step4[4. Check inbox for 6-digit OTP]
    Step4 --> Step5[5. Enter OTP & confirm token received and badge shows Verified Student]
    Step5 --> Step6[6. Go to a Teacher & submit a review]
    Step6 --> Step7[7. Verify review immediately appears & averages recalculate]
    Step7 --> Step8[8. Click Helpful upvote & verify counter increments]
    Step8 --> Step9[9. Try posting a 2nd review for the same teacher -> Expect friendly rejection]
```

---

## Phase 7: Monitoring, Health Checks & Maintenance

### 7.1 Add a Health Check Endpoint
In [backend/app/main.py](file:///d:/Experiments%20with%20AI/sirkaisahai/backend/app/main.py):
```python
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unhealthy: {e}")
```

### 7.2 Set Up Free Uptime Monitoring
* Create an account at **UptimeRobot** ([uptimerobot.com](https://uptimerobot.com)) or **BetterStack** ([betterstack.com](https://betterstack.com)).
* Add a 5-minute HTTP monitor pointing to `https://backend-production-xxxx.up.railway.app/health`.
* Receive instant WhatsApp/Email alerts if the backend goes down or the free container sleeps.

### 7.3 Automated DB Backups
* In Supabase / Neon, enable the default daily snapshot schedule.
* Keep manual exports before releasing major new features.
