.PHONY: help setup install build start stop restart logs clean test deploy-k8s deploy-pages

# Default target
help:
	@echo "DevOps Task Manager - Available Commands:"
	@echo ""
	@echo "  make setup         - Set up development environment"
	@echo "  make install       - Install dependencies"
	@echo "  make build         - Build Docker images"
	@echo "  make start         - Start all services"
	@echo "  make stop          - Stop all services"
	@echo "  make restart       - Restart all services"
	@echo "  make logs          - View logs"
	@echo "  make clean         - Clean up containers and volumes"
	@echo "  make test          - Run tests"
	@echo "  make deploy-k8s    - Deploy to Kubernetes"
	@echo "  make deploy-pages  - Deploy to GitHub Pages"
	@echo ""

setup:
	@echo "🔧 Setting up development environment..."
	./scripts/setup.sh

install:
	@echo "📦 Installing dependencies..."
	cd backend && npm install
	cd frontend && npm install

build:
	@echo "🏗️  Building Docker images..."
	docker-compose build

start:
	@echo "🚀 Starting all services..."
	docker-compose up -d
	@echo ""
	@echo "✅ Services started!"
	@echo "Frontend:    http://localhost:3000"
	@echo "Backend:     http://localhost:5000"
	@echo "Prometheus:  http://localhost:9090"
	@echo "Grafana:     http://localhost:3001 (admin/admin)"

stop:
	@echo "🛑 Stopping all services..."
	docker-compose down

restart:
	@echo "🔄 Restarting all services..."
	docker-compose restart

logs:
	@echo "📋 Viewing logs..."
	docker-compose logs -f

clean:
	@echo "🧹 Cleaning up..."
	./scripts/cleanup.sh

test:
	@echo "🧪 Running tests..."
	./scripts/test.sh

deploy-k8s:
	@echo "☸️  Deploying to Kubernetes..."
	kubectl apply -f k8s/
	@echo "✅ Deployed to Kubernetes!"

deploy-pages:
	@echo "🚀 Deploying to GitHub Pages..."
	./scripts/deploy-github-pages.sh

dev-backend:
	@echo "🔧 Starting backend in development mode..."
	cd backend && npm run dev

dev-frontend:
	@echo "🔧 Starting frontend in development mode..."
	cd frontend && npm start

status:
	@echo "📊 Service Status:"
	@docker-compose ps
