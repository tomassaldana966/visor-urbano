import React, { Suspense, useEffect } from 'react';
import type { Preview } from '@storybook/react';
import { createMemoryRouter, RouterProvider } from 'react-router';

import i18n from '../app/i18n';

import '../app/app.css';
import { I18nextProvider } from 'react-i18next';

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
  decorators: [
    (story, context) => {
      const { locale } = context.globals;

      useEffect(() => {
        i18n.changeLanguage(locale);
      }, [locale]);

      const router = createMemoryRouter(
        [
          {
            path: '/',
            handle: {
              title: 'Root',
            },
          },
          {
            path: '/component',
            handle: {
              title: 'Component',
              breadcrumb: 'Component',
            },
            element: story(),
          },
        ],
        {
          initialEntries: ['/component'],
        }
      );

      return (
        <Suspense fallback={<div>Loading translations...</div>}>
          <I18nextProvider i18n={i18n}>
            <RouterProvider router={router} />
          </I18nextProvider>
        </Suspense>
      );
    },
  ],
};

export const globalTypes = {
  locale: {
    name: 'Locale',
    description: 'Internationalization locale',
    toolbar: {
      icon: 'globe',
      items: [
        {
          value: 'es',
          title: 'Spanish',
        },
        {
          value: 'en',
          title: 'English',
        },
        {
          value: 'fr',
          title: 'French',
        },
        {
          value: 'pt',
          title: 'Portuguese',
        },
      ],
      showName: true,
    },
  },
};

export default preview;
