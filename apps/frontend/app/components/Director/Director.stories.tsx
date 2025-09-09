import type { Meta, StoryObj } from '@storybook/react';
import { QuickActionsPanel } from './QuickActionsPanel';
import { MetricsCard } from './MetricsCard';
import { ActivityFeed } from './ActivityFeed';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';
import { Users, FileCheck } from 'lucide-react';

const meta: Meta = {
  title: 'Components/Director',
  parameters: {
    layout: 'padded',
  },
  tags: ['autodocs'],
  decorators: [
    Story => (
      <I18nextProvider i18n={i18n}>
        <div className="max-w-6xl mx-auto p-6">
          <Story />
        </div>
      </I18nextProvider>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof meta>;

const mockActivities = [
  {
    id: '1',
    type: 'submission' as const,
    title: 'Nueva solicitud enviada',
    description: 'Solicitud CONST-2024-001 enviada por Juan Pérez',
    timestamp: '2024-01-15T10:30:00Z',
    user: 'Juan Pérez',
    folio: 'CONST-2024-001',
    priority: 'medium' as const,
  },
  {
    id: '2',
    type: 'approval' as const,
    title: 'Procedimiento aprobado',
    description: 'Solicitud COMM-2024-002 aprobada por Director',
    timestamp: '2024-01-15T09:15:00Z',
    user: 'Director Municipal',
    folio: 'COMM-2024-002',
    priority: 'high' as const,
  },
];

const mockNotifications = [
  {
    id: '1',
    title: 'Revisión pendiente',
    message: 'Hay 5 solicitudes esperando revisión técnica',
    type: 'warning' as const,
    timestamp: new Date('2024-01-15T11:00:00Z'),
    read: false,
    category: 'permits' as const,
    priority: 'high' as const,
  },
  {
    id: '2',
    title: 'Sistema actualizado',
    message: 'El sistema se actualizó exitosamente',
    type: 'success' as const,
    timestamp: new Date('2024-01-15T08:00:00Z'),
    read: true,
    category: 'system' as const,
    priority: 'low' as const,
  },
];

export const DirectorDashboardOverview: Story = {
  render: () => (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Panel de Director
        </h2>
        <p className="text-gray-600 mb-8">
          Componentes principales del panel de control para directores
          municipales, incluyendo métricas, acciones rápidas, actividades
          recientes y notificaciones.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Métricas</h3>
          <div className="grid grid-cols-2 gap-4">
            <MetricsCard
              title="Solicitudes Activas"
              value="24"
              icon={<FileCheck className="w-5 h-5" />}
              trend="up"
              trendValue="12%"
              color="primary"
            />
            <MetricsCard
              title="Usuarios Activos"
              value="156"
              icon={<Users className="w-5 h-5" />}
              trend="down"
              trendValue="3%"
              color="success"
            />
          </div>
        </div>

        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Notificaciones
          </h3>
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <p className="text-gray-600 text-sm">
              Sistema de notificaciones integrado para alertas importantes,
              actualizaciones del sistema y recordatorios de tareas pendientes.
            </p>
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Acciones Rápidas
        </h3>
        <QuickActionsPanel
          onNavigateToUsers={() => {}}
          onNavigateToAnalytics={() => {}}
          onNavigateToSettings={() => {}}
          onNavigateToMunicipalLayers={() => {}}
          onNavigateToImpactMap={() => {}}
          onNavigateToRoles={() => {}}
          onNavigateToRequirements={() => {}}
          onNavigateToBusinessTypes={() => {}}
          onNavigateToDependencies={() => {}}
          onNavigateToBlog={() => {}}
          onExportReports={() => {}}
          onViewNotifications={() => {}}
        />
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Actividad Reciente
        </h3>
        <ActivityFeed activities={mockActivities} />
      </div>

      <div className="bg-gray-50 p-4 rounded-lg">
        <h4 className="text-sm font-medium text-gray-800 mb-2">
          Funcionalidades Principales
        </h4>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• Panel de métricas en tiempo real</li>
          <li>• Sistema de notificaciones integrado</li>
          <li>• Acceso rápido a funciones administrativas</li>
          <li>• Seguimiento de actividades del sistema</li>
          <li>• Gestión de flujos de trabajo</li>
        </ul>
      </div>
    </div>
  ),
};
