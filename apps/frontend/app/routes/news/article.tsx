import { useTranslation } from 'react-i18next';
import { useLoaderData, type LoaderFunctionArgs, Link } from 'react-router';
import { Calendar, Share2 } from 'lucide-react';
import { getAuthUser } from '@/utils/auth/auth.server';
import { getNewsByFriendlyUrl } from '@/utils/api/api.server';
import { Header } from '@/components/Header/Header';
import { Footer } from '@/components/Footer/Footer';
import { Button } from '@/components/Button/Button';
import { Socials } from '@/components/Socials/Socials';
import { formatDate } from '@/utils/dates/dates';

export const handle = {
  title: 'News Article',
  breadcrumb: 'News Article',
};

interface NewsItem {
  id: number;
  title: string;
  slug: string;
  summary: string;
  image: string;
  news_date: string;
  body?: string;
}

export async function loader({ request, params }: LoaderFunctionArgs) {
  const user = await getAuthUser(request);
  const { year, month, slug } = params;

  if (!year || !month || !slug) {
    throw new Response('Invalid news article URL', { status: 400 });
  }

  try {
    const article: NewsItem = await getNewsByFriendlyUrl(
      parseInt(year),
      parseInt(month),
      slug
    );

    return { user, article };
  } catch (error) {
    console.error('Failed to fetch news article:', error);

    if (error instanceof Error && error.message.includes('HTTP 404')) {
      throw new Response('News article not found', { status: 404 });
    }

    throw new Response('Failed to load news article', { status: 500 });
  }
}

export function meta({ data }: { data: any }) {
  if (!data?.article) {
    return [{ title: 'News Article Not Found - Visor Urbano' }];
  }

  return [
    { title: `${data.article.title} - Visor Urbano` },
    { name: 'description', content: data.article.summary },
    { property: 'og:title', content: data.article.title },
    { property: 'og:description', content: data.article.summary },
    { property: 'og:image', content: data.article.image },
    { property: 'og:type', content: 'article' },
  ];
}

export default function NewsArticle() {
  const { user, article } = useLoaderData<typeof loader>();
  const { t } = useTranslation('news');

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: article.title,
          text: article.summary,
          url: window.location.href,
        });
      } catch (error) {
        console.error('Error sharing:', error);
      }
    } else {
      // Fallback to copying URL to clipboard
      navigator.clipboard.writeText(window.location.href);
      // You could show a toast notification here
    }
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

      <main className="max-w-4xl mx-auto px-4 pt-24 pb-16 lg:pt-28 lg:pb-24">
        {/* Article Header */}
        <header className="mb-8">
          <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
            <div className="flex items-center gap-2">
              <Calendar size={16} />
              <time dateTime={article.news_date}>
                {formatDate(article.news_date)}
              </time>
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={handleShare}
              className="ml-auto"
            >
              <Share2 size={16} className="mr-2" />
              {t('article.share')}
            </Button>
          </div>

          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 leading-tight mb-6">
            {article.title}
          </h1>

          <p className="text-xl text-gray-600 leading-relaxed">
            {article.summary}
          </p>
        </header>

        {/* Featured Image */}
        <div className="mb-8">
          <img
            src={article.image}
            alt={article.title}
            className="w-full h-64 md:h-96 object-cover rounded-2xl"
          />
        </div>

        {/* Article Content */}
        <article className="prose prose-lg max-w-none">
          {article.body ? (
            <div dangerouslySetInnerHTML={{ __html: article.body }} />
          ) : (
            <p className="text-gray-600 text-lg leading-relaxed">
              {article.summary}
            </p>
          )}
        </article>

        {/* Back to News */}
        <div className="mt-16 pt-8 border-t border-gray-200">
          <Button asChild size="lg">
            <Link to="/news">{t('article.viewAllNews')}</Link>
          </Button>
        </div>
      </main>
      <Socials />
      <Footer />
    </div>
  );
}
