import { Popover, PopoverContent, PopoverTrigger } from './Popover';
import type { Meta, StoryObj } from '@storybook/react';

import type { ComponentProps } from 'react';
import { Button } from '../Button/Button';

const meta = {
  title: 'Components/Popover',
  component: Popover,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'This uses Radix primitives, please refer to the [Radix documentation](https://www.radix-ui.com/primitives/docs/components/popover) for more information.',
      },
    },
  },
  tags: ['autodocs'],
  render: () => (
    <div className="flex justify-center p-20">
      <Popover>
        <PopoverTrigger asChild>
          <Button>Click to open</Button>
        </PopoverTrigger>
        <PopoverContent>Content</PopoverContent>
      </Popover>
    </div>
  ),
} satisfies Meta<ComponentProps<typeof Popover>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'desktop',
    },
  },
};
