# 🤝 Contributing to CyberRakshak AI

First off, thank you for considering contributing! Every contribution — bug reports, feature requests, documentation, or code — is highly appreciated.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Commit Guidelines](#commit-guidelines)
- [Branching Strategy](#branching-strategy)
- [Testing](#testing)
- [Style Guides](#style-guides)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

By participating, you agree to uphold our [Code of Conduct](.github/CODE_OF_CONDUCT.md). Please report unacceptable behavior to the maintainers.

## Getting Started

1. **Fork** the repository and create your branch from `main`.
2. Clone your fork locally and add the original as `upstream`:

   ```bash
   git clone https://github.com/<your-username>/CyberRakshak-AI.git
   cd CyberRakshak-AI
   git remote add upstream https://github.com/rishik9028/CyberRakshak-AI.git
   ```

3. Set up the local environment (see [README.md](README.md) → Quickstart).

## Development Workflow

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Make your changes with clear, atomic commits.
3. Run the full test suite (see [Testing](#testing)).
4. Push your branch and open a Pull Request against `main`.

## Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

<optional body>

<optional footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

Examples:

- `feat(backend): add threat scoring endpoint`
- `fix(frontend): correct dashboard timezone handling`
- `docs: clarify deployment steps`

## Branching Strategy

- `main` — stable, always deployable.
- `feat/*` — new features.
- `fix/*` — bug fixes.
- `docs/*` — documentation changes.
- `chore/*` — maintenance tasks.

## Testing

- **Backend:** `cd backend && pytest`
- **Frontend:** `cd frontend && npm run build`
- **Linting:** `cd backend && ruff check .`

All new code must include appropriate tests and pass existing ones.

## Style Guides

### Python (Backend)

- Python 3.11+
- Follow [PEP 8](https://peps.python.org/pep-0008/) and [PEP 20](https://peps.python.org/pep-0020/).
- Use type hints on all public functions.
- Lint with `ruff`, format with `black` (88 char line length).
- Imports order: standard library → third-party → local.

### JavaScript / React (Frontend)

- React 18, functional components + hooks.
- Prefer named exports for components.
- Use descriptive component and variable names.

## Reporting Issues

Please use the issue templates:

- [🐛 Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)
- [✨ Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)

Include steps to reproduce, expected behavior, and environment details where relevant.

---

Thank you for helping make CyberRakshak AI better! 🙌
