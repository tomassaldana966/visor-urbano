import type { Meta, StoryObj } from '@storybook/react';
import { IssueLicenseModal } from './IssueLicenseModal';

const meta: Meta<typeof IssueLicenseModal> = {
  title: 'Components/IssueLicenseModal',
  component: IssueLicenseModal,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component:
          'Modal component for issuing procedure licenses. Allows users to either generate a license automatically or upload a scanned license with additional business details.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    isOpen: {
      control: 'boolean',
      description: 'Controls whether the modal is open or closed',
    },
    onClose: {
      action: 'closed',
      description: 'Callback function when modal is closed',
    },
    folio: {
      control: 'text',
      description: 'Procedure folio number',
    },
    authToken: {
      control: 'text',
      description: 'Authentication token for API calls',
    },
    onLicenseIssued: {
      action: 'license-issued',
      description: 'Callback function when license is successfully issued',
    },
  },
  decorators: [
    Story => (
      <div style={{ height: '100vh', width: '100vw' }}>
        <Story />
      </div>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    isOpen: true,
    folio: 'TEST-2024-001',
    authToken: 'mock-auth-token',
    onClose: () => {},
    onLicenseIssued: () => {},
  },
};

export const Closed: Story = {
  args: {
    isOpen: false,
    folio: 'TEST-2024-001',
    authToken: 'mock-auth-token',
    onClose: () => {},
    onLicenseIssued: () => {},
  },
};

export const WithoutAuthToken: Story = {
  args: {
    isOpen: true,
    folio: 'TEST-2024-001',
    authToken: undefined,
    onClose: () => {},
    onLicenseIssued: () => {},
  },
};

export const LongFolio: Story = {
  args: {
    isOpen: true,
    folio: 'VERY-LONG-FOLIO-NUMBER-TEST-2024-001-EXTENDED',
    authToken: 'mock-auth-token',
    onClose: () => {},
    onLicenseIssued: () => {},
  },
};
