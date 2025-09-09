import type { Meta, StoryObj } from '@storybook/react';

import { Input } from './Input';
import type { ComponentProps } from 'react';
import { Mail } from 'lucide-react';

const meta = {
  title: 'Components/Input',
  component: Input,
  args: {
    label: 'Label',
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Input>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const WithLeftIcon: Story = {
  args: {
    pre: <Mail size={16} color="gray" />,
  },
};

export const WithRightIcon: Story = {
  args: {
    post: <Mail size={16} color="gray" />,
  },
};

export const WithError: Story = {
  args: {
    error: 'custom error message',
  },
};

export const Checkbox: Story = {
  args: {
    type: 'checkbox',
  },
};

export const ReadOnly: Story = {
  args: {
    readOnly: true,
  },
};
