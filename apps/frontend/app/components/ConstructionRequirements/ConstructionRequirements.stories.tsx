import type { Meta, StoryObj } from '@storybook/react';
import { ConstructionRequirementsDisplay } from './ConstructionRequirements';

const meta: Meta<typeof ConstructionRequirementsDisplay> = {
  title: 'Components/ConstructionRequirements',
  component: ConstructionRequirementsDisplay,
  parameters: {
    layout: 'padded',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

const mockRequirements = [
  {
    title: 'Solicitud de Licencia de Construcción',
    description:
      'Formulario oficial debidamente llenado y firmado por el propietario o su representante legal.',
    department_issued: true,
  },
  {
    title: 'Planos Arquitectónicos',
    description:
      'Planos completos del proyecto arquitectónico, incluyendo plantas, cortes, fachadas y detalles constructivos.',
    department_issued: false,
  },
  {
    title: 'Planos Estructurales',
    description:
      'Planos estructurales firmados por ingeniero civil colegiado, incluyendo cálculos estructurales.',
    department_issued: false,
  },
  {
    title: 'Estudio de Suelos',
    description:
      'Estudio geotécnico del terreno realizado por laboratorio certificado.',
    department_issued: false,
  },
  {
    title: 'Certificado de Libertad y Tradición',
    description:
      'Documento que acredita la propiedad del inmueble, con vigencia no mayor a 30 días.',
    department_issued: false,
  },
  {
    title: 'Licencia de Urbanismo',
    description:
      'Licencia vigente que autorice el uso del suelo para el tipo de construcción propuesta.',
    department_issued: true,
  },
  {
    title: 'Pago de Derechos',
    description:
      'Recibo de pago de los derechos correspondientes según la tarifa municipal vigente.',
    department_issued: true,
  },
];

export const Default: Story = {
  args: {
    requirements: mockRequirements,
    folio: 'CONST-2024-001',
    municipalityName: 'Medellín',
    address: 'Carrera 45 # 67-89, Barrio Laureles',
    interestedParty: 'Juan Carlos Pérez Gómez',
  },
};

export const ShortList: Story = {
  args: {
    requirements: [
      {
        title: 'Solicitud de Licencia',
        description: 'Formulario oficial llenado y firmado.',
        department_issued: true,
      },
      {
        title: 'Planos Arquitectónicos',
        description: 'Planos completos del proyecto.',
        department_issued: false,
      },
      {
        title: 'Certificado de Propiedad',
        description: 'Documento que acredite la propiedad.',
        department_issued: false,
      },
    ],
    folio: 'CONST-2024-002',
    municipalityName: 'Bogotá',
    address: 'Calle 72 # 11-86, Chapinero',
    interestedParty: 'María Elena Rodríguez',
  },
};

export const MixedRequirements: Story = {
  args: {
    requirements: [
      {
        title: 'Formulario de Solicitud',
        description: 'Formulario único nacional debidamente diligenciado.',
        department_issued: true,
      },
      {
        title: 'Planos Técnicos',
        description: 'Conjunto completo de planos técnicos y arquitectónicos.',
        department_issued: false,
      },
      {
        title: 'Estudio de Impacto Ambiental',
        description:
          'Evaluación del impacto ambiental del proyecto de construcción.',
        department_issued: false,
      },
      {
        title: 'Visto Bueno de Bomberos',
        description:
          'Aprobación del cuerpo de bomberos para medidas de seguridad.',
        department_issued: true,
      },
    ],
    folio: 'CONST-2024-003',
    municipalityName: 'Cali',
    address: 'Avenida 6N # 23-45, Granada',
    interestedParty: 'Constructora XYZ S.A.S.',
  },
};

export const LongAddress: Story = {
  args: {
    requirements: mockRequirements.slice(0, 4),
    folio: 'CONST-2024-004',
    municipalityName: 'Barranquilla',
    address:
      'Carrera 50B # 84-157, Apartamento 502, Torre 3, Conjunto Residencial Los Almendros, Barrio Alto Prado',
    interestedParty: 'Ana Patricia Fernández de García',
  },
};

export const EmptyRequirements: Story = {
  args: {
    requirements: [],
    folio: 'CONST-2024-005',
    municipalityName: 'Cartagena',
    address: 'Calle de la Muralla # 123',
    interestedParty: 'Sin Interesado',
  },
};
