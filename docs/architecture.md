# CyberRakshak AI — Architecture

## 1. High-Level Flow

```
        ┌────────────────────┐        ┌────────────────────┐
        │  React Web Client  │        │ Flutter Android App │
        │  (PC / laptop)     │        │  (Phase 2+)          │
        └─────────┬──────────┘        └──────────┬──────────┘
                  │  HTTPS REST (JSON)             │  HTTPS REST (JSON)
                  └───────────────┬─────────────────┘
                                  v
                       ┌─────────────────────┐
                       │   FastAPI Backend    │
                       │  /api/v1/*  routes    │
                       └──────────┬────────────┘
                                  │
        ┌───────────┬────────────┼────────────┬─────────────┐
        v            v            v            v             v
      Auth        Message      URL/QR       Reports      Admin/
     Module      Analysis     Analysis      Module       Analytics
        │            │            │            │             │
        └───────────┴────────────┴────────────┴─────────────┘
                                  │
                                  v
                          PostgreSQL Database
```

Both frontends are thin clients over the **same** versioned REST API — no client-specific backend
logic. This is why keeping the existing React web client and adding Flutter later is safe: the
contract is the API, not the UI.

## 2. Request Lifecycle (URL Analysis example)

1. User submits a URL in web or Flutter UI.
2. Client calls `POST /api/v1/analyze/url` with JWT (if logged in) or as anonymous, per endpoint policy.
3. FastAPI validates payload via Pydantic schema.
4. `url_analyzer` service extracts static features (HTTPS, length, subdomains, IP-hostname,
   shortener, keyword hits).
5. `threat_intel` provider (mock or real) is queried if configured.
6. Risk-scoring layer combines indicators → score → LOW/MEDIUM/HIGH/CRITICAL.
7. Explanation layer produces human-readable text (LLM API call with template fallback — see
   `rules.md` §AI Explanation Layer).
8. Result optionally persisted to `Analysis` table.
9. JSON response returned; client renders risk card.

## 3. AI / Analysis Pipeline (all analyzers)

```
Input → Normalization → Rule-based indicators → (optional ML classifier)
      → Threat intelligence → Risk scoring → Explanation generation
```

Rule-based indicators + transparent scoring are the backbone; ML and LLM explanation are
additive layers that must degrade gracefully if unavailable (see `rules.md`).

## 4. Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Web frontend | React 18 + Vite | Already scaffolded by opencode; kept as the PC/web client |
| Mobile frontend | Flutter + Dart | Added starting Phase 2, targets Android |
| Backend | Python, FastAPI, Uvicorn, Pydantic v2 | Already scaffolded |
| ORM / migrations | SQLAlchemy + Alembic | To be added in Milestone 1 |
| Database | PostgreSQL | To be added in Milestone 1 |
| Auth | JWT (python-jose) + bcrypt (passlib) | `core/security.py` exists; endpoints pending |
| AI / ML | scikit-learn, pandas, numpy | Baseline classifiers, Phase 3+ |
| Explanation LLM | Claude API (or equivalent) | With deterministic template fallback |
| OCR | Tesseract or EasyOCR | Phase for screenshot input |
| Threat intel | PhishTank / OpenPhish / VirusTotal | Pluggable provider interface, env-toggle |
| Infra | Docker, Docker Compose, GitHub Actions | Already scaffolded |
| Testing | pytest (backend), Vitest/RTL or similar (web), Flutter test (mobile) | |

## 5. Backend Folder Structure (current + planned)

