import type { Meta, StoryObj } from '@storybook/react';
import { LicensesTable } from './LicensesTable';

const meta: Meta<typeof LicensesTable> = {
  title: 'Components/LicensesTable',
  component: LicensesTable,
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component:
          'A table component for displaying business licenses with search functionality, pagination, and various status indicators.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    licenses: {
      description: 'Array of business license objects to display',
      control: 'object',
    },
    isLoading: {
      control: 'boolean',
      description: 'Shows loading spinner when true',
    },
    onSearch: {
      action: 'search',
      description: 'Callback function when search is performed',
    },
    onPageChange: {
      action: 'page-change',
      description: 'Callback function when page is changed',
    },
    currentPage: {
      control: { type: 'number', min: 1 },
      description: 'Current page number',
    },
    totalPages: {
      control: { type: 'number', min: 1 },
      description: 'Total number of pages',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const mockLicenses = [
  {
    license_folio: 'LIC-2024-001',
    commercial_activity: 'Restaurante',
    industry_classification_code: '722511',
    municipality_id: 1,
    municipality_name: 'Guadalajara',
    license_status: 'active',
    license_type: 'Commercial',
  },
  {
    license_folio: 'LIC-2024-002',
    commercial_activity: 'Tienda de Abarrotes',
    industry_classification_code: '461110',
    municipality_id: 2,
    municipality_name: 'Zapopan',
    license_status: 'pending',
    license_type: 'Commercial',
  },
  {
    license_folio: 'LIC-2024-003',
    commercial_activity: 'Farmacia',
    industry_classification_code: '464111',
    municipality_id: 1,
    municipality_name: 'Guadalajara',
    license_status: 'suspended',
    license_type: 'Healthcare',
  },
  {
    license_folio: 'LIC-2024-004',
    commercial_activity: 'Oficina de Contabilidad',
    industry_classification_code: '541211',
    municipality_id: 3,
    municipality_name: 'Tlaquepaque',
    license_status: 'cancelled',
    license_type: 'Professional Services',
  },
  {
    license_folio: 'LIC-2024-005',
    commercial_activity: 'Taller Mecánico',
    industry_classification_code: '811111',
    municipality_id: 2,
    municipality_name: 'Zapopan',
    license_status: 'active',
    license_type: 'Automotive',
  },
];

export const Default: Story = {
  args: {
    licenses: mockLicenses,
    isLoading: false,
    currentPage: 1,
    totalPages: 3,
  },
};

export const Loading: Story = {
  args: {
    licenses: [],
    isLoading: true,
    currentPage: 1,
    totalPages: 1,
  },
};

export const Empty: Story = {
  args: {
    licenses: [],
    isLoading: false,
    currentPage: 1,
    totalPages: 1,
  },
};

export const SinglePage: Story = {
  args: {
    licenses: mockLicenses.slice(0, 2),
    isLoading: false,
    currentPage: 1,
    totalPages: 1,
  },
};

export const WithPagination: Story = {
  args: {
    licenses: mockLicenses,
    isLoading: false,
    currentPage: 2,
    totalPages: 5,
  },
};

export const LastPage: Story = {
  args: {
    licenses: mockLicenses.slice(0, 3),
    isLoading: false,
    currentPage: 5,
    totalPages: 5,
  },
};

export const FirstPage: Story = {
  args: {
    licenses: mockLicenses,
    isLoading: false,
    currentPage: 1,
    totalPages: 5,
  },
};

export const OnlyActiveLicenses: Story = {
  args: {
    licenses: mockLicenses.filter(
      license => license.license_status === 'active'
    ),
    isLoading: false,
    currentPage: 1,
    totalPages: 1,
  },
};

export const OnlyPendingLicenses: Story = {
  args: {
    licenses: mockLicenses.filter(
      license => license.license_status === 'pending'
    ),
    isLoading: false,
    currentPage: 1,
    totalPages: 1,
  },
};

export const MixedStatuses: Story = {
  args: {
    licenses: [
      ...mockLicenses,
      {
        license_folio: 'LIC-2024-006',
        commercial_activity: 'Servicio sin Estado',
        industry_classification_code: '999999',
        municipality_id: 4,
        municipality_name: 'Tonalá',
        license_status: undefined,
        license_type: 'Unknown',
      },
    ],
    isLoading: false,
    currentPage: 1,
    totalPages: 2,
  },
};

export const LongContent: Story = {
  args: {
    licenses: [
      {
        license_folio: 'LIC-2024-VERY-LONG-FOLIO-NUMBER-001',
        commercial_activity:
          'Restaurante Especializado en Comida Internacional con Servicio de Delivery y Catering para Eventos Corporativos',
        industry_classification_code: '722511-EXTENDED',
        municipality_id: 1,
        municipality_name: 'Guadalajara Metropolitana',
        license_status: 'active',
        license_type: 'Commercial Extended',
      },
    ],
    isLoading: false,
    currentPage: 1,
    totalPages: 1,
  },
};

export const MissingData: Story = {
  args: {
    licenses: [
      {
        license_folio: 'LIC-2024-007',
        commercial_activity: 'Negocio con Datos Faltantes',
        industry_classification_code: '',
        municipality_name: '',
        license_status: '',
        license_type: '',
      },
    ],
    isLoading: false,
    currentPage: 1,
    totalPages: 1,
  },
};
