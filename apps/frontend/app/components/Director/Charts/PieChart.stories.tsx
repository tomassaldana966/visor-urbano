import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { PieChart } from './PieChart';

const mockData = [
  { estado: 'Aprobado', cantidad: 45, porcentaje: 45, color: '#10b981' },
  { estado: 'En Proceso', cantidad: 32, porcentaje: 32, color: '#f59e0b' },
  { estado: 'Rechazado', cantidad: 13, porcentaje: 13, color: '#ef4444' },
  { estado: 'Pendiente', cantidad: 10, porcentaje: 10, color: '#6b7280' },
];

const businessTypesData = [
  { estado: 'Restaurantes', cantidad: 28, porcentaje: 35, color: '#3b82f6' },
  { estado: 'Tiendas', cantidad: 22, porcentaje: 27.5, color: '#8b5cf6' },
  { estado: 'Servicios', cantidad: 18, porcentaje: 22.5, color: '#06b6d4' },
  { estado: 'Oficinas', cantidad: 12, porcentaje: 15, color: '#84cc16' },
];

const simpleData = [
  { estado: 'Completados', cantidad: 75, porcentaje: 75, color: '#10b981' },
  { estado: 'Pendientes', cantidad: 25, porcentaje: 25, color: '#f59e0b' },
];

const complexData = [
  { estado: 'Comercial', cantidad: 25, porcentaje: 20.8, color: '#3b82f6' },
  { estado: 'Residencial', cantidad: 30, porcentaje: 25, color: '#8b5cf6' },
  { estado: 'Industrial', cantidad: 15, porcentaje: 12.5, color: '#06b6d4' },
  { estado: 'Servicios', cantidad: 20, porcentaje: 16.7, color: '#84cc16' },
  { estado: 'Educativo', cantidad: 18, porcentaje: 15, color: '#f59e0b' },
  { estado: 'Salud', cantidad: 12, porcentaje: 10, color: '#ef4444' },
];

const meta = {
  title: 'Components/Director/Charts/PieChart',
  component: PieChart,
  args: {
    data: mockData,
    title: 'Estado de Trámites',
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof PieChart>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const BusinessTypes: Story = {
  args: {
    data: businessTypesData,
    title: 'Tipos de Negocio',
  },
};

export const SimpleDistribution: Story = {
  args: {
    data: simpleData,
    title: 'Distribución Simple',
  },
};

export const ComplexData: Story = {
  args: {
    data: complexData,
    title: 'Sectores Económicos',
  },
};

export const NonInteractive: Story = {
  args: {
    interactive: false,
    title: 'Gráfico Estático',
  },
};

export const EmptyData: Story = {
  args: {
    data: [],
    title: 'Sin Datos',
  },
};
