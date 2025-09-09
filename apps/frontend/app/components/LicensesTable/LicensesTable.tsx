import { useState } from 'react';
import { useTranslation } from 'react-i18next';

interface BusinessLicense {
  license_folio: string;
  commercial_activity: string;
  industry_classification_code: string;
  municipality_id?: number;
  municipality_name?: string;
  license_status?: string;
  license_type?: string;
}

interface LicensesTableProps {
  licenses: BusinessLicense[];
  isLoading: boolean;
  onSearch?: (searchTerm: string) => void;
  onPageChange?: (page: number) => void;
  currentPage?: number;
  totalPages?: number;
}

export function LicensesTable({
  licenses,
  isLoading,
  onSearch,
  onPageChange,
  currentPage = 1,
  totalPages = 1,
}: LicensesTableProps) {
  const { t } = useTranslation('licenses');
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch?.(searchTerm);
  };

  const getStatusBadgeClass = (status?: string) => {
    switch (status?.toLowerCase()) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'suspended':
        return 'bg-red-100 text-red-800';
      case 'cancelled':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Search Bar */}
      <form onSubmit={handleSearchSubmit} className="flex gap-4">
        <div className="flex-1">
          <label htmlFor="license-search" className="sr-only">
            {t('search.placeholder')}
          </label>
          <input
            id="license-search"
            type="text"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            placeholder={t('search.placeholder')}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <button
          type="submit"
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
        >
          {t('search.button')}
        </button>
      </form>

      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && licenses.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-500 text-lg">
            {t('empty.noResultsFound')}
          </div>
          <div className="text-gray-400 text-sm mt-2">
            {t('empty.tryDifferentFilters')}
          </div>
        </div>
      )}

      {/* Table */}
      {!isLoading && licenses.length > 0 && (
        <div className="bg-white shadow-sm rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {t('table.folio')}
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {t('table.commercialActivity')}
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {t('table.scianCode')}
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {t('table.municipality')}
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {t('table.type')}
                  </th>
                  <th
                    scope="col"
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {t('table.status')}
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {licenses.map((license, index) => (
                  <tr
                    key={`${license.license_folio}-${index}`}
                    className="hover:bg-gray-50"
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {license.license_folio}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {license.commercial_activity}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {license.industry_classification_code || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {license.municipality_name || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {license.license_type || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusBadgeClass(
                          license.license_status
                        )}`}
                      >
                        {license.license_status
                          ? t(
                              `status.${license.license_status.toLowerCase()}`,
                              { defaultValue: license.license_status }
                            )
                          : '-'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Pagination */}
      {!isLoading && licenses.length > 0 && totalPages > 1 && (
        <div className="flex justify-center items-center space-x-2">
          <button
            onClick={() => onPageChange?.(currentPage - 1)}
            disabled={currentPage <= 1}
            className="px-3 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {t('pagination.previous')}
          </button>

          <span className="px-4 py-2 text-sm text-gray-700">
            {t('pagination.pageOf', {
              current: currentPage,
              total: totalPages,
            })}
          </span>

          <button
            onClick={() => onPageChange?.(currentPage + 1)}
            disabled={currentPage >= totalPages}
            className="px-3 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {t('pagination.next')}
          </button>
        </div>
      )}
    </div>
  );
}
