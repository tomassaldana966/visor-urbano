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
    route: '/home',
    file: 'routes/home.tsx',
    description: 'Página principal con dashboard y estadísticas',
    status: 'complete',
    storybook: [
      { name: 'Hero', path: 'components-hero--default', category: 'Layout' },
      {
        name: 'Dashboard Cards',
        path: 'components-dashboard--cards',
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
    route: '/map',
    file: 'routes/map.tsx',
    description: 'Mapa interactivo con capas y búsqueda geoespacial',
    status: 'complete',
    storybook: [
      {
        name: 'Map Container',
        path: 'components-map--interactive',
        category: 'Map',
      },
      { name: 'Map Layers', path: 'components-map--layers', category: 'Map' },
      {
        name: 'Map Controls',
        path: 'components-map--controls',
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
    route: '/licenses',
    file: 'routes/licenses.tsx',
    description: 'Gestión de licencias comerciales y permisos',
    status: 'complete',
    storybook: [
      {
        name: 'License Form',
        path: 'forms-license--default',
        category: 'Forms',
      },
      {
        name: 'License Card',
        path: 'components-license--card',
        category: 'Data Display',
      },
      {
        name: 'Issue License Modal',
        path: 'modals-issuelicense--default',
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
    route: '/licenses-issued',
    file: 'routes/licenses-issued.tsx',
    description: 'Vista de licencias emitidas y su estado',
    status: 'partial',
    storybook: [
      {
        name: 'Licenses Table',
        path: 'components-licensestable--default',
        category: 'Data Display',
      },
      {
        name: 'Status Badge',
        path: 'components-badge--status',
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
    route: '/notifications',
    file: 'routes/notifications.tsx',
    description: 'Centro de notificaciones del usuario',
    status: 'partial',
    storybook: [
      {
        name: 'Notification Card',
        path: 'components-notification--card',
        category: 'Data Display',
      },
      {
        name: 'Notification List',
        path: 'components-notification--list',
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
    route: '/login',
    file: 'routes/login.tsx',
    description: 'Página de inicio de sesión',
    status: 'minimal',
    storybook: [
      { name: 'Login Form', path: 'forms-login--default', category: 'Forms' },
      { name: 'Input', path: 'components-input--default', category: 'Forms' },
      { name: 'Button', path: 'components-button--primary', category: 'Forms' },
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
                      href={`http://localhost:6006/?path=/story/${story.path}`}
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
