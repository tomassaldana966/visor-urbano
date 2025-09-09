import type { StoryObj } from '@storybook/react';
import { BloombergLogo } from './Bloomberg';
import { CityLogo } from './City';

const meta = {
  title: 'Components/Logos',
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Bloomberg: Story = {
  render: () => <BloombergLogo />,
};

export const City: Story = {
  render: () => <CityLogo />,
};
