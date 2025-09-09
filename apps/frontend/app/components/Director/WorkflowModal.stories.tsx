import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { WorkflowModal } from './WorkflowModal';

const mockWorkflow = {
  id: '1',
  name: 'Licencia de Funcionamiento',
  type: 'Comercial',
  steps: 5,
  avgDays: 15,
  active: true,
  documentType: 'FUNC',
  description:
    'Licencia requerida para el funcionamiento de establecimientos comerciales',
  legalFoundation: 'Artículo 123 del Reglamento Municipal',
  requirements: [
    {
      id: 'req1',
      title: 'Acta Constitutiva',
      description: 'Documento que acredita la constitución legal de la empresa',
      mandatory: true,
      departmentIssued: false,
    },
    {
      id: 'req2',
      title: 'Constancia de Uso de Suelo',
      description: 'Documento emitido por el departamento de desarrollo urbano',
      mandatory: true,
      departmentIssued: true,
    },
  ],
  departments: ['Desarrollo Urbano', 'Hacienda', 'Bomberos'],
};

const mockNewWorkflow = {
  id: '',
  name: '',
  type: '',
  steps: 0,
  avgDays: 0,
  active: true,
};

const meta = {
  title: 'Components/Director/WorkflowModal',
  component: WorkflowModal,
  args: {
    isOpen: true,
    onClose: () => {},
    workflow: mockWorkflow,
    onSave: workflow => {},
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof WorkflowModal>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const EditExisting: Story = {};

export const CreateNew: Story = {
  args: {
    workflow: mockNewWorkflow,
  },
};

export const Closed: Story = {
  args: {
    isOpen: false,
  },
};

export const NoWorkflow: Story = {
  args: {
    workflow: null,
  },
};
