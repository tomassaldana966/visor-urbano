import { useTranslation } from 'react-i18next';
import { useLoaderData, type LoaderFunctionArgs, Link } from 'react-router';
import { getAuthUser } from '@/utils/auth/auth.server';
import { getNewsList } from '@/utils/api/api.server';
import { Header } from '@/components/Header/Header';
import { Footer } from '@/components/Footer/Footer';
import { Button } from '@/components/Button/Button';
import { formatDate } from '@/utils/dates/dates';
import { Socials } from '@/components/Socials/Socials';
export const handle = {
  title: 'News',
  breadcrumb: 'News',
};

export function meta() {
  return [{ title: 'News - Visor Urbano' }];
}

interface NewsItem {
  id: number;
  title: string;
  slug: string;
  summary: string;
  image: string;
  news_date: string;
  body?: string;
}

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await getAuthUser(request);

  // Fetch news from the API
  const url = new URL(request.url);
  const page = url.searchParams.get('page') || '1';

  try {
    const news: NewsItem[] = await getNewsList({
      page: parseInt(page),
      per_page: 12,
    });

    return { user, news, currentPage: parseInt(page) };
  } catch (error) {
    console.error('Failed to fetch news:', error);
    return { user, news: [], currentPage: 1 };
  }
}

export default function NewsIndex() {
  const { user, news, currentPage } = useLoaderData<typeof loader>();
  const { t } = useTranslation('news');

  const generateNewsUrl = (item: NewsItem) => {
    if (item.slug) {
      const date = new Date(item.news_date);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      return `/news/${year}/${month}/${item.slug}`;
    }
    return `/news/${item.id}`;
  };

  return (
    <div className="min-h-screen bg-white">
      <Header
        user={user}
        logo={
          <Link to="/">
            <img
              src="/logos/visor-urbano.svg"
              alt="Visor Urbano"
              className="h-10"
            />
          </Link>
        }
        navItems={[
          {
            translation: 'home',
            to: '/',
          },
          {
            translation: 'about',
            to: '/about',
          },
          {
            translation: 'licenses',
            to: '/licenses',
          },
          {
            translation: 'map',
            to: '/map',
          },
          {
            translation: 'news',
            to: '/news',
          },
        ]}
      />

      <main className="max-w-7xl mx-auto px-4 pt-24 pb-16 lg:pt-28 lg:pb-24">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight text-gray-900">
            {t('index.title')}
          </h1>

          <p className="text-xl md:text-2xl text-gray-600 leading-relaxed max-w-3xl mx-auto">
            {t('index.subtitle')}
          </p>
        </div>

        {/* News Grid */}
        {news.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
            {news.map(item => (
              <article
                key={item.id}
                className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-shadow group"
              >
                <Link to={generateNewsUrl(item)}>
                  <img
                    className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                    src={item.image}
                    alt={item.title}
                  />
                </Link>

                <div className="p-6">
                  <div className="flex items-center gap-2 text-sm text-primary mb-3">
                    <time dateTime={item.news_date}>
                      {formatDate(item.news_date)}
                    </time>
                  </div>

                  <h2 className="text-xl font-semibold text-gray-900 mb-3 group-hover:text-primary transition-colors">
                    <Link to={generateNewsUrl(item)}>{item.title}</Link>
                  </h2>

                  <p className="text-gray-600 mb-4 line-clamp-3">
                    {item.summary}
                  </p>

                  <Button asChild variant="outline" size="sm">
                    <Link to={generateNewsUrl(item)}>
                      {t('index.readMore')}
                    </Link>
                  </Button>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              {t('index.noNews')}
            </h2>
            <p className="text-gray-600">{t('index.checkBack')}</p>
          </div>
        )}

        {/* Pagination */}
        {news.length >= 12 && (
          <div className="flex justify-center gap-4">
            {currentPage > 1 && (
              <Button asChild variant="secondary">
                <Link to={`/news?page=${currentPage - 1}`}>
                  {t('index.pagination.previous')}
                </Link>
              </Button>
            )}

            <span className="flex items-center px-4 py-2 text-gray-600">
              {t('index.pagination.page')} {currentPage}
            </span>

            {news.length === 12 && (
              <Button asChild variant="secondary">
                <Link to={`/news?page=${currentPage + 1}`}>
                  {t('index.pagination.next')}
                </Link>
              </Button>
            )}
          </div>
        )}
      </main>
      <Socials />
      <Footer />
    </div>
  );
}
