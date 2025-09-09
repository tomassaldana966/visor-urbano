import { useState, useEffect } from 'react';
import {
  getBusinessLicensesListClient,
  type BusinessLicense as ApiBusinessLicense,
} from '@/utils/api/api.client';

interface BusinessLicense {
  license_folio: string;
  commercial_activity: string;
  industry_classification_code: string;
  municipality_id?: number;
  municipality_name?: string;
  license_status?: string;
  license_type?: string;
}

interface FetchLicensesParams {
  page?: number;
  per_page?: number;
  search?: string;
  municipality_id?: number;
}

interface UseLicensesParams {
  initialPage?: number;
  initialPerPage?: number;
  initialSearch?: string;
  initialMunicipalityId?: number;
}

export function useLicenses({
  initialPage = 1,
  initialPerPage = 10,
  initialSearch = '',
  initialMunicipalityId,
}: UseLicensesParams = {}) {
  const [licenses, setLicenses] = useState<BusinessLicense[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [searchTerm, setSearchTerm] = useState(initialSearch);
  const [municipalityId, setMunicipalityId] = useState(initialMunicipalityId);
  const [totalPages, setTotalPages] = useState(1);

  const fetchLicenses = async (
    page: number = currentPage,
    search: string = searchTerm,
    municipality: number | undefined = municipalityId
  ) => {
    setIsLoading(true);
    setError(null);

    try {
      const params: FetchLicensesParams = {
        page,
        per_page: initialPerPage,
      };

      if (search.trim()) {
        params.search = search.trim();
      }

      if (municipality) {
        params.municipality_id = municipality;
      }

      const response = await getBusinessLicensesListClient(params);
      setLicenses(response.items || []);

      // Use pagination information from the API response
      setTotalPages(response.total_pages);
    } catch (err) {
      console.error('Error fetching licenses:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch licenses');
      setLicenses([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (newSearchTerm: string) => {
    setSearchTerm(newSearchTerm);
    setCurrentPage(1); // Reset to first page when searching
    fetchLicenses(1, newSearchTerm, municipalityId);
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    fetchLicenses(page, searchTerm, municipalityId);
  };

  const handleMunicipalityChange = (newMunicipalityId: number | undefined) => {
    setMunicipalityId(newMunicipalityId);
    setCurrentPage(1); // Reset to first page when changing municipality
    fetchLicenses(1, searchTerm, newMunicipalityId);
  };

  const refetch = () => {
    fetchLicenses(currentPage, searchTerm, municipalityId);
  };

  useEffect(() => {
    fetchLicenses();
  }, []); // Only run on mount

  return {
    licenses,
    isLoading,
    error,
    currentPage,
    totalPages,
    searchTerm,
    municipalityId,
    handleSearch,
    handlePageChange,
    handleMunicipalityChange,
    refetch,
  };
}
