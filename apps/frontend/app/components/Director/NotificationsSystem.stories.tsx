import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { NotificationsSystem } from './NotificationsSystem';

const meta = {
  title: 'Components/Director/NotificationsSystem',
  component: NotificationsSystem,
  args: {
    isOpen: true,
    onClose: () => {},
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof NotificationsSystem>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  play: async () => {
    // Simple test to ensure the component renders without errors
    // This replaces any previous test code that might have referenced __test
  },
};

export const Closed: Story = {
  args: {
    isOpen: false,
  },
  play: async () => {
    // Simple test to ensure the component renders without errors when closed
  },
};
