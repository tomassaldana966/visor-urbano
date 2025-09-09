import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { ProcedureFilesModal } from './ProcedureFilesModal';

const meta = {
  title: 'Components/ProcedureFilesModal',
  component: ProcedureFilesModal,
  args: {
    isOpen: true,
    onClose: () => {},
    procedureId: 123,
    authToken: 'mock-auth-token',
  },
  parameters: {
    layout: 'centered',
    mockData: [
      {
        url: '/v1/notifications/procedure/123/files',
        method: 'GET',
        status: 200,
        response: [
          {
            id: 1,
            file_path: '/uploads/documents/plan.pdf',
            file_name: 'Construction Plan.pdf',
            file_type: 'application/pdf',
            file_size: 2048576,
            uploaded_at: '2023-06-15T10:30:00Z',
            created_at: '2023-06-15T10:30:00Z',
            updated_at: '2023-06-15T10:30:00Z',
          },
          {
            id: 2,
            file_path: '/uploads/documents/blueprint.dwg',
            file_name: 'Building Blueprint.dwg',
            file_type: 'application/dwg',
            file_size: 5242880,
            uploaded_at: '2023-06-15T11:00:00Z',
            created_at: '2023-06-15T11:00:00Z',
            updated_at: '2023-06-15T11:00:00Z',
          },
        ],
      },
    ],
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof ProcedureFilesModal>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Closed: Story = {
  args: {
    isOpen: false,
  },
};

export const NoProcedureId: Story = {
  args: {
    procedureId: null,
  },
};

export const Loading: Story = {
  parameters: {
    mockData: [
      {
        url: '/v1/notifications/procedure/123/files',
        method: 'GET',
        delay: 3000,
        status: 200,
        response: [],
      },
    ],
  },
};

export const Error: Story = {
  parameters: {
    mockData: [
      {
        url: '/v1/notifications/procedure/123/files',
        method: 'GET',
        status: 500,
        response: { error: 'Failed to load files' },
      },
    ],
  },
};
