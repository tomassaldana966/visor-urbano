import type { Meta, StoryObj } from '@storybook/react';

import { Header } from './Header';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/Header',
  component: Header,
  args: {
    logo: <img src="https://placehold.co/84x35" alt="Logo" />,
    navItems: [
      {
        translation: 'home',
        to: '/',
      },
      {
        translation: 'about',
        to: '/about',
      },
      {
        translation: 'licenses',
        to: '/licenses',
      },
      {
        translation: 'map',
        to: '/map',
      },
      {
        translation: 'news',
        to: '/news',
      },
    ],
  },
  parameters: {
    layout: 'fullscreen',
    backgrounds: {
      default: 'dark',
    },
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Header>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Desktop: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'desktop',
    },
  },
};

export const Tablet: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'tablet',
    },
  },
};

export const Mobile: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};
