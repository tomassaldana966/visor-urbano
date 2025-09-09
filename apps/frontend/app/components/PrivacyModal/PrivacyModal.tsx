import type { PropsWithChildren } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
  DialogTrigger,
} from '../Dialog/Dialog';
import { useTranslation } from 'react-i18next';
import { TransWithComponents } from '../TransWithComponents/TransWithComponents';

export function PrivacyModal({ children }: PropsWithChildren) {
  const { t: tPrivacy } = useTranslation('privacy');

  return (
    <Dialog>
      <DialogTrigger asChild>{children}</DialogTrigger>

      <DialogContent>
        <DialogTitle className="text-primary">{tPrivacy('title')}</DialogTitle>

        <DialogDescription className="flex flex-col gap-4">
          <TransWithComponents i18nKey="privacy:description" />
        </DialogDescription>
      </DialogContent>
    </Dialog>
  );
}
