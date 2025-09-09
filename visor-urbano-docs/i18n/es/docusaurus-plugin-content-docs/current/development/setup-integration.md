# 🚀 Setup Completo para Integración API-Storybook-Swagger

Esta guía te ayudará a configurar el entorno completo de desarrollo para trabajar con la integración entre Storybook, Swagger y la documentación de Visor Urbano.

## 📋 Prerrequisitos

- **Node.js** v18+ y **pnpm**
- **Python** 3.11+ y **pip**
- **Docker** (opcional, para base de datos)
- **Git** configurado

## 🛠️ Configuración Inicial

### 1. Clonar y configurar el monorepo

```bash
# Clonar el repositorio
git clone <repository-url>
cd visor-urbano

# Instalar dependencias del monorepo
pnpm install

# Configurar variables de entorno
cp apps/backend/.env.example apps/backend/.env
cp apps/frontend/.env.example apps/frontend/.env
```

### 2. Configurar el Backend (FastAPI + Swagger)

```bash
# Navegar al backend
cd apps/backend

# Crear entorno virtual de Python
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos (PostgreSQL recomendado)
# Opción 1: Docker
docker-compose up -d postgres

# Opción 2: PostgreSQL local
createdb visor_urbano_dev

# Ejecutar migraciones
alembic upgrade head

# Iniciar el servidor de desarrollo
uvicorn app.main:app --reload --port 8000
```

**🔗 Swagger estará disponible en:** `http://localhost:8000/docs`
**🔗 ReDoc estará disponible en:** `http://localhost:8000/redoc`

### 3. Configurar el Frontend (Remix + Storybook)
