import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { RadioGroup } from './RadioGroup';

const meta = {
  title: 'Components/RadioGroup',
  component: RadioGroup,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component:
          'A radio group component built on top of Radix UI Radio Group with customizable styling. Allows users to select one option from a list of mutually exclusive options.',
      },
    },
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof RadioGroup>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    defaultValue: 'option1',
    options: [
      { value: 'option1', label: 'Option 1' },
      { value: 'option2', label: 'Option 2' },
      { value: 'option3', label: 'Option 3' },
    ],
  },
};

export const WithLabel: Story = {
  args: {
    label: 'Choose an option',
    defaultValue: 'option1',
    options: [
      { value: 'option1', label: 'Option 1' },
      { value: 'option2', label: 'Option 2' },
      { value: 'option3', label: 'Option 3' },
    ],
  },
};

export const WithDescriptions: Story = {
  args: {
    defaultValue: 'comfortable',
    options: [
      {
        value: 'compact',
        label: 'Compact',
        description: 'Saves space with a condensed layout',
      },
      {
        value: 'comfortable',
        label: 'Comfortable',
        description: 'Balanced spacing for comfortable viewing table',
      },
      {
        value: 'spacious',
        label: 'Spacious',
        description: 'Extra spacing for enhanced readability',
      },
    ],
  },
};

export const WithJSXDescriptions: Story = {
  args: {
    defaultValue: 'green',
    options: [
      {
        value: 'red',
        label: 'Red',
        description: (
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-red-500 rounded-sm" />
            <span className="text-xs text-muted-foreground">
              Red color option
            </span>
          </div>
        ),
      },
      {
        value: 'green',
        label: 'Green',
        description: (
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-sm" />
            <span className="text-xs text-muted-foreground">
              Green color option
            </span>
          </div>
        ),
      },
      {
        value: 'blue',
        label: 'Blue',
        description: (
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-blue-500 rounded-sm" />
            <span className="text-xs text-muted-foreground">
              Blue color option
            </span>
          </div>
        ),
      },
    ],
  },
};

export const Disabled: Story = {
  args: {
    defaultValue: 'option1',
    options: [
      { value: 'option1', label: 'Available Option' },
      { value: 'option2', label: 'Disabled Option', disabled: true },
      { value: 'option3', label: 'Another Disabled Option', disabled: true },
    ],
  },
};
