"""End-to-end API tests against an in-memory MongoDB.

Covers health, metrics, the full task CRUD lifecycle, input validation,
error paths, and security hardening (headers + request-size limits).
"""
from datetime import datetime, timezone

import pytest
from bson import ObjectId

from main import doc_to_task


# --- Helper unit tests ---


def test_doc_to_task_with_datetime():
    oid = ObjectId()
    doc = {
        "_id": oid,
        "title": "Sample",
        "completed": True,
        "created_at": datetime(2024, 1, 1, tzinfo=timezone.utc),
    }
    result = doc_to_task(doc)
    assert result["id"] == str(oid)
    assert result["title"] == "Sample"
    assert result["completed"] is True
    assert result["created_at"].startswith("2024-01-01")


def test_doc_to_task_defaults_completed_false():
    doc = {"_id": ObjectId(), "title": "No completed field"}
    result = doc_to_task(doc)
    assert result["completed"] is False
    assert result["created_at"] == ""


# --- Health & metrics ---


@pytest.mark.asyncio
async def test_health_endpoint_connected(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["mongodb"] == "connected"
    assert "version" in data


@pytest.mark.asyncio
async def test_metrics_endpoint_exposes_prometheus(client):
    # Generate traffic so the counter has a sample to expose.
    await client.get("/health")
    resp = await client.get("/metrics")
    assert resp.status_code == 200
    assert "http_requests_total" in resp.text
    assert "http_request_duration_seconds" in resp.text


# --- Task CRUD lifecycle ---


@pytest.mark.asyncio
async def test_get_tasks_empty(client):
    resp = await client.get("/api/tasks")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_then_list_task(client):
    create = await client.post("/api/tasks", json={"title": "Write tests"})
    assert create.status_code == 201
    created = create.json()
    assert created["title"] == "Write tests"
    assert created["completed"] is False
    assert created["id"]

    listing = await client.get("/api/tasks")
    assert listing.status_code == 200
    tasks = listing.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == created["id"]


@pytest.mark.asyncio
async def test_update_task_completed(client):
    created = (await client.post("/api/tasks", json={"title": "Toggle me"})).json()
    resp = await client.put(f"/api/tasks/{created['id']}", json={"completed": True})
    assert resp.status_code == 200
    assert resp.json()["completed"] is True


@pytest.mark.asyncio
async def test_delete_task(client):
    created = (await client.post("/api/tasks", json={"title": "Delete me"})).json()
    resp = await client.delete(f"/api/tasks/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Task deleted successfully"
    # Confirm it is gone.
    listing = await client.get("/api/tasks")
    assert listing.json() == []


# --- Validation & error paths ---


@pytest.mark.asyncio
async def test_create_task_empty_title_rejected(client):
    resp = await client.post("/api/tasks", json={"title": ""})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_create_task_extra_field_rejected(client):
    resp = await client.post(
        "/api/tasks", json={"title": "ok", "completed": True}
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_update_invalid_object_id(client):
    resp = await client.put("/api/tasks/not-a-valid-id", json={"completed": True})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Invalid task ID"


@pytest.mark.asyncio
async def test_update_nonexistent_task(client):
    fake_id = str(ObjectId())
    resp = await client.put(f"/api/tasks/{fake_id}", json={"completed": True})
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_task(client):
    fake_id = str(ObjectId())
    resp = await client.delete(f"/api/tasks/{fake_id}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_invalid_object_id(client):
    resp = await client.delete("/api/tasks/bad-id")
    assert resp.status_code == 400


# --- Security hardening ---


@pytest.mark.asyncio
async def test_security_headers_present(client):
    resp = await client.get("/health")
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in resp.headers
    assert "Referrer-Policy" in resp.headers


@pytest.mark.asyncio
async def test_oversized_request_rejected(client):
    huge_title = "x" * 20000  # exceeds the 16 KiB body cap
    resp = await client.post("/api/tasks", json={"title": huge_title})
    assert resp.status_code == 413
    assert resp.json()["detail"] == "Request body too large"
