import { useTranslation } from 'react-i18next';
import { Button } from '../Button/Button';
import { useMemo, type ReactNode } from 'react';
import { BloombergLogo } from '../Logos/Bloomberg';

export function Hero({
  icons = [],
  onMapClick,
}: {
  icons?: ReactNode[];
  onMapClick?: () => void;
}) {
  const { t: tHero } = useTranslation('hero');

  const iconsWithID = useMemo(
    () =>
      icons.map(icon => ({
        element: icon,
        id: crypto.randomUUID(),
      })),
    [icons]
  );

  return (
    <section
      className="bg-no-repeat pb-72 md:pb-0 bg-contain md:bg-[50%_auto] md:bg-right bg-bottom container"
      style={{
        backgroundImage: `url(${tHero('backgroundImage')})`,
      }}
    >
      <div className="md:w-1/2 flex flex-col gap-6">
        <h1 className="text-5xl font-semibold">{tHero('title')}</h1>

        <div className="flex flex-col gap-4">
          <p className="text-xl md:text-2xl">{tHero('description')}</p>

          <Button
            asChild={!onMapClick}
            className="md:max-w-1/2"
            onClick={onMapClick}
          >
            {onMapClick ? tHero('cta') : <a href="/map">{tHero('cta')}</a>}
          </Button>
        </div>

        <ul className="flex gap-4 justify-center md:justify-between items-center flex-wrap">
          <li>
            <BloombergLogo className="h-12" />
          </li>

          {iconsWithID.map(({ element, id }) => (
            <li key={id}>{element}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
