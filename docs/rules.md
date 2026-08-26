# CyberRakshak AI — Development Rules

These rules apply to every contributor and every AI coding agent (Claude, opencode, or otherwise)
working on this repo. When in doubt, pick the smallest reasonable implementation that supports
the MVP — do not expand scope without justification.

## 1. What To Do

- Build **vertically** — one working end-to-end slice before moving to the next module.
- Use typed models/schemas everywhere (Pydantic on backend, TypeScript-leaning prop discipline
  or PropTypes on the React side where practical, strong typing in Dart).
- Validate all input at the API boundary.
- Handle errors explicitly; never let a raw exception leak to the client.
- Write tests for anything with real logic (scoring, validation, auth) — not just happy paths.
- Keep code modular: one responsibility per service/module.
- Use environment variables for all config and secrets; keep `.env.example` in sync with real keys.
- Preserve existing working functionality — do not overwrite/rewrite working code unnecessarily.
- Document non-obvious decisions inline or in `docs/`.
- Keep `docs/memory.md` updated at the end of every work session (see that file).

## 2. What To Avoid

- Do not build the entire application in one giant pass. Small, working, tested milestones only.
- Do not hardcode secrets, API keys, or credentials anywhere in source.
- Do not commit `.env`.
- Do not trust frontend-supplied role/permission claims — authorization is enforced server-side, always.
- Do not store raw scam-message content indefinitely (privacy). Summarize/derive indicators and
  discard or expire raw text per a retention policy.
- Do not collect precise victim location — approximate area only.
- Do not claim guaranteed detection accuracy anywhere in UI copy, docs, or model output framing.
- Do not introduce deep learning or heavy ML by default — a strong rule-based baseline is
  preferred until there's a validated reason to add a classifier.
- Do not add a library "because it's popular" — prefer mature, maintained, minimal, well-documented.

## 3. AI Safety Boundaries (hard limits)

The application analyzes scam indicators; it must never become a tool that enables abuse. Do NOT
implement, under any framing (including "for testing" or "for the demo"):

- Credential harvesting or phishing-page generation
- Exploit or malware generation
- Unauthorized scanning of real third-party systems
- Password cracking or bypassing security controls
- Attacks against real targets

For demos and tests, use only: synthetic scam messages, public datasets, intentionally safe test
domains, and controlled local environments. Never visit arbitrary live suspicious URLs from a
server/user device without a deliberately designed safe-analysis mechanism — prefer static
analysis and reputation APIs for the MVP.

## 4. AI Explanation Layer (LLM usage rules)

- The LLM (e.g. Claude API) is used **only** to phrase the human-readable explanation of an
  already-computed risk score/indicator set — it does not decide the score itself.
- Every call must have a **deterministic template fallback** if the API is unavailable, rate
  limited, or errors — the app must remain fully functional without the LLM.
- Never send raw personal/sensitive user data to the external AI provider beyond what's needed
  for the explanation (indicators + score, not full message text with PII where avoidable).
- Cache/short-circuit repeated identical explanation requests where reasonable to control cost.

## 5. Threat Intelligence Provider Rule

Design external integrations (PhishTank, OpenPhish, VirusTotal, etc.) behind a common interface
so any one API being unavailable never breaks the app:

```
ThreatIntelProvider (interface)
   ├── MockThreatIntelProvider   (default/local dev)
   ├── VirusTotalProvider
   └── PhishTankProvider
```

Enable/disable per provider via environment variables.

## 6. Error Handling Conventions

- Backend: raise typed `HTTPException`s with clear status codes; return generic messages for
  auth/security failures (do not leak "user not found" vs "wrong password" distinctions).
- Log errors server-side with enough context to debug, but **never log sensitive content**
  (passwords, raw scam message text, tokens).
- Frontend (web + mobile): every API call needs a loading, success, and failure state in the UI —
  no silent failures, no unhandled promise rejections.
- Validate at both schema level (Pydantic/Dart) and business-logic level (e.g. score bounds
  clamped to 0–100).

## 7. Security Requirements (non-negotiable)

- HTTPS in any deployed environment.
- JWT-based auth; Argon2id or bcrypt password hashing (bcrypt already wired via passlib).
- Rate limiting on expensive/abusable endpoints (analysis, reporting, auth).
- Strict CORS configuration — only allow the actual frontend origins.
- File upload validation: restrict type, restrict size, sanitize filenames.
- Least-privilege DB credentials; no `.env` in git; audit logging for admin actions.

## 8. Library Preferences

| Need | Preferred | Avoid unless justified |
|---|---|---|
| Backend framework | FastAPI (already chosen) | — |
| ORM | SQLAlchemy + Alembic | Raw SQL scattered in routes |
| Validation | Pydantic v2 | Manual dict validation |
| Auth | python-jose + passlib[bcrypt] (already chosen) | Rolling custom crypto |
| ML baseline | scikit-learn | TensorFlow/PyTorch unless a clear need emerges |
| OCR | Tesseract or EasyOCR | Heavier vision pipelines |
| Web frontend | React + Vite (already chosen) | Adding a second framework |
| Mobile | Flutter + Dart | Native dual (Kotlin+Swift) — too costly for 3 months |
| Testing | pytest, Flutter `test`, Vitest/RTL | Ad hoc manual testing only |

## 9. Response Format For Substantial Dev Work

When implementing any non-trivial feature (backend or frontend), structure the work as:

**Understanding → Plan → Changes → Implementation → Testing → Security Notes → Next Step**

Do not give vague advice when actual implementation is requested — implement it.

## 10. Definition of Done

A feature is done only when: it works locally, has API validation, handles error cases,
enforces correct auth/authorization, has tests for important logic, has UI success/failure
states, has updated docs, is committed, and another team member could run it from a clean clone.
