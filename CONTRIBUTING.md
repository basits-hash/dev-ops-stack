# Contributing

Thanks for your interest in improving the DevOps Task Manager. This guide covers
the local workflow and the standards every change is expected to meet.

## Getting started

```bash
git clone https://github.com/BasitS-hash/dev-ops-stack.git
cd dev-ops-stack
cp .env.example .env          # set MONGO_PASSWORD and GRAFANA_PASSWORD
docker compose up --build     # run the full stack
```

### Backend (local, without Docker)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn main:app --reload --port 8000
```

### Frontend (local, without Docker)

```bash
cd frontend
npm ci
npm start
```

## Development workflow

1. **Branch** off `main` — never commit directly to `main`.
   ```bash
   git checkout -b feat/short-description
   ```
2. **Write tests first** for new behavior, then implement.
3. **Run the checks locally** before pushing (see below).
4. **Open a PR** against `main`. CI must be green before review.

## Quality gates

Your change must pass all of these — the same checks run in CI:

```bash
# Backend
cd backend
ruff check .                                   # lint
bandit -r main.py config.py -ll                # SAST
pip-audit -r requirements.txt                  # dependency CVEs
pytest --cov=. --cov-fail-under=80             # tests + coverage gate

# Frontend
cd frontend
npx eslint src --max-warnings=0                # lint
CI=true npm test -- --watchAll=false           # tests
npm run build                                   # build
npm audit --omit=dev --audit-level=high        # prod dependency audit
```

Or run the aggregate targets:

```bash
make lint
make test
make test-frontend
```

## Standards

- **Tests:** new features require tests; keep backend coverage at or above 80%.
- **Security:** never commit secrets. Validate all input at boundaries.
  Parameterize all queries. Add security headers where relevant.
- **Containers:** keep images multi-stage and non-root; pin base image versions.
- **File size:** prefer small, focused modules (≤ 400 lines).
- **Commits:** use [Conventional Commits](https://www.conventionalcommits.org/):
  `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `ci:`, `perf:`.

## Reporting security issues

Do not open public issues for vulnerabilities — see [SECURITY.md](SECURITY.md).
