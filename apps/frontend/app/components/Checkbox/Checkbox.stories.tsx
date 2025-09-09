import type { Meta, StoryObj } from '@storybook/react';
import * as React from 'react';
import { Checkbox } from './Checkbox';

const meta: Meta<typeof Checkbox> = {
  title: 'Components/Checkbox',
  component: Checkbox,
  args: {
    label: 'Accept terms and conditions',
  },
  tags: ['autodocs'],
};

export default meta;

type Story = StoryObj<typeof Checkbox>;

export const Default: Story = {};

export const Checked: Story = {
  args: {
    checked: true,
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
  },
};

export const CheckedDisabled: Story = {
  args: {
    checked: true,
    disabled: true,
  },
};

export const WithError: Story = {
  args: {
    error: 'Custom error message',
  },
};
