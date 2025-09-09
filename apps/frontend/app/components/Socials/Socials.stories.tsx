import type { Meta, StoryObj } from '@storybook/react';

import { Socials } from './Socials';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/Socials',
  component: Socials,
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Socials>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};
