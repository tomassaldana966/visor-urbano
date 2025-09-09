import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { LineChart } from './LineChart';

const mockData = [
  { mes: 'Ene', tramites: 45, eficiencia: 85 },
  { mes: 'Feb', tramites: 52, eficiencia: 78 },
  { mes: 'Mar', tramites: 61, eficiencia: 92 },
  { mes: 'Abr', tramites: 48, eficiencia: 88 },
  { mes: 'May', tramites: 67, eficiencia: 95 },
  { mes: 'Jun', tramites: 73, eficiencia: 91 },
  { mes: 'Jul', tramites: 69, eficiencia: 89 },
  { mes: 'Ago', tramites: 58, eficiencia: 93 },
];

const trendingUpData = [
  { mes: 'Q1', tramites: 120, eficiencia: 75 },
  { mes: 'Q2', tramites: 150, eficiencia: 82 },
  { mes: 'Q3', tramites: 180, eficiencia: 88 },
  { mes: 'Q4', tramites: 210, eficiencia: 94 },
];

const volatileData = [
  { mes: 'Sem1', tramites: 25, eficiencia: 60 },
  { mes: 'Sem2', tramites: 45, eficiencia: 85 },
  { mes: 'Sem3', tramites: 15, eficiencia: 70 },
  { mes: 'Sem4', tramites: 65, eficiencia: 95 },
  { mes: 'Sem5', tramites: 35, eficiencia: 80 },
];

const meta = {
  title: 'Components/Director/Charts/LineChart',
  component: LineChart,
  args: {
    data: mockData,
    title: 'Tendencia de Trámites y Eficiencia',
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof LineChart>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const TrendingUp: Story = {
  args: {
    data: trendingUpData,
    title: 'Crecimiento Trimestral',
  },
};

export const VolatileData: Story = {
  args: {
    data: volatileData,
    title: 'Datos Semanales',
  },
};

export const WithoutZoom: Story = {
  args: {
    showZoom: false,
    title: 'Sin Controles de Zoom',
  },
};

export const CustomHeight: Story = {
  args: {
    height: 400,
    title: 'Gráfico Más Alto',
  },
};

export const MinimalData: Story = {
  args: {
    data: [
      { mes: 'Anterior', tramites: 30, eficiencia: 75 },
      { mes: 'Actual', tramites: 42, eficiencia: 85 },
    ],
    title: 'Comparación Simple',
  },
};
