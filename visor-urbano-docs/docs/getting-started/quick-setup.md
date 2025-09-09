# Quick Setup

Get Visor Urbano running quickly on your local development environment.

## Prerequisites

- Node.js 18+ and pnpm
- Python 3.9+ and pip
- PostgreSQL 14+
- Docker (optional, for containerized setup)

## Clone Repository

```bash
git clone https://github.com/Delivery-Associates/visor-urbano.git
cd visor-urbano
```

## Option 1: Local Development Setup

### 1. Install Dependencies

```bash
# Install all dependencies
pnpm install

# Backend dependencies
cd apps/backend
pip install -r requirements.txt
cd ../..
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb visor_urbano

# Run migrations
cd apps/backend
alembic upgrade head
cd ../..
```

### 3. Environment Configuration

```bash
# Copy environment templates
cp apps/backend/.env.example apps/backend/.env
cp apps/frontend/.env.example apps/frontend/.env

# Edit configuration files as needed
```

### 4. Start Development Servers

```bash
# Start all services
pnpm dev

# Or start individually:
# Frontend: pnpm dev:frontend
# Backend: pnpm dev:backend
```

## Option 2: Docker Setup

```bash
# Start with Docker Compose
docker-compose up -d

# Initialize database
docker-compose exec backend alembic upgrade head
```

## Verify Installation

1. Frontend: [http://localhost:3000](http://localhost:3000)
2. Backend API: [http://localhost:8000](http://localhost:8000)
3. API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## Next Steps

- Review [System Requirements](./system-requirements.md)
- Explore [API Integration Guide](../development/api-integration.md)
- Check [Implementation Guide](../implementation/step-by-step-guide.md)
