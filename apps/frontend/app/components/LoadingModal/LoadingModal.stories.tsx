import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { LoadingModal } from './LoadingModal';

const meta: Meta<typeof LoadingModal> = {
  title: 'Components/LoadingModal',
  component: LoadingModal,
  parameters: {
    layout: 'fullscreen',
  },
  tags: ['autodocs'],
  argTypes: {
    isOpen: {
      control: 'boolean',
    },
    message: {
      control: 'text',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    isOpen: true,
    message: 'Guardando información...',
  },
};

export const CustomMessage: Story = {
  args: {
    isOpen: true,
    message: 'Procesando su solicitud, esto puede tomar unos momentos...',
  },
};

export const ShortMessage: Story = {
  args: {
    isOpen: true,
    message: 'Enviando...',
  },
};

export const LongMessage: Story = {
  args: {
    isOpen: true,
    message:
      'Estamos procesando su documentación y validando toda la información proporcionada. Este proceso puede tomar varios minutos dependiendo del tamaño de los archivos.',
  },
};

export const Closed: Story = {
  args: {
    isOpen: false,
    message: 'Esta modal está cerrada',
  },
};

// Interactive story to demonstrate opening/closing
export const Interactive: Story = {
  render: () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
      <div className="p-8">
        <button
          onClick={() => setIsOpen(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Abrir Modal de Carga
        </button>

        <LoadingModal
          isOpen={isOpen}
          message="Guardando los cambios realizados..."
        />

        {isOpen && (
          <button
            onClick={() => setIsOpen(false)}
            className="fixed top-4 right-4 z-[60] px-3 py-1 bg-red-600 text-white text-sm rounded"
          >
            Cerrar (Para Demo)
          </button>
        )}
      </div>
    );
  },
};
