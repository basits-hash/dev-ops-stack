#!/usr/bin/env bash
# Smoke test: bring up the full stack and verify every service responds.
# Usage: ./scripts/smoke-test.sh
# Requires: docker compose, curl. Reads credentials from .env (or env vars).
set -euo pipefail

cd "$(dirname "$0")/.."

# Fail fast if required secrets are missing.
: "${MONGO_PASSWORD:?Set MONGO_PASSWORD (or source .env) before running}"
: "${GRAFANA_PASSWORD:?Set GRAFANA_PASSWORD (or source .env) before running}"

RETRIES=30
SLEEP=5

wait_for() {
  local name="$1" url="$2" expect="${3:-200}"
  echo "Waiting for ${name} (${url})..."
  for i in $(seq 1 "${RETRIES}"); do
    code=$(curl -s -o /dev/null -w "%{http_code}" "${url}" || true)
    if [ "${code}" = "${expect}" ]; then
      echo "  OK ${name} -> ${code}"
      return 0
    fi
    sleep "${SLEEP}"
  done
  echo "  FAIL ${name} did not return ${expect} (last: ${code:-none})"
  return 1
}

cleanup() {
  echo "Tearing down stack..."
  docker compose down -v >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "Building and starting the stack..."
docker compose up -d --build

# Core service health checks.
wait_for "backend health"   "http://localhost:8000/health"
wait_for "backend metrics"  "http://localhost:8000/metrics"
wait_for "frontend"         "http://localhost:3000/"
wait_for "prometheus"       "http://localhost:9090/-/healthy"
wait_for "grafana"          "http://localhost:3002/api/health"
wait_for "alertmanager"     "http://localhost:9093/-/healthy"

# Functional check: create a task and confirm it comes back.
echo "Creating a task via the API..."
created=$(curl -s -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title":"smoke-test task"}')
echo "  Created: ${created}"
echo "${created}" | grep -q "smoke-test task" || {
  echo "  FAIL task was not created"
  exit 1
}

echo ""
echo "Smoke test PASSED — all services healthy and API functional."
