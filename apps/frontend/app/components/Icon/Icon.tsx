import { DocumentIcon } from './icons/document';
import { MapIcon } from './icons/map';
import { StoreIcon } from './icons/store';

export const icons = {
  document: () => <DocumentIcon />,
  map: () => <MapIcon />,
  store: () => <StoreIcon />,
} as const;

export function Icon({ name }: { name: keyof typeof icons | string }) {
  if (!(name in icons)) {
    return null;
  }

  const SelectedIcon = icons[name as keyof typeof icons];

  return <SelectedIcon />;
}
