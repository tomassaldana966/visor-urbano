import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import {
  Select,
  Option,
  SelectGroup,
  SelectSeparator,
  SelectGroupLabel,
} from './Select';

const meta: Meta<typeof Select> = {
  title: 'Components/Select',
  component: Select,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component:
          'A flexible select component built on top of Radix UI Select with customizable styling and sizes.',
      },
    },
  },
  args: {
    onValueChange: fn(),
    placeholder: 'Select an framework',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Select>;

export const Default: Story = {
  render: args => (
    <Select {...args}>
      <Option value="react">React</Option>
      <Option value="vue">Vue</Option>
      <Option value="angular">Angular</Option>
      <Option value="svelte">Svelte</Option>
    </Select>
  ),
};

export const WithLabel: Story = {
  args: {
    label: 'Select a framework',
  },
  render: args => (
    <Select {...args}>
      <Option value="react">React</Option>
      <Option value="vue">Vue</Option>
      <Option value="angular">Angular</Option>
      <Option value="svelte">Svelte</Option>
    </Select>
  ),
};

export const WithDefaultValue: Story = {
  args: {
    defaultValue: 'react',
  },
  render: args => (
    <Select {...args}>
      <Option value="react">React</Option>
      <Option value="vue">Vue</Option>
      <Option value="angular">Angular</Option>
      <Option value="svelte">Svelte</Option>
    </Select>
  ),
};

export const Disabled: Story = {
  args: {
    disabled: true,
    defaultValue: 'react',
  },
  render: args => (
    <Select {...args}>
      <Option value="react">React</Option>
      <Option value="vue">Vue</Option>
      <Option value="angular">Angular</Option>
      <Option value="svelte">Svelte</Option>
    </Select>
  ),
};

export const WithGroups: Story = {
  render: args => (
    <Select {...args}>
      <SelectGroup>
        <SelectGroupLabel>Frontend Frameworks</SelectGroupLabel>
        <Option value="react">React</Option>
        <Option value="vue">Vue</Option>
        <Option value="angular">Angular</Option>
        <Option value="svelte">Svelte</Option>
      </SelectGroup>
      <SelectSeparator />
      <SelectGroup>
        <SelectGroupLabel>Backend Frameworks</SelectGroupLabel>
        <Option value="express">Express</Option>
        <Option value="fastapi">FastAPI</Option>
        <Option value="django">Django</Option>
        <Option value="rails">Rails</Option>
      </SelectGroup>
    </Select>
  ),
};

export const WithManyOptions: Story = {
  render: args => (
    <Select {...args}>
      <Option value="af">Afghanistan</Option>
      <Option value="al">Albania</Option>
      <Option value="dz">Algeria</Option>
      <Option value="as">American Samoa</Option>
      <Option value="ad">Andorra</Option>
      <Option value="ao">Angola</Option>
      <Option value="ai">Anguilla</Option>
      <Option value="aq">Antarctica</Option>
      <Option value="ag">Antigua and Barbuda</Option>
      <Option value="ar">Argentina</Option>
      <Option value="am">Armenia</Option>
      <Option value="aw">Aruba</Option>
      <Option value="au">Australia</Option>
      <Option value="at">Austria</Option>
      <Option value="az">Azerbaijan</Option>
      <Option value="bs">Bahamas</Option>
      <Option value="bh">Bahrain</Option>
      <Option value="bd">Bangladesh</Option>
      <Option value="bb">Barbados</Option>
      <Option value="by">Belarus</Option>
      <Option value="be">Belgium</Option>
      <Option value="bz">Belize</Option>
      <Option value="bj">Benin</Option>
      <Option value="bm">Bermuda</Option>
      <Option value="bt">Bhutan</Option>
      <Option value="bo">Bolivia</Option>
      <Option value="ba">Bosnia and Herzegovina</Option>
      <Option value="bw">Botswana</Option>
      <Option value="br">Brazil</Option>
      <Option value="bn">Brunei</Option>
      <Option value="bg">Bulgaria</Option>
      <Option value="bf">Burkina Faso</Option>
      <Option value="bi">Burundi</Option>
    </Select>
  ),
};

export const WithDisabledItems: Story = {
  render: args => (
    <Select {...args}>
      <Option value="free">Free Plan</Option>
      <Option value="basic">Basic Plan</Option>
      <Option value="pro" disabled>
        Pro Plan (Coming Soon)
      </Option>
      <Option value="enterprise" disabled>
        Enterprise Plan (Contact Sales)
      </Option>
    </Select>
  ),
};
