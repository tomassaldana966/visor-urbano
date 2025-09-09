import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { I18nextProvider } from 'react-i18next';
import i18n from '../../i18n';
import { Modal } from './Modal';
import { Button } from '../Button/Button';

const meta: Meta<typeof Modal> = {
  title: 'Components/Modal',
  component: Modal,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg', 'xl', '2xl'],
    },
    showCloseButton: {
      control: 'boolean',
    },
    preventCloseOnOverlayClick: {
      control: 'boolean',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

// Helper component to handle modal state in stories
function ModalDemo({ children, ...props }: any) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setIsOpen(true)}>Abrir Modal</Button>
      <Modal {...props} isOpen={isOpen} onClose={() => setIsOpen(false)}>
        {children}
      </Modal>
    </>
  );
}

export const Default: Story = {
  render: args => (
    <ModalDemo {...args}>
      <div className="space-y-4">
        <p className="text-gray-600">
          Este es el contenido del modal. Puedes poner cualquier contenido aquí.
        </p>
        <div className="flex justify-end space-x-3">
          <Button variant="secondary">Cancelar</Button>
          <Button>Confirmar</Button>
        </div>
      </div>
    </ModalDemo>
  ),
  args: {
    title: 'Modal de Ejemplo',
    size: 'md',
    showCloseButton: true,
    preventCloseOnOverlayClick: false,
  },
};

export const WithForm: Story = {
  render: args => (
    <ModalDemo {...args}>
      <form className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Nombre
          </label>
          <input
            type="text"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Ingresa tu nombre"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            type="email"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="tu@email.com"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Mensaje
          </label>
          <textarea
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Escribe tu mensaje aquí..."
          />
        </div>
        <div className="flex justify-end space-x-3 pt-4">
          <Button type="button" variant="secondary">
            Cancelar
          </Button>
          <Button type="submit">Enviar</Button>
        </div>
      </form>
    </ModalDemo>
  ),
  args: {
    title: 'Formulario de Contacto',
    size: 'lg',
    showCloseButton: true,
    preventCloseOnOverlayClick: false,
  },
};

export const SmallSize: Story = {
  render: args => (
    <ModalDemo {...args}>
      <div className="text-center space-y-4">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
          <svg
            className="h-6 w-6 text-red-600"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth="1.5"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
            />
          </svg>
        </div>
        <div>
          <h3 className="text-lg font-medium text-gray-900">
            ¿Eliminar elemento?
          </h3>
          <p className="mt-2 text-sm text-gray-500">
            Esta acción no se puede deshacer. El elemento será eliminado
            permanentemente.
          </p>
        </div>
        <div className="flex justify-center space-x-3">
          <Button variant="secondary">Cancelar</Button>
          <Button variant="destructive">Eliminar</Button>
        </div>
      </div>
    </ModalDemo>
  ),
  args: {
    title: '',
    size: 'sm',
    showCloseButton: true,
    preventCloseOnOverlayClick: true,
  },
};

export const LargeSize: Story = {
  render: args => (
    <ModalDemo {...args}>
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nombre
            </label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Apellido
            </label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              type="email"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Teléfono
            </label>
            <input
              type="tel"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Dirección
          </label>
          <input
            type="text"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Comentarios
          </label>
          <textarea
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div className="flex justify-end space-x-3">
          <Button variant="secondary">Cancelar</Button>
          <Button>Guardar</Button>
        </div>
      </div>
    </ModalDemo>
  ),
  args: {
    title: 'Información Detallada',
    size: 'xl',
    showCloseButton: true,
    preventCloseOnOverlayClick: false,
  },
};

export const WithoutCloseButton: Story = {
  render: args => (
    <ModalDemo {...args}>
      <div className="text-center space-y-4">
        <p className="text-gray-600">
          Este modal no tiene botón de cerrar. Solo se puede cerrar con las
          acciones de abajo.
        </p>
        <div className="flex justify-center space-x-3">
          <Button variant="secondary">Cancelar</Button>
          <Button>Aceptar</Button>
        </div>
      </div>
    </ModalDemo>
  ),
  args: {
    title: 'Modal sin botón cerrar',
    size: 'md',
    showCloseButton: false,
    preventCloseOnOverlayClick: true,
  },
};
