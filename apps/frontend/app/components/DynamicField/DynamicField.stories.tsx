import type { Meta, StoryObj } from '@storybook/react';
import { DynamicFieldRenderer } from './DynamicFieldRenderer';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';

const meta: Meta = {
  title: 'Components/DynamicField',
  parameters: {
    layout: 'padded',
  },
  tags: ['autodocs'],
  decorators: [
    Story => (
      <I18nextProvider i18n={i18n}>
        <div className="max-w-2xl mx-auto p-6">
          <Story />
        </div>
      </I18nextProvider>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const DynamicFieldOverview: Story = {
  render: () => (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Campos Dinámicos
        </h2>
        <p className="text-gray-600 mb-8">
          Los campos dinámicos permiten crear formularios flexibles que se
          adaptan según las necesidades específicas de cada procedimiento o
          municipio.
        </p>
      </div>

      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Tipos de Campo Disponibles
          </h3>
          <div className="grid gap-4">
            <DynamicFieldRenderer
              field={{
                id: 1,
                name: 'text_input',
                field_type: 'input',
                description: 'Campo de Texto',
                required: true,
              }}
              value=""
              onChange={() => {}}
              formValues={{}}
            />

            <DynamicFieldRenderer
              field={{
                id: 2,
                name: 'select_input',
                field_type: 'select',
                description: 'Lista Desplegable',
                required: true,
                options: 'Opción 1|Opción 2|Opción 3',
              }}
              value=""
              onChange={() => {}}
              formValues={{}}
            />

            <DynamicFieldRenderer
              field={{
                id: 3,
                name: 'textarea_input',
                field_type: 'textarea',
                description: 'Área de Texto',
                required: false,
              }}
              value=""
              onChange={() => {}}
              formValues={{}}
            />

            <DynamicFieldRenderer
              field={{
                id: 4,
                name: 'file_input',
                field_type: 'file',
                description: 'Campo de Archivo',
                required: true,
                options: 'accept:.pdf,.doc,.docx',
              }}
              value={null}
              onChange={() => {}}
              formValues={{}}
            />
          </div>
        </div>

        <div className="bg-blue-50 p-4 rounded-lg">
          <h4 className="text-sm font-medium text-blue-800 mb-2">
            Características
          </h4>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• Validación automática según el tipo de campo</li>
            <li>• Soporte para condiciones de visibilidad</li>
            <li>• Opciones configurables por municipio</li>
            <li>• Integración con sistema de archivos</li>
          </ul>
        </div>
      </div>
    </div>
  ),
};
