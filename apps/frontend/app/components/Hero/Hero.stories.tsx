import type { Meta, StoryObj } from '@storybook/react';

import { Hero } from './Hero';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/Hero',
  component: Hero,
  args: {},
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Hero>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

export const WithIcons: Story = {
  args: {
    icons: [
      <img key="1" alt="City" src="https://placehold.co/84x35" />,
      <a href="//google.com" key="2">
        <img key="1" alt="Google" src="https://placehold.co/100x50" />
      </a>,
    ],
  },
};
