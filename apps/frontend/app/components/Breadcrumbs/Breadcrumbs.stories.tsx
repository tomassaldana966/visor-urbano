import type { Meta, StoryObj } from '@storybook/react';

import { Breadcrumbs } from './Breadcrumbs';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/Breadcrumbs',
  component: Breadcrumbs,
  tags: ['autodocs'],
  render: () => <Breadcrumbs />,
} satisfies Meta<ComponentProps<typeof Breadcrumbs>>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};
