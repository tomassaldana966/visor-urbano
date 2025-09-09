# 🔗 Integración API-Storybook-Swagger

Esta sección documenta la integración completa entre las rutas del frontend, componentes de Storybook y endpoints de la API backend, proporcionando una experiencia de desarrollo unificada.

## 🎯 Objetivo

Crear un mapeo claro y accesible que permita a los desarrolladores:

- **Navegar rápidamente** entre frontend y backend
- **Encontrar componentes reutilizables** en Storybook
- **Entender los endpoints de API** disponibles en Swagger
- **Mantener consistencia** en el desarrollo

## 📊 Enlaces Rápidos

| Herramienta        | URL Local                                           | Descripción                                 |
| ------------------ | --------------------------------------------------- | ------------------------------------------- |
| 🎨 **Storybook**   | [localhost:6006](http://localhost:6006)             | Documentación interactiva de componentes UI |
| 📡 **Swagger API** | [localhost:8000/docs](http://localhost:8000/docs)   | Documentación completa de endpoints REST    |
| 🔧 **ReDoc API**   | [localhost:8000/redoc](http://localhost:8000/redoc) | Vista alternativa y elegante de la API      |
| 📖 **Docusaurus**  | [localhost:3000](http://localhost:3000)             | Esta documentación técnica                  |

## 🗺️ Mapeo Interactivo

import ApiIntegrationTable from '@site/src/components/ApiIntegrationTable';

<ApiIntegrationTable />

## 🛠️ Cómo usar esta documentación

### Para Desarrolladores Frontend

1. **Antes de crear un componente nuevo:**

   - Busca en Storybook si ya existe algo similar
   - Revisa los patrones de diseño establecidos
   - Consulta la tabla de integración para ver ejemplos de uso

2. **Al trabajar en una ruta:**

   - Identifica qué endpoints necesitas en la tabla
   - Verifica la documentación de Swagger para entender los schemas
   - Usa componentes existentes de Storybook cuando sea posible

3. **Para mantener consistencia:**
   - Sigue los patrones establecidos en otras rutas similares
   - Usa los mismos componentes base para elementos comunes
   - Mantén la nomenclatura consistente con el resto del proyecto

### Para Desarrolladores Backend

1. **Al crear nuevos endpoints:**

   - Documenta claramente en Swagger con ejemplos
   - Usa nomenclatura consistente con endpoints similares
   - Agrupa endpoints relacionados en el mismo router

2. **Para integración con frontend:**

   - Revisa qué rutas frontend consumirán tu API
   - Asegúrate de que los schemas sean claros y completos
   - Considera los casos de error y valida las respuestas

3. **Mantenimiento:**
   - Actualiza la documentación cuando cambies endpoints
   - Ejecuta el script de generación después de cambios importantes

### Para DevOps y QA

1. **Validación de integración:**

   - Usa los enlaces directos para probar cada componente
   - Verifica que los endpoints respondan correctamente
   - Valida que la documentación esté actualizada

2. **Automatización:**
   - El script `generate-api-docs.sh` debe ejecutarse en CI/CD
   - Los enlaces deben validarse automáticamente
   - La documentación debe regenerarse con cada deployment

## 🔄 Automatización

### Regenerar Documentación

```bash
# Método 1: Script directo
./scripts/generate-api-docs.sh

# Método 2: Comando npm/pnpm
pnpm docs:generate-api

# Método 3: Como parte del workflow de desarrollo
pnpm dev:docs  # Incluye regeneración automática
```

### Configuración de CI/CD

Para mantener la documentación siempre actualizada, agrega esto a tu pipeline:

```yaml
# .github/workflows/docs.yml
- name: Generate API Documentation
  run: |
    ./scripts/generate-api-docs.sh
    git add docs/development/generated-api-integration.md
    git commit -m "docs: update API integration mapping" || true
```

## 📋 Convenciones

### Nomenclatura de Stories

```typescript
// ✅ Correcto
export default {
  title: 'Components/Forms/LoginForm',
  component: LoginForm,
};

// ❌ Evitar
export default {
  title: 'login-form',
  component: LoginForm,
};
```

### Documentación de Endpoints

```python
# ✅ Correcto
@router.get("/business-licenses/",
    summary="List business licenses",
    description="Retrieve a paginated list of business licenses with optional filtering",
    response_model=BusinessLicenseResponse
)

# ❌ Evitar
@router.get("/licenses/")  # Sin documentación
```

### Estructura de Rutas

```typescript
// ✅ Correcto - archivo: routes/licenses.tsx
export default function LicensesRoute() {
  // Importar componentes específicos de Storybook
  // Usar endpoints documentados en Swagger
}

// ❌ Evitar - lógica compleja sin componentización
```

## 🎨 Patrones de Diseño

### Componentes Base

| Componente | Uso                 | Storybook                                                                         |
| ---------- | ------------------- | --------------------------------------------------------------------------------- |
| `Button`   | Todas las acciones  | [Ver en Storybook](http://localhost:6006/?path=/story/components-button--default) |
| `Input`    | Formularios         | [Ver en Storybook](http://localhost:6006/?path=/story/components-input--default)  |
| `Table`    | Listados de datos   | [Ver en Storybook](http://localhost:6006/?path=/story/components-table--default)  |
| `Modal`    | Ventanas emergentes | [Ver en Storybook](http://localhost:6006/?path=/story/components-modal--default)  |

### Patrones de API

| Patrón     | Endpoint                   | Descripción           |
| ---------- | -------------------------- | --------------------- |
| Listado    | `GET /v1/resource/`        | Listar con paginación |
| Detalle    | `GET /v1/resource/{id}`    | Obtener por ID        |
| Crear      | `POST /v1/resource/`       | Crear nuevo recurso   |
| Actualizar | `PUT /v1/resource/{id}`    | Actualizar existente  |
| Eliminar   | `DELETE /v1/resource/{id}` | Eliminar recurso      |

## 🔍 Búsqueda y Navegación

### Encontrar Componentes

1. **Por funcionalidad:** Usa la búsqueda en la tabla interactiva arriba
2. **Por categoría:** Navega directamente en Storybook por carpetas
3. **Por ruta:** Encuentra qué componentes usa cada página

### Encontrar Endpoints

1. **Por router:** Usa la documentación generada automáticamente
2. **Por funcionalidad:** Busca en Swagger por tags y operaciones
3. **Por ruta frontend:** Consulta la tabla de integración

## 📚 Recursos Adicionales

- [Documentación Generada Automáticamente](./generated-api-integration) - Mapeo completo actualizado
- [README de Desarrollo](/development/) - Guía para contribuidores
- [Arquitectura del Proyecto](../getting-started/overview) - Visión general del sistema

## 🤝 Contribuir

1. **Añadir nuevos componentes:** Crea el story correspondiente en Storybook
2. **Nuevos endpoints:** Documenta en Swagger y ejecuta el script de generación
3. **Nuevas rutas:** Asegúrate de mapear componentes y APIs utilizados
4. **Mejoras:** Sugiere mejoras a esta documentación o al script de automatización

---

> 💡 **Tip:** Esta documentación es un punto de partida. El mapeo exacto y actualizado siempre estará en la [documentación generada automáticamente](./generated-api-integration).

- **Componentes Storybook:**
  - [License Table](http://localhost:6006/?path=/story/tables-license--issued)
  - [Status Badge](http://localhost:6006/?path=/story/components-badge--status)
  - [Download Button](http://localhost:6006/?path=/story/buttons-download--pdf)
- **Endpoints API:**
  - `GET /v1/business-licenses/issued` - Licencias emitidas
  - `GET /v1/business-licenses/{id}/pdf` - Descargar PDF
  - `GET /v1/business-licenses/{id}/receipt` - Descargar recibo

### ✅ Aprobaciones de Procedimientos

**Ruta:** `/procedure-approvals`

- **Componente Principal:** `routes/procedure-approvals.tsx`
- **Componentes Storybook:**
  - [Approval Table](http://localhost:6006/?path=/story/tables-approval--procedures)
  - [Approval Modal](http://localhost:6006/?path=/story/modals-approval--default)
  - [Status Timeline](http://localhost:6006/?path=/story/components-timeline--status)
- **Endpoints API:**
  - `GET /v1/procedures/` - Listar procedimientos
  - `POST /v1/procedures/{id}/approve` - Aprobar procedimiento
  - `POST /v1/procedures/{id}/reject` - Rechazar procedimiento
  - `GET /v1/procedures/{id}/history` - Historial de cambios

### 🔔 Notificaciones

**Ruta:** `/notifications`

- **Componente Principal:** `routes/notifications.tsx`
- **Componentes Storybook:**
  - [Notification List](http://localhost:6006/?path=/story/components-notification--list)
  - [Notification Item](http://localhost:6006/?path=/story/components-notification--item)
  - [Notification Badge](http://localhost:6006/?path=/story/components-notification--badge)
- **Endpoints API:**
  - `GET /v1/notifications/` - Listar notificaciones
  - `POST /v1/notifications/{id}/mark-read` - Marcar como leída
  - `POST /v1/notifications/mark-all-read` - Marcar todas como leídas

### 🔐 Autenticación

**Rutas:** `/login`, `/register`, `/forgot`, `/logout`

- **Componentes Principales:**
  - `routes/login.tsx`
  - `routes/register.tsx`
  - `routes/forgot.tsx`
  - `routes/logout.tsx`
- **Componentes Storybook:**
  - [Login Form](http://localhost:6006/?path=/story/forms-auth--login)
  - [Register Form](http://localhost:6006/?path=/story/forms-auth--register)
  - [Button Component](http://localhost:6006/?path=/story/components-button--primary)
- **Endpoints API:**
  - `POST /v1/auth/token` - Iniciar sesión
  - `POST /v1/auth/register` - Registrar usuario
  - `POST /v1/auth/forgot-password` - Recuperar contraseña
  - `POST /v1/auth/logout` - Cerrar sesión

### 📄 Hojas Técnicas y PDFs

**Rutas:** `/technical-sheet`, `/requirements-pdf`

- **Componentes Principales:**
  - `routes/technical-sheet.tsx`
  - `routes/requirements-pdf.tsx`
- **Componentes Storybook:**
  - [PDF Viewer](http://localhost:6006/?path=/story/components-pdf--viewer)
  - [Document Form](http://localhost:6006/?path=/story/forms-document--technical)
- **Endpoints API:**
  - `GET /v1/documents/technical-sheet/{id}` - Obtener hoja técnica
  - `GET /v1/documents/requirements/{id}` - Obtener requisitos PDF
  - `POST /v1/documents/generate` - Generar documento

### ℹ️ Información

**Ruta:** `/about`

- **Componente Principal:** `routes/about.tsx`
- **Componentes Storybook:**
  - [About Section](http://localhost:6006/?path=/story/components-about--section)
  - [Feature Cards](http://localhost:6006/?path=/story/components-feature--cards)

## 🔧 Configuración de Desarrollo

### Storybook (Puerto 6006)

```bash
# Iniciar Storybook
cd apps/frontend
pnpm run storybook

# Construir Storybook estático
pnpm run build-storybook
```

### Swagger API (Puerto 8000)

```bash
# Iniciar backend FastAPI
cd apps/backend
uvicorn app.main:app --reload --port 8000

# Acceder a documentación
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

## 📚 Convenciones

### Nomenclatura de Stories

- **Componentes:** `ComponentName.stories.tsx`
- **Path:** `/story/category-componentname--variant`
- **Categorías:** `components`, `forms`, `modals`, `tables`, `buttons`

### Endpoints API

- **Versioning:** `/v1/`
- **RESTful:** `GET`, `POST`, `PUT`, `DELETE`
- **Autenticación:** Bearer Token en headers
- **Documentación:** Automática con FastAPI + Swagger

## 🚀 Próximos Pasos

1. **Automatización:** Script para generar esta documentación automáticamente
2. **E2E Testing:** Integrar Playwright con Storybook y API
3. **Deployment:** URLs de producción para Storybook y API docs
4. **Monitoreo:** Health checks y métricas de performance

---

> 💡 **Tip:** Esta documentación se actualiza automáticamente cuando se agregan nuevas rutas, componentes o endpoints al proyecto.
