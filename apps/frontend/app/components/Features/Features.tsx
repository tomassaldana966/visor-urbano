import { useTranslation } from 'react-i18next';
import { Button } from '../Button/Button';
import { Link } from 'react-router';
import { Icon } from '../Icon/Icon';

export function Features() {
  const { t: tFeatures } = useTranslation('features');

  const features = tFeatures('features', {
    returnObjects: true,
    defaultValue: [],
  }) as {
    icon: string;
    title: string;
  }[];

  return (
    <section className="flex flex-col gap-16 container items-center">
      <h1 className="text-4xl md:text-5xl text-center">
        {tFeatures('title', {
          interpolation: {
            escapeValue: false,
          },
        })}
      </h1>

      <ul className="grid grid-cols-1 md:grid-cols-3 gap-8 justify-center">
        {features?.map(feature => (
          <li key={feature.title} className="flex flex-col gap-4 items-center">
            <Icon name={feature.icon} />

            <h2>{feature.title}</h2>
          </li>
        ))}
      </ul>

      <Button asChild className="max-w-xs w-full">
        <Link to="/map">{tFeatures('cta')}</Link>
      </Button>
    </section>
  );
}
