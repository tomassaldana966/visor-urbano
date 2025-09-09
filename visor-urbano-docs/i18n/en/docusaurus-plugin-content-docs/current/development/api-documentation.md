# 📚 API Documentation

This section provides comprehensive documentation for the Visor Urbano backend API, including authentication, endpoints, and integration patterns.

## 🎯 Overview

The Visor Urbano API is built with FastAPI and provides RESTful endpoints for:

- **Geographic Information Systems (GIS)** operations
- **Urban permit management** and workflows
- **Multi-tenant city configuration**
- **User authentication and authorization**
- **Document and file management**

## 🔐 Authentication

### Authentication Methods

The API supports multiple authentication methods:

1. **Bearer Token Authentication**

   ```bash
   Authorization: Bearer <your-token>
   ```

2. **Session-based Authentication**
   - Cookie-based for web applications
   - Session management through FastAPI

### Getting Access Tokens

```python
# Example: Login to get access token
import requests

response = requests.post('http://localhost:8000/auth/login', {
    'username': 'your_username',
    'password': 'your_password'
})

token = response.json()['access_token']
```

## 📡 API Endpoints

### Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com/api`

### Core Endpoints

#### Authentication Endpoints

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| `POST` | `/auth/login`    | User login            |
| `POST` | `/auth/logout`   | User logout           |
| `POST` | `/auth/register` | User registration     |
| `GET`  | `/auth/me`       | Get current user info |
| `POST` | `/auth/refresh`  | Refresh access token  |

#### GIS Endpoints

| Method | Endpoint                 | Description              |
| ------ | ------------------------ | ------------------------ |
| `GET`  | `/gis/layers`            | Get available GIS layers |
| `GET`  | `/gis/layers/{layer_id}` | Get specific layer data  |
| `POST` | `/gis/query`             | Spatial query operations |
| `GET`  | `/gis/geometry/{id}`     | Get geometry by ID       |

#### Permit Management

| Method   | Endpoint               | Description        |
| -------- | ---------------------- | ------------------ |
| `GET`    | `/permits`             | List permits       |
| `POST`   | `/permits`             | Create new permit  |
| `GET`    | `/permits/{permit_id}` | Get permit details |
| `PUT`    | `/permits/{permit_id}` | Update permit      |
| `DELETE` | `/permits/{permit_id}` | Delete permit      |

#### City Configuration

| Method | Endpoint            | Description               |
| ------ | ------------------- | ------------------------- |
| `GET`  | `/cities`           | List configured cities    |
| `GET`  | `/cities/{city_id}` | Get city configuration    |
| `POST` | `/cities`           | Create city configuration |
| `PUT`  | `/cities/{city_id}` | Update city configuration |

## 🔗 Interactive Documentation

### Swagger UI

Access the complete interactive API documentation at:

- **Local Development**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

The Swagger interface provides:

- **Complete endpoint listing** with parameters
- **Request/response schemas** with examples
- **Try it out functionality** for testing
- **Authentication testing** capabilities

### API Integration Mapping

For a complete view of how API endpoints integrate with frontend routes and UI components, see the [API Integration documentation](./api-integration.md).

## 🛠️ Development Setup

### Running the API Locally

```bash
# Start the backend development server
cd apps/backend
pnpm dev:backend

# API will be available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

### Environment Configuration

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/visor_urbano
DATABASE_URL_TEST=postgresql://user:password@localhost/visor_urbano_test

# Authentication
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# GIS Configuration
POSTGIS_VERSION=3.1
GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

# File Storage
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=10485760  # 10MB
```

## 📊 Data Models

### Core Models

#### User Model

```python
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "is_active": "boolean",
  "created_at": "datetime",
  "role": "string",
  "city_id": "integer"
}
```

#### Permit Model

```python
{
  "id": "integer",
  "permit_type": "string",
  "status": "string",
  "applicant_name": "string",
  "property_address": "string",
  "geometry": "GeoJSON",
  "documents": "array",
  "created_at": "datetime",
  "updated_at": "datetime",
  "city_id": "integer"
}
```

#### GIS Layer Model

```python
{
  "id": "integer",
  "name": "string",
  "layer_type": "string",
  "style_config": "object",
  "data_source": "string",
  "is_visible": "boolean",
  "z_index": "integer",
  "city_id": "integer"
}
```

## 🔍 Common API Patterns

### Pagination

Most list endpoints support pagination:

```python
# Request
GET /permits?page=1&size=20&sort=created_at&order=desc

# Response
{
  "items": [...],
  "total": 150,
  "page": 1,
  "size": 20,
  "pages": 8
}
```

### Filtering

Use query parameters for filtering:

```python
# Filter permits by status and type
GET /permits?status=pending&permit_type=construction

# Date range filtering
GET /permits?created_after=2024-01-01&created_before=2024-12-31
```

### Spatial Queries

GIS endpoints support spatial operations:

```python
# Point-in-polygon query
POST /gis/query
{
  "operation": "intersects",
  "geometry": {
    "type": "Point",
    "coordinates": [-70.6693, -33.4489]
  },
  "layers": ["zoning", "districts"]
}
```

## 🚨 Error Handling

### Standard Error Response

```python
{
  "detail": "Error description",
  "error_code": "VALIDATION_ERROR",
  "field_errors": {
    "field_name": ["Field-specific error message"]
  }
}
```

### HTTP Status Codes

| Code  | Meaning               | Usage                    |
| ----- | --------------------- | ------------------------ |
| `200` | OK                    | Successful GET, PUT      |
| `201` | Created               | Successful POST          |
| `204` | No Content            | Successful DELETE        |
| `400` | Bad Request           | Validation errors        |
| `401` | Unauthorized          | Authentication required  |
| `403` | Forbidden             | Insufficient permissions |
| `404` | Not Found             | Resource not found       |
| `422` | Unprocessable Entity  | Validation errors        |
| `500` | Internal Server Error | Server errors            |

## 🧪 Testing the API

### Using curl

```bash
# Login and get token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'

# Use token for authenticated requests
curl -X GET "http://localhost:8000/permits" \
  -H "Authorization: Bearer <your-token>"
```

### Using Python

```python
import requests

# Login
response = requests.post('http://localhost:8000/auth/login', {
    'username': 'test',
    'password': 'test'
})
token = response.json()['access_token']

# Authenticated request
headers = {'Authorization': f'Bearer {token}'}
permits = requests.get('http://localhost:8000/permits', headers=headers)
```

## 📋 API Best Practices

### Request Guidelines

1. **Always include appropriate headers**

   ```
   Content-Type: application/json
   Authorization: Bearer <token>
   ```

2. **Use proper HTTP methods**

   - GET for reading data
   - POST for creating resources
   - PUT for updating resources
   - DELETE for removing resources

3. **Handle errors gracefully**
   - Check response status codes
   - Parse error messages
   - Implement retry logic for transient errors

### Performance Tips

1. **Use pagination for large datasets**
2. **Implement caching for static data**
3. **Optimize spatial queries with proper indexing**
4. **Use efficient serialization for large responses**

## 🔗 Related Documentation

- [API Integration Guide](./api-integration.md) - Complete frontend-backend integration
- [Setup Integration](./setup-integration.md) - Development environment configuration
- [Development README](./README.md) - General development guide

---

For the most up-to-date API documentation, always refer to the Swagger interface at [http://localhost:8000/docs](http://localhost:8000/docs) during development.
