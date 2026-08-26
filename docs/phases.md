# CyberRakshak AI — Phases & Roadmap (3 Months / 12 Weeks)

Adapted from the original team roadmap to reflect the actual starting point (opencode-scaffolded
FastAPI + React repo) and the confirmed decisions: **web (React) now, Flutter Android added
starting Phase 2, both on the same backend; light/trustworthy design; LLM-assisted explanations
with template fallback.**

## Phase 0 — Where We Are Now (Week 1, in progress)

- [x] Repo scaffolded: FastAPI backend skeleton, React+Vite frontend skeleton, Docker Compose, CI
- [x] `/api/v1/health` working end-to-end
- [x] Password hashing + JWT token creation utilities exist (not yet wired to endpoints)
- [ ] Planning docs (`prd.md`, `architecture.md`, `rules.md`, `phases.md`, `design.md`,
      `memory.md`) — this pass
- [ ] Milestone 1: end-to-end URL analysis (see below) — **next**

## Milestone 1 — End-to-End URL Analysis (immediate target)

1. PostgreSQL connection + SQLAlchemy session + Alembic init
2. `Analysis` model + migration
3. `url_analyzer` service — static indicators (HTTPS, length, subdomains, IP-hostname, shortener,
   keywords) → transparent risk score
4. `ThreatIntelProvider` interface + `MockThreatIntelProvider`
5. `POST /api/v1/analyze/url` endpoint + Pydantic request/response schemas
6. Explanation service — template-based first, LLM-enhanced with fallback
7. React web page: URL input → call endpoint → risk card result
8. pytest coverage for the analyzer + endpoint (valid, invalid, edge-case URLs)

*This is the technical backbone milestone — once it works, everything else follows the same
pattern.*

## Phase 1 — Foundation + Auth (Weeks 1–3)

- Week 1: Planning finalized (this doc set), dataset research started, dev environment confirmed
- Week 2: DB + Alembic in place, auth skeleton (`/auth/register`, `/auth/login`, `/auth/me`),
  Milestone 1 URL analysis shipped
- Week 3: Auth fully wired with JWT dependency on protected routes, basic report model +
  `POST /reports` stub, web dashboard shell

## Phase 2 — Core Modules + Flutter Start (Weeks 4–6)

- Week 4: URL module hardened (more indicators, real threat-intel provider optional), Flutter
  project initialized targeting the same backend, mobile URL checker screen
- Week 5: Message analyzer — dataset preprocessing, baseline classifier (scikit-learn), API + UI
  (web first, then mobile)
- Week 6: QR module — decode (camera on Flutter, upload on web) → feed into URL analyzer;
  QR must never auto-open the destination

## Phase 3 — Threat Intel + Community (Weeks 7–8)

- Week 7: Threat-intel adapter finalized (PhishTank/OpenPhish/VirusTotal via env-toggled
  providers), result normalization, scoring integration
- Week 8: Screenshot OCR (Tesseract/EasyOCR), community reporting completed on both clients,
  admin moderation endpoints, initial analytics

## Phase 4 — Awareness + Integration (Weeks 9–10)

- Week 9: Awareness content, quiz system, "what to do if scammed" guidance, accessibility pass
- Week 10: Full end-to-end integration across web + mobile, error-handling audit, security
  hardening pass, performance pass

## Phase 5 — Testing (Week 11)

- Unit + integration tests, ML evaluation (accuracy/precision/recall/F1/confusion matrix — not
  accuracy alone), security testing (SQLi, XSS, auth bypass, broken authz, rate limiting, file
  upload abuse, CORS), user testing, bug fixing

## Phase 6 — Final (Week 12)

- Deployment, final documentation, screenshots, demo dataset, presentation, project report,
  full rehearsal of the demo scenario below

## Final Demo Scenario (single coherent journey)

1. User pastes a fake-KYC message → indicators shown (urgency, impersonation, KYC request, link)
2. User checks the embedded URL → risk score + indicators + threat-intel result
3. User scans the QR version of the same scam → same URL analysis triggered automatically
4. User submits a community report
5. Admin reviews and updates report status
6. Community dashboard shows aggregated trend, no victim PII exposed
7. User opens awareness section for guidance on avoiding similar scams

## Priority Order If Time Runs Short

**Tier 1 (must have):** Backend, DB, auth, URL checker, message analyzer, QR scanner, community reports
**Tier 2 (should have):** Admin dashboard, awareness/quiz, OCR, analytics
**Tier 3 (nice to have):** Map, multilingual UI, voice assistant, AI chatbot, advanced ML

Never sacrifice a stable Tier 1 feature to chase an unfinished Tier 3 feature.
