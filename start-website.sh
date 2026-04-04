#!/bin/bash

echo "Starting DevOps Task Manager (Demo Mode — No Docker Required)"
echo "=============================================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed."
    echo "Please install Node.js from: https://nodejs.org/"
    exit 1
fi

echo "Node.js found: $(node --version)"
echo ""
echo "This will run in DEMO MODE (no backend needed)."
echo "All data will be stored in your browser."
echo ""

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Build frontend
echo "Building frontend..."
cd frontend
REACT_APP_DEMO_MODE=true npm run build
cd ..

echo ""
echo "Build complete. Opening in browser..."
echo ""

# Open the built site
if command -v open &> /dev/null; then
    open frontend/build/index.html
elif command -v xdg-open &> /dev/null; then
    xdg-open frontend/build/index.html
else
    echo "Open this file in your browser:"
    echo "  $(pwd)/frontend/build/index.html"
fi

echo ""
echo "Website is running in DEMO MODE."
echo "  - All features work; data saved in browser."
echo "  - To run with the Python FastAPI backend, use Docker:"
echo "      docker compose up -d"
echo "  - Backend API will be at http://localhost:8000"
echo "  - Swagger UI at http://localhost:8000/docs"
