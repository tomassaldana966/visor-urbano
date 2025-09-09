import { useTranslation } from 'react-i18next';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  DialogTrigger,
} from '../Dialog/Dialog';
import i18n from '@/i18n';
import { footerNav } from 'config/constants';
import { PrivacyModal } from '../PrivacyModal/PrivacyModal';
import { TransWithComponents } from '../TransWithComponents/TransWithComponents';
import { BloombergLogo } from '../Logos/Bloomberg';
import { Link } from 'react-router';

export function Footer() {
  const { t: tFooter } = useTranslation('footer');
  const { t: tSCIAN } = useTranslation('scian');

  const language = i18n.language;

  const nav2 = footerNav[language as keyof typeof footerNav] ?? footerNav.es;

  return (
    <footer
      className="bg-support-4 w-full pt-36 pb-10 bg-bottom"
      style={{
        backgroundImage: 'url(/background/footer.svg)',
      }}
    >
      <div className="container grid grid-cols-1 md:grid-cols-3 gap-2 mx-auto">
        <div className="flex items-end">
          <ul className="flex flex-col items-center w-full gap-2">
            <li>
              <PrivacyModal>
                <button type="button" className="text-primary cursor-pointer">
                  {tFooter('privacy')}
                </button>
              </PrivacyModal>
            </li>

            <li>
              <Dialog>
                <DialogTrigger asChild>
                  <button type="button" className="text-primary cursor-pointer">
                    {tFooter('scian')}
                  </button>
                </DialogTrigger>

                <DialogContent>
                  <DialogTitle className="text-primary">
                    {tSCIAN('title')}
                  </DialogTitle>

                  <DialogDescription className="flex flex-col gap-4">
                    <TransWithComponents i18nKey="scian:description" />
                  </DialogDescription>
                </DialogContent>
              </Dialog>
            </li>

            <li className="hidden md:block">
              <BloombergLogo />
            </li>
          </ul>
        </div>

        <div className="flex items-end">
          <ul className="flex flex-col items-center w-full gap-2">
            {nav2.map(item => (
              <li className="text-primary" key={item.key}>
                {item}
              </li>
            ))}
          </ul>
        </div>
        <Link to="/">
          <img
            src="/logos/visor-urbano.svg"
            alt="Visor Urbano"
            className="h-24"
          />
        </Link>
      </div>
    </footer>
  );
}
