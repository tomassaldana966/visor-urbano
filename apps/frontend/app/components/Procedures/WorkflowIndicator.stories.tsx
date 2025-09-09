import type { Meta, StoryObj } from '@storybook/react';
import { WorkflowIndicator } from './WorkflowIndicator';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';

const meta: Meta<typeof WorkflowIndicator> = {
  title: 'Components/Procedures/WorkflowIndicator',
  component: WorkflowIndicator,
  parameters: {
    layout: 'padded',
  },
  tags: ['autodocs'],
  decorators: [
    Story => (
      <I18nextProvider i18n={i18n}>
        <div className="max-w-4xl mx-auto p-6">
          <Story />
        </div>
      </I18nextProvider>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof meta>;

const mockT = (key: string) => {
  const translations: Record<string, string> = {
    'detail.workflow.steps.submit': 'Envío de Solicitud',
    'detail.workflow.steps.submitDescription':
      'Solicitud enviada y registrada en el sistema',
    'detail.workflow.steps.review': 'Revisión Técnica',
    'detail.workflow.steps.reviewDescription':
      'Revisión de documentos y requisitos técnicos',
    'detail.workflow.steps.approval': 'Aprobación',
    'detail.workflow.steps.approvalDescription':
      'Aprobación final de la solicitud',
    'detail.workflow.steps.license': 'Generación de Licencia',
    'detail.workflow.steps.licenseDescription':
      'Generación y entrega de la licencia',
  };
  return translations[key] || key;
};

const baseProcedure = {
  id: 1,
  folio: 'CONST-2024-001',
  procedure_type: 'construction',
  created_at: '2024-01-15T10:00:00Z',
  sent_to_reviewers: false,
  director_approval: false,
  step_one: 0,
  step_two: 0,
  step_three: 0,
  step_four: 0,
  window_license_generated: false,
};

export const InitialState: Story = {
  args: {
    procedure: {
      ...baseProcedure,
      status: 1,
    },
    t: mockT,
  },
};

export const InReview: Story = {
  args: {
    procedure: {
      ...baseProcedure,
      status: 3,
      sent_to_reviewers: true,
      step_one: 1,
    },
    t: mockT,
  },
};

export const DirectorApproval: Story = {
  args: {
    procedure: {
      ...baseProcedure,
      status: 5,
      sent_to_reviewers: true,
      director_approval: true,
      step_one: 2,
      step_two: 2,
      step_three: 1,
    },
    t: mockT,
  },
};

export const Completed: Story = {
  args: {
    procedure: {
      ...baseProcedure,
      status: 7,
      sent_to_reviewers: true,
      director_approval: true,
      step_one: 2,
      step_two: 2,
      step_three: 2,
      step_four: 2,
      window_license_generated: true,
    },
    t: mockT,
    workflowStatus: {
      current_workflow_step: 'completed',
    },
  },
};

export const Rejected: Story = {
  args: {
    procedure: {
      ...baseProcedure,
      status: 4,
      sent_to_reviewers: true,
      step_one: -1,
    },
    t: mockT,
    workflowStatus: {
      current_workflow_step: 'rejected',
    },
  },
};

export const CommercialProcedure: Story = {
  args: {
    procedure: {
      ...baseProcedure,
      procedure_type: 'commercial',
      status: 4,
      sent_to_reviewers: true,
      step_one: 2,
      step_two: 1,
    },
    t: mockT,
  },
};

export const WindowProcedure: Story = {
  args: {
    procedure: {
      ...baseProcedure,
      procedure_type: 'window',
      status: 6,
      sent_to_reviewers: true,
      director_approval: true,
      step_one: 2,
      step_two: 2,
      step_three: 2,
      window_license_generated: false,
    },
    t: mockT,
  },
};
