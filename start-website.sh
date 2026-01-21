#!/bin/bash

echo "🚀 Starting DevOps Task Manager (No Docker Required!)"
echo "======================================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "📥 Please install Node.js from: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"
echo ""

# Check if MongoDB is needed
echo "⚠️  This will run in DEMO MODE (no database needed)"
echo "   All data will be stored in your browser"
echo ""

# Install frontend dependencies
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Build frontend for local preview
echo "🏗️  Building frontend..."
cd frontend
REACT_APP_DEMO_MODE=true npm run build
echo ""
echo "✅ Build complete!"
echo ""
echo "🌐 Opening website in your browser..."
echo ""

# Open the built site in default browser
if command -v open &> /dev/null; then
    # macOS
    open build/index.html
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open build/index.html
else
    echo "📂 Open this file in your browser:"
    echo "   $(pwd)/build/index.html"
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  ✅ Website is now running in your browser!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "The website is running in DEMO MODE:"
echo "  - All features work!"
echo "  - Data saved in browser"
echo "  - No backend needed"
echo ""
echo "To run with full backend, install Docker and run:"
echo "  docker compose up -d"
