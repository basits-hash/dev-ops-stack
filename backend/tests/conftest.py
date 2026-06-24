"""Shared pytest fixtures.

A real in-memory MongoDB (mongomock-motor) is wired into the app so tests
exercise the actual route logic end-to-end without a live database.
"""
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

import main


@pytest.fixture
def mock_client():
    """An in-memory async Mongo client whose default DB is `taskmanager`."""
    client = AsyncMongoMockClient()
    # get_default_database() relies on a DB name in the URI; mongomock has none,
    # so we expose a fixed default database for the app helper to resolve.
    client.get_default_database = lambda: client["taskmanager"]
    return client


@pytest_asyncio.fixture
async def client(mock_client):
    """An ASGI test client with the in-memory DB injected, bypassing lifespan."""
    main.db_client = mock_client
    transport = ASGITransport(app=main.app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    main.db_client = None
