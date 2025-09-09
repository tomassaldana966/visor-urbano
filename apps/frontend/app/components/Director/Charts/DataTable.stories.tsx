import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';
import { Badge } from '../../Badge/Badge';

import { DataTable } from './DataTable';

interface ProcedureData {
  folio: string;
  tipo: string;
  solicitante: string;
  estado: string;
  fecha: string;
  dias: number;
}

const mockData: ProcedureData[] = [
  {
    folio: 'PROC-2023-001',
    tipo: 'Licencia de Funcionamiento',
    solicitante: 'Restaurante El Sabor',
    estado: 'En Proceso',
    fecha: '2023-06-15',
    dias: 5,
  },
  {
    folio: 'PROC-2023-002',
    tipo: 'Permiso de Construcción',
    solicitante: 'Constructora ABC',
    estado: 'Aprobado',
    fecha: '2023-06-10',
    dias: 12,
  },
  {
    folio: 'PROC-2023-003',
    tipo: 'Licencia Comercial',
    solicitante: 'Tienda Fashion',
    estado: 'Rechazado',
    fecha: '2023-06-08',
    dias: 8,
  },
  {
    folio: 'PROC-2023-004',
    tipo: 'Permiso de Eventos',
    solicitante: 'Eventos Monterrey',
    estado: 'Pendiente',
    fecha: '2023-06-20',
    dias: 1,
  },
  {
    folio: 'PROC-2023-005',
    tipo: 'Licencia de Funcionamiento',
    solicitante: 'Consultorio Médico',
    estado: 'En Proceso',
    fecha: '2023-06-18',
    dias: 3,
  },
];

const columns = [
  { key: 'folio' as keyof ProcedureData, label: 'Folio', sortable: true },
  {
    key: 'tipo' as keyof ProcedureData,
    label: 'Tipo de Trámite',
    sortable: true,
  },
  {
    key: 'solicitante' as keyof ProcedureData,
    label: 'Solicitante',
    sortable: true,
  },
  {
    key: 'estado' as keyof ProcedureData,
    label: 'Estado',
    sortable: true,
    render: (value: string) => {
      const variant =
        value === 'Aprobado'
          ? 'success'
          : value === 'Rechazado'
            ? 'destructive'
            : value === 'En Proceso'
              ? 'warning'
              : 'secondary';
      return <Badge variant={variant}>{value}</Badge>;
    },
  },
  { key: 'fecha' as keyof ProcedureData, label: 'Fecha', sortable: true },
  {
    key: 'dias' as keyof ProcedureData,
    label: 'Días Transcurridos',
    sortable: true,
  },
];

const simpleData = mockData.slice(0, 2);

const meta = {
  title: 'Components/Director/Charts/DataTable',
  component: DataTable,
  args: {
    data: mockData,
    columns,
    title: 'Registro de Trámites',
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    exportable: {
      control: 'boolean',
    },
    searchable: {
      control: 'boolean',
    },
    filterable: {
      control: 'boolean',
    },
    itemsPerPage: {
      control: 'number',
    },
    initialSort: {
      control: 'object',
      description: 'Initial sort configuration with key and direction',
    },
  },
} satisfies Meta<ComponentProps<typeof DataTable<ProcedureData>>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const SimpleData: Story = {
  args: {
    data: simpleData,
    title: 'Tabla Básica',
  },
};

export const WithoutFeatures: Story = {
  args: {
    exportable: false,
    searchable: false,
    filterable: false,
    title: 'Tabla Sin Funciones Extra',
  },
};

export const SmallPageSize: Story = {
  args: {
    itemsPerPage: 3,
    title: 'Tabla con Paginación',
  },
};

export const EmptyTable: Story = {
  args: {
    data: [],
    title: 'Tabla Vacía',
  },
};

export const WithInitialSortByFolio: Story = {
  args: {
    title: 'Tabla Ordenada por Folio',
    initialSort: { key: 'folio', direction: 'asc' },
  },
};

export const WithInitialSortByDate: Story = {
  args: {
    title: 'Tabla Ordenada por Fecha (Descendente)',
    initialSort: { key: 'fecha', direction: 'desc' },
  },
};

export const WithInitialSortByDays: Story = {
  args: {
    title: 'Tabla Ordenada por Días Transcurridos',
    initialSort: { key: 'dias', direction: 'desc' },
  },
};
