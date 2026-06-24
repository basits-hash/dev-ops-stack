# syntax=docker/dockerfile:1
# Multi-stage build for the React frontend, served by nginx-unprivileged.
# Base images pinned to explicit patch versions for reproducible builds.

# --- Build stage ---
FROM node:26.3.1-alpine AS build

WORKDIR /app

# Install with the committed lockfile for reproducible builds; fail the build
# on high/critical production CVEs.
COPY package.json package-lock.json ./
RUN npm ci --no-fund && npm audit --omit=dev --audit-level=high

# Build the production bundle.
COPY . .
RUN npm run build


# --- Production stage: unprivileged nginx ---
# nginxinc/nginx-unprivileged runs as a non-root user (uid 101) and listens
# on an unprivileged port by default — no setuid binaries needed at runtime.
FROM nginxinc/nginx-unprivileged:1.27-alpine

LABEL org.opencontainers.image.title="task-manager-frontend" \
      org.opencontainers.image.description="React frontend for the DevOps Task Manager" \
      org.opencontainers.image.source="https://github.com/basitsherazi/dev-ops-stack" \
      org.opencontainers.image.licenses="MIT"

# Serve the built static assets.
COPY --from=build /app/build /usr/share/nginx/html

# Custom server config (listens on 8080 as the unprivileged image expects).
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Already non-root (uid 101) in the base image; declared for clarity.
USER 101

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD ["wget", "--quiet", "--tries=1", "--spider", "http://localhost:8080/"]

CMD ["nginx", "-g", "daemon off;"]
