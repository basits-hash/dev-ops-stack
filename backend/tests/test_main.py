import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch
from bson import ObjectId
from datetime import datetime, timezone

# Patch motor before importing app
import sys
sys.modules.setdefault("motor", MagicMock())
sys.modules.setdefault("motor.motor_asyncio", MagicMock())

with patch("motor.motor_asyncio.AsyncIOMotorClient"):
    from main import app, doc_to_task


@pytest.fixture
def sample_task():
    oid = ObjectId()
    return {
        "_id": oid,
        "title": "Test task",
        "completed": False,
        "created_at": datetime.now(timezone.utc),
    }


@pytest.mark.asyncio
async def test_health_endpoint():
    mock_client = AsyncMock()
    mock_client.admin.command = AsyncMock(return_value={"ok": 1})

    import main as m
    m.db_client = mock_client

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_get_tasks_empty():
    mock_cursor = MagicMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.__aiter__ = AsyncMock(return_value=iter([]))

    mock_collection = MagicMock()
    mock_collection.find.return_value = mock_cursor

    mock_db = MagicMock()
    mock_db.tasks = mock_collection

    mock_client = MagicMock()
    mock_client.get_default_database.return_value = mock_db

    import main as m
    m.db_client = mock_client

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/tasks")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_task(sample_task):
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = sample_task["_id"]

    mock_collection = AsyncMock()
    mock_collection.insert_one = AsyncMock(return_value=mock_insert_result)

    mock_db = MagicMock()
    mock_db.tasks = mock_collection

    mock_client = MagicMock()
    mock_client.get_default_database.return_value = mock_db

    import main as m
    m.db_client = mock_client

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/tasks", json={"title": "Test task"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test task"
    assert data["completed"] is False


@pytest.mark.asyncio
async def test_create_task_empty_title():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/tasks", json={"title": ""})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_delete_task_not_found():
    mock_result = MagicMock()
    mock_result.deleted_count = 0

    mock_collection = AsyncMock()
    mock_collection.delete_one = AsyncMock(return_value=mock_result)

    mock_db = MagicMock()
    mock_db.tasks = mock_collection

    mock_client = MagicMock()
    mock_client.get_default_database.return_value = mock_db

    import main as m
    m.db_client = mock_client

    fake_id = str(ObjectId())
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.delete(f"/api/tasks/{fake_id}")
    assert resp.status_code == 404


def test_doc_to_task():
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
