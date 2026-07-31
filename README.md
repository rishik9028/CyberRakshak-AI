# 🛡️ CyberRakshak AI

> AI-powered cybersecurity threat detection and response platform

**CyberRakshak AI** (Cyber = Cyber, Rakshak = Protector in Hindi) is an intelligent platform that leverages artificial intelligence and machine learning to detect, analyze, and respond to cyber threats in real time.

## ✨ Features

- 🔍 **Real-time Threat Detection** — AI/ML models that identify anomalies and malicious activity
- 🤖 **Automated Response** — Intelligent mitigation actions for common attack vectors
- 📊 **Threat Intelligence Dashboard** — Visualize attacks, trends, and system health
- 🧩 **Modular Architecture** — Pluggable detectors and response actions
- 🔐 **Secure by Default** — Role-based access control, encrypted traffic, audited actions

## 🏗️ Tech Stack

| Layer      | Technology                                     |
|------------|------------------------------------------------|
| Frontend   | React 18, Vite, HTML5, CSS3                    |
| Backend    | Python, FastAPI, Uvicorn, Pydantic v2          |
| Data       | PostgreSQL, Redis (planned)                    |
| ML / AI    | scikit-learn, TensorFlow (planned)             |
| DevOps     | Docker, Docker Compose, GitHub Actions         |

## 🚀 Quickstart

### Option A — Docker (recommended)

```bash
# 1. Clone the repository
git clone https://github.com/rishik9028/CyberRakshak-AI.git
cd CyberRakshak-AI

# 2. Copy environment defaults
cp .env.example .env

# 3. Start the full stack
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs

### Option B — Local development

**Backend**

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
├── .github/              # GitHub templates & CI/CD workflows
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/          # API routes & versioning
│   │   ├── core/         # Security, config
│   │   ├── models/       # Data models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── main.py       # Application entrypoint
│   └── tests/            # Backend test suite
├── frontend/             # React + Vite application
│   └── src/
│       ├── api/          # API client
│       └── App.jsx       # Root component
├── docker-compose.yml    # Full-stack orchestration
└── ...
```

## 🧪 Testing

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm run build
```

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for the full development roadmap.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](.github/CODE_OF_CONDUCT.md).

## 🔒 Security

Found a vulnerability? Please see [SECURITY.md](SECURITY.md) for our responsible disclosure policy.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

Built with ❤️ to make the digital world safer.
