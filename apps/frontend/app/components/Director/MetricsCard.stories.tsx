import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';
import { FileText, Users, Clock, CheckCircle } from 'lucide-react';

import { MetricsCard } from './MetricsCard';

const meta = {
  title: 'Components/Director/MetricsCard',
  component: MetricsCard,
  args: {
    title: 'Total Procedures',
    value: 1245,
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof MetricsCard>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const WithUpTrend: Story = {
  args: {
    title: 'Completed This Month',
    value: 342,
    trend: 'up',
    trendValue: '+12%',
    color: 'success',
    icon: <CheckCircle className="w-5 h-5" />,
  },
};

export const WithDownTrend: Story = {
  args: {
    title: 'Pending Reviews',
    value: 56,
    trend: 'down',
    trendValue: '-8%',
    color: 'warning',
    icon: <Clock className="w-5 h-5" />,
  },
};

export const StableTrend: Story = {
  args: {
    title: 'Active Users',
    value: 189,
    trend: 'stable',
    trendValue: '0%',
    color: 'primary',
    icon: <Users className="w-5 h-5" />,
  },
};

export const DangerCard: Story = {
  args: {
    title: 'Overdue Items',
    value: 23,
    trend: 'up',
    trendValue: '+5',
    color: 'danger',
    icon: <FileText className="w-5 h-5" />,
  },
};

export const WithStringValue: Story = {
  args: {
    title: 'Average Processing Time',
    value: '5.2 days',
    trend: 'down',
    trendValue: '-0.8 days',
    color: 'success',
  },
};

export const Clickable: Story = {
  args: {
    title: 'Click Me',
    value: 999,
    onClick: () => alert('Card clicked!'),
    icon: <FileText className="w-5 h-5" />,
  },
};
