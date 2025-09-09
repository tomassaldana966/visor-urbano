import type { Meta, StoryObj } from '@storybook/react';

import { Footer } from './Footer';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/Footer',
  component: Footer,
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Footer>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
