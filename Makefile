.PHONY: help build start stop restart logs clean test

help:
	@echo "DevOps Task Manager"
	@echo ""
	@echo "  make build    - Build Docker images"
	@echo "  make start    - Start all services"
	@echo "  make stop     - Stop all services"
	@echo "  make restart  - Restart all services"
	@echo "  make logs     - Tail logs"
	@echo "  make clean    - Stop and remove containers + volumes"
	@echo "  make test     - Run backend tests"
	@echo ""

build:
	docker-compose build

start:
	docker-compose up -d
	@echo "Frontend:   http://localhost:3000"
	@echo "Backend:    http://localhost:8000"
	@echo "API Docs:   http://localhost:8000/docs"
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana:    http://localhost:3001 (admin/admin)"

stop:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

clean:
	docker-compose down -v

test:
	cd backend && pip install -r requirements-dev.txt -q && pytest -v --tb=short
