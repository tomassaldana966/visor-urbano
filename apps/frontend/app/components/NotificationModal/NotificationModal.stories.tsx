import type { Meta, StoryObj } from '@storybook/react';
import type { ComponentProps } from 'react';

import { NotificationModal, type NotificationData } from './NotificationModal';

const mockNotification: NotificationData = {
  id: 1,
  folio: 'PROC-2023-001',
  notification_type: 1,
  notifying_department: 1,
  comment:
    'Your procedure has been updated with new requirements. Please review the changes and submit additional documentation if needed.',
  creation_date: '2023-06-15T10:30:00Z',
  notified: 0,
  user_id: 123,
  applicant_email: 'user@example.com',
};

const mockReadNotification: NotificationData = {
  ...mockNotification,
  id: 2,
  notification_type: 2,
  notified: 1,
  comment: 'Your procedure has been approved and is ready for the next stage.',
};

const mockWarningNotification: NotificationData = {
  ...mockNotification,
  id: 3,
  notification_type: 4,
  comment:
    'Action required: Missing documentation detected. Please upload the required files within 5 business days.',
};

const meta = {
  title: 'Components/NotificationModal',
  component: NotificationModal,
  args: {
    notification: mockNotification,
    isOpen: true,
    onClose: () => {},
    onMarkAsRead: () => {},
  },
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof NotificationModal>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const ReadNotification: Story = {
  args: {
    notification: mockReadNotification,
  },
};

export const WarningNotification: Story = {
  args: {
    notification: mockWarningNotification,
  },
};

export const Closed: Story = {
  args: {
    isOpen: false,
  },
};

export const NoNotification: Story = {
  args: {
    notification: null,
  },
};
