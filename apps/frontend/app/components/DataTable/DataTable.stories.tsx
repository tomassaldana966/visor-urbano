import type { Meta, StoryObj } from '@storybook/react';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';
import { DataTable } from './DataTable';

const meta: Meta<typeof DataTable> = {
  title: 'Components/DataTable',
  component: DataTable,
  decorators: [
    Story => (
      <I18nextProvider i18n={i18n}>
        <Story />
      </I18nextProvider>
    ),
  ],
  parameters: {
    layout: 'padded',
  },
  tags: ['autodocs'],
  argTypes: {
    enablePagination: {
      control: 'boolean',
    },
    enableSorting: {
      control: 'boolean',
    },
    enableFiltering: {
      control: 'boolean',
    },
    pageSize: {
      control: 'number',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const sampleData = [
  {
    id: '1',
    name: 'Juan Pérez',
    email: 'juan.perez@example.com',
    role: 'Administrador',
    status: 'Activo',
    lastLogin: '2024-01-20',
  },
  {
    id: '2',
    name: 'María García',
    email: 'maria.garcia@example.com',
    role: 'Director',
    status: 'Activo',
    lastLogin: '2024-01-19',
  },
  {
    id: '3',
    name: 'Carlos López',
    email: 'carlos.lopez@example.com',
    role: 'Revisor',
    status: 'Inactivo',
    lastLogin: '2024-01-15',
  },
  {
    id: '4',
    name: 'Ana Martínez',
    email: 'ana.martinez@example.com',
    role: 'Usuario',
    status: 'Activo',
    lastLogin: '2024-01-18',
  },
  {
    id: '5',
    name: 'Roberto Silva',
    email: 'roberto.silva@example.com',
    role: 'Revisor',
    status: 'Activo',
    lastLogin: '2024-01-17',
  },
];

const columns = [
  {
    header: 'Nombre',
    accessorKey: 'name',
  },
  {
    header: 'Email',
    accessorKey: 'email',
  },
  {
    header: 'Rol',
    accessorKey: 'role',
    cell: ({ row }: any) => (
      <span
        className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
          row.original.role === 'Administrador'
            ? 'bg-red-100 text-red-800'
            : row.original.role === 'Director'
              ? 'bg-purple-100 text-purple-800'
              : row.original.role === 'Revisor'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-800'
        }`}
      >
        {row.original.role}
      </span>
    ),
  },
  {
    header: 'Estado',
    accessorKey: 'status',
    cell: ({ row }: any) => (
      <span
        className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
          row.original.status === 'Activo'
            ? 'bg-green-100 text-green-800'
            : 'bg-red-100 text-red-800'
        }`}
      >
        {row.original.status}
      </span>
    ),
  },
  {
    header: 'Último Acceso',
    accessorKey: 'lastLogin',
  },
];

export const Default: Story = {
  args: {
    data: sampleData,
    columns,
    searchPlaceholder: 'Buscar usuarios...',
    noDataMessage: 'No se encontraron usuarios',
    enablePagination: true,
    enableSorting: true,
    enableFiltering: true,
    pageSize: 5,
  },
};

export const WithoutPagination: Story = {
  args: {
    data: sampleData,
    columns,
    enablePagination: false,
    enableSorting: true,
    enableFiltering: true,
  },
};

export const WithoutSorting: Story = {
  args: {
    data: sampleData,
    columns,
    enablePagination: true,
    enableSorting: false,
    enableFiltering: true,
    pageSize: 5,
  },
};

export const WithoutFiltering: Story = {
  args: {
    data: sampleData,
    columns,
    enablePagination: true,
    enableSorting: true,
    enableFiltering: false,
    pageSize: 5,
  },
};

export const EmptyState: Story = {
  args: {
    data: [],
    columns,
    searchPlaceholder: 'Buscar usuarios...',
    noDataMessage: 'No hay usuarios para mostrar',
    enablePagination: true,
    enableSorting: true,
    enableFiltering: true,
  },
};

export const LargeDataset: Story = {
  args: {
    data: Array.from({ length: 50 }, (_, i) => ({
      id: `${i + 1}`,
      name: `Usuario ${i + 1}`,
      email: `usuario${i + 1}@example.com`,
      role: ['Administrador', 'Director', 'Revisor', 'Usuario'][i % 4],
      status: i % 3 === 0 ? 'Inactivo' : 'Activo',
      lastLogin: `2024-01-${String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')}`,
    })),
    columns,
    searchPlaceholder: 'Buscar en 50 usuarios...',
    enablePagination: true,
    enableSorting: true,
    enableFiltering: true,
    pageSize: 10,
  },
};
