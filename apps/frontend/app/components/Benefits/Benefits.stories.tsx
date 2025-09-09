import type { Meta, StoryObj } from '@storybook/react';

import { Benefits } from './Benefits';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/Benefits',
  component: Benefits,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Benefits>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Mobile: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};
