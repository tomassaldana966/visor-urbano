import type { Meta, StoryObj } from '@storybook/react';

import { PropertyInfo } from './PropertyInfo';
import type { ComponentProps } from 'react';

const meta = {
  title: 'Components/PropertyInfo',
  component: PropertyInfo,
  tags: ['autodocs'],
} satisfies Meta<ComponentProps<typeof PropertyInfo>>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    property: {
      id: 'sample-property-1',
      municipality: 'Municipality Name',
      locality: 'Locality Name',
      postalCode: '12345',
      area: {
        raw: 150,
        sup: 2,
        unit: 'm²',
        value: '150',
      },
      areaBuilt: {
        raw: 100,
        sup: 2,
        unit: 'm²',
        value: '100',
      },
      minimapURL: 'https://placehold.co/250',
      downloadURL: new URL('https://example.com/download.zip'),
      neighborhood: 'Neighborhood Name',
      street: 'Main Street 123',
      address: 'Main Street 123, Neighborhood Name',
      coordinates: [[0, 0]],
      boundingBox: [0, 0, 1, 1],
      municipalityId: 1,
      businessTypes: [
        {
          id: 1,
          name: 'Restaurant',
          business_type_id: 1,
          municipality_id: 1,
          is_disabled: false,
          has_certificate: false,
          impact_level: 2,
          description: 'Restaurant business',
          code: 'REST001',
          related_words: 'food,dining',
        },
        {
          id: 2,
          name: 'Retail Store',
          business_type_id: 2,
          municipality_id: 1,
          is_disabled: false,
          has_certificate: false,
          impact_level: 1,
          description: 'Retail store business',
          code: 'RET001',
          related_words: 'shop,store',
        },
      ],
      dynamicFields: [],
      type: '',
      totalFeatures: 0,
      numberMatched: 0,
      numberReturned: 0,
      timeStamp: '',
    },
  },
};
