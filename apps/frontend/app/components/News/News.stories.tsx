import type { Meta, StoryObj } from '@storybook/react';

import { News } from './News';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/News',
  component: News,
  args: {
    items: [
      {
        id: '1',
        date: '2021-09-01',
        img: 'https://placehold.co/150',
        link: '/news/1',
        summary: 'Summary of the news article',
        title: 'News Article Title',
      },
      {
        id: '2',
        date: '2021-09-02',
        img: 'https://placehold.co/150x300',
        link: '/news/2',
        summary: 'Summary of the news article',
        title: 'News Article Title',
      },
      {
        id: '3',
        date: '2021-09-03',
        img: 'https://placehold.co/300x150',
        link: '/news/3',
        summary: 'Summary of the news article',
        title: 'News Article Title',
      },
      {
        id: '4',
        date: '2021-09-04',
        img: 'https://placehold.co/100x120',
        link: '/news/4',
        summary: 'Summary of the news article',
        title: 'News Article Title',
      },
      {
        id: '5',
        date: '2021-09-05',
        img: 'https://placehold.co/100',
        link: '/news/5',
        summary: 'Summary of the news article',
        title: 'News Article',
      },
    ],
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof News>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const Mobile: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
  },
};
