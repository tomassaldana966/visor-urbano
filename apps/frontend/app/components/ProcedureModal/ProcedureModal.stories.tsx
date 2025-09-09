import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { ProcedureModal } from './ProcedureModal';

const mockProcedure = {
  id: 1,
  folio: 'PROC-2023-001',
  street: 'Av. Principal',
  exterior_number: '123',
  interior_number: 'A',
  neighborhood: 'Centro',
  municipality: 'Guadalajara',
  state: 'Jalisco',
  business_name: 'Restaurante El Sabor',
  business_type: 'Restaurante',
  status: 'pending_review' as const,
  created_at: '2023-06-15T10:30:00Z',
  updated_at: '2023-06-15T14:45:00Z',
  applicant_name: 'Juan Pérez',
  applicant_email: 'juan.perez@example.com',
  phone: '+52 33 1234 5678',
  description:
    'Solicitud de licencia para apertura de restaurante con capacidad para 50 personas.',
};

const mockCompletedProcedure = {
  ...mockProcedure,
  id: 2,
  folio: 'PROC-2023-002',
  status: 'approved' as const,
  business_name: 'Tienda de Ropa Fashion',
  business_type: 'Comercio minorista',
};

const mockPendingProcedure = {
  ...mockProcedure,
  id: 3,
  folio: 'PROC-2023-003',
  status: 'in_review' as const,
  business_name: 'Consultorio Médico',
  business_type: 'Servicios de salud',
};

const mockRejectedProcedure = {
  ...mockProcedure,
  id: 4,
  folio: 'PROC-2023-004',
  status: 'rejected' as const,
  business_name: 'Bar La Cantina',
  business_type: 'Entretenimiento',
};

const meta = {
  title: 'Components/ProcedureModal',
  component: ProcedureModal,
  args: {
    isOpen: true,
    onClose: () => {},
    procedure: mockProcedure,
    onContinue: () => {},
    onViewFiles: () => {},
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof ProcedureModal>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const CompletedProcedure: Story = {
  args: {
    procedure: mockCompletedProcedure,
  },
};

export const PendingProcedure: Story = {
  args: {
    procedure: mockPendingProcedure,
  },
};

export const RejectedProcedure: Story = {
  args: {
    procedure: mockRejectedProcedure,
  },
};

export const Closed: Story = {
  args: {
    isOpen: false,
  },
};

export const NoProcedure: Story = {
  args: {
    procedure: null,
  },
};

export const WithoutActions: Story = {
  args: {
    onContinue: undefined,
    onViewFiles: undefined,
  },
};
