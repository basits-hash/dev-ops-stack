from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from bson import ObjectId
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/taskmanager")
PORT = int(os.getenv("PORT", 8000))

app = FastAPI(title="Task Manager API", version="2.0.0")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
)

db_client: AsyncIOMotorClient = None


@app.on_event("startup")
async def startup():
    global db_client
    db_client = AsyncIOMotorClient(MONGODB_URI)
    logger.info("Connected to MongoDB")


@app.on_event("shutdown")
async def shutdown():
    db_client.close()
    logger.info("MongoDB connection closed")


def get_db():
    return db_client.get_default_database()


# --- Models ---

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)


class TaskUpdate(BaseModel):
    completed: bool


class Task(BaseModel):
    id: str
    title: str
    completed: bool
    created_at: str

    class Config:
        populate_by_name = True


def doc_to_task(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "completed": doc.get("completed", False),
        "created_at": doc.get("created_at", "").isoformat() if hasattr(doc.get("created_at", ""), "isoformat") else str(doc.get("created_at", "")),
    }


# --- Middleware for metrics ---

@app.middleware("http")
async def track_metrics(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
    ).inc()
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)
    return response


# --- Routes ---

@app.get("/health")
async def health():
    try:
        await db_client.admin.command("ping")
        mongo_status = "connected"
    except Exception:
        mongo_status = "disconnected"
    return {
        "status": "healthy",
        "mongodb": mongo_status,
        "version": "2.0.0",
    }


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/api/tasks")
async def get_tasks():
    db = get_db()
    cursor = db.tasks.find().sort("created_at", -1)
    tasks = [doc_to_task(doc) async for doc in cursor]
    return tasks


@app.post("/api/tasks", status_code=201)
async def create_task(payload: TaskCreate):
    from datetime import datetime, timezone
    db = get_db()
    doc = {
        "title": payload.title,
        "completed": False,
        "created_at": datetime.now(timezone.utc),
    }
    result = await db.tasks.insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc_to_task(doc)


@app.put("/api/tasks/{task_id}")
async def update_task(task_id: str, payload: TaskUpdate):
    db = get_db()
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID")
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
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    result = await db.tasks.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
