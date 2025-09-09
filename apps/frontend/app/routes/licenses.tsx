import { useTranslation } from 'react-i18next';
import { Header } from '@/components/Header/Header';
import { Footer } from '@/components/Footer/Footer';
import { LicensesTable } from '@/components/LicensesTable/LicensesTable';
import { useLicenses } from '@/hooks/useLicenses';
import { Link, useLoaderData, type LoaderFunctionArgs } from 'react-router';
import { getAuthUser } from '@/utils/auth/auth.server';

export function meta() {
  return [{ title: 'Business Licenses - Visor Urbano' }];
}

export async function loader({ request }: LoaderFunctionArgs) {
  // Check if user is authenticated, but don't require it (licenses page is public)
  const user = await getAuthUser(request);
  return { user };
}

export default function Licenses() {
  const { t } = useTranslation('licenses');
  const { user } = useLoaderData<typeof loader>();

  const {
    licenses,
    isLoading,
    error,
    currentPage,
    totalPages,
    handleSearch,
    handlePageChange,
  } = useLicenses({
    initialPerPage: 20, // Show more items per page for the public listing
  });

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
          },
          {
            translation: 'news',
            to: '/news',
          },
        ]}
      />

      <main className="min-h-screen bg-gray-50 pt-24 pb-16 lg:pt-28 lg:pb-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Page Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              {t('title.issuedLicenses')}
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              {t('description.managementAndConsultation', {
                municipalityName: 'la región',
              })}
            </p>
          </div>

          {/* Error State */}
          {error && (
            <div className="mb-8 bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg
                    className="h-5 w-5 text-red-400"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">
                    Error loading licenses
                  </h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>{error}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Licenses Table */}
          <div className="bg-white shadow-sm rounded-lg overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">
                {t('table.tableTitle')}
              </h2>
            </div>

            <div className="p-6">
              <LicensesTable
                licenses={licenses}
                isLoading={isLoading}
                onSearch={handleSearch}
                onPageChange={handlePageChange}
                currentPage={currentPage}
                totalPages={totalPages}
              />
            </div>
          </div>

          {/* Additional Information */}
          <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-blue-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">
                  {t('about.title')}
                </h3>
                <div className="mt-2 text-sm text-blue-700">
                  <p>{t('about.description')}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
}
