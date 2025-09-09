import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { QuickActionsPanel } from './QuickActionsPanel';

const meta = {
  title: 'Components/Director/QuickActionsPanel',
  component: QuickActionsPanel,
  args: {
    onNavigateToUsers: () => {},
    onNavigateToAnalytics: () => {},
    onNavigateToSettings: () => {},
    onNavigateToMunicipalLayers: () => {},
    onNavigateToImpactMap: () => {},
    onNavigateToRoles: () => {},
    onNavigateToRequirements: () => {},
    onNavigateToBusinessTypes: () => {},
    onNavigateToDependencies: () => {},
    onNavigateToBlog: () => {},
    onExportReports: () => {},
    onViewNotifications: () => {},
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof QuickActionsPanel>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const StandardUsage: Story = {
  args: {},
};
