# CyberRakshak AI — Design Guide

Direction: **clean, trustworthy, light theme** — like a bank/fintech app, not a hacker-dashboard.
Users are often anxious or unsure when they arrive (they just got scammed or suspect they might
be); the UI should feel calm, credible, and easy to act on — not alarming or "hacker-y."

## 1. Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Primary | Trust Blue | `#1F5FBF` | Primary buttons, links, active nav, brand accents |
| Primary Dark | Deep Blue | `#123B80` | Hover/pressed states, headers |
| Background | Off-White | `#F7F9FC` | App background |
| Surface | White | `#FFFFFF` | Cards, panels, inputs |
| Border/Divider | Cool Gray | `#E2E8F0` | Card borders, dividers |
| Text Primary | Slate 900 | `#1A202C` | Headings, body text |
| Text Secondary | Slate 500 | `#64748B` | Captions, helper text |
| Risk — LOW | Green | `#1E8E5A` | Low-risk badge/result |
| Risk — MEDIUM | Amber | `#B98900` | Medium-risk badge/result |
| Risk — HIGH | Orange | `#C2510C` | High-risk badge/result |
| Risk — CRITICAL | Red | `#C0332B` | Critical-risk badge/result |
| Success | Green | `#1E8E5A` | Confirmations |
| Error | Red | `#C0332B` | Form/validation errors |

Notes:
- Risk colors are intentionally distinct from generic success/error so a MEDIUM result isn't
  confused with a form error.
- All text/background pairs must meet WCAG AA contrast (4.5:1 for body text).
- No neon/dark "cyberpunk" styling — that undercuts the "calm and credible" goal for a
  general-public safety tool.

## 2. Typography

- **Primary typeface:** Inter (or system UI stack fallback: `-apple-system, "Segoe UI", Roboto,
  Helvetica, Arial, sans-serif`) — clean, highly legible, works well at small sizes for
  non-technical users.
- **Scale:**
  - H1: 28–32px / semi-bold — page titles
  - H2: 22–24px / semi-bold — section headers
  - H3: 18px / medium — card titles
  - Body: 15–16px / regular — never below 14px for primary content (accessibility)
  - Caption/helper: 13px / regular, Text Secondary color
- **Line height:** 1.5 for body text, 1.2–1.3 for headings.
- Mobile (Flutter) mirrors the same scale using the Flutter Material typography system with the
  same font family where licensing/bundling allows, or the closest system default otherwise.

## 3. Components & Tone

- **Risk result card**: the centerpiece component. Large risk badge (color per table above),
  numeric score, short plain-language explanation, bullet list of indicators, clear recommended
  action as a primary button/next step (e.g. "Do not click this link" / "Verify with your bank
  directly").
- **Buttons**: rounded corners (8px radius), solid primary for main actions, outline/secondary
  for less critical actions. Avoid destructive-red buttons except for actual destructive actions.
- **Forms**: generous spacing, inline validation messages (not just red borders), clear labels
  (no placeholder-only inputs for anything important).
- **Empty/loading states**: never a blank screen — always a skeleton, spinner, or friendly
  message during analysis, since scoring/LLM explanation calls take a moment.
- **Copy tone**: plain language, second person, reassuring but direct. Avoid jargon
  ("heuristic," "entropy") in user-facing text — save that for admin/technical views only.
  Example: "This link shows signs of a phishing attempt" not "URL failed heuristic entropy check."

## 4. Layout

- Web: centered content column (max-width ~960px) for analysis tools; wider dashboard layout for
  admin/community views.
- Mobile (Flutter): single-column, thumb-reachable primary actions near the bottom, camera-based
  QR scan as a prominent home-screen action.
- Consistent spacing scale: 4 / 8 / 12 / 16 / 24 / 32 / 48px.

## 5. Iconography & Imagery

- Simple line icons (e.g. Lucide/Feather-style) — shield, link, QR, flag/report, book (awareness).
- Avoid stock "hacker in a hoodie" imagery — reinforces fear rather than empowerment.
- Risk badges can use a small icon (checkmark / info / warning / alert) alongside color, so the
  meaning isn't color-only (accessibility for color-blind users).

## 6. Dark Mode

Not required for MVP. If added later (Tier 3 territory), invert using the same blue accent on a
slate-900 background, keep risk colors adjusted for contrast on dark surfaces rather than reused
as-is.
