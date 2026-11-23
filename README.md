<div align="center">

# 🎓 SirKaisaHai (سر کیسا ہے؟)
### *Unfiltered, Anonymous & Verified University Teacher Reviews*

[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://supabase.com/)

<p align="center">
  <strong>Currently live for Superior University (Lahore) — Scaling across universities nationwide across Pakistan.</strong>
</p>

</div>

---

## 📖 About The Project

**SirKaisaHai** is a modern, student-first faculty rating and course intelligence platform. It bridges the transparency gap in higher education, helping university students make informed semester registration choices based on authentic peer experiences — without fear of academic retaliation.

### 📍 Current Scope & National Vision
* **Phase 1 (Active):** Specialized deployment for **Superior University, Lahore** covering the Faculty of Computing & Information Technology (Computer Science, Software Engineering, Cyber Security, Data Science, AI, IT, and IoT).
* **Phase 2 (Roadmap):** Expansion to all campus faculties (Business, Engineering, Pharmacy, Media, Law).
* **Phase 3 (Nationwide):** Scaling into a nationwide multi-tenant academic transparency network for public and private universities across Pakistan (NUST, FAST, LUMS, COMSATS, ITU, PU, etc.).

---

## ✨ Key Features

### 🛡️ 1. Zero-Knowledge Student Verification & True Anonymity
* **One-Time Email OTP Verification:** Validates authentic student identity via official institutional email (`@superior.edu.pk`).
* **Irreversible SHA-256 Hashing:** Student email addresses are salted and hashed cryptographically. The actual email is **never stored** alongside submitted reviews or comments.
* **Server-Side Session Invalidation:** Instant logout and remote database session invalidation.

### 📊 2. Multi-Dimensional Faculty Evaluations
* Evaluates teachers across realistic academic criteria rather than arbitrary single numbers:
  * **Teaching Clarity (1.0 - 5.0)**
  * **Grading Fairness (1.0 - 5.0)**
  * **Workload & Assignment Intensity (1.0 - 5.0)**
  * **Recommendation Percentage & Verified Badges**
* Includes grade received breakdown and semester metadata.

### ⚡ 3. Enterprise-Grade Security & Anti-Abuse
* **Dual-Layer Rate Limiting:** SlowAPI network throttling (`5 OTP requests / 15 min per IP`) + in-memory sliding window tracking per email.
* **Brute-Force Lockout:** Automatic 15-minute cooldown on repeated incorrect OTP verification attempts.
* **Automated Content Moderation:** Client & server-side profanity filtering ensuring constructive academic feedback.

### 📱 4. Bento Grid UI & Mobile-First Experience
* Tailored modern design system using glassmorphism, fluid micro-interactions, custom SVG branding, and full responsive compatibility across mobile phones, tablets, and desktop workstations.

---

## 🛠️ Tech Stack

### Frontend
* **Framework:** [Vue 3](https://vuejs.org/) (Composition API, `<script setup>`)
* **Build Tool:** [Vite](https://vitejs.dev/) with hot module replacement
* **Styling:** [Tailwind CSS](https://tailwindcss.com/) with custom design tokens & glassmorphic panels
* **State Management:** [Pinia](https://pinia.vuejs.org/)
* **Routing:** [Vue Router](https://router.vuejs.org/)

### Backend
* **API Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
* **Database / ORM:** [PostgreSQL (Supabase)](https://supabase.com/) via [SQLAlchemy](https://www.sqlalchemy.org/)
* **Security & Auth:** `httpOnly` secure session cookies, `passlib`, `hashlib` SHA-256 with secret salt
* **Rate Limiting:** `SlowAPI` with Redis/Memory backends

---

## 🚀 Getting Started (Local Development)

### Prerequisites
* [Node.js](https://nodejs.org/) (v18+)
* [Python](https://www.python.org/) (v3.10+)
* [Git](https://git-scm.com/)

---

### 1. Clone the Repository
```bash
git clone https://github.com/daredevil717/SirKaisaHai.git
cd SirKaisaHai
```

---

### 2. Backend Setup
```bash
cd backend

# Create & activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Open .env and set DATABASE_URL, EMAIL_HASH_SECRET, VOTE_SECRET, and ADMIN_SECRET_KEY

# Run database migrations & safe reference seeding
alembic upgrade head
python -m app.seed

# Start backend server
uvicorn app.main:app --reload
```
* Backend API will run at: `http://127.0.0.1:8000`
* Interactive API Docs (Swagger): `http://127.0.0.1:8000/docs`

---

### 3. Frontend Setup
```bash
cd ../sirkaisahai_first

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
* Frontend will run at: `http://localhost:5173` (also accessible on local mobile Wi-Fi network via `--host`).

---

## 🗺️ Project Roadmap

- [x] Initial release for Superior University (Lahore) — Computing & IT faculties
- [x] Cloud PostgreSQL migration (Supabase Shared Pooler)
- [x] Email OTP verification with SHA-256 anonymous hashing
- [x] Dual-layer rate limiting & 15-minute brute-force lockout
- [x] Mobile-responsive UI & animated slogan hero
- [ ] Add remaining Superior University faculties (Management, Engineering, Pharmacy)
- [ ] Student AI review summaries (Gemini / Claude powered summaries per professor)
- [ ] Multi-University tenant architecture for nationwide university onboarding (NUST, FAST, COMSATS, PU, etc.)

---

## 🤝 Contributing

Contributions, issues, and feature suggestions are welcome! Feel free to check the [Issues page](https://github.com/daredevil717/SirKaisaHai/issues).

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

<div align="center">
  <sub>Built with ❤️ by students, for students.</sub>
</div>
