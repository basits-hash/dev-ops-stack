"""Unit tests for environment-driven configuration."""
import pytest

from config import Settings


def test_settings_from_env_defaults(monkeypatch):
    for var in ("PORT", "ALLOWED_ORIGINS", "MONGODB_URI", "RATE_LIMIT"):
        monkeypatch.delenv(var, raising=False)
    settings = Settings.from_env()
    assert settings.port == 8000
    assert settings.allowed_origins == ("http://localhost:3000",)
    assert settings.rate_limit == "100/minute"


def test_settings_parses_csv_origins(monkeypatch):
    monkeypatch.setenv("ALLOWED_ORIGINS", "http://a.com, http://b.com ,")
    settings = Settings.from_env()
    assert settings.allowed_origins == ("http://a.com", "http://b.com")


def test_settings_rejects_invalid_port(monkeypatch):
    monkeypatch.setenv("PORT", "not-a-number")
    with pytest.raises(ValueError, match="PORT must be an integer"):
        Settings.from_env()


def test_settings_rejects_empty_origins(monkeypatch):
    monkeypatch.setenv("ALLOWED_ORIGINS", " , ")
    with pytest.raises(ValueError, match="at least one origin"):
        Settings.from_env()
