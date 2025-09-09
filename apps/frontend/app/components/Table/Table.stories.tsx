import type { Meta, StoryObj } from '@storybook/react';

import { Table } from './Table';
import { useState, type ComponentProps } from 'react';

function Render(args: ComponentProps<typeof Table>) {
  const [data, setData] = useState<Record<string, string>[]>([]);

  return (
    <div className="flex flex-col gap-8">
      <button
        className="bg-blue-500 text-white p-2 rounded cursor-pointer"
        onClick={() => {
          const randomLength = Math.floor(Math.random() * 10) + 1;

          const randomData = Array.from({ length: randomLength }, () => ({
            column1: Math.random().toString(36).substring(2, 15),
            column2: Math.random().toString(36).substring(2, 15),
            column3: Math.random().toString(36).substring(2, 15),
          }));

          setData(randomData);
        }}
      >
        Randomize data
      </button>

      <Table {...args} data={data} />
    </div>
  );
}

const meta = {
  title: 'Components/Table',
  component: Table,
  args: {
    columns: [
      {
        id: 'column1',
        header: 'Column 1',
      },
      {
        id: 'column3',
        header: 'Column 3',
      },
      {
        id: 'column2',
        header: 'Column 2',
      },
    ],
    data: [],
  },
  tags: ['autodocs'],
  render: args => <Render {...args} />,
} satisfies Meta<ComponentProps<typeof Table>>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {};
