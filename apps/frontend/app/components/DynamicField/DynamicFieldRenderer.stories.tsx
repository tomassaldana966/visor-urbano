import type { Meta, StoryObj } from '@storybook/react';
import { DynamicFieldRenderer } from './DynamicFieldRenderer';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';
import { useState } from 'react';

const meta: Meta<typeof DynamicFieldRenderer> = {
  title: 'Components/DynamicField/DynamicFieldRenderer',
  component: DynamicFieldRenderer,
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

const baseProps = {
  formValues: {},
  onChange: (value: unknown) => console.warn('Field changed:', value),
  procedureId: 123,
  authToken: 'mock-auth-token',
  folio: 'TEST-2024-001',
};

export const TextInput: Story = {
  args: {
    ...baseProps,
    field: {
      id: 1,
      name: 'project_name',
      field_type: 'input',
      description: 'Nombre del Proyecto',
      required: true,
      options: 'placeholder:Ingrese el nombre del proyecto',
    },
    value: '',
  },
};

export const TextInputWithValue: Story = {
  args: {
    ...baseProps,
    field: {
      id: 2,
      name: 'project_name',
      field_type: 'input',
      description: 'Nombre del Proyecto',
      required: true,
      options: 'placeholder:Ingrese el nombre del proyecto',
    },
    value: 'Centro Comercial Plaza Mayor',
  },
};

export const TextArea: Story = {
  args: {
    ...baseProps,
    field: {
      id: 3,
      name: 'project_description',
      field_type: 'textarea',
      description: 'Descripción del Proyecto',
      required: false,
      options:
        'placeholder:Describe brevemente el proyecto de construcción|rows:4',
    },
    value: '',
  },
};

export const SelectField: Story = {
  args: {
    ...baseProps,
    field: {
      id: 4,
      name: 'project_type',
      field_type: 'select',
      description: 'Tipo de Proyecto',
      required: true,
      options: 'Residencial|Comercial|Industrial|Institucional',
    },
    value: '',
  },
};

export const SelectWithValue: Story = {
  args: {
    ...baseProps,
    field: {
      id: 5,
      name: 'project_type',
      field_type: 'select',
      description: 'Tipo de Proyecto',
      required: true,
      options: 'Residencial|Comercial|Industrial|Institucional',
    },
    value: 'Comercial',
  },
};

export const FileField: Story = {
  args: {
    ...baseProps,
    field: {
      id: 6,
      name: 'architectural_plans',
      field_type: 'file',
      description: 'Planos Arquitectónicos',
      required: true,
      options: 'accept:.pdf,.dwg,.dxf',
    },
    value: null,
  },
};

// Simple demo showing multiple field types
export const MultipleFieldTypes: Story = {
  render: () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Tipos de Campos Dinámicos
      </h3>

      <div className="space-y-4">
        <DynamicFieldRenderer
          field={{
            id: 10,
            name: 'text_example',
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
            id: 11,
            name: 'select_example',
            field_type: 'select',
            description: 'Campo de Selección',
            required: true,
            options: 'Opción 1|Opción 2|Opción 3',
          }}
          value=""
          onChange={() => {}}
          formValues={{}}
        />

        <DynamicFieldRenderer
          field={{
            id: 12,
            name: 'textarea_example',
            field_type: 'textarea',
            description: 'Área de Texto',
            required: false,
          }}
          value=""
          onChange={() => {}}
          formValues={{}}
        />
      </div>
    </div>
  ),
};
