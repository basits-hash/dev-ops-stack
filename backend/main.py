"""Task Manager API — a production-grade FastAPI service.

Features:
- Async MongoDB access via Motor.
- Prometheus metrics at /metrics and a /health readiness probe.
- Defense-in-depth: rate limiting, security headers, request-size caps,
  strict CORS allowlist, and Pydantic input validation.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from urllib.parse import urlparse, urlunparse

from bson import ObjectId
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)
from pydantic import BaseModel, ConfigDict, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Prometheus metrics ---

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

# --- Rate limiting ---

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])

# --- Database client (set during lifespan startup) ---

db_client: AsyncIOMotorClient | None = None


def _redact_uri(uri: str) -> str:
    """Strip any embedded credentials from a connection URI before logging."""
    try:
        parsed = urlparse(uri)
        host = parsed.hostname or ""
        netloc = f"{host}:{parsed.port}" if parsed.port else host
        return urlunparse(parsed._replace(netloc=netloc))
    except Exception:
        return "<redacted>"


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Open and close the MongoDB connection alongside the app lifecycle."""
    global db_client
    db_client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
    logger.info("MongoDB client initialized: %s", _redact_uri(settings.mongodb_uri))
    try:
        yield
    finally:
        if db_client is not None:
            db_client.close()
            logger.info("MongoDB connection closed")


app = FastAPI(
    title="Task Manager API",
    version=settings.app_version,
    description="Production-grade task manager backend with metrics and hardening.",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=600,
)


# --- Security & request-size middleware ---

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Attach hardened response headers to every response."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers.setdefault(header, value)
        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Reject oversized request bodies before they are read into memory.

    Guards both the declared Content-Length and the actual streamed byte count,
    so chunked Transfer-Encoding uploads cannot bypass the cap.
    """

    def __init__(self, app, max_bytes: int) -> None:
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length is not None:
            try:
                declared = int(content_length)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid Content-Length header"},
                )
            if declared > self.max_bytes:
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Request body too large"},
                )

        # Drain the stream ourselves so a missing/forged Content-Length (e.g.
        # chunked uploads) can't slip an unbounded body past the check.
        body = b""
        async for chunk in request.stream():
            body += chunk
            if len(body) > self.max_bytes:
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Request body too large"},
                )

        # Re-expose the buffered body to downstream handlers.
        request._body = body
        return await call_next(request)


app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestSizeLimitMiddleware, max_bytes=settings.max_request_bytes)


@app.middleware("http")
async def track_metrics(request: Request, call_next):
    """Record request count and latency, keyed by route template not raw path."""
    import time

    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    # Use the matched route path template to keep label cardinality bounded.
    route = request.scope.get("route")
    endpoint = getattr(route, "path", request.url.path)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        status_code=response.status_code,
    ).inc()
    REQUEST_DURATION.labels(method=request.method, endpoint=endpoint).observe(duration)
    return response


# --- Database helper ---


def get_db():
    if db_client is None:
        raise HTTPException(status_code=503, detail="Database not initialized")
    return db_client.get_default_database()


# --- Models ---


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., min_length=1, max_length=500)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    completed: bool


class Task(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    title: str
    completed: bool
    created_at: str


def doc_to_task(doc: dict) -> dict:
    created = doc.get("created_at", "")
    created_str = created.isoformat() if hasattr(created, "isoformat") else str(created)
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "completed": doc.get("completed", False),
        "created_at": created_str,
    }


def parse_object_id(task_id: str) -> ObjectId:
    try:
        return ObjectId(task_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid task ID") from exc


# --- Routes ---


@app.get("/health")
async def health():
    mongo_status = "disconnected"
    if db_client is not None:
        try:
            await db_client.admin.command("ping")
            mongo_status = "connected"
        except Exception:
            mongo_status = "disconnected"
    return {
        "status": "healthy",
        "mongodb": mongo_status,
        "version": settings.app_version,
    }


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/api/tasks", response_model=list[Task])
async def get_tasks():
    db = get_db()
    cursor = db.tasks.find().sort("created_at", -1)
    return [doc_to_task(doc) async for doc in cursor]


@app.post("/api/tasks", status_code=201, response_model=Task)
async def create_task(payload: TaskCreate):
    db = get_db()
    doc = {
        "title": payload.title,
        "completed": False,
        "created_at": datetime.now(timezone.utc),
    }
    result = await db.tasks.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc_to_task(doc)


@app.put("/api/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, payload: TaskUpdate):
    db = get_db()
    oid = parse_object_id(task_id)
    result = await db.tasks.find_one_and_update(
        {"_id": oid},
        {"$set": {"completed": payload.completed}},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return doc_to_task(result)


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    db = get_db()
    oid = parse_object_id(task_id)
    result = await db.tasks.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
