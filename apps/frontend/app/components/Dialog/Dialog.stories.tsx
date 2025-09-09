import type { Meta, StoryObj } from '@storybook/react';

import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './Dialog';
import type { ComponentProps } from 'react';
import { Button } from '../Button/Button';

const meta = {
  title: 'Components/Dialog',
  component: Dialog,
  args: {},
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof Dialog>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Open Dialog</Button>
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Dialog Title</DialogTitle>
          <DialogDescription>Dialog Description</DialogDescription>
        </DialogHeader>

        <DialogFooter>
          <DialogClose asChild>
            <Button>Close</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  ),
};

export const LongContent: Story = {
  render: () => (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Open Dialog</Button>
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Dialog Title</DialogTitle>
          <DialogDescription>
            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>

            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos,
              dolores sed quisquam dicta corrupti eveniet sint officiis? In
              magnam tempore hic soluta, beatae, ducimus accusamus iusto
              necessitatibus corporis nam odit!
            </p>
          </DialogDescription>
        </DialogHeader>

        <DialogFooter>
          <DialogClose asChild>
            <Button>Close</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  ),
};
