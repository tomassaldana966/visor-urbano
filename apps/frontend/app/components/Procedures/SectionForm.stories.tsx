import type { Meta, StoryObj } from '@storybook/react';
import { SectionForm } from './SectionForm';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';
import { FileText } from 'lucide-react';

const meta: Meta<typeof SectionForm> = {
  title: 'Components/Procedures/SectionForm',
  component: SectionForm,
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

const mockFields = [
  {
    id: 'field-1',
    name: 'project_name',
    label: 'Nombre del Proyecto',
    type: 'text',
    required: true,
    placeholder: 'Ingrese el nombre del proyecto',
  },
  {
    id: 'field-2',
    name: 'project_description',
    label: 'Descripción del Proyecto',
    type: 'textarea',
    required: false,
    placeholder: 'Describe brevemente el proyecto',
  },
  {
    id: 'field-3',
    name: 'project_type',
    label: 'Tipo de Proyecto',
    type: 'select',
    required: true,
    options: 'Residencial|Comercial|Industrial',
  },
  {
    id: 'field-4',
    name: 'project_file',
    label: 'Archivo del Proyecto',
    type: 'file',
    required: false,
  },
];

const mockT = (key: string) => key;

export const Default: Story = {
  args: {
    sectionId: 'section-1',
    fields: mockFields,
    sectionTitle: 'Información General del Proyecto',
    sectionIcon: FileText,
    sectionDescription:
      'Complete la información básica del proyecto de construcción',
    folio: 'FOLIO-2024-001',
    isExpanded: true,
    onToggle: () => console.warn('Toggle section'),
    t: mockT,
    procedureId: 123,
    authToken: 'mock-auth-token',
  },
};

export const Collapsed: Story = {
  args: {
    ...Default.args,
    isExpanded: false,
  },
};

export const WithComplexFields: Story = {
  args: {
    ...Default.args,
    sectionTitle: 'Documentación Técnica',
    sectionDescription: 'Adjunte los documentos técnicos requeridos',
    fields: [
      {
        id: 'field-5',
        name: 'architectural_plans',
        label: 'Planos Arquitectónicos',
        type: 'file',
        required: true,
        accept: '.pdf,.dwg,.dxf',
      },
      {
        id: 'field-6',
        name: 'structural_plans',
        label: 'Planos Estructurales',
        type: 'file',
        required: true,
        accept: '.pdf,.dwg,.dxf',
      },
      {
        id: 'field-7',
        name: 'construction_area',
        label: 'Área de Construcción (m²)',
        type: 'number',
        required: true,
        min: 1,
        placeholder: 'Ingrese el área en metros cuadrados',
      },
      {
        id: 'field-8',
        name: 'has_parking',
        label: '¿Incluye estacionamiento?',
        type: 'checkbox',
        required: false,
      },
    ],
  },
};

export const LongForm: Story = {
  args: {
    ...Default.args,
    sectionTitle: 'Información Detallada del Solicitante',
    fields: [
      {
        id: 'applicant-1',
        name: 'full_name',
        label: 'Nombre Completo',
        type: 'text',
        required: true,
      },
      {
        id: 'applicant-2',
        name: 'identification',
        label: 'Número de Identificación',
        type: 'text',
        required: true,
      },
      {
        id: 'applicant-3',
        name: 'email',
        label: 'Correo Electrónico',
        type: 'email',
        required: true,
      },
      {
        id: 'applicant-4',
        name: 'phone',
        label: 'Teléfono',
        type: 'tel',
        required: true,
      },
      {
        id: 'applicant-5',
        name: 'address',
        label: 'Dirección',
        type: 'textarea',
        required: true,
      },
      {
        id: 'applicant-6',
        name: 'profession',
        label: 'Profesión',
        type: 'select',
        required: false,
        options: 'Arquitecto|Ingeniero Civil|Ingeniero Industrial|Otro',
      },
    ],
  },
};
