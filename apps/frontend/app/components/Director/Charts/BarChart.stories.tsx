import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { BarChart } from './BarChart';

const mockData = [
  { mes: 'Ene', tramites: 45, eficiencia: 85 },
  { mes: 'Feb', tramites: 52, eficiencia: 78 },
  { mes: 'Mar', tramites: 61, eficiencia: 92 },
  { mes: 'Abr', tramites: 48, eficiencia: 88 },
  { mes: 'May', tramites: 67, eficiencia: 95 },
  { mes: 'Jun', tramites: 73, eficiencia: 91 },
];

const smallData = [
  { mes: 'Q1', tramites: 158, eficiencia: 85 },
  { mes: 'Q2', tramites: 188, eficiencia: 91 },
  { mes: 'Q3', tramites: 145, eficiencia: 87 },
];

const singleData = [{ mes: 'Actual', tramites: 42, eficiencia: 89 }];

const meta = {
  title: 'Components/Director/Charts/BarChart',
  component: BarChart,
  args: {
    data: mockData,
    title: 'Trámites por Mes',
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof BarChart>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const QuarterlyData: Story = {
  args: {
    data: smallData,
    title: 'Trámites por Trimestre',
  },
};

export const SinglePeriod: Story = {
  args: {
    data: singleData,
    title: 'Período Actual',
  },
};

export const CustomHeight: Story = {
  args: {
    height: 400,
    title: 'Gráfico Más Alto',
  },
};

export const EmptyData: Story = {
  args: {
    data: [],
    title: 'Sin Datos',
  },
};
