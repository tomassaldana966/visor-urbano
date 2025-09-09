import { Hero } from '@/components/Hero/Hero';
import { Header } from '@/components/Header/Header';
import { Benefits } from '@/components/Benefits/Benefits';
import { Features } from '@/components/Features/Features';
import { Tutorial } from '@/components/Tutorial/Tutorial';
import { News } from '@/components/News/News';
import { Socials } from '@/components/Socials/Socials';
import { Footer } from '@/components/Footer/Footer';
import { LoadingModal } from '@/components/LoadingModal/LoadingModal';
import { useLoaderData, type LoaderFunctionArgs, Link } from 'react-router';
import { getAuthUser } from '@/utils/auth/auth.server';
import { getNewsList } from '@/utils/api/api.server';
import { useMapNavigation } from '@/hooks/useMapNavigation';

export function meta() {
  return [{ title: 'Visor Urbano' }];
}

export async function loader({ request }: LoaderFunctionArgs) {
  // Check if user is authenticated, but don't require it (home page is public)
  const user = await getAuthUser(request);

  // Fetch latest news articles for the homepage
  let newsItems: any[] = [];
  try {
    newsItems = await getNewsList();
  } catch (error) {
    console.error('Failed to fetch news items:', error);
    // Fallback to empty array, component will handle gracefully
  }

  return { user, newsItems };
}

export default function () {
  const { user, newsItems } = useLoaderData<typeof loader>();
  const { isMapLoading, navigateToMap } = useMapNavigation();

  // Generate friendly URLs for news items
  const generateNewsUrl = (item: any) => {
    if (item.slug) {
      const date = new Date(item.news_date);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      return `/news/${year}/${month}/${item.slug}`;
    }
    return `/news/${item.id}`;
  };

  // Transform news items for the News component
  const transformedNewsItems = newsItems.map((item: any) => ({
    id: item.id.toString(),
    date: item.news_date,
    img: item.image,
    link: generateNewsUrl(item),
    summary: item.summary,
    title: item.title,
  }));

  return (
    <>
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
            onClick: (e: any) => {
              e.preventDefault();
              navigateToMap();
            },
          },
          {
            translation: 'news',
            to: '/news',
          },
        ]}
      />

      <main className="flex flex-col gap-24 items-center pt-30">
        <Hero onMapClick={navigateToMap} />

        <Features />

        <Benefits />

        <Tutorial />

        <News
          items={
            transformedNewsItems.length > 0
              ? transformedNewsItems
              : [
                  {
                    id: '1',
                    date: '2021-09-01',
                    img: 'https://placehold.co/150',
                    link: '/news/1',
                    summary: 'Summary of the news article',
                    title: 'News Article Title',
                  },
                  {
                    id: '2',
                    date: '2021-09-02',
                    img: 'https://placehold.co/150x300',
                    link: '/news/2',
                    summary: 'Summary of the news article',
                    title: 'News Article Title',
                  },
                  {
                    id: '3',
                    date: '2021-09-03',
                    img: 'https://placehold.co/300x150',
                    link: '/news/3',
                    summary: 'Summary of the news article',
                    title: 'News Article Title',
                  },
                  {
                    id: '4',
                    date: '2021-09-04',
                    img: 'https://placehold.co/100x120',
                    link: '/news/4',
                    summary: 'Summary of the news article',
                    title: 'News Article Title',
                  },
                  {
                    id: '5',
                    date: '2021-09-05',
                    img: 'https://placehold.co/100',
                    link: '/news/5',
                    summary: 'Summary of the news article',
                    title: 'News Article',
                  },
                ]
          }
        />

        <Socials />
      </main>

      <Footer />

      <LoadingModal isOpen={isMapLoading} type="map" useTranslations={true} />
    </>
  );
}
