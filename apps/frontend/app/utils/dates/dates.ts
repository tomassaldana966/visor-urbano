import i18n from '@/i18n';

export function formatDate(date: string) {
  const locale = i18n.language;

  return Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(date));
}
