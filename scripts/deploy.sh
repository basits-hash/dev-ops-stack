#!/bin/bash

# Deployment script for Task Manager application

set -e

echo "🚀 Starting deployment process..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

print_status "Docker is running"

# Build Docker images
print_status "Building Docker images..."
docker-compose build --no-cache

# Start services
print_status "Starting services..."
docker-compose up -d

# Wait for services to be healthy
print_status "Waiting for services to be healthy..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    print_status "All services are running"
else
    print_error "Some services failed to start"
    docker-compose logs
    exit 1
fi

# Display service URLs
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  🎉 Deployment Successful!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "  Frontend:    http://localhost:3000"
echo "  Backend API: http://localhost:5000"
echo "  Prometheus:  http://localhost:9090"
echo "  Grafana:     http://localhost:3001 (admin/admin)"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

print_status "Deployment complete!"
