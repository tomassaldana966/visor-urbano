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
./scripts/generate-api-docs.sh

# Opción 2: Comando npm
pnpm run docs:generate-api

# Resultado: Se actualiza docs/development/generated-api-integration.md
```

## 📊 Estadísticas del Proyecto

Según el último escaneo:

- **33 rutas** del frontend
- **43 stories** de Storybook
- **164 endpoints** del backend

## 🔗 Enlaces de Desarrollo

### Local Development

- **Frontend:** http://localhost:5173
- **Storybook:** http://localhost:6006
- **Swagger API:** http://localhost:8000/docs
- **ReDoc API:** http://localhost:8000/redoc
- **Documentación:** http://localhost:3000

### Documentación Específica

- **Integración Manual:** http://localhost:3000/development/api-integration
- **Integración Generada:** http://localhost:3000/development/generated-api-integration

## 📝 Estructura de Archivos

```
visor-urbano/
├── apps/
│   ├── frontend/
│   │   ├── app/routes/          # Rutas del frontend
│   │   └── **/*.stories.tsx     # Stories de Storybook
│   └── backend/
│       └── app/routers/         # Endpoints de la API
├── scripts/
│   └── generate-api-docs.sh     # Script de generación automática
└── visor-urbano-docs/
    ├── docs/development/
    │   ├── api-integration.md           # Documentación manual
    │   └── generated-api-integration.md # Documentación generada
    └── src/components/
        └── ApiIntegrationTable.tsx      # Componente React interactivo
```

## 🛠️ Componente React Interactivo

Se creó `ApiIntegrationTable.tsx` que muestra:

- Lista de rutas con sus archivos fuente
- Enlaces directos a stories de Storybook
- Enlaces directos a endpoints en Swagger
- Códigos de colores por método HTTP (GET, POST, PUT, DELETE)

## 🔄 Automatización

### Script de Generación

El script `generate-api-docs.sh`:

1. **Escanea** rutas en `apps/frontend/app/routes/`
2. **Detecta** stories en archivos `*.stories.tsx`
3. **Extrae** endpoints de `apps/backend/app/routers/`
4. **Genera** documentación markdown automática
5. **Actualiza** estadísticas del proyecto

### Integración con CI/CD

Puedes agregar esto a tu pipeline:

```yaml
- name: Generate API Documentation
  run: |
    chmod +x ./scripts/generate-api-docs.sh
    ./scripts/generate-api-docs.sh
```

## 🎨 Beneficios para Desarrolladores

### 🔍 Navegación Rápida

- Desde una ruta → ver sus componentes en Storybook
- Desde una ruta → ver sus endpoints en Swagger
- Documentación centralizada y actualizada

### 🚀 Onboarding Nuevo Equipo

- Vista completa de la arquitectura
- Enlaces directos a herramientas de desarrollo
- Mapeo claro entre frontend y backend

### 📈 Mantenimiento

- Detección automática de componentes huérfanos
- Verificación de consistencia entre rutas y endpoints
- Estadísticas de cobertura de documentación

## 🔜 Siguientes Pasos

### Automatización Avanzada

- [ ] Detección automática de componentes sin stories
- [ ] Validación de enlaces rotos
- [ ] Generación de diagramas de arquitectura

### Integración E2E

- [ ] Playwright tests que usen esta documentación
- [ ] Tests de consistencia entre rutas y endpoints
- [ ] Validación automática en CI/CD

### Deployment

- [ ] URLs de producción para Storybook publicado
- [ ] API docs públicas para consumidores externos
- [ ] Documentación versionada por release

---

> 💡 **Tip:** Esta integración te permite tener una vista completa del proyecto desde documentación técnica hasta herramientas de desarrollo en un solo lugar.
