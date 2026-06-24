"""Application configuration loaded and validated from the environment.

All runtime configuration is sourced from environment variables so that no
secrets or environment-specific values are ever committed to source control.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

# Default to a credential-less local URI. In any real deployment MONGODB_URI is
# injected from the environment (see docker-compose.yml / .env.example).
DEFAULT_MONGODB_URI = "mongodb://localhost:27017/taskmanager"
DEFAULT_ALLOWED_ORIGINS = "http://localhost:3000"
DEFAULT_PORT = 8000
DEFAULT_RATE_LIMIT = "100/minute"

# Reject request bodies larger than this to blunt memory-exhaustion attempts.
MAX_REQUEST_BYTES = 16 * 1024  # 16 KiB is generous for a task payload.


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    """Immutable, validated runtime settings."""

    mongodb_uri: str
    allowed_origins: tuple[str, ...]
    port: int
    rate_limit: str
    max_request_bytes: int = MAX_REQUEST_BYTES
    app_version: str = "2.1.0"

    @classmethod
    def from_env(cls) -> "Settings":
        port_raw = os.getenv("PORT", str(DEFAULT_PORT))
        try:
            port = int(port_raw)
        except ValueError as exc:  # fail fast on misconfiguration
            raise ValueError(f"PORT must be an integer, got {port_raw!r}") from exc

        origins = tuple(
            _split_csv(os.getenv("ALLOWED_ORIGINS", DEFAULT_ALLOWED_ORIGINS))
        )
        if not origins:
            raise ValueError("ALLOWED_ORIGINS must contain at least one origin")

        return cls(
            mongodb_uri=os.getenv("MONGODB_URI", DEFAULT_MONGODB_URI),
            allowed_origins=origins,
            port=port,
            rate_limit=os.getenv("RATE_LIMIT", DEFAULT_RATE_LIMIT),
        )


settings = Settings.from_env()
