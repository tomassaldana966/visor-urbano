import type { Meta, StoryObj } from '@storybook/react';
import { StatusBadge } from './StatusBadge';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';

const meta: Meta<typeof StatusBadge> = {
  title: 'Components/Procedures/StatusBadge',
  component: StatusBadge,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  decorators: [
    Story => (
      <I18nextProvider i18n={i18n}>
        <div className="p-4">
          <Story />
        </div>
      </I18nextProvider>
    ),
  ],
  argTypes: {
    status: {
      control: 'select',
      options: [
        'approved',
        'in_review',
        'rejected',
        'pending_review',
        'unknown',
      ],
    },
    step: {
      control: 'number',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const mockT = (key: string) => {
  const translations: Record<string, string> = {
    'detail.status.approved': 'Aprobado',
    'detail.status.inReview': 'En Revisión',
    'detail.status.rejected': 'Rechazado',
    'detail.status.pending': 'Pendiente',
    'detail.status.unknown': 'Desconocido',
    'detail.stepStatus.pending': 'Pendiente',
    'detail.stepStatus.inProgress': 'En Progreso',
    'detail.stepStatus.completed': 'Completado',
    'detail.stepStatus.skipped': 'Omitido',
  };
  return translations[key] || key;
};

export const ApprovedStatus: Story = {
  args: {
    status: 'approved',
    t: mockT,
  },
};

export const InReviewStatus: Story = {
  args: {
    status: 'in_review',
    t: mockT,
  },
};

export const RejectedStatus: Story = {
  args: {
    status: 'rejected',
    t: mockT,
  },
};

export const PendingStatus: Story = {
  args: {
    status: 'pending_review',
    t: mockT,
  },
};

export const UnknownStatus: Story = {
  args: {
    status: 'unknown',
    t: mockT,
  },
};

export const StepPending: Story = {
  args: {
    step: 0,
    t: mockT,
  },
};

export const StepInProgress: Story = {
  args: {
    step: 1,
    t: mockT,
  },
};

export const StepCompleted: Story = {
  args: {
    step: 2,
    t: mockT,
  },
};

export const StepSkipped: Story = {
  args: {
    step: -1,
    t: mockT,
  },
};

export const AllStatusVariants: Story = {
  render: () => (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Estado del Procedimiento
          </h3>
          <div className="space-y-2">
            <StatusBadge status="approved" t={mockT} />
            <StatusBadge status="in_review" t={mockT} />
            <StatusBadge status="rejected" t={mockT} />
            <StatusBadge status="pending_review" t={mockT} />
            <StatusBadge status="unknown" t={mockT} />
          </div>
        </div>
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Estado del Paso
          </h3>
          <div className="space-y-2">
            <StatusBadge step={0} t={mockT} />
            <StatusBadge step={1} t={mockT} />
            <StatusBadge step={2} t={mockT} />
            <StatusBadge step={-1} t={mockT} />
          </div>
        </div>
      </div>
    </div>
  ),
};