```
backend/
├── app/
│   ├── main.py                 # ✅ exists
│   ├── config.py                # ✅ exists
│   ├── core/
│   │   ├── security.py          # ✅ exists (hashing, JWT creation)
│   │   └── logging.py           # ⬜ planned
│   ├── db/
│   │   ├── session.py           # ⬜ Milestone 1
│   │   └── base.py              # ⬜ Milestone 1
│   ├── models/
│   │   ├── user.py              # ⬜ Milestone 1 (auth)
│   │   ├── analysis.py          # ⬜ Milestone 1 (URL analysis)
│   │   ├── report.py            # ⬜ later milestone
│   │   └── scam_category.py     # ⬜ later milestone
│   ├── schemas/
│   │   ├── health.py            # ✅ exists
│   │   ├── url_analysis.py      # ⬜ Milestone 1
│   │   └── ...
│   ├── api/v1/
│   │   ├── router.py            # ✅ exists
│   │   └── endpoints/
│   │       ├── health.py        # ✅ exists
│   │       ├── url_analysis.py  # ⬜ Milestone 1
│   │       ├── auth.py          # ⬜ near-term (needed for persistence + reports)
│   │       ├── message_analysis.py  # ⬜ later
│   │       ├── qr.py            # ⬜ later
│   │       └── reports.py       # ⬜ later
│   └── services/
│       ├── url_analyzer.py      # ⬜ Milestone 1
│       ├── threat_intel.py      # ⬜ Milestone 1 (provider interface + mock)
│       ├── explanation.py       # ⬜ Milestone 1 (LLM + template fallback)
│       ├── message_analyzer.py  # ⬜ later
│       ├── qr_service.py        # ⬜ later
│       └── report_service.py    # ⬜ later
├── alembic/                     # ⬜ Milestone 1
├── tests/
│   └── test_health.py           # ✅ exists
├── requirements.txt              # ✅ exists (needs sqlalchemy, alembic, psycopg additions)
└── .env.example                 # ✅ exists (needs DATABASE_URL confirmed, LLM key)
```

## 6. Frontend Folder Structure

**Web (React, existing):**
```
frontend/
├── src/
│   ├── api/client.js        # ✅ exists
│   ├── App.jsx               # ✅ exists — currently placeholder
│   └── features/             # ⬜ planned: url-checker, message-analyzer, reports, awareness
```

**Mobile (Flutter, planned — Phase 2):**
```
mobile/
├── lib/
│   ├── main.dart
│   ├── core/ (constants, theme, networking, storage)
│   ├── models/
│   ├── services/              # HTTP client to same FastAPI backend
│   ├── features/
│   │   ├── url_checker/
│   │   ├── qr_scanner/        # camera-based, mobile-only advantage
│   │   ├── message_analyzer/
│   │   ├── reports/
│   │   └── awareness/
│   └── widgets/
```

## 7. Database Entities (initial)

- **User**: id, email, password_hash, display_name, role (USER/ADMIN), preferred_language, timestamps
- **Analysis**: id, user_id (nullable for anonymous), input_type (URL/MESSAGE/QR), risk_score,
  risk_level, indicators (JSON), result_summary, created_at — *do not store raw message content
  long-term*
- **ThreatIntelligenceResult**: id, analysis_id, provider, indicator, result, checked_at
- **ScamReport**: id, user_id, category_id, description, channel, approximate_location,
  latitude_approx, longitude_approx, reported_url, status, created_at, reviewed_at, reviewed_by
- **ScamCategory**: id, name, description

## 8. API Surface (versioned, `/api/v1`)

```
POST   /auth/register
POST   /auth/login
GET    /auth/me

POST   /analyze/url            ← Milestone 1
POST   /analyze/message
POST   /analyze/screenshot
POST   /analyze/qr

POST   /reports
GET    /reports
GET    /reports/{id}

GET    /admin/reports
PATCH  /admin/reports/{id}
GET    /admin/analytics

GET    /health                 ← already exists
```

## 9. Risk Scoring (initial, must be re-validated against a test dataset later)

```
base = 0
+20 urgency indicator
+20 credential/KYC request
+20 suspicious URL indicator
+15 impersonation indicator
+10 shortened URL
+10 domain reputation issue
+10 known threat-intel match
score = min(score, 100)

0–29 LOW · 30–59 MEDIUM · 60–79 HIGH · 80–100 CRITICAL
```
