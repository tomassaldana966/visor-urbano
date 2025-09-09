import { useTranslation } from 'react-i18next';
import { Award, Users, Building, CheckCircle, Star } from 'lucide-react';
import { Button } from '@root/app/components/Button/Button';
import { Header } from '@root/app/components/Header/Header';
import { Footer } from '@root/app/components/Footer/Footer';
import { useLoaderData, type LoaderFunctionArgs, Link } from 'react-router';
import { getAuthUser } from '@/utils/auth/auth.server';
import { Socials } from '@/components/Socials/Socials';

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await getAuthUser(request);

  return { user };
}

export const handle = {
  title: 'about:title',
  breadcrumb: 'About',
};

export function meta() {
  const { t } = useTranslation('about');
  return [{ title: `${t('title')}` }];
}

export default function About() {
  const { t, ready } = useTranslation('about');

  const loaderData = useLoaderData<typeof loader>();
  const user = loaderData?.user || null;

  if (!ready) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[var(--color-vu-light-gray)]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--color-vu-primary)] mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

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

      <section className="relative bg-[var(--color-vu-primary)] text-white overflow-hidden">
        <div className="absolute inset-0 bg-[url('/background/pattern.svg')] opacity-10"></div>

        <div className="relative max-w-7xl mx-auto px-4 py-20 lg:py-32">
          <div className="max-w-4xl">
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
              {t('title')}
            </h1>

            <p className="text-xl md:text-2xl text-white/90 leading-relaxed max-w-3xl">
              {t('description.content')}
            </p>
          </div>
        </div>
      </section>

      <main className="max-w-7xl mx-auto px-4 py-16 lg:py-24">
        <section className="mb-20">
          <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6 flex items-center gap-3">
                <div className="w-12 h-12 bg-[var(--color-vu-primary)] rounded-xl flex items-center justify-center">
                  <Building className="w-6 h-6 text-white" />
                </div>
                {t('background.title')}
              </h2>
              <div className="space-y-6 text-gray-700 leading-relaxed">
                <p className="text-lg">{t('background.paragraph1')}</p>
                <p className="text-lg">{t('background.paragraph2')}</p>
              </div>
            </div>

            <div>
              <div className="aspect-square bg-gray-100 rounded-3xl p-8 flex items-center justify-center">
                {' '}
                <div className="text-center">
                  <div className="w-24 h-24 bg-[var(--color-vu-primary)] rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Award className="w-12 h-12 text-white" />
                  </div>
                  <p className="text-2xl font-bold text-gray-900">
                    {t('awards.year')}
                  </p>
                  <p className="text-gray-600">
                    {t('awards.mayorsChallengeTitle')}
                  </p>
                  <p className="text-gray-600">
                    {t('awards.mayorsChallengeSubtitle')}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              {t('benefits.title')}
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              {t('benefits.subtitle')}
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-8 lg:gap-12">
            <div className="bg-[var(--color-vu-light-green)] rounded-3xl p-8 lg:p-10">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-14 h-14 bg-[var(--color-vu-primary)] rounded-2xl flex items-center justify-center">
                  <Users className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900">
                  {t('benefits.citizens.title')}
                </h3>
              </div>
              <ul className="space-y-4">
                {(
                  t('benefits.citizens.items', {
                    returnObjects: true,
                  }) as string[]
                ).map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-[var(--color-vu-primary)] mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700 leading-relaxed">
                      {item}
                    </span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-[var(--color-vu-light-gray)] rounded-3xl p-8 lg:p-10">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-14 h-14 bg-[var(--color-vu-gray)] rounded-2xl flex items-center justify-center">
                  <Building className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900">
                  {t('benefits.municipalities.title')}
                </h3>
              </div>
              <ul className="space-y-4">
                {(
                  t('benefits.municipalities.items', {
                    returnObjects: true,
                  }) as string[]
                ).map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-[var(--color-vu-gray)] mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700 leading-relaxed">
                      {item}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        <section className="mb-20">
          <div className="bg-[var(--color-vu-light-gray)] rounded-3xl p-8 lg:p-12">
            <div className="text-center mb-12">
              <div className="w-16 h-16 bg-[var(--color-vu-primary)] rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Star className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                {t('awards.title')}
              </h2>
              <p className="text-lg text-gray-700 max-w-2xl mx-auto">
                {t('awards.intro')}
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
              {(t('awards.items', { returnObjects: true }) as string[]).map(
                (award, index) => (
                  <div
                    key={index}
                    className="bg-white rounded-2xl p-6 shadow-sm"
                  >
                    <div className="flex items-start gap-3">
                      <div className="w-8 h-8 bg-[var(--color-vu-primary)] rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                        <Award className="w-4 h-4 text-white" />
                      </div>
                      <p className="text-gray-700 leading-relaxed text-sm">
                        {award}
                      </p>
                    </div>
                  </div>
                )
              )}
            </div>

            <div className="bg-white rounded-2xl p-6 lg:p-8 shadow-sm">
              <p className="text-gray-700 leading-relaxed text-lg">
                {t('awards.conclusion')}
              </p>
            </div>
          </div>
        </section>

        <section className="text-center">
          <div className="p-8 lg:p-12 text-[var(--color-vu-primary)]">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              {t('cta.title')}
            </h2>
            <p className="text-xl text-[var(--color-vu-primary)] mb-8 max-w-2xl mx-auto">
              {t('cta.description')}
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button asChild size="lg" variant="primary">
                <Link to="/map">{t('cta.exploreMap')}</Link>
              </Button>
              <Button asChild size="lg" variant="secondary">
                <Link to="/login">{t('cta.login')}</Link>
              </Button>
            </div>
          </div>
        </section>
      </main>
      <Socials />
      <Footer />
    </div>
  );
}
