import type { Meta, StoryObj } from '@storybook/react';

import { OpenLayerMap, OpenLayerMapLayersControls } from './OpenLayerMap';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/OpenLayerMap',
  component: OpenLayerMap,
  args: {},
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  render: (args: ComponentProps<typeof OpenLayerMap>) => (
    <div className="w-2xl h-screen">
      <OpenLayerMap {...args} />
    </div>
  ),
} satisfies Meta<ComponentProps<typeof OpenLayerMap>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};

export const WithLayers: Story = {
  args: {
    children: (
      <OpenLayerMapLayersControls open={true} onToggle={() => {}}>
        <div className="w-full bg-red-500">
          <p>Layer 1</p>
        </div>
        <div className="w-full bg-blue-500">
          <p>Layer 2</p>
        </div>
      </OpenLayerMapLayersControls>
    ),
  },
};
