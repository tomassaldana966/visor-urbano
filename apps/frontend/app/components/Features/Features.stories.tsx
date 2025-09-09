import type { Meta, StoryObj } from '@storybook/react';

import { Features } from './Features';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/Features',
  component: Features,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Features>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

export const Mobile: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};
