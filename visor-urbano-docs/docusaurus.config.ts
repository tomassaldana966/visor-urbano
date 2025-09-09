import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Visor Urbano Documentation',
  tagline:
    'Municipal Urban Planning Management System - Global Implementation Guide',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://docs.visor-urbano.org',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Delivery-Associates', // Usually your GitHub org/user name.
  projectName: 'visor-urbano-docs', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'es',
    locales: ['es', 'en', 'fr', 'pt'],
    localeConfigs: {
      es: {
        label: 'Español',
        direction: 'ltr',
        htmlLang: 'es-CL', // Configurado para Chile inicialmente
        calendar: 'gregory',
      },
      en: {
        label: 'English',
        direction: 'ltr',
        htmlLang: 'en-US',
      },
      fr: {
        label: 'Français',
        direction: 'ltr',
        htmlLang: 'fr-FR',
      },
      pt: {
        label: 'Português',
        direction: 'ltr',
        htmlLang: 'pt-BR',
      },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/', // Serve docs at the site's root
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/Delivery-Associates/visor-urbano-docs/tree/main/',
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
        },
        blog: false, // Disable blog functionality
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      hideOnScroll: false,
      logo: {
        alt: 'Visor Urbano Logo',
        src: 'img/logo.svg',
        srcDark: 'img/logo.svg',
        width: 180,
        height: 40,
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          to: '/implementation/step-by-step-guide',
          label: '📋 Guía de Implementación',
          position: 'left',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/Delivery-Associates/visor-urbano',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Implementaciones',
          items: [
            {
              label: '📋 Guía Paso a Paso',
              to: '/implementation/step-by-step-guide',
            },
            {
              label: '🇲🇽 Adaptación México',
              to: '/getting-started/overview',
            },
            {
              label: 'Marco Legal Chile',
              to: '/city-adaptation/legal-framework-chile',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Visor Urbano. Built with Docusaurus.`,
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
