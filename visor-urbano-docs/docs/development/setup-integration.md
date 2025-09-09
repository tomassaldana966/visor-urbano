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

```bash
# Navegar al frontend
cd apps/frontend

# Instalar dependencias (si no se hizo desde la raíz)
pnpm install

# Iniciar Storybook
pnpm storybook

# En otra terminal, iniciar el servidor de desarrollo
pnpm dev
```

**🔗 Storybook estará disponible en:** `http://localhost:6006`
**🔗 Frontend estará disponible en:** `http://localhost:3000`

### 4. Configurar la Documentación (Docusaurus)

```bash
# Navegar a la documentación
cd visor-urbano-docs

# Instalar dependencias (si no se hizo desde la raíz)
pnpm install

# Iniciar el servidor de documentación
pnpm start
```

**🔗 Documentación estará disponible en:** `http://localhost:3000` (puerto diferente si el frontend está corriendo)

## 🔧 Scripts de Automatización

### Generar Documentación de Integración

```bash
# Desde la raíz del proyecto
./scripts/generate-api-docs.sh

# O usando pnpm
pnpm docs:generate-api
```

### Iniciar Todo el Entorno

Crea un script `dev-all.sh` en la raíz:

```bash
#!/bin/bash
# Script para iniciar todo el entorno de desarrollo

echo "🚀 Iniciando entorno completo de Visor Urbano..."

# Terminal 1: Backend
gnome-terminal --tab --title="Backend" -- bash -c "cd apps/backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000; exec bash"

# Terminal 2: Frontend
gnome-terminal --tab --title="Frontend" -- bash -c "cd apps/frontend && pnpm dev; exec bash"

# Terminal 3: Storybook
gnome-terminal --tab --title="Storybook" -- bash -c "cd apps/frontend && pnpm storybook; exec bash"

# Terminal 4: Documentación
gnome-terminal --tab --title="Docs" -- bash -c "cd visor-urbano-docs && pnpm start; exec bash"

echo "✅ Todos los servicios iniciados!"
echo "🔗 Enlaces:"
echo "   Frontend: http://localhost:3000"
echo "   Storybook: http://localhost:6006"
echo "   Swagger: http://localhost:8000/docs"
echo "   Documentación: http://localhost:3001"
```

### Para macOS (usando iTerm2):

```bash
#!/bin/bash
# dev-all-mac.sh

echo "🚀 Iniciando entorno completo de Visor Urbano..."

# Backend
osascript -e 'tell application "iTerm" to create window with default profile'
osascript -e 'tell application "iTerm" to tell current session of current window to write text "cd apps/backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000"'

# Frontend
osascript -e 'tell application "iTerm" to tell current window to create tab with default profile'
osascript -e 'tell application "iTerm" to tell current session of current window to write text "cd apps/frontend && pnpm dev"'

# Storybook
osascript -e 'tell application "iTerm" to tell current window to create tab with default profile'
osascript -e 'tell application "iTerm" to tell current session of current window to write text "cd apps/frontend && pnpm storybook"'

# Documentación
osascript -e 'tell application "iTerm" to tell current window to create tab with default profile'
osascript -e 'tell application "iTerm" to tell current session of current window to write text "cd visor-urbano-docs && pnpm start"'

echo "✅ Todos los servicios iniciados en iTerm2!"
```

## 🐳 Configuración con Docker

### docker-compose.yml completo

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: visor_urbano_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - '5432:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile
    ports:
      - '8000:8000'
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/visor_urbano_dev
    depends_on:
      - postgres
    volumes:
      - ./apps/backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./apps/frontend
      dockerfile: Dockerfile
    ports:
      - '3000:3000'
    volumes:
      - ./apps/frontend:/app
      - /app/node_modules
    command: pnpm dev

  storybook:
    build:
      context: ./apps/frontend
      dockerfile: Dockerfile
    ports:
      - '6006:6006'
    volumes:
      - ./apps/frontend:/app
      - /app/node_modules
    command: pnpm storybook

  docs:
    build:
      context: ./visor-urbano-docs
      dockerfile: Dockerfile
    ports:
      - '3001:3000'
    volumes:
      - ./visor-urbano-docs:/app
      - /app/node_modules
    command: pnpm start --host 0.0.0.0

volumes:
  postgres_data:
```

### Comandos Docker

```bash
# Iniciar todo con Docker
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar todo
docker-compose down

# Rebuild después de cambios
docker-compose up --build
```

## 🔍 Validación del Setup

### Checklist de Verificación

- [ ] ✅ Backend corriendo en `http://localhost:8000`
- [ ] ✅ Swagger disponible en `http://localhost:8000/docs`
- [ ] ✅ Frontend corriendo en `http://localhost:3000`
- [ ] ✅ Storybook disponible en `http://localhost:6006`
- [ ] ✅ Documentación disponible en `http://localhost:3001`
- [ ] ✅ Script de generación funcionando: `./scripts/generate-api-docs.sh`

### Tests de Integración

```bash
# Test de API
curl http://localhost:8000/v1/health

# Test de Frontend
curl http://localhost:3000

# Test de Storybook
curl http://localhost:6006

# Test de Documentación
curl http://localhost:3001
```

## 🚨 Troubleshooting

### Problemas Comunes

**Error: Puerto ocupado**

```bash
# Encontrar proceso usando el puerto
lsof -i :8000
kill -9 <PID>
```

**Error: Base de datos no conecta**

```bash
# Verificar PostgreSQL
pg_isready -h localhost -p 5432

# Verificar variables de entorno
echo $DATABASE_URL
```

**Error: Dependencias no instaladas**

```bash
# Limpiar y reinstalar
rm -rf node_modules package-lock.json
pnpm install

# Para Python
pip install --upgrade -r requirements.txt
```

**Error: Script de generación falla**

```bash
# Verificar permisos
chmod +x ./scripts/generate-api-docs.sh

# Ejecutar en modo debug
bash -x ./scripts/generate-api-docs.sh
```

### Logs útiles

```bash
# Backend logs
tail -f apps/backend/backend.log

# Frontend logs (en modo dev)
# Se muestran en la consola

# Storybook logs
# Se muestran en la consola

# Documentación logs
# Se muestran en la consola
```

## 📚 Próximos Pasos

Una vez que tengas todo configurado:

1. **Explora la [Integración API-Storybook](./api-integration)** para entender cómo navegar entre herramientas
2. **Revisa la [Documentación Generada](./generated-api-integration)** para ver el mapeo completo
3. **Lee el [README de Desarrollo](/development/)** para conocer las convenciones del proyecto
4. **Contribuye** añadiendo nuevos componentes, endpoints o mejorando la documentación

## 🤝 Soporte

Si tienes problemas con el setup:

1. Revisa esta documentación completa
2. Busca en los issues del repositorio
3. Pregunta en el canal de desarrollo del equipo
4. Crea un issue nuevo con detalles del problema

---

> 💡 **Tip:** Guarda los enlaces de desarrollo en tus bookmarks para acceso rápido durante el desarrollo diario.
