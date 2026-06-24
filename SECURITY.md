# Security Policy

## Reporting a vulnerability

If you discover a security vulnerability, please **do not open a public issue**.
Instead, report it privately via [GitHub Security Advisories](https://github.com/BasitS-hash/dev-ops-stack/security/advisories/new)
or email the maintainer. You can expect an acknowledgement within 72 hours and a
remediation plan for confirmed issues.

Please include:

- A description of the vulnerability and its impact
- Steps to reproduce (proof of concept where possible)
- Affected component(s) and version/commit

## Supported versions

This is a portfolio project; the `main` branch is the only supported version.
Security fixes land on `main`.

## Security controls in place

### Application

- **Input validation** — Pydantic models enforce types, length bounds, and
  reject unknown fields (`extra="forbid"`).
- **CORS** — explicit origin allowlist via `ALLOWED_ORIGINS`; never `*`;
  credentials disabled.
- **Rate limiting** — per-client request limits (slowapi), configurable via
  `RATE_LIMIT`.
- **Security headers** — `Content-Security-Policy`, `X-Frame-Options: DENY`,
  `X-Content-Type-Options: nosniff`, `Referrer-Policy`, and `Permissions-Policy`
  are set by the backend and reinforced at the nginx layer.
- **Request-size limits** — request bodies over 16 KiB are rejected with `413`
  before being read into memory.
- **Error hygiene** — error responses do not leak stack traces or internal
  details.

### Secrets

- **No secrets in source control.** All credentials are supplied via
  environment variables (`.env`, which is gitignored). `.env.example` documents
  the required keys with placeholder values only.
- Docker Compose **fails fast** if `MONGO_PASSWORD` or `GRAFANA_PASSWORD` is
  missing.
- Gitleaks runs in CI to catch accidentally committed secrets.

> **Operators:** rotate any credential that has ever been committed or shared.
> Use long, random values for `MONGO_PASSWORD` and `GRAFANA_PASSWORD`.

### Containers

- Multi-stage builds; final images contain no build toolchain.
- Both services run as **non-root** users.
- Base images pinned to explicit patch versions.
- `no-new-privileges` set on every service.
- Configuration files mounted **read-only**.
- Management ports (Mongo, Prometheus, Grafana, Alertmanager, backend) bind to
  `127.0.0.1` only.
- Healthchecks and log rotation configured for every service.

### Dependencies

- Exact version pins in `requirements.txt` and `package-lock.json`.
- **pip-audit** and **npm audit** gate the CI pipeline.
- **Trivy** scans both the filesystem and the built images.
- **Dependabot** opens weekly update PRs for pip, npm, Docker, and Actions.

### CI/CD

- **Bandit** — Python static application security testing.
- **CodeQL** — semantic SAST for Python and JavaScript/TypeScript.
- **Hadolint** — Dockerfile linting (fails on warnings).
- Least-privilege default `permissions` on workflows; `security-events: write`
  granted only to jobs that upload SARIF.

## Known accepted risks

- Frontend dev/build tooling (e.g. `webpack-dev-server` via `react-scripts`)
  carries advisories. These packages are **never shipped** to the production
  nginx image, so `npm audit` in CI scans production dependencies only
  (`--omit=dev`).
- Base images are pinned by patch tag, not yet by `sha256` digest (tracked on
  the roadmap).
