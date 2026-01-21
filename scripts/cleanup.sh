#!/bin/bash

# Cleanup script

set -e

echo "🧹 Cleaning up..."

# Stop and remove containers
docker-compose down -v

# Remove Docker images (optional - uncomment if needed)
# docker rmi $(docker images -q task-manager-*)

echo "✓ Cleanup complete!"
