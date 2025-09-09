import type { Meta, StoryObj } from '@storybook/react';

import { Icon, icons } from './Icon';
import type { ComponentProps, CSSProperties } from 'react';

const iconEnum = Object.getOwnPropertyNames(icons);

const meta = {
  title: 'Components/Icon',
  component: Icon,
  args: {
    name: 'store',
  },
  parameters: {
    layout: 'centered',
  },
  argTypes: {
    name: {
      control: {
        type: 'select',
        options: iconEnum,
      },
    },
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Icon>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const WithTheme: Story = {
  parameters: {
    docs: {
      description: {
        story:
          'When you change the page theme, the icons will change colors accordingly.',
      },
    },
  },
  render: args => (
    <div
      style={
        {
          '--color-primary': '#6c5ce7',
          '--color-support-5': '#a29bfe',
        } as CSSProperties
      }
      key={args.name}
    >
      <Icon {...args} />
    </div>
  ),
};
