import React, { useState, useMemo } from 'react';

interface RouteMapping {
  route: string;
  file: string;
  description: string;
  storybook: StorybookLink[];
  endpoints: EndpointLink[];
  status: 'complete' | 'partial' | 'minimal';
}

interface StorybookLink {
  name: string;
  path: string;
  category?: string;
}

interface EndpointLink {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  path: string;
  description?: string;
  router: string;
}

const routeMappings: RouteMapping[] = [
  {
    route: '/ (home)',
    file: 'routes/home.tsx',
    description: 'Página principal con dashboard y estadísticas',
    status: 'complete',
    storybook: [
      {
        name: 'Hero',
        path: '?path=/docs/components-hero--docs',
        category: 'Layout',
      },
      {
        name: 'Dashboard Cards',
        path: '?path=/docs/components-dashboard--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/dashboard/stats',
        description: 'Estadísticas del dashboard',
        router: 'dashboard',
      },
      {
        method: 'GET',
        path: '/v1/notifications/recent',
        description: 'Notificaciones recientes',
        router: 'notifications',
      },
    ],
  },
  {
    route: '/about',
    file: 'routes/about.tsx',
    description: 'Página de información sobre el proyecto',
    status: 'minimal',
    storybook: [
      {
        name: 'Hero',
        path: '?path=/docs/components-hero--docs',
        category: 'Layout',
      },
      {
        name: 'Footer',
        path: '?path=/docs/components-footer--docs',
        category: 'Layout',
      },
    ],
    endpoints: [],
  },
  {
    route: '/forgot',
    file: 'routes/forgot.tsx',
    description: 'Recuperación de contraseña',
    status: 'partial',
    storybook: [
      {
        name: 'Input',
        path: '?path=/docs/components-input--docs',
        category: 'Forms',
      },
      {
        name: 'Button',
        path: '?path=/docs/components-button--docs',
        category: 'Forms',
      },
    ],
    endpoints: [
      {
        method: 'POST',
        path: '/v1/auth/forgot-password',
        description: 'Solicitar recuperación',
        router: 'password',
      },
    ],
  },
  {
    route: '/login',
    file: 'routes/login.tsx',
    description: 'Página de inicio de sesión',
    status: 'complete',
    storybook: [
      {
        name: 'Login Form',
        path: '?path=/docs/forms-login--docs',
        category: 'Forms',
      },
      {
        name: 'Input',
        path: '?path=/docs/components-input--docs',
        category: 'Forms',
      },
      {
        name: 'Button',
        path: '?path=/docs/components-button--docs',
        category: 'Forms',
      },
    ],
    endpoints: [
      {
        method: 'POST',
        path: '/v1/auth/login',
        description: 'Iniciar sesión',
        router: 'auth',
      },
      {
        method: 'POST',
        path: '/v1/auth/refresh',
        description: 'Renovar token',
        router: 'auth',
      },
    ],
  },
  {
    route: '/logout',
    file: 'routes/logout.tsx',
    description: 'Cerrar sesión',
    status: 'minimal',
    storybook: [],
    endpoints: [
      {
        method: 'POST',
        path: '/v1/auth/logout',
        description: 'Cerrar sesión',
        router: 'auth',
      },
    ],
  },
  {
    route: '/map',
    file: 'routes/map.tsx',
    description: 'Mapa interactivo con capas y búsqueda geoespacial',
    status: 'complete',
    storybook: [
      {
        name: 'Map Container',
        path: '?path=/docs/components-map--docs',
        category: 'Map',
      },
      {
        name: 'Map Layers',
        path: '?path=/docs/components-maplayers--docs',
        category: 'Map',
      },
      {
        name: 'Map Controls',
        path: '?path=/docs/components-mapcontrols--docs',
        category: 'Map',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/map/layers',
        description: 'Capas del mapa',
        router: 'map',
      },
      {
        method: 'GET',
        path: '/v1/map/features',
        description: 'Características geográficas',
        router: 'map',
      },
      {
        method: 'POST',
        path: '/v1/map/search',
        description: 'Búsqueda geoespacial',
        router: 'map',
      },
    ],
  },
  {
    route: '/register',
    file: 'routes/register.tsx',
    description: 'Registro de nuevos usuarios',
    status: 'partial',
    storybook: [
      {
        name: 'Register Form',
        path: '?path=/docs/forms-register--docs',
        category: 'Forms',
      },
      {
        name: 'Input',
        path: '?path=/docs/components-input--docs',
        category: 'Forms',
      },
      {
        name: 'Button',
        path: '?path=/docs/components-button--docs',
        category: 'Forms',
      },
    ],
    endpoints: [
      {
        method: 'POST',
        path: '/v1/auth/register',
        description: 'Registrar usuario',
        router: 'auth',
      },
    ],
  },
  {
    route: '/licenses',
    file: 'routes/licenses.tsx',
    description: 'Gestión de licencias comerciales y permisos',
    status: 'complete',
    storybook: [
      {
        name: 'License Form',
        path: '?path=/docs/forms-license--docs',
        category: 'Forms',
      },
      {
        name: 'License Card',
        path: '?path=/docs/components-license--docs',
        category: 'Data Display',
      },
      {
        name: 'Issue License Modal',
        path: '?path=/docs/components-issuelicensemodal--docs',
        category: 'Overlays',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/business-licenses/',
        description: 'Listar licencias',
        router: 'business_licenses',
      },
      {
        method: 'POST',
        path: '/v1/business-licenses/',
        description: 'Crear nueva licencia',
        router: 'business_licenses',
      },
      {
        method: 'PUT',
        path: '/v1/business-licenses/{id}',
        description: 'Actualizar licencia',
        router: 'business_licenses',
      },
      {
        method: 'DELETE',
        path: '/v1/business-licenses/{id}',
        description: 'Eliminar licencia',
        router: 'business_licenses',
      },
    ],
  },
  {
    route: '/technical-sheet/:uuid',
    file: 'routes/technical-sheet.tsx',
    description: 'Ficha técnica de procedimientos',
    status: 'partial',
    storybook: [
      {
        name: 'Technical Sheet',
        path: '?path=/docs/components-technicalsheet--docs',
        category: 'Data Display',
      },
      {
        name: 'Badge',
        path: '?path=/docs/components-badge--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/technical-sheet/{uuid}',
        description: 'Obtener ficha técnica',
        router: 'technical_sheet_downloads',
      },
    ],
  },
  {
    route: '/requirements-queries/:folio/requirements/pdf',
    file: 'routes/requirements-pdf.tsx',
    description: 'Descarga de PDF de requerimientos',
    status: 'minimal',
    storybook: [],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/requirements-queries/{folio}/pdf',
        description: 'Descargar PDF',
        router: 'requirements_queries',
      },
    ],
  },
  {
    route: '/news',
    file: 'routes/news/index.tsx',
    description: 'Listado de noticias y artículos',
    status: 'partial',
    storybook: [
      {
        name: 'News Card',
        path: '?path=/docs/components-news--docs',
        category: 'Data Display',
      },
      {
        name: 'News List',
        path: '?path=/docs/components-news--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/blog/posts',
        description: 'Listar artículos',
        router: 'blog',
      },
    ],
  },
  {
    route: '/news/:year/:month/:slug',
    file: 'routes/news/article.tsx',
    description: 'Artículo individual de noticias',
    status: 'partial',
    storybook: [
      {
        name: 'News Article',
        path: '?path=/docs/components-news--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/blog/posts/{slug}',
        description: 'Obtener artículo',
        router: 'blog',
      },
    ],
  },
  {
    route: '/news/:id',
    file: 'routes/news/legacy.tsx',
    description: 'Artículo legacy de noticias (ID numérico)',
    status: 'minimal',
    storybook: [
      {
        name: 'News Article',
        path: '?path=/docs/components-news--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/news/:id',
        description: 'Obtener noticia legacy',
        router: 'news',
      },
    ],
  },
  {
    route: '/procedures',
    file: 'routes/procedures/index.tsx',
    description: 'Listado de procedimientos del usuario',
    status: 'complete',
    storybook: [
      {
        name: 'Procedures Table',
        path: '?path=/docs/components-procedurestable--docs',
        category: 'Data Display',
      },
      {
        name: 'Status Badge',
        path: '?path=/docs/components-badge--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/procedures/',
        description: 'Listar procedimientos',
        router: 'procedures',
      },
    ],
  },
  {
    route: '/procedures/new',
    file: 'routes/procedures/new.tsx',
    description: 'Crear nuevo procedimiento',
    status: 'complete',
    storybook: [
      {
        name: 'Procedure Form',
        path: '?path=/docs/forms-procedure--docs',
        category: 'Forms',
      },
      {
        name: 'Select',
        path: '?path=/docs/components-select--docs',
        category: 'Forms',
      },
    ],
    endpoints: [
      {
        method: 'POST',
        path: '/v1/procedures/',
        description: 'Crear procedimiento',
        router: 'procedures',
      },
      {
        method: 'GET',
        path: '/v1/business-types/',
        description: 'Tipos de negocio',
        router: 'business_types',
      },
    ],
  },
  {
    route: '/procedures/:folio/detail',
    file: 'routes/procedures/detail.tsx',
    description: 'Detalle de procedimiento específico',
    status: 'complete',
    storybook: [
      {
        name: 'Procedure Detail',
        path: '?path=/docs/components-proceduredetail--docs',
        category: 'Data Display',
      },
      {
        name: 'Timeline',
        path: '?path=/docs/components-timeline--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/procedures/{folio}',
        description: 'Obtener procedimiento',
        router: 'procedures',
      },
      {
        method: 'GET',
        path: '/v1/procedures/{folio}/history',
        description: 'Historial',
        router: 'procedures',
      },
    ],
  },
  {
    route: '/procedures/:folio/edit',
    file: 'routes/procedures/edit.tsx',
    description: 'Editar procedimiento existente',
    status: 'partial',
    storybook: [
      {
        name: 'Procedure Form',
        path: '?path=/docs/forms-procedure--docs',
        category: 'Forms',
      },
    ],
    endpoints: [
      {
        method: 'PUT',
        path: '/v1/procedures/{folio}',
        description: 'Actualizar procedimiento',
        router: 'procedures',
      },
    ],
  },
  {
    route: '/procedure-approvals',
    file: 'routes/procedure-approvals.tsx',
    description: 'Aprobación y gestión de procedimientos administrativos',
    status: 'complete',
    storybook: [
      {
        name: 'Approval Table',
        path: '?path=/docs/components-approvaltable--docs',
        category: 'Data Display',
      },
      {
        name: 'Approval Modal',
        path: '?path=/docs/components-approvalmodal--docs',
        category: 'Overlays',
      },
      {
        name: 'Timeline Status',
        path: '?path=/docs/components-timeline--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/procedures/',
        description: 'Listar procedimientos',
        router: 'procedures',
      },
      {
        method: 'POST',
        path: '/v1/procedures/{id}/approve',
        description: 'Aprobar',
        router: 'procedures',
      },
      {
        method: 'POST',
        path: '/v1/procedures/{id}/reject',
        description: 'Rechazar',
        router: 'procedures',
      },
    ],
  },
  {
    route: '/notifications',
    file: 'routes/notifications.tsx',
    description: 'Centro de notificaciones del usuario',
    status: 'partial',
    storybook: [
      {
        name: 'Notification Card',
        path: '?path=/docs/components-notification--docs',
        category: 'Data Display',
      },
      {
        name: 'Notification List',
        path: '?path=/docs/components-notification--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/notifications/',
        description: 'Listar notificaciones',
        router: 'notifications',
      },
      {
        method: 'PUT',
        path: '/v1/notifications/{id}/read',
        description: 'Marcar como leída',
        router: 'notifications',
      },
    ],
  },
  {
    route: '/licenses-issued',
    file: 'routes/licenses-issued.tsx',
    description: 'Vista de licencias emitidas y su estado',
    status: 'partial',
    storybook: [
      {
        name: 'Licenses Table',
        path: '?path=/docs/components-licensestable--docs',
        category: 'Data Display',
      },
      {
        name: 'Status Badge',
        path: '?path=/docs/components-badge--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/business-licenses/public',
        description: 'Licencias públicas',
        router: 'business_licenses',
      },
      {
        method: 'GET',
        path: '/v1/business-licenses/{id}/status_history',
        description: 'Historial de estados',
        router: 'business_licenses',
      },
    ],
  },
  {
    route: '/director/dashboard',
    file: 'routes/director/dashboard.tsx',
    description: 'Dashboard administrativo para directores',
    status: 'complete',
    storybook: [
      {
        name: 'Director Dashboard',
        path: '?path=/docs/components-directordashboard--docs',
        category: 'Data Display',
      },
      {
        name: 'Analytics Cards',
        path: '?path=/docs/components-analytics--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/analytics/dashboard',
        description: 'Datos del dashboard',
        router: 'analytics',
      },
      {
        method: 'GET',
        path: '/v1/director/stats',
        description: 'Estadísticas director',
        router: 'director',
      },
    ],
  },
  {
    route: '/director/reviews',
    file: 'routes/director/reviews.tsx',
    description: 'Gestión de revisiones por director',
    status: 'complete',
    storybook: [
      {
        name: 'Reviews Table',
        path: '?path=/docs/components-reviewstable--docs',
        category: 'Data Display',
      },
      {
        name: 'Review Modal',
        path: '?path=/docs/components-reviewmodal--docs',
        category: 'Overlays',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/dependency-reviews/',
        description: 'Listar revisiones',
        router: 'dependency_reviews',
      },
      {
        method: 'POST',
        path: '/v1/dependency-reviews/{id}/approve',
        description: 'Aprobar revisión',
        router: 'dependency_reviews',
      },
    ],
  },
  {
    route: '/director/approvals',
    file: 'routes/director/approvals.tsx',
    description: 'Aprobaciones administrativas',
    status: 'complete',
    storybook: [
      {
        name: 'Approvals Table',
        path: '?path=/docs/components-approvalstable--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/procedures/pending-approval',
        description: 'Pendientes de aprobación',
        router: 'procedures',
      },
    ],
  },
  {
    route: '/director/analytics',
    file: 'routes/director/analytics.tsx',
    description: 'Analytics y reportes para directores',
    status: 'partial',
    storybook: [
      {
        name: 'Analytics Charts',
        path: '?path=/docs/components-charts--docs',
        category: 'Data Display',
      },
      {
        name: 'Reports Table',
        path: '?path=/docs/components-reportstable--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/analytics/',
        description: 'Datos de analytics',
        router: 'analytics',
      },
      {
        method: 'GET',
        path: '/v1/reports/',
        description: 'Reportes',
        router: 'reports',
      },
    ],
  },
  {
    route: '/director/users',
    file: 'routes/director/users.tsx',
    description: 'Gestión de usuarios del sistema',
    status: 'complete',
    storybook: [
      {
        name: 'Users Table',
        path: '?path=/docs/components-userstable--docs',
        category: 'Data Display',
      },
      {
        name: 'User Modal',
        path: '?path=/docs/components-usermodal--docs',
        category: 'Overlays',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/users/',
        description: 'Listar usuarios',
        router: 'users',
      },
      {
        method: 'POST',
        path: '/v1/users/',
        description: 'Crear usuario',
        router: 'users',
      },
      {
        method: 'PUT',
        path: '/v1/users/{id}',
        description: 'Actualizar usuario',
        router: 'users',
      },
    ],
  },
  {
    route: '/director/settings',
    file: 'routes/director/settings.tsx',
    description: 'Configuración del sistema',
    status: 'partial',
    storybook: [
      {
        name: 'Settings Form',
        path: '?path=/docs/forms-settings--docs',
        category: 'Forms',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/system/settings',
        description: 'Obtener configuración',
        router: 'system',
      },
      {
        method: 'PUT',
        path: '/v1/system/settings',
        description: 'Actualizar configuración',
        router: 'system',
      },
    ],
  },
  {
    route: '/director/roles',
    file: 'routes/director/roles.tsx',
    description: 'Gestión de roles y permisos',
    status: 'complete',
    storybook: [
      {
        name: 'Roles Table',
        path: '?path=/docs/components-rolestable--docs',
        category: 'Data Display',
      },
      {
        name: 'Role Modal',
        path: '?path=/docs/components-rolemodal--docs',
        category: 'Overlays',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/user-roles/',
        description: 'Listar roles',
        router: 'user_roles',
      },
      {
        method: 'POST',
        path: '/v1/user-roles/',
        description: 'Crear rol',
        router: 'user_roles',
      },
    ],
  },
  {
    route: '/director/requirements',
    file: 'routes/director/requirements.tsx',
    description: 'Gestión de requerimientos',
    status: 'partial',
    storybook: [
      {
        name: 'Requirements Table',
        path: '?path=/docs/components-requirementstable--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/requirements/',
        description: 'Listar requerimientos',
        router: 'requirements',
      },
      {
        method: 'POST',
        path: '/v1/requirements/',
        description: 'Crear requerimiento',
        router: 'requirements',
      },
    ],
  },
  {
    route: '/director/business-types',
    file: 'routes/director/business-types.tsx',
    description: 'Configuración de tipos de negocio',
    status: 'partial',
    storybook: [
      {
        name: 'Business Types Table',
        path: '?path=/docs/components-businesstypestable--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/business-types/',
        description: 'Listar tipos',
        router: 'business_types',
      },
      {
        method: 'POST',
        path: '/v1/business-types/',
        description: 'Crear tipo',
        router: 'business_types',
      },
    ],
  },
  {
    route: '/director/municipal-layers',
    file: 'routes/director/municipal-layers.tsx',
    description: 'Gestión de capas municipales',
    status: 'minimal',
    storybook: [
      {
        name: 'Municipal Layers',
        path: '?path=/docs/components-municipallayers--docs',
        category: 'Map',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/map/municipal-layers',
        description: 'Capas municipales',
        router: 'map',
      },
    ],
  },
  {
    route: '/director/impact-management',
    file: 'routes/director/impact-management.tsx',
    description: 'Gestión de evaluaciones de impacto',
    status: 'minimal',
    storybook: [
      {
        name: 'Impact Management',
        path: '?path=/docs/components-impactmanagement--docs',
        category: 'Data Display',
      },
    ],
    endpoints: [
      {
        method: 'GET',
        path: '/v1/impact-assessments/',
        description: 'Evaluaciones de impacto',
        router: 'impact_assessments',
      },
    ],
  },
];

