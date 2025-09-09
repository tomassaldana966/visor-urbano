import type { Meta, StoryObj } from '@storybook/react';

import { Button } from './Button';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/Button',
  component: Button,
  args: {
    children: 'Button',
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Button>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
  },
};

export const Tertiary: Story = {
  args: {
    variant: 'tertiary',
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
  },
};

export const Destructive: Story = {
  args: {
    variant: 'destructive',
  },
};
