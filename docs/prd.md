# CyberRakshak AI — Product Requirements Document (PRD)

## 1. What We're Building

CyberRakshak AI is a **community cybersecurity and digital-scam-prevention platform**. It helps
ordinary users assess whether a message, URL, or QR-linked website looks like a scam, explains
*why*, teaches basic cyber-safety, and lets the community report and track scam trends.

It is a **risk-assessment assistant, not an absolute-truth oracle**. All outputs are framed as
risk scores / indicators / confidence — never as guaranteed "safe" or "malicious."

> One-line pitch: *"Paste a suspicious message or link, get an explained risk score, learn what
> to do next, and help your community see scam trends — without exposing anyone's private data."*

## 2. Problem

Non-technical users in India (and elsewhere) are constantly targeted by:

- Phishing links, fake KYC/bank messages, UPI/payment scams, QR-code scams
- Fake job/loan offers, fake shopping sites, investment/crypto scams
- Social-media impersonation, fake courier messages, OTP social engineering, tech-support scams

Most victims have no fast, free, explainable way to check "is this legit?" before it's too late.

## 3. Target Users

| User type | Need |
|---|---|
| **General public / students / families** (primary) | Quick check of a suspicious message, link, or QR before acting on it |
| **Community members** | Want to warn others / see what scams are trending nearby |
| **Admin / moderators** (project team acting as admins for demo) | Review and verify community-submitted reports |
| **Evaluators / supervisors** (academic context) | Need a coherent, demonstrable, honestly-scoped project |

Not targeting: enterprises, SOC teams, or anyone needing production-grade national fraud
infrastructure. This is a community safety tool, not a threat-intel platform for organizations.

## 4. Scope Statement (Important)

> CyberRakshak AI performs risk assessment of selected scam indicators — suspicious messages,
> URLs, and QR-linked websites — while providing awareness, community reporting, and
> incident-response guidance.

**Never claim:** 100% detection, guaranteed safe/malicious, perfect AI, complete malware
detection. **Always use:** "risk assessment," "suspicious," "potential phishing," "risk score,"
"confidence," "indicators detected."

## 5. Features — MVP (must work, in priority order)

1. **Scam Message Analyzer** — paste SMS/email/WhatsApp/OCR text → risk level (LOW/MED/HIGH),
   score, indicators, explanation, recommended action.
2. **URL / Phishing Checker** — analyze URL syntax, HTTPS, domain traits, keywords, length,
   subdomains, IP-hostname, shorteners, plus optional threat-intel APIs (PhishTank, OpenPhish,
   VirusTotal) behind a pluggable provider interface.
3. **QR Code Scanner** — decode QR (camera on Android, upload on web) → extract URL → run through
   URL analyzer → show risk. **Never auto-opens the destination.**
4. **Community Scam Reporting** — category, description, approximate location, date/time,
   channel, optional URL/screenshot. Status: PENDING → REVIEWED → VERIFIED/REJECTED. No precise
   location, minimal PII.
5. **Cyber Awareness** — short guides, examples, quizzes, prevention tips, "what to do if
   scammed," warning signs, UPI/QR/phishing/MFA basics. Written for non-technical readers.

## 6. Secondary Features (after MVP is stable)

Screenshot OCR, multilingual UI, voice assistance, community trend dashboard/heatmap, user
reputation, AI safety chatbot, advanced analytics, browser extension, more file types.

## 7. Explicitly Deferred (not core requirements)

Deepfake detection, full APK malware analysis, real-time SMS/WhatsApp interception, a
production-grade national fraud database.

## 8. Success Criteria (end of 3 months)

- [ ] Working Android app (Flutter) + working web client (React) on the same backend
- [ ] FastAPI backend + PostgreSQL
- [ ] Secure auth (JWT, hashed passwords)
- [ ] Message analysis, URL analysis, QR analysis all working end-to-end
- [ ] Community reporting + admin moderation
- [ ] Awareness/quiz module
- [ ] Basic analytics, ML evaluation metrics
- [ ] Automated tests (unit + integration + security)
- [ ] Deployed demo, technical + user documentation
- [ ] One coherent final demo scenario (see `phases.md`)

## 9. Non-Goals

- Not a replacement for professional incident response or law enforcement reporting
- Not attempting to intercept or read users' private messages automatically
- Not storing raw scam message content indefinitely
- Not generating phishing pages, exploits, or malware under any circumstance (see `rules.md`)
