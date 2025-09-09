import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { Badge } from './Badge';

const meta = {
  title: 'Components/Badge',
  component: Badge,
  args: {
    children: 'Badge',
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Badge>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
  },
};

export const Success: Story = {
  args: {
    variant: 'success',
  },
};

export const Warning: Story = {
  args: {
    variant: 'warning',
  },
};

export const Destructive: Story = {
  args: {
    variant: 'destructive',
  },
};

export const Outline: Story = {
  args: {
    variant: 'outline',
  },
};
