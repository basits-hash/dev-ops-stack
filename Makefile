.PHONY: help build start stop restart logs clean test test-frontend lint smoke

help:
	@echo "DevOps Task Manager"
	@echo ""
	@echo "  make build         - Build Docker images"
	@echo "  make start         - Start all services (detached)"
	@echo "  make stop          - Stop all services"
	@echo "  make restart       - Restart all services"
	@echo "  make logs          - Tail logs"
	@echo "  make clean         - Stop and remove containers + volumes"
	@echo "  make test          - Run backend tests with coverage"
	@echo "  make test-frontend - Run frontend tests"
	@echo "  make lint          - Lint backend (ruff) and frontend (eslint)"
	@echo "  make smoke         - Bring up the stack and run the smoke test"
	@echo ""

build:
	docker compose build

start:
	docker compose up -d
	@echo "Frontend:     http://localhost:3000"
	@echo "Backend:      http://localhost:8000"
	@echo "API Docs:     http://localhost:8000/docs"
	@echo "Prometheus:   http://localhost:9090"
	@echo "Grafana:      http://localhost:3002"
	@echo "Alertmanager: http://localhost:9093"

stop:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

clean:
	docker compose down -v

test:
	cd backend && pip install -r requirements-dev.txt -q && pytest -v --tb=short --cov=. --cov-report=term-missing

test-frontend:
	cd frontend && npm ci && CI=true npm test -- --watchAll=false

lint:
	cd backend && ruff check .
	cd frontend && npx eslint src --max-warnings=0

smoke:
	./scripts/smoke-test.sh
