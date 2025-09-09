import i18n from '@root/app/i18n';
import { footerNav } from '@root/config/constants';

export function CityLogo() {
  const language = i18n.language;

  const cityLogo =
    (footerNav[language as keyof typeof footerNav] ?? footerNav.es)[2] ?? null;

  return cityLogo;
}
