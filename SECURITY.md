# 🔒 Security Policy

## Supported Versions

We currently provide security updates for the latest release on the `main` branch.

| Version | Supported          |
|---------|--------------------|
| main    | ✅ Active          |
| < 1.0   | ❌ Not yet released |

## Reporting a Vulnerability

We take security seriously. If you discover a vulnerability, **please do not open a public issue**.

Instead, report it privately via email to the maintainers:

- **Email:** rishi.24bce10896@vitbhopal.ac.in

### What to include

- A clear description of the vulnerability.
- Steps to reproduce it (if possible).
- Affected versions/components.
- Any potential impact or exploit scenario.

### Response timeline

| Timeframe            | Action                                              |
|----------------------|-----------------------------------------------------|
| 48 hours             | Acknowledgment of your report                       |
| 1 week               | Initial triage & severity assessment                |
| 2–4 weeks            | Fix, testing, and release (severity dependent)      |

We will credit you for your report unless you prefer to remain anonymous.

## Security Best Practices for Contributors

- Never commit secrets, tokens, or keys. Use `.env` files and the environment.
- Keep dependencies up to date and run `pip-audit` / `npm audit` before releases.
- Prefer parameterized queries and ORMs over raw SQL.
- Validate all user input; follow OWASP Top 10 guidance.
- Report security-adjacent bugs through the same private channel.

Thank you for helping keep CyberRakshak AI safe. 🛡️
