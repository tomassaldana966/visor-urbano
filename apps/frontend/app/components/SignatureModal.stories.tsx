import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { I18nextProvider } from 'react-i18next';
import i18n from '../i18n';
import SignatureModal from './SignatureModal';

const meta: Meta<typeof SignatureModal> = {
  title: 'Components/SignatureModal',
  component: SignatureModal,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  decorators: [
    Story => (
      <I18nextProvider i18n={i18n}>
        <Story />
      </I18nextProvider>
    ),
  ],
  argTypes: {
    isOpen: {
      control: 'boolean',
    },
    isLoading: {
      control: 'boolean',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

const mockSignature = {
  id: 1,
  signer_name: 'Carlos Alberto Pérez',
  position_title: 'Director de Planeación Municipal',
  order_index: 1,
  signature_image:
    'https://via.placeholder.com/300x150/4f46e5/ffffff?text=Firma+Digital',
  municipality_id: 1,
  created_at: '2024-01-15T10:00:00Z',
  updated_at: '2024-01-15T10:00:00Z',
};

export const Default: Story = {
  args: {
    isOpen: true,
    onClose: () => {},
    signature: null,
    onSave: async (data: any, file?: File) => {
      // Simulate saving
      await new Promise(resolve => setTimeout(resolve, 1000));
    },
    isLoading: false,
  },
};

export const EditExistingSignature: Story = {
  args: {
    isOpen: true,
    onClose: () => {},
    signature: mockSignature,
    onSave: async (data: any, file?: File) => {
      // Simulate updating
      await new Promise(resolve => setTimeout(resolve, 1000));
    },
    isLoading: false,
  },
};

export const LoadingState: Story = {
  args: {
    isOpen: true,
    onClose: () => {},
    signature: mockSignature,
    onSave: async (data: any, file?: File) => {
      // Simulate saving
    },
    isLoading: true,
  },
};

export const NewSignature: Story = {
  args: {
    isOpen: true,
    onClose: () => {},
    signature: null,
    onSave: async (data: any, file?: File) => {
      // Simulate creating
      await new Promise(resolve => setTimeout(resolve, 1500));
    },
    isLoading: false,
  },
};

export const Closed: Story = {
  args: {
    isOpen: false,
    onClose: () => {},
    signature: null,
    onSave: async (data: any, file?: File) => {
      // Simulate saving
    },
    isLoading: false,
  },
};

// Interactive story
export const Interactive: Story = {
  render: () => {
    const [isOpen, setIsOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [currentSignature, setCurrentSignature] = useState<any>(null);

    const handleSave = async (data: any, file?: File) => {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));

      setIsLoading(false);
      setIsOpen(false);

      // Update signature after save
      setCurrentSignature({
        ...mockSignature,
        ...data,
      });
    };

    return (
      <div className="p-8">
        <div className="space-x-4">
          <button
            onClick={() => {
              setCurrentSignature(null);
              setIsOpen(true);
            }}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Nueva Firma
          </button>

          <button
            onClick={() => {
              setCurrentSignature(mockSignature);
              setIsOpen(true);
            }}
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Editar Firma Existente
          </button>
        </div>

        {currentSignature && (
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium text-gray-900 mb-2">Firma Actual:</h3>
            <p>
              <strong>Nombre:</strong> {currentSignature.signer_name}
            </p>
            <p>
              <strong>Cargo:</strong> {currentSignature.position_title}
            </p>
            <p>
              <strong>Orden:</strong> {currentSignature.order_index}
            </p>
          </div>
        )}

        <SignatureModal
          isOpen={isOpen}
          onClose={() => setIsOpen(false)}
          signature={currentSignature}
          onSave={handleSave}
          isLoading={isLoading}
        />
      </div>
    );
  },
};
