# Development Documentation

Development documentation and guides for Visor Urbano.

## Overview

This development section contains comprehensive guides for developers working with Visor Urbano, including:

- API integration patterns
- Setup and configuration
- Frontend component development
- Backend service architecture

## Quick Links

- [API Integration Guide](./api-integration.md) - Complete mapping of routes, components, and endpoints
- [Setup Integration](./setup-integration.md) - Development environment configuration

## Development Workflow

1. **Environment Setup**: Configure your development environment
2. **API Integration**: Understand the API endpoints and frontend routes
3. **Component Development**: Build and test UI components
4. **Testing**: Run unit and integration tests
5. **Documentation**: Update relevant documentation

## Architecture

Visor Urbano follows a modern full-stack architecture:

- **Frontend**: React with TypeScript, Vite, and React Router
- **Backend**: FastAPI with Python, PostgreSQL database
- **Components**: Storybook for component documentation
- **Testing**: Vitest for frontend, pytest for backend

## Getting Started

1. Review [System Requirements](../getting-started/system-requirements.md)
2. Follow [Quick Setup](../getting-started/quick-setup.md)
3. Explore [API Integration](./api-integration.md)

## 🚀 Quick Start

### Start Complete Environment

```bash
# Terminal 1: Backend con Swagger
cd apps/backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend con Storybook
cd apps/frontend
pnpm run dev  # Inicia React Router + Storybook en puerto 6006

# Terminal 3: Documentación
pnpm run docs:dev  # Puerto 3000
```

### Generar Documentación Automática

```bash
# Opción 1: Script directo
```
