import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { ActivityFeed } from './ActivityFeed';

const mockActivities = [
  {
    id: '1',
    type: 'approval' as const,
    title: 'Licencia Aprobada',
    description:
      'La licencia de funcionamiento para Restaurante El Sabor ha sido aprobada',
    timestamp: '2023-06-15T10:30:00Z',
    folio: 'PROC-2023-001',
    user: 'María González',
    priority: 'high' as const,
  },
  {
    id: '2',
    type: 'review' as const,
    title: 'Documentos en Revisión',
    description:
      'Los documentos del expediente PROC-2023-002 están siendo revisados',
    timestamp: '2023-06-15T09:15:00Z',
    folio: 'PROC-2023-002',
    user: 'Carlos Ramírez',
    priority: 'medium' as const,
  },
  {
    id: '3',
    type: 'submission' as const,
    title: 'Nueva Solicitud',
    description: 'Se ha recibido una nueva solicitud de licencia comercial',
    timestamp: '2023-06-15T08:45:00Z',
    folio: 'PROC-2023-003',
    user: 'Ana Martínez',
    priority: 'low' as const,
  },
  {
    id: '4',
    type: 'rejection' as const,
    title: 'Solicitud Rechazada',
    description:
      'La solicitud PROC-2023-004 ha sido rechazada por documentación incompleta',
    timestamp: '2023-06-14T16:20:00Z',
    folio: 'PROC-2023-004',
    user: 'Roberto Silva',
    priority: 'high' as const,
  },
  {
    id: '5',
    type: 'alert' as const,
    title: 'Alerta de Vencimiento',
    description: 'El expediente PROC-2023-005 está próximo a vencer',
    timestamp: '2023-06-14T14:10:00Z',
    folio: 'PROC-2023-005',
    priority: 'high' as const,
  },
];

const meta = {
  title: 'Components/Director/ActivityFeed',
  component: ActivityFeed,
  args: {
    activities: mockActivities,
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof ActivityFeed>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const LimitedItems: Story = {
  args: {
    maxItems: 3,
  },
};

export const WithoutViewAll: Story = {
  args: {
    showViewAll: false,
  },
};

export const EmptyFeed: Story = {
  args: {
    activities: [],
  },
};

export const SingleActivity: Story = {
  args: {
    activities: [mockActivities[0]],
  },
};
