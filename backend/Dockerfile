# syntax=docker/dockerfile:1
# Multi-stage build for the Python FastAPI backend.
# Base image pinned to an explicit patch version for reproducible builds.
# Hardening roadmap: pin by sha256 digest once CI publishes a verified digest.
FROM python:3.12.8-slim AS builder

WORKDIR /app

# Build-only dependencies; removed from the final image.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- Production stage: minimal, non-root, read-only friendly ---
FROM python:3.12.8-slim

LABEL org.opencontainers.image.title="task-manager-backend" \
      org.opencontainers.image.description="FastAPI backend for the DevOps Task Manager" \
      org.opencontainers.image.source="https://github.com/basitsherazi/dev-ops-stack" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Copy the pre-built dependency tree from the builder stage.
COPY --from=builder /install /usr/local

# Copy application source (config first so layer caching stays effective).
COPY config.py main.py ./

# Run as a dedicated unprivileged user (CIS Docker 4.1).
RUN addgroup --gid 1001 appgroup \
    && adduser --uid 1001 --gid 1001 --no-create-home --disabled-password appuser
USER 1001:1001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://localhost:8000/health').status==200 else sys.exit(1)"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
