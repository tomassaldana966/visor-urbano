import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { Label } from './Label';

const meta = {
  title: 'Components/Label',
  component: Label,
  args: {
    children: 'Label text',
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Label>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const WithCustomClassName: Story = {
  args: {
    className: 'text-blue-600 font-bold',
    children: 'Custom styled label',
  },
};

export const LongLabel: Story = {
  args: {
    children:
      'This is a longer label text to demonstrate how it looks with more content',
  },
};
