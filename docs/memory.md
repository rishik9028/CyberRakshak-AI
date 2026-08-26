# CyberRakshak AI — Project Memory (Living State)

> Update this file at the end of every work session, whichever agent (Claude, opencode, human)
> does the work. This is the single source of truth for "where are we right now" — read this
> before starting any new task.

**Last updated:** 2026-08-27
**Updated by:** Claude (planning session)

---

## Current Milestone

**Milestone 1 — End-to-end URL analysis** (not started yet — planning just completed)

## Repo State As Of Last Inspection

Source: `master` branch, opencode-generated scaffold.

**Backend (`backend/`)**
- ✅ FastAPI app boots (`app/main.py`), versioned router (`app/api/v1/router.py`)
- ✅ `GET /api/v1/health` implemented + tested (`tests/test_health.py`)
- ✅ `app/config.py` — Pydantic Settings (DB URL, Redis URL, JWT secret placeholders already present)
- ✅ `app/core/security.py` — password hashing (bcrypt) + JWT `create_access_token` utility exist,
  **not yet wired to any endpoint**
- ❌ No SQLAlchemy session/engine, no `app/db/`
- ❌ No models (`app/models/` only has `__init__.py`)
- ❌ No Alembic
- ❌ No auth endpoints (register/login/me)
- ❌ No URL/message/QR/report endpoints
- `requirements.txt`: fastapi, uvicorn, pydantic, pydantic-settings, python-multipart,
  python-jose, passlib[bcrypt], bcrypt — **missing** sqlalchemy, alembic, psycopg (or asyncpg),
  and an LLM client lib for the explanation layer

**Frontend — web (`frontend/`)**
- ✅ React + Vite scaffold, `src/api/client.js` stub, placeholder `App.jsx`
- ❌ No real feature pages yet (no URL checker UI, no routing)

**Frontend — mobile**
- ❌ Does not exist yet (planned Phase 2, per `phases.md`)

**Docs**
- ✅ `docs/prd.md`, `docs/architecture.md`, `docs/rules.md`, `docs/phases.md`, `docs/design.md`,
  `docs/memory.md` (this file) — created this session
- ⚠️ Root `README.md` and `ROADMAP.md` describe a generic "network threat detection" product —
  this is stale/mismatched with the actual scam-prevention scope in `prd.md`. **Needs a rewrite
  pass** (not urgent, but flag it so nobody gets confused reading the repo root).

## Key Decisions Locked In (do not re-litigate without reason)

- Frontend: keep React/Vite for web/PC (already built), add Flutter for Android starting Phase 2
  — both consume the same FastAPI backend, no client-specific backend logic.
- Design direction: clean/light/trustworthy (bank-app feel), not dark/cyberpunk. See `design.md`.
- Explanation layer: LLM-generated (e.g. Claude API) with a deterministic template fallback if
  the API is unavailable — never a hard dependency.
- AI pipeline stays rule-based-first; ML/LLM are additive, app must work with them disabled.

## What's Currently Being Worked On

*(nothing yet — planning docs just landed; Milestone 1 implementation is next)*

## Next Steps (in order)

1. Add SQLAlchemy session (`app/db/session.py`, `app/db/base.py`) + Alembic init
2. Add `Analysis` model + first migration
3. Add `url_analyzer` service (rule-based indicators) + `ThreatIntelProvider` interface with
   `MockThreatIntelProvider`
4. Add `POST /api/v1/analyze/url` endpoint + Pydantic schemas
5. Add explanation service (template first, LLM-enhanced with fallback)
6. Wire a real React page for URL checking
7. Write pytest tests for the analyzer + endpoint
8. Update this file with results before ending that session

## Open Questions / Things To Revisit

- Root README/ROADMAP rewrite — low priority, schedule for a documentation pass
- Which LLM API key/provider to actually configure in `.env.example` for the explanation layer
- Real threat-intel provider(s) to prioritize (PhishTank is free/simplest to start with)
