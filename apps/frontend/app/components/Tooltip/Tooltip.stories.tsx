import { Tooltip, TooltipContent, TooltipTrigger } from './Tooltip';
import type { Meta, StoryObj } from '@storybook/react';

import type { ComponentProps } from 'react';
import { Button } from '../Button/Button';

const meta = {
  title: 'Components/Tooltip',
  component: Tooltip,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'This uses Radix primitives, please refer to the [Radix documentation](https://www.radix-ui.com/primitives/docs/components/tooltip) for more information.',
      },
    },
  },
  tags: ['autodocs'],
  render: () => (
    <div className="flex justify-center p-20">
      <Tooltip>
        <TooltipTrigger asChild>
          <Button>Hover</Button>
        </TooltipTrigger>

        <TooltipContent>Content</TooltipContent>
      </Tooltip>
    </div>
  ),
} satisfies Meta<ComponentProps<typeof Tooltip>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'desktop',
    },
  },
};
