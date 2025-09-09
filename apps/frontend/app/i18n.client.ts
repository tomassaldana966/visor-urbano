import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

// Cliente configuration - para el navegador
i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    debug: process.env.NODE_ENV === 'development',
    fallbackLng: 'es',
    supportedLngs: ['es', 'en', 'fr', 'pt'],
    ns: [
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
    ],
    defaultNS: 'header',
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
    interpolation: {
      escapeValue: false,
    },
    // Configuración específica para cliente
    react: {
      useSuspense: false,
    },
    // Carga inmediata en el cliente
    initImmediate: true,
    load: 'languageOnly',
  });

export default i18n;
