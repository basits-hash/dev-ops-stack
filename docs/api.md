# API Documentation

## Base URL

```
Local: http://localhost:5000
Production: https://your-domain.com
```

## Authentication

Currently, the API does not require authentication. This will be added in future versions.

## Endpoints

### Health Check

Check the health status of the API.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-20T10:30:00.000Z",
  "uptime": 3600.5,
  "mongodb": "connected"
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is unhealthy

---

### Metrics

Get Prometheus metrics for monitoring.

**Endpoint:** `GET /metrics`

**Response:** Prometheus text format

**Example:**
```
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",route="/api/tasks",status_code="200"} 150
```

---

### Get All Tasks

Retrieve all tasks.

**Endpoint:** `GET /api/tasks`

**Response:**
```json
[
  {
    "_id": "65abc123def456789",
    "title": "Complete DevOps project",
    "completed": false,
    "createdAt": "2026-01-20T10:00:00.000Z"
  },
  {
    "_id": "65abc123def456790",
    "title": "Deploy to production",
    "completed": true,
    "createdAt": "2026-01-20T09:00:00.000Z"
  }
]
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Server error

---

### Create Task

Create a new task.

**Endpoint:** `POST /api/tasks`

**Request Body:**
```json
{
  "title": "New task title"
}
```

**Response:**
```json
{
  "_id": "65abc123def456791",
  "title": "New task title",
  "completed": false,
  "createdAt": "2026-01-20T11:00:00.000Z"
}
```

**Status Codes:**
- `201 Created` - Task created successfully
- `400 Bad Request` - Invalid request body
- `500 Internal Server Error` - Server error

**Validation:**
- `title` is required
- `title` must be a non-empty string

---

### Update Task

Update an existing task (toggle completion status).

**Endpoint:** `PUT /api/tasks/:id`

**URL Parameters:**
- `id` - Task ID

**Request Body:**
```json
{
  "completed": true
}
```

**Response:**
```json
{
  "_id": "65abc123def456791",
  "title": "New task title",
  "completed": true,
  "createdAt": "2026-01-20T11:00:00.000Z"
}
```

**Status Codes:**
- `200 OK` - Task updated successfully
- `404 Not Found` - Task not found
- `400 Bad Request` - Invalid request body
- `500 Internal Server Error` - Server error

---

### Delete Task

Delete a task.

**Endpoint:** `DELETE /api/tasks/:id`

**URL Parameters:**
- `id` - Task ID

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

**Status Codes:**
- `200 OK` - Task deleted successfully
- `404 Not Found` - Task not found
- `400 Bad Request` - Invalid task ID
- `500 Internal Server Error` - Server error

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error message describing what went wrong"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. This will be added in future versions.

## CORS

CORS is enabled for all origins in development. In production, configure specific origins.

## Examples

### Using cURL

**Create a task:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Kubernetes"}'
```

**Get all tasks:**
```bash
curl http://localhost:5000/api/tasks
```

**Update a task:**
```bash
curl -X PUT http://localhost:5000/api/tasks/65abc123def456791 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

**Delete a task:**
```bash
curl -X DELETE http://localhost:5000/api/tasks/65abc123def456791
```

### Using JavaScript (Axios)

```javascript
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

// Create task
const createTask = async (title) => {
  const response = await axios.post(`${API_URL}/tasks`, { title });
  return response.data;
};

// Get all tasks
const getTasks = async () => {
  const response = await axios.get(`${API_URL}/tasks`);
  return response.data;
};

// Update task
const updateTask = async (id, completed) => {
  const response = await axios.put(`${API_URL}/tasks/${id}`, { completed });
  return response.data;
};

// Delete task
const deleteTask = async (id) => {
  const response = await axios.delete(`${API_URL}/tasks/${id}`);
  return response.data;
};
```

### Using Python (requests)

```python
import requests

API_URL = 'http://localhost:5000/api'

# Create task
response = requests.post(f'{API_URL}/tasks', json={'title': 'New task'})
task = response.json()

# Get all tasks
response = requests.get(f'{API_URL}/tasks')
tasks = response.json()

# Update task
response = requests.put(f'{API_URL}/tasks/{task["_id"]}', json={'completed': True})
updated_task = response.json()

# Delete task
response = requests.delete(f'{API_URL}/tasks/{task["_id"]}')
result = response.json()
```

## WebSocket Support

Not currently implemented. Future versions may include WebSocket support for real-time updates.

## Versioning

Current version: v1

Future API versions will be prefixed: `/api/v2/tasks`

## Monitoring

Monitor API performance using:
- Prometheus metrics at `/metrics`
- Health checks at `/health`
- Application logs

## Support

For API issues or questions:
- Check server logs: `docker-compose logs backend`
- Review error messages in response
- Check network connectivity
- Verify MongoDB is running
