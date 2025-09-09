import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import fs from 'fs';
import path from 'path';

// Función para cargar traducciones desde archivos JSON
function loadTranslations() {
  const localesPath = path.join(process.cwd(), 'public', 'locales');
  const resources: any = {};

  const languages = ['es', 'en', 'fr', 'pt'];
  const namespaces = [
    'about',
    'benefits',
    'business-types',
    'common',
    'director',
    'errors',
    'features',
    'footer',
    'forgot',
    'header',
    'hero',
    'licenses',
    'login',
    'map',
    'nav',
    'news',
    'notifications',
    'privacy',
    'procedures',
    'register',
    'requirements',
    'scian',
    'socials',
    'tutorial',
  ];

  languages.forEach(lang => {
    resources[lang] = {};
    namespaces.forEach(ns => {
      try {
        const filePath = path.join(localesPath, lang, `${ns}.json`);
        if (fs.existsSync(filePath)) {
          const data = fs.readFileSync(filePath, 'utf8');
          resources[lang][ns] = JSON.parse(data);
        }
      } catch (error) {
        // Silently handle translation file loading errors
      }
    });
  });

  return resources;
}

// Configuración básica para SSR usando los mismos archivos JSON que el cliente
i18n.use(initReactI18next).init({
  debug: false, // Desactivar debug en servidor
  fallbackLng: 'es',
  supportedLngs: ['es', 'en', 'fr', 'pt'],
  ns: [
    'header',
    'hero',
    'features',
    'benefits',
    'tutorial',
    'news',
    'socials',
    'footer',
    'login',
    'register',
    'forgot',
    'map',
    'procedures',
    'notifications',
    'nav',
    'scian',
    'errors',
    'privacy',
    'director',
    'licenses',
    'common',
    'about',
    'requirements',
  ],
  defaultNS: 'header',
  interpolation: {
    escapeValue: false,
  },
  // Cargar los mismos recursos que usa el cliente para evitar hydration mismatch
  resources: loadTranslations(),
  // Configuración para SSR
  react: {
    useSuspense: false,
  },
  initImmediate: false,
});

export default i18n;
