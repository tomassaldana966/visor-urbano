import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    debug: false,
    lng: 'es',
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
    interpolation: {
      escapeValue: false,
    },
    backend: {
      loadPath: `${typeof window !== 'undefined' ? window.location.origin : 'http://localhost:5173'}/locales/{{lng}}/{{ns}}.json`,
      requestOptions: {
        cache: 'no-store',
      },
    },
    react: {
      useSuspense: false,
    },
  });

export default i18n;
