#!/bin/bash

# Testing script - runs all tests

set -e

echo "🧪 Running tests..."

# Backend tests
echo "Testing backend..."
cd backend
npm test

# Frontend tests
echo "Testing frontend..."
cd ../frontend
npm test -- --passWithNoTests --watchAll=false

cd ..

echo "✅ All tests passed!"
