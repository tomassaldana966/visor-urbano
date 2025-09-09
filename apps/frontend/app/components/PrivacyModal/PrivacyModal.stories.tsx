import type { Meta, StoryObj } from '@storybook/react';

import { PrivacyModal } from './PrivacyModal';
import type { ComponentProps } from 'react';
import { Button } from '../Button/Button';

const meta = {
  title: 'Components/PrivacyModal',
  component: PrivacyModal,
  args: {
    children: <Button>Open Privacy</Button>,
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof PrivacyModal>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
