# ⚙️ Setup Integration

This guide covers the complete setup and configuration process for Visor Urbano development environment, including database setup, API configuration, and frontend-backend integration.

## 🎯 Prerequisites

Before starting, ensure you have the following installed:

- **Node.js** (v18 or higher)
- **pnpm** (v8 or higher)
- **Python** (v3.9 or higher)
- **PostgreSQL** (v13 or higher) with **PostGIS** extension
- **Git**

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd visor-urbano

# Install dependencies
pnpm install

# Setup environment files
cp apps/backend/.env.example apps/backend/.env
cp apps/frontend/.env.example apps/frontend/.env
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb visor_urbano
createdb visor_urbano_test

# Enable PostGIS extension
psql visor_urbano -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql visor_urbano_test -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Run database migrations
cd apps/backend
python -m alembic upgrade head
```

### 3. Environment Configuration

#### Backend Configuration (`apps/backend/.env`)

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/visor_urbano
DATABASE_URL_TEST=postgresql://username:password@localhost/visor_urbano_test

# Security
SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# File Upload
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=10485760  # 10MB in bytes

# GIS Configuration
POSTGIS_VERSION=3.1
GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Redis (optional - for caching)
REDIS_URL=redis://localhost:6379/0
```

#### Frontend Configuration (`apps/frontend/.env`)

```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_API_VERSION=v1

# Map Configuration
VITE_DEFAULT_MAP_CENTER_LAT=-33.4489
VITE_DEFAULT_MAP_CENTER_LNG=-70.6693
VITE_DEFAULT_MAP_ZOOM=12

# Feature Flags
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true

# External Services (optional)
VITE_MAPBOX_TOKEN=your-mapbox-token
VITE_GOOGLE_MAPS_API_KEY=your-google-maps-key
```

## 🔧 Development Servers

### Start All Services

```bash
# Start all development services in parallel
pnpm dev
```

This command starts:

- **Frontend**: `http://localhost:5173`
- **Backend**: `http://localhost:8000`
- **Storybook**: `http://localhost:6006`
- **Documentation**: `http://localhost:3000`

### Start Individual Services

```bash
# Frontend only
pnpm dev:frontend

# Backend only
pnpm dev:backend

# Storybook only
pnpm storybook

# Documentation only
pnpm dev:docs
```

## 🗄️ Database Management

### Migrations

```bash
# Create a new migration
cd apps/backend
python -m alembic revision --autogenerate -m "Description of changes"

# Apply migrations
python -m alembic upgrade head

# Rollback migrations
python -m alembic downgrade -1
```

### Seeding Data

```bash
# Run database seeds
cd apps/backend
python -m scripts.seed_database

# Seed specific data
python -m scripts.seed_users
python -m scripts.seed_cities
python -m scripts.seed_gis_layers
```

### Backup and Restore

```bash
# Backup database
pg_dump visor_urbano > backup.sql

# Restore database
psql visor_urbano < backup.sql

# Backup with spatial data
pg_dump -Fc visor_urbano > backup.dump
pg_restore -d visor_urbano backup.dump
```

## 🎨 Frontend Development Setup

### Component Development with Storybook

```bash
# Start Storybook
pnpm storybook

# Build Storybook
pnpm build-storybook
```

### Testing Setup

```bash
# Run frontend tests
pnpm test:frontend

# Run tests in watch mode
pnpm test:frontend --watch

# Run tests with coverage
pnpm test:frontend --coverage
```

### Code Quality Tools

```bash
# Lint code
pnpm lint

# Fix linting issues
pnpm lint:fix

# Format code
pnpm format

# Type checking
pnpm type-check
```

## 🐍 Backend Development Setup

### Python Environment

```bash
# Create virtual environment
cd apps/backend
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Backend Services

```bash
# Start FastAPI development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start with specific configuration
uvicorn app.main:app --reload --env-file .env
```

### Backend Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with database
pytest --db-url=postgresql://user:pass@localhost/test_db
```

## 🗺️ GIS Configuration

### PostGIS Setup

```sql
-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Check PostGIS version
SELECT PostGIS_Version();

-- Create spatial index example
CREATE INDEX idx_geometry_gist ON your_table USING GIST (geometry);
```

### Spatial Data Import

```bash
# Import Shapefile
shp2pgsql -I -s 4326 data.shp public.table_name | psql -d visor_urbano

# Import GeoJSON
ogr2ogr -f "PostgreSQL" PG:"dbname=visor_urbano" data.geojson -nln table_name

# Convert coordinate systems
ogr2ogr -t_srs EPSG:4326 -s_srs EPSG:32719 output.shp input.shp
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: pnpm install
      - run: pnpm test:frontend

  test-backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgis/postgis:13-3.1
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pytest
```

## 🐳 Docker Development

### Using Docker Compose

```bash
# Start all services with Docker
docker-compose up -d

# Start specific services
docker-compose up frontend backend

# Rebuild images
docker-compose build

# View logs
docker-compose logs -f backend
```

### Docker Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: ./apps/frontend
    ports:
      - '5173:5173'
    environment:
      - VITE_API_URL=http://localhost:8000

  backend:
    build: ./apps/backend
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/visor_urbano
    depends_on:
      - db

  db:
    image: postgis/postgis:13-3.1
    environment:
      - POSTGRES_DB=visor_urbano
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
psql -l | grep visor_urbano

# Test connection
psql "postgresql://user:pass@localhost/visor_urbano" -c "SELECT version();"
```

#### 2. Frontend Build Issues

```bash
# Clear node_modules and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Clear Vite cache
rm -rf apps/frontend/.vite

# Check Node.js version
node --version  # Should be v18+
```

#### 3. Backend Import Issues

```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check virtual environment
which python
```

#### 4. PostGIS Issues

```sql
-- Check PostGIS installation
SELECT name, default_version,installed_version
FROM pg_available_extensions WHERE name LIKE 'postgis%';

-- Create extension if missing
CREATE EXTENSION IF NOT EXISTS postgis;
```

### Performance Optimization

#### Database Performance

```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM permits WHERE ST_Intersects(geometry, ST_Point(-70.6693, -33.4489));

-- Create spatial indexes
CREATE INDEX CONCURRENTLY idx_permits_geom ON permits USING GIST(geometry);

-- Update table statistics
ANALYZE permits;
```

#### Frontend Performance

```bash
# Analyze bundle size
pnpm build
pnpm analyze

# Optimize images
pnpm optimize-images

# Check for unused dependencies
pnpm depcheck
```

## 📚 Integration Testing

### End-to-End Testing

```bash
# Start all services
pnpm dev

# Run E2E tests
pnpm test:e2e

# Run specific test
pnpm test:e2e --grep "permit creation flow"
```

### API Integration Testing

```python
# Test API integration
import requests

# Test auth flow
auth_response = requests.post('http://localhost:8000/auth/login', {
    'username': 'test',
    'password': 'test'
})
token = auth_response.json()['access_token']

# Test authenticated endpoint
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/permits', headers=headers)
assert response.status_code == 200
```

## 🔗 Related Documentation

- [API Documentation](./api-documentation.md) - Complete API reference
- [API Integration](./api-integration.md) - Frontend-backend integration mapping
- [Development README](./README.md) - General development guidelines

---

This setup guide should get you up and running with the complete Visor Urbano development environment. For specific issues or advanced configuration, refer to the individual service documentation.
