import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: '🚀 Comenzar',
      items: [
        'getting-started/overview',
        'getting-started/quick-setup',
        'getting-started/system-requirements',
      ],
    },
    {
      type: 'category',
      label: '🌍 Adaptación por Ciudad',
      items: [
        {
          type: 'category',
          label: '🇨🇱 Chile',
          items: [
            'city-adaptation/legal-framework-chile',
            'city-adaptation/integration-chile',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: '👨‍💻 Desarrollo',
      items: [
        'development/README',
        'development/setup-integration',
        'development/api-integration',
        'development/api-documentation',
        'development/generated-api-integration',
      ],
    },
    {
      type: 'category',
      label: '🚀 Implementación',
      items: [
        'implementation/step-by-step-guide',
        'deployment/production-deployment',
      ],
    },
  ],
};

export default sidebars;
