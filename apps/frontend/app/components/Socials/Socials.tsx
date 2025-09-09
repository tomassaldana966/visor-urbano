import { useTranslation } from 'react-i18next';
import { Link } from 'react-router';
import {
  SiFacebook,
  SiInstagram,
  SiX,
  SiYoutube,
} from '@icons-pack/react-simple-icons';

const socials = [
  {
    title: 'Facebook',
    url: 'https://www.facebook.com/Visor-Urbano-Jalisco-263801398813410',
    icon: <SiFacebook />,
  },
  {
    title: 'X',
    url: 'https://x.com/VisorUrbanoJal',
    icon: <SiX />,
  },
  {
    title: 'Instagram',
    url: 'https://www.instagram.com/visorurbano.mx/',
    icon: <SiInstagram />,
  },
  {
    title: 'YouTube',
    url: 'https://www.youtube.com/channel/UC5Up17-rhu-oXyUyJFjx7bA',
    icon: <SiYoutube />,
  },
];

export function Socials() {
  const { t: tSocials } = useTranslation('socials');

  return (
    <section className="bg-primary w-full flex justify-center">
      <div className="container flex justify-center py-10">
        <h1 className="sr-only">{tSocials('title')}</h1>

        <ul className="flex gap-6 text-white">
          {socials.map(({ title, url, icon }) => (
            <li key={title}>
              <Link
                to={url}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={title}
              >
                {icon}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
