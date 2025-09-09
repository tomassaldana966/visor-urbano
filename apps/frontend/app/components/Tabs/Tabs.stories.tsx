import type { Meta, StoryObj } from '@storybook/react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './Tabs';

const meta: Meta<typeof Tabs> = {
  title: 'Components/Tabs',
  component: Tabs,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Tabs>;

export const Default: Story = {
  render: () => (
    <Tabs defaultValue="tab1" className="w-[400px]">
      <TabsList>
        <TabsTrigger value="tab1">Tab 1</TabsTrigger>
        <TabsTrigger value="tab2">Tab 2</TabsTrigger>
        <TabsTrigger value="tab3">Tab 3</TabsTrigger>
      </TabsList>
      <TabsContent value="tab1">
        <div className="p-4 rounded-lg border mt-2">
          <h3 className="font-medium">Content for Tab 1</h3>
          <p className="text-sm text-gray-500">
            This is the content for the first tab panel.
          </p>
        </div>
      </TabsContent>
      <TabsContent value="tab2">
        <div className="p-4 rounded-lg border mt-2">
          <h3 className="font-medium">Content for Tab 2</h3>
          <p className="text-sm text-gray-500">
            This is the content for the second tab panel.
          </p>
        </div>
      </TabsContent>
      <TabsContent value="tab3">
        <div className="p-4 rounded-lg border mt-2">
          <h3 className="font-medium">Content for Tab 3</h3>
          <p className="text-sm text-gray-500">
            This is the content for the third tab panel.
          </p>
        </div>
      </TabsContent>
    </Tabs>
  ),
};

export const Disabled: Story = {
  render: () => (
    <Tabs defaultValue="tab1" className="w-[400px]">
      <TabsList>
        <TabsTrigger value="tab1">Active</TabsTrigger>
        <TabsTrigger value="tab2" disabled>
          Disabled
        </TabsTrigger>
        <TabsTrigger value="tab3">Tab 3</TabsTrigger>
      </TabsList>
      <TabsContent value="tab1">
        <div className="p-4 rounded-lg border mt-2">
          <p className="text-sm text-gray-500">
            Notice the second tab is disabled.
          </p>
        </div>
      </TabsContent>
      <TabsContent value="tab3">
        <div className="p-4 rounded-lg border mt-2">
          <p className="text-sm text-gray-500">Content for the third tab.</p>
        </div>
      </TabsContent>
    </Tabs>
  ),
};

export const VerticalLayout: Story = {
  render: () => (
    <Tabs defaultValue="tab1" orientation="vertical" className="w-[600px]">
      <div className="flex">
        <TabsList className="flex-col h-auto mr-4">
          <TabsTrigger value="tab1">Profile</TabsTrigger>
          <TabsTrigger value="tab2">Settings</TabsTrigger>
          <TabsTrigger value="tab3">Notifications</TabsTrigger>
        </TabsList>
        <div className="flex-1">
          <TabsContent value="tab1">
            <div className="p-4 rounded-lg border">
              <h3 className="font-medium">Profile Settings</h3>
              <p className="text-sm text-gray-500">
                Manage your profile information.
              </p>
            </div>
          </TabsContent>
          <TabsContent value="tab2">
            <div className="p-4 rounded-lg border">
              <h3 className="font-medium">Account Settings</h3>
              <p className="text-sm text-gray-500">
                Manage your account preferences.
              </p>
            </div>
          </TabsContent>
          <TabsContent value="tab3">
            <div className="p-4 rounded-lg border">
              <h3 className="font-medium">Notification Settings</h3>
              <p className="text-sm text-gray-500">
                Manage your notification preferences.
              </p>
            </div>
          </TabsContent>
        </div>
      </div>
    </Tabs>
  ),
};
