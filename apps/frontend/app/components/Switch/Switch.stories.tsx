import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { Switch } from './Switch';

const meta: Meta<typeof Switch> = {
  title: 'Components/Switch',
  component: Switch,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    checked: {
      control: 'boolean',
      description: 'Whether the switch is checked',
    },
    onCheckedChange: {
      action: 'onCheckedChange',
      description: 'Callback fired when the switch is toggled',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the switch is disabled',
    },
    className: {
      control: 'text',
      description: 'Additional CSS classes',
    },
    'aria-label': {
      control: 'text',
      description: 'Accessible label for the switch',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

// Wrapper component for controlled stories
const SwitchWrapper = (args: any) => {
  const [checked, setChecked] = useState(args.checked || false);

  return (
    <Switch
      {...args}
      checked={checked}
      onCheckedChange={value => {
        setChecked(value);
        args.onCheckedChange?.(value);
      }}
    />
  );
};

export const Default: Story = {
  render: SwitchWrapper,
  args: {
    checked: false,
    'aria-label': 'Default switch',
  },
};

export const Checked: Story = {
  render: SwitchWrapper,
  args: {
    checked: true,
    'aria-label': 'Checked switch',
  },
};

export const Disabled: Story = {
  render: SwitchWrapper,
  args: {
    checked: false,
    disabled: true,
    'aria-label': 'Disabled switch',
  },
};

export const DisabledChecked: Story = {
  render: SwitchWrapper,
  args: {
    checked: true,
    disabled: true,
    'aria-label': 'Disabled checked switch',
  },
};

export const WithCustomClass: Story = {
  render: SwitchWrapper,
  args: {
    checked: false,
    className: 'border-2 border-red-500',
    'aria-label': 'Switch with custom styling',
  },
};

export const Interactive: Story = {
  render: () => {
    const [checked, setChecked] = useState(false);

    return (
      <div className="space-y-4">
        <div className="flex items-center space-x-3">
          <Switch
            checked={checked}
            onCheckedChange={setChecked}
            aria-label="Interactive switch"
          />
          <span className="text-sm">Switch is {checked ? 'ON' : 'OFF'}</span>
        </div>
        <div className="text-xs text-gray-500">
          Click the switch to toggle its state
        </div>
      </div>
    );
  },
};

export const Multiple: Story = {
  render: () => {
    const [switch1, setSwitch1] = useState(false);
    const [switch2, setSwitch2] = useState(true);
    const [switch3, setSwitch3] = useState(false);

    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between w-64">
          <span className="text-sm">Enable notifications</span>
          <Switch
            checked={switch1}
            onCheckedChange={setSwitch1}
            aria-label="Enable notifications"
          />
        </div>
        <div className="flex items-center justify-between w-64">
          <span className="text-sm">Auto-save</span>
          <Switch
            checked={switch2}
            onCheckedChange={setSwitch2}
            aria-label="Enable auto-save"
          />
        </div>
        <div className="flex items-center justify-between w-64">
          <span className="text-sm">Dark mode</span>
          <Switch
            checked={switch3}
            onCheckedChange={setSwitch3}
            aria-label="Enable dark mode"
          />
        </div>
      </div>
    );
  },
};
