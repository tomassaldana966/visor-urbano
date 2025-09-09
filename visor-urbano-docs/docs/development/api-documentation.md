# API Documentation

Complete reference for Visor Urbano REST API endpoints.

## Overview

The Visor Urbano API provides RESTful endpoints for municipal urban planning management. All endpoints are documented using OpenAPI/Swagger standards.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.your-domain.com`

## Authentication

### JWT Authentication

```bash
# Login to get access token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Use token in subsequent requests
curl -X GET "http://localhost:8000/api/projects" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### API Key Authentication

```bash
# Using API key in header
curl -X GET "http://localhost:8000/api/projects" \
  -H "X-API-Key: YOUR_API_KEY"
```

## Core Endpoints

### Projects API

#### List Projects

```http
GET /api/projects
```

**Query Parameters:**

- `city` (string): Filter by city
- `status` (string): Filter by project status
- `limit` (integer): Number of results (default: 20)
- `offset` (integer): Pagination offset

**Response:**

```json
{
  "projects": [
    {
      "id": "uuid",
      "name": "Project Name",
      "city": "Santiago",
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 50,
  "limit": 20,
  "offset": 0
}
```

#### Get Project

```http
GET /api/projects/{project_id}
```

#### Create Project

```http
POST /api/projects
```

**Request Body:**

```json
{
  "name": "New Project",
  "description": "Project description",
  "city": "Santiago",
  "location": {
    "type": "Point",
    "coordinates": [-70.6693, -33.4489]
  }
}
```

#### Update Project

```http
PUT /api/projects/{project_id}
```

#### Delete Project

```http
DELETE /api/projects/{project_id}
```

### Procedures API (Trámites)

#### List Procedures

```http
GET /api/procedures
```

#### Get Procedure

```http
GET /api/procedures/{procedure_id}
```

#### Create Procedure

```http
POST /api/procedures
```

#### Update Procedure Status

```http
PATCH /api/procedures/{procedure_id}/status
```

### Documents API

#### Upload Document

```http
POST /api/documents
Content-Type: multipart/form-data
```

#### Download Document

```http
GET /api/documents/{document_id}/download
```

#### List Documents

```http
GET /api/documents
```

### Users API

#### List Users

```http
GET /api/users
```

#### Create User

```http
POST /api/users
```

#### Update User

```http
PUT /api/users/{user_id}
```

### Geographic Data API

#### Get Geographic Boundaries

```http
GET /api/geography/boundaries
```

#### Get Zoning Information

```http
GET /api/geography/zoning
```

#### Get Land Use Data

```http
GET /api/geography/land-use
```

## WebSocket Endpoints

### Real-time Updates

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');

// Listen for project updates
ws.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log('Project update:', data);
};
```

## Error Handling

### Standard Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "name",
      "reason": "Field is required"
    }
  }
}
```

### Common Error Codes

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Rate Limiting

- **Public endpoints**: 100 requests per minute
- **Authenticated endpoints**: 1000 requests per minute
- **File uploads**: 10 requests per minute

## API Versioning

The API uses URL versioning:

- Current version: `v1`
- Base path: `/v1/`

## Interactive Documentation

Access the interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Schema**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## SDK and Client Libraries

### Python Client

```python
from visor_urbano import VisorUrbanoClient

client = VisorUrbanoClient(
    base_url="http://localhost:8000",
    api_key="your-api-key"
)

# List projects
projects = client.projects.list(city="Santiago")

# Create project
project = client.projects.create({
    "name": "New Project",
    "city": "Santiago"
})
```

### JavaScript Client

```javascript
import { VisorUrbanoAPI } from '@visor-urbano/api-client';

const api = new VisorUrbanoAPI({
  baseURL: 'http://localhost:8000',
  apiKey: 'your-api-key',
});

// List projects
const projects = await api.projects.list({ city: 'Santiago' });

// Create project
const project = await api.projects.create({
  name: 'New Project',
  city: 'Santiago',
});
```

## Data Models

### Project Model

```json
{
  "id": "string (uuid)",
  "name": "string",
  "description": "string",
  "city": "string",
  "status": "draft|active|completed|cancelled",
  "location": {
    "type": "Point",
    "coordinates": [longitude, latitude]
  },
  "created_at": "string (datetime)",
  "updated_at": "string (datetime)",
  "created_by": "string (uuid)"
}
```

### Procedure Model

```json
{
  "id": "string (uuid)",
  "project_id": "string (uuid)",
  "type": "building_permit|land_use|environmental",
  "status": "pending|approved|rejected|in_review",
  "submitted_at": "string (datetime)",
  "documents": ["string (uuid)"],
  "notes": "string"
}
```

## Testing

### API Testing with curl

```bash
# Test authentication
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'

# Test project creation
curl -X POST "http://localhost:8000/api/projects" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name": "Test Project", "city": "Santiago"}'
```

### Integration Testing

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_project():
    response = client.post(
        "/api/projects",
        json={"name": "Test Project", "city": "Santiago"},
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Project"
```

## Performance

### Optimization Tips

1. **Use pagination** for large result sets
2. **Filter data** using query parameters
3. **Cache responses** for static data
4. **Use compression** for large payloads

### Monitoring

Monitor API performance using:

- Response times
- Error rates
- Request volumes
- Database query performance

## Security

### Best Practices

1. Always use HTTPS in production
2. Validate all input data
3. Implement rate limiting
4. Use proper authentication
5. Log security events

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## Next Steps

- Explore [API Integration Guide](./api-integration.md)
- Review [Frontend Routes](../../../apps/frontend/app/routes.ts)
- Check [Development Setup](./setup-integration.md)
