import type { Meta, StoryObj } from '@storybook/react';

import { TransWithComponents } from './TransWithComponents';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/TransWithComponents',
  component: TransWithComponents,
  args: {
    children: 'privacy:description',
  },
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        story:
          'This component is a wrapper around the `Trans` component from `react-i18next` that provides default components for the `Trans` component to render large rich text like privacy.',
      },
    },
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof TransWithComponents>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
