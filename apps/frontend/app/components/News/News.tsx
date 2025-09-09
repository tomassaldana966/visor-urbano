import { useTranslation } from 'react-i18next';
import { Link } from 'react-router';
import { Button } from '../Button/Button';
import { formatDate } from '@/utils/dates/dates';

type NewsItem = {
  id: string;
  date: string;
  img: string;
  link: string;
  summary: string;
  title: string;
};

export function News({ items }: { items: NewsItem[] }) {
  const { t: tNews } = useTranslation('news');

  return (
    <section className="container flex flex-col gap-8">
      <h1 className="text-4xl md:text-5xl text-center">{tNews('title')}</h1>

      <ul className="grid md:grid-cols-2 gap-8">
        {items.map(item => (
          <li key={item.id}>
            <article className="flex flex-col gap-4">
              <Link to={item.link}>
                <img
                  className="overflow-hidden rounded-xl w-full aspect-video object-cover"
                  src={item.img}
                  alt={item.title}
                />
              </Link>

              <div className="flex flex-col gap-2 px-2">
                <h1 className="font-semibold text-lg">{item.title}</h1>

                <small className="text-primary">{formatDate(item.date)}</small>

                <p>{item.summary}</p>
              </div>

              <Button asChild className="max-w-60 w-full mx-auto">
                <Link to={item.link}>{tNews('cta')}</Link>
              </Button>
            </article>
          </li>
        ))}
      </ul>
    </section>
  );
}
