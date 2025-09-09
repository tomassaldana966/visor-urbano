import type { Meta, StoryObj } from '@storybook/react';
import { Slider } from './Slider';

type SliderArgs = React.ComponentProps<typeof Slider>;

const meta: Meta<typeof Slider> = {
  title: 'Components/Slider',
  component: Slider,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    min: {
      control: { type: 'number' },
      description: 'Minimum value',
    },
    max: {
      control: { type: 'number' },
      description: 'Maximum value',
    },
    step: {
      control: { type: 'number' },
      description: 'Step increment',
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Whether the slider is disabled',
    },
    orientation: {
      control: { type: 'select' },
      options: ['horizontal', 'vertical'],
      description: 'Orientation of the slider',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    defaultValue: [50],
    min: 0,
    max: 100,
  },
  render: (args: SliderArgs) => (
    <div className="w-80">
      <Slider {...args} />
    </div>
  ),
};

export const Range: Story = {
  args: {
    defaultValue: [25, 75],
    min: 0,
    max: 100,
  },
  render: (args: SliderArgs) => (
    <div className="w-80">
      <Slider {...args} />
    </div>
  ),
};

export const WithStep: Story = {
  args: {
    defaultValue: [20],
    min: 0,
    max: 100,
    step: 10,
  },
  render: (args: SliderArgs) => (
    <div className="w-80">
      <Slider {...args} />
    </div>
  ),
};

export const SmallRange: Story = {
  args: {
    defaultValue: [2],
    min: 0,
    max: 10,
    step: 1,
  },
  render: (args: SliderArgs) => (
    <div className="w-80">
      <Slider {...args} />
    </div>
  ),
};

export const Disabled: Story = {
  args: {
    defaultValue: [40],
    min: 0,
    max: 100,
    disabled: true,
  },
  render: (args: SliderArgs) => (
    <div className="w-80">
      <Slider {...args} />
    </div>
  ),
};

export const Vertical: Story = {
  args: {
    defaultValue: [50],
    min: 0,
    max: 100,
    orientation: 'vertical' as const,
  },
  render: (args: SliderArgs) => (
    <div className="h-64">
      <Slider {...args} />
    </div>
  ),
};

export const VerticalRange: Story = {
  args: {
    defaultValue: [25, 75],
    min: 0,
    max: 100,
    orientation: 'vertical' as const,
  },
  render: (args: SliderArgs) => (
    <div className="h-64">
      <Slider {...args} />
    </div>
  ),
};

export const CustomStyling: Story = {
  args: {
    defaultValue: [60],
    min: 0,
    max: 100,
    className: 'accent-red-500',
  },
  render: (args: SliderArgs) => (
    <div className="w-80">
      <Slider {...args} />
    </div>
  ),
};

export const MultipleThumbsRange: Story = {
  args: {
    defaultValue: [10, 30, 60, 90],
    min: 0,
    max: 100,
  },
  render: (args: SliderArgs) => (
    <div className="w-80">
      <Slider {...args} />
    </div>
  ),
};

export const WithLabel: Story = {
  args: {
    defaultValue: [50],
    min: 0,
    max: 100,
    label: 'Volume Level',
  },
  render: (args: SliderArgs) => (
    <div className="w-80">
      <Slider {...args} />
    </div>
  ),
};

export const WithError: Story = {
  args: {
    defaultValue: [15],
    min: 0,
    max: 100,
    label: 'Temperature',
    error: 'Temperature too low',
  },
  render: (args: SliderArgs) => (
    <div className="w-80">
      <Slider {...args} />
    </div>
  ),
};

export const RangeWithLabel: Story = {
  args: {
    defaultValue: [20, 80],
    min: 0,
    max: 100,
    label: 'Price Range',
  },
  render: (args: SliderArgs) => (
    <div className="w-80">
      <Slider {...args} />
    </div>
  ),
};

export const VerticalWithLabel: Story = {
  args: {
    defaultValue: [60],
    min: 0,
    max: 100,
    orientation: 'vertical' as const,
    label: 'Height',
  },
  render: (args: SliderArgs) => (
    <div className="h-64">
      <Slider {...args} />
    </div>
  ),
};
