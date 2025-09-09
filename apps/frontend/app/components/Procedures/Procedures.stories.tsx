import type { Meta, StoryObj } from '@storybook/react';
import { SectionForm } from './SectionForm';
import { StatusBadge } from './StatusBadge';
import { WorkflowIndicator } from './WorkflowIndicator';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';
import { FileText } from 'lucide-react';

const meta: Meta = {
  title: 'Components/Procedures',
  parameters: {
    layout: 'padded',
  },
  tags: ['autodocs'],
  decorators: [
    Story => (
      <I18nextProvider i18n={i18n}>
        <div className="max-w-4xl mx-auto">
          <Story />
        </div>
      </I18nextProvider>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof meta>;

const mockT = (key: string) => key;

const mockFields = [
  {
    id: 1,
    name: 'project_name',
    field_type: 'input' as const,
    description: 'Nombre del Proyecto',
    required: true,
    options: 'placeholder:Ingrese el nombre del proyecto',
  },
  {
    id: 2,
    name: 'project_type',
    field_type: 'select' as const,
    description: 'Tipo de Proyecto',
    required: true,
    options: 'Residencial|Comercial|Industrial',
  },
];

const mockProcedure = {
  id: 1,
  folio: 'CONST-2024-001',
  procedure_type: 'construction',
  status: 3,
  created_at: '2024-01-15T10:00:00Z',
  sent_to_reviewers: true,
  director_approval: false,
  step_one: 1,
  step_two: 0,
  step_three: 0,
  step_four: 0,
  window_license_generated: false,
};

export const ProceduresOverview: Story = {
  render: () => (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Componentes de Procedimientos
        </h2>
        <p className="text-gray-600 mb-8">
          Esta sección muestra los componentes principales utilizados en el
          módulo de procedimientos, incluyendo formularios de sección,
          indicadores de estado y flujo de trabajo.
        </p>
      </div>

      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Estado de Procedimiento
          </h3>
          <div className="flex gap-4 flex-wrap">
            <StatusBadge status="approved" t={mockT} />
            <StatusBadge status="in_review" t={mockT} />
            <StatusBadge status="rejected" t={mockT} />
            <StatusBadge status="pending_review" t={mockT} />
          </div>
        </div>

        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Indicador de Flujo de Trabajo
          </h3>
          <WorkflowIndicator procedure={mockProcedure} t={mockT} />
        </div>

        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Formulario de Sección
          </h3>
          <SectionForm
            sectionId="demo-section"
            fields={mockFields}
            sectionTitle="Información del Proyecto"
            sectionIcon={FileText}
            sectionDescription="Complete la información básica del proyecto"
            folio="DEMO-2024-001"
            isExpanded={true}
            onToggle={() => {}}
            t={mockT}
            procedureId={123}
            authToken="demo-token"
          />
        </div>
      </div>
    </div>
  ),
};
