# DevOps Task Manager

**Built by [Basit Sherazi](https://linkedin.com/in/basitsherazi)**

A production-grade full-stack task manager built to demonstrate real DevOps and cloud security practices end-to-end — not a tutorial project. Every component was designed, built, and shipped independently: Python FastAPI backend, React frontend, MongoDB, Docker multi-stage builds, a 3-job GitHub Actions CI/CD pipeline with automated security scanning, and a live Prometheus + Grafana observability stack tracking real-time system metrics.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | Python 3.12 + FastAPI + Motor (async MongoDB) |
| Frontend | React.js + nginx |
| Database | MongoDB 7 |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Security Scanning | Bandit + pip-audit + Trivy |
| Monitoring | Prometheus + Grafana + Alertmanager |

---

## Architecture

6 services orchestrated via Docker Compose:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   React     │────▶│  FastAPI    │────▶│   MongoDB   │
│  (nginx)    │     │  Backend    │     │             │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │ /metrics
                    ┌──────▼──────┐     ┌─────────────┐
                    │ Prometheus  │────▶│   Grafana   │
                    └──────┬──────┘     └─────────────┘
                           │ alerts
                    ┌──────▼──────┐
                    │Alertmanager │
                    └─────────────┘
```

---

## Security Features

- **CORS restricted** — configurable via `ALLOWED_ORIGINS` env var, not open to `*`
- **No hardcoded credentials** — all secrets via environment variables
- **Non-root Docker containers** — backend runs as `appuser` (uid 1001)
- **Bandit** — static analysis on every CI run to catch Python security issues
- **pip-audit** — scans Python dependencies for known CVEs on every CI run
- **Trivy** — filesystem vulnerability scan, results uploaded to GitHub Security tab
- **Input validation** — Pydantic enforces request shapes and field constraints
- **Alerting** — Prometheus alert rules for service downtime, high error rate, p95 latency, CPU, and memory; routed through Alertmanager with configurable Slack/email receivers

---

## CI/CD Pipeline

Every push to `main` or `develop` runs 3 jobs in order:

```
Test → Security → Build
```

| Job | What it does |
|---|---|
| **Test** | pytest against mocked MongoDB |
| **Security** | Bandit static analysis + pip-audit CVE detection + Trivy filesystem scan (SARIF upload to GitHub Security tab) |
| **Build** | Builds backend + frontend Docker images |

---

## Live Deployment

Backend deployed to **Azure Container Apps** (westus2):

| Endpoint | URL |
|---|---|
| API Docs (Swagger) | https://task-manager-api.victoriousgrass-3dbb5698.westus2.azurecontainerapps.io/docs |
| Health Check | https://task-manager-api.victoriousgrass-3dbb5698.westus2.azurecontainerapps.io/health |
| Metrics | https://task-manager-api.victoriousgrass-3dbb5698.westus2.azurecontainerapps.io/metrics |

---

## Quick Start (Local)

```bash
cp .env.example .env        # fill in MONGO_PASSWORD
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Metrics | http://localhost:8000/metrics |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3002 (admin/admin) |
| Alertmanager | http://localhost:9093 |

---

## Local Backend Development

```bash
cd backend
pip install -r requirements-dev.txt
pytest -v
uvicorn main:app --reload --port 8000
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check + MongoDB status |
| GET | `/metrics` | Prometheus metrics |
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create task `{"title": "..."}` |
| PUT | `/api/tasks/{id}` | Update task `{"completed": true}` |
| DELETE | `/api/tasks/{id}` | Delete task |

---

## Environment Variables

```env
MONGO_USERNAME=admin
MONGO_PASSWORD=your_secure_password
ALLOWED_ORIGINS=http://localhost:3000
```

---

## Project Structure

```
dev-ops-basit-/
├── .github/workflows/
│   └── ci.yml                # Test + Security + Build pipeline
├── backend/
│   ├── main.py               # FastAPI app with Prometheus metrics
│   ├── requirements.txt
│   ├── requirements-dev.txt  # + pytest, bandit, pip-audit
│   ├── Dockerfile            # Multi-stage, non-root user
│   └── tests/
│       └── test_main.py
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf            # Reverse proxy to backend
│   └── src/
├── monitoring/
│   ├── prometheus/           # Scrape config + alert rules
│   ├── alertmanager/         # Alert routing config
│   └── grafana/              # Dashboards + datasources
├── docker-compose.yml
├── Makefile                  # make start / stop / test / clean
└── .env.example
```
