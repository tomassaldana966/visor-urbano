import type { Meta, StoryObj } from '@storybook/react';

import { Tutorial } from './Tutorial';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/Tutorial',
  component: Tutorial,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Tutorial>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};