const statusColors = {
  complete: '#10b981', // green
  partial: '#f59e0b', // amber
  minimal: '#ef4444', // red
};

const statusLabels = {
  complete: 'Completo',
  partial: 'Parcial',
  minimal: 'Mínimo',
};

const methodColors = {
  GET: '#3b82f6', // blue
  POST: '#10b981', // green
  PUT: '#f59e0b', // amber
  DELETE: '#ef4444', // red
  PATCH: '#8b5cf6', // purple
};

export default function ApiIntegrationTable() {
  const [filter, setFilter] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');

  const filteredMappings = useMemo(() => {
    return routeMappings.filter(mapping => {
      const matchesFilter = filter === 'all' || mapping.status === filter;
      const matchesSearch =
        searchTerm === '' ||
        mapping.route.toLowerCase().includes(searchTerm.toLowerCase()) ||
        mapping.description.toLowerCase().includes(searchTerm.toLowerCase());

      return matchesFilter && matchesSearch;
    });
  }, [filter, searchTerm]);

  const stats = useMemo(() => {
    const total = routeMappings.length;
    const complete = routeMappings.filter(r => r.status === 'complete').length;
    const partial = routeMappings.filter(r => r.status === 'partial').length;
    const minimal = routeMappings.filter(r => r.status === 'minimal').length;

    return { total, complete, partial, minimal };
  }, []);

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', margin: '20px 0' }}>
      {/* Header con estadísticas */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '16px',
          marginBottom: '24px',
        }}
      >
        <div
          style={{
            padding: '16px',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            backgroundColor: '#f9fafb',
          }}
        >
          <div
            style={{ fontSize: '24px', fontWeight: 'bold', color: '#111827' }}
          >
            {stats.total}
          </div>
          <div style={{ fontSize: '14px', color: '#6b7280' }}>
            Total de Rutas
          </div>
        </div>
        <div
          style={{
            padding: '16px',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            backgroundColor: '#f0fdf4',
          }}
        >
          <div
            style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: statusColors.complete,
            }}
          >
            {stats.complete}
          </div>
          <div style={{ fontSize: '14px', color: '#6b7280' }}>
            Integración Completa
          </div>
        </div>
        <div
          style={{
            padding: '16px',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            backgroundColor: '#fffbeb',
          }}
        >
          <div
            style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: statusColors.partial,
            }}
          >
            {stats.partial}
          </div>
          <div style={{ fontSize: '14px', color: '#6b7280' }}>
            Integración Parcial
          </div>
        </div>
        <div
          style={{
            padding: '16px',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            backgroundColor: '#fef2f2',
          }}
        >
          <div
            style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: statusColors.minimal,
            }}
          >
            {stats.minimal}
          </div>
          <div style={{ fontSize: '14px', color: '#6b7280' }}>
            Integración Mínima
          </div>
        </div>
      </div>

      {/* Controles de filtro */}
      <div
        style={{
          display: 'flex',
          gap: '16px',
          marginBottom: '24px',
          flexWrap: 'wrap',
          alignItems: 'center',
        }}
      >
        <input
          type="text"
          placeholder="Buscar ruta o descripción..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          style={{
            padding: '8px 12px',
            border: '1px solid #d1d5db',
            borderRadius: '6px',
            fontSize: '14px',
            minWidth: '250px',
          }}
        />

        <select
          value={filter}
          onChange={e => setFilter(e.target.value)}
          style={{
            padding: '8px 12px',
            border: '1px solid #d1d5db',
            borderRadius: '6px',
            fontSize: '14px',
          }}
        >
          <option value="all">Todas las rutas</option>
          <option value="complete">Integración completa</option>
          <option value="partial">Integración parcial</option>
          <option value="minimal">Integración mínima</option>
        </select>
      </div>

      {/* Tabla de rutas */}
      <div style={{ overflowX: 'auto' }}>
        {filteredMappings.map((mapping, index) => (
          <div
            key={mapping.route}
            style={{
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              marginBottom: '16px',
              backgroundColor: '#ffffff',
            }}
          >
            {/* Header de la ruta */}
            <div
              style={{
                padding: '16px',
                borderBottom: '1px solid #f3f4f6',
                backgroundColor: '#f9fafb',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  flexWrap: 'wrap',
                }}
              >
                <code
                  style={{
                    fontSize: '18px',
                    fontWeight: 'bold',
                    color: '#111827',
                    backgroundColor: '#f3f4f6',
                    padding: '4px 8px',
                    borderRadius: '4px',
                  }}
                >
                  {mapping.route}
                </code>

                <span
                  style={{
                    fontSize: '12px',
                    padding: '2px 8px',
                    borderRadius: '12px',
                    backgroundColor: statusColors[mapping.status],
                    color: 'white',
                    fontWeight: '500',
                  }}
                >
                  {statusLabels[mapping.status]}
                </span>

                <span style={{ fontSize: '14px', color: '#6b7280' }}>
                  {mapping.file}
                </span>
              </div>

              <p
                style={{
                  margin: '8px 0 0 0',
                  fontSize: '14px',
                  color: '#4b5563',
                }}
              >
                {mapping.description}
              </p>
            </div>

            {/* Contenido de la ruta */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                gap: '16px',
                padding: '16px',
              }}
            >
              {/* Componentes Storybook */}
              <div>
                <h4
                  style={{
                    margin: '0 0 12px 0',
                    fontSize: '16px',
                    color: '#111827',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                  }}
                >
                  🎨 Componentes Storybook
                  <span
                    style={{
                      fontSize: '12px',
                      backgroundColor: '#dbeafe',
                      color: '#1d4ed8',
                      padding: '2px 6px',
                      borderRadius: '4px',
                    }}
                  >
                    {mapping.storybook.length}
                  </span>
                </h4>

                <div
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '8px',
                  }}
                >
                  {mapping.storybook.map((story, idx) => (
                    <a
                      key={idx}
                      href={`http://localhost:6006/${story.path}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '8px 12px',
                        border: '1px solid #e5e7eb',
                        borderRadius: '6px',
                        textDecoration: 'none',
                        color: '#374151',
                        backgroundColor: '#f9fafb',
                        transition: 'all 0.2s',
                        fontSize: '14px',
                      }}
                      onMouseEnter={e => {
                        e.currentTarget.style.backgroundColor = '#f3f4f6';
                        e.currentTarget.style.borderColor = '#d1d5db';
                      }}
                      onMouseLeave={e => {
                        e.currentTarget.style.backgroundColor = '#f9fafb';
                        e.currentTarget.style.borderColor = '#e5e7eb';
                      }}
                    >
                      <span style={{ fontWeight: '500' }}>{story.name}</span>
                      {story.category && (
                        <span
                          style={{
                            fontSize: '11px',
                            backgroundColor: '#dbeafe',
                            color: '#1d4ed8',
                            padding: '1px 6px',
                            borderRadius: '4px',
                            marginLeft: 'auto',
                          }}
                        >
                          {story.category}
                        </span>
                      )}
                    </a>
                  ))}
                </div>
              </div>

              {/* Endpoints API */}
              <div>
                <h4
                  style={{
                    margin: '0 0 12px 0',
                    fontSize: '16px',
                    color: '#111827',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                  }}
                >
                  📡 Endpoints API
                  <span
                    style={{
                      fontSize: '12px',
                      backgroundColor: '#dcfce7',
                      color: '#166534',
                      padding: '2px 6px',
                      borderRadius: '4px',
                    }}
                  >
                    {mapping.endpoints.length}
                  </span>
                </h4>

                <div
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '8px',
                  }}
                >
                  {mapping.endpoints.map((endpoint, idx) => (
                    <a
                      key={idx}
                      href={`http://localhost:8000/docs#operations-${endpoint.router}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '8px 12px',
                        border: '1px solid #e5e7eb',
                        borderRadius: '6px',
                        textDecoration: 'none',
                        color: '#374151',
                        backgroundColor: '#f9fafb',
                        transition: 'all 0.2s',
                        fontSize: '14px',
                      }}
                      onMouseEnter={e => {
                        e.currentTarget.style.backgroundColor = '#f3f4f6';
                        e.currentTarget.style.borderColor = '#d1d5db';
                      }}
                      onMouseLeave={e => {
                        e.currentTarget.style.backgroundColor = '#f9fafb';
                        e.currentTarget.style.borderColor = '#e5e7eb';
                      }}
                    >
                      <span
                        style={{
                          fontSize: '12px',
                          fontWeight: 'bold',
                          padding: '2px 6px',
                          borderRadius: '4px',
                          backgroundColor: methodColors[endpoint.method],
                          color: 'white',
                          minWidth: '50px',
                          textAlign: 'center',
                        }}
                      >
                        {endpoint.method}
                      </span>

                      <code
                        style={{
                          fontSize: '13px',
                          fontFamily: 'Monaco, Consolas, monospace',
                          flex: 1,
                        }}
                      >
                        {endpoint.path}
                      </code>

                      {endpoint.description && (
                        <span
                          style={{
                            fontSize: '11px',
                            color: '#6b7280',
                            fontStyle: 'italic',
                          }}
                        >
                          {endpoint.description}
                        </span>
                      )}
                    </a>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredMappings.length === 0 && (
        <div
          style={{
            padding: '40px',
            textAlign: 'center',
            color: '#6b7280',
            border: '2px dashed #e5e7eb',
            borderRadius: '8px',
          }}
        >
          <p style={{ margin: 0, fontSize: '16px' }}>
            No se encontraron rutas que coincidan con los filtros aplicados.
          </p>
        </div>
      )}

      {/* Footer con información */}
      <div
        style={{
          marginTop: '32px',
          padding: '16px',
          backgroundColor: '#f9fafb',
          borderRadius: '8px',
          fontSize: '14px',
          color: '#6b7280',
        }}
      >
        <p style={{ margin: '0 0 8px 0' }}>
          <strong>💡 Tip:</strong> Haz clic en los enlaces para abrir
          directamente los componentes en Storybook o los endpoints en Swagger.
        </p>
        <p style={{ margin: 0 }}>
          <strong>🔄 Actualización:</strong> Esta tabla se actualiza
          automáticamente cuando se ejecuta{' '}
          <code>./scripts/generate-api-docs.sh</code>
        </p>
      </div>
    </div>
  );
}
