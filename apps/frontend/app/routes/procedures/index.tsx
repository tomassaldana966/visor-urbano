import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@root/app/components/Tabs/Tabs';
import { Table } from '@root/app/components/Table/Table';
import { Button } from '@root/app/components/Button/Button';
import { Badge } from '@root/app/components/Badge/Badge';
import { ProcedureModal } from '@root/app/components/ProcedureModal/ProcedureModal';
import { ProcedureFilesModal } from '@root/app/components/ProcedureFilesModal/ProcedureFilesModal';
import { useTranslation } from 'react-i18next';
import { useState, useEffect, useMemo } from 'react';
import {
  useLoaderData,
  type LoaderFunctionArgs,
  useNavigate,
} from 'react-router';
import { requireAuth, getAccessToken } from '@root/app/utils/auth/auth.server';
import { getProceduresEnhanced } from '@root/app/utils/api/api.server';
import type {
  ProcedureData,
  BusinessCommercialProcedureData,
  ConstructionProcedureData,
} from '@root/app/types/procedures';
import { FileText, Eye, MoreHorizontal, Search } from 'lucide-react';

export const handle = {
  title: 'procedures:myProcedures',
  breadcrumb: 'procedures:myProcedures',
};

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);
  const authToken = await getAccessToken(request);

  if (!authToken) {
    throw new Response('Unauthorized', { status: 401 });
  }

  if (!user?.id) {
    throw new Response('User context is invalid', { status: 401 });
  }

  try {
    const municipalityId = user.municipality_id || 2;
    const proceduresResult = await getProceduresEnhanced(authToken);

    const businessProcedures = proceduresResult.filter(
      p =>
        p.procedure_type === 'business_license' ||
        p.procedure_type === 'license_renewal' ||
        p.procedure_type === 'commercial_license' ||
        p.procedure_type === 'giro comercial' ||
        (p.procedure_type && p.procedure_type.includes('business_license'))
    );

    const constructionProcedures = proceduresResult.filter(
      p =>
        p.procedure_type === 'construction_permit' ||
        p.procedure_type === 'construction_license' ||
        (p.procedure_type &&
          p.procedure_type.includes('permits_building_license')) ||
        (p.procedure_type && p.procedure_type.includes('construccion'))
    );

    return {
      businessProcedures,
      constructionProcedures,
    };
  } catch (error) {
    throw new Response(
      error instanceof Error
        ? error.message
        : 'Unknown error loading procedures',
      { status: 500 }
    );
  }
}

export default function ProceduresPage() {
  const { t: tProcedures, ready } = useTranslation('procedures');
  const { businessProcedures, constructionProcedures } =
    useLoaderData<typeof loader>();
  const navigate = useNavigate();

  type AnyProcedureData =
    | BusinessCommercialProcedureData
    | ConstructionProcedureData
    | ProcedureData;

  const toProcedureData = (procedure: AnyProcedureData): ProcedureData => ({
    ...procedure,
    folio: procedure.folio ?? null,
  });

  if (!ready) {
    return (
      <div className="p-4 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto mb-2"></div>
          <p>
            {tProcedures('loading.translations') || 'Loading translations...'}
          </p>
        </div>
      </div>
    );
  }

  const businessProceduresAtLimit = businessProcedures.length >= 100;
  const constructionProceduresAtLimit = constructionProcedures.length >= 100;

  const [selectedProcedure, setSelectedProcedure] = useState<any>(null);
  const [isProcedureModalOpen, setIsProcedureModalOpen] = useState(false);
  const [isFilesModalOpen, setIsFilesModalOpen] = useState(false);
  const [selectedProcedureId, setSelectedProcedureId] = useState<number | null>(
    null
  );

  const [searchTerm, setSearchTerm] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<{
    businessProcedures: any[];
    constructionProcedures: any[];
  } | null>(null);

  const [authToken, setAuthToken] = useState('');

  useEffect(() => {
    if (typeof window !== 'undefined') {
      setAuthToken(localStorage.getItem('authToken') || '');
    }
  }, []);

  const searchSpecificProcedures = async (searchTerm: string) => {
    if (!authToken || !searchTerm.trim()) return;

    setIsSearching(true);
    try {
      const user = { municipality_id: 2 };
      const municipalityId = user.municipality_id || 2;

      const [businessSearchResult, constructionSearchResult] =
        await Promise.allSettled([
          fetch(
            `/v1/business_commercial_procedures/?municipality_id=${municipalityId}&limit=500`,
            {
              headers: { Authorization: `Bearer ${authToken}` },
            }
          ),
          fetch(
            `/v1/construction_procedures/?municipality_id=${municipalityId}&limit=500`,
            {
              headers: { Authorization: `Bearer ${authToken}` },
            }
          ),
        ]);

      const businessData =
        businessSearchResult.status === 'fulfilled' &&
        businessSearchResult.value.ok
          ? await businessSearchResult.value.json()
          : { procedures: [] };

      const constructionData =
        constructionSearchResult.status === 'fulfilled' &&
        constructionSearchResult.value.ok
          ? await constructionSearchResult.value.json()
          : { procedures: [] };

      const term = searchTerm.toLowerCase().trim();
      const filteredBusiness = (businessData.procedures || []).filter(
        (procedure: any) =>
          (procedure.folio && procedure.folio.toLowerCase().includes(term)) ||
          (procedure.establishment_address &&
            procedure.establishment_address.toLowerCase().includes(term)) ||
          (procedure.full_address &&
            procedure.full_address.toLowerCase().includes(term)) ||
          (procedure.official_applicant_name &&
            procedure.official_applicant_name.toLowerCase().includes(term)) ||
          (procedure.street && procedure.street.toLowerCase().includes(term)) ||
          (procedure.scian_code &&
            procedure.scian_code.toLowerCase().includes(term)) ||
          (procedure.scian_name &&
            procedure.scian_name.toLowerCase().includes(term))
      );

      const filteredConstruction = (constructionData.procedures || []).filter(
        (procedure: any) =>
          (procedure.folio && procedure.folio.toLowerCase().includes(term)) ||
          (procedure.establishment_address &&
            procedure.establishment_address.toLowerCase().includes(term)) ||
          (procedure.full_address &&
            procedure.full_address.toLowerCase().includes(term)) ||
          (procedure.official_applicant_name &&
            procedure.official_applicant_name.toLowerCase().includes(term)) ||
          (procedure.street && procedure.street.toLowerCase().includes(term))
      );

      setSearchResults({
        businessProcedures: filteredBusiness,
        constructionProcedures: filteredConstruction,
      });
    } catch (error) {
      setSearchResults({ businessProcedures: [], constructionProcedures: [] });
    } finally {
      setIsSearching(false);
    }
  };

  useEffect(() => {
    if (!searchTerm.trim()) {
      setSearchResults(null);
    }
  }, [searchTerm]);

  const continueWithClientAPI = async (procedure: AnyProcedureData) => {
    if (!procedure.folio || !authToken) return;

    try {
      const encodedFolio = btoa(procedure.folio);
      const response = await fetch(`/v1/procedures/continue/${encodedFolio}`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      navigate(`/procedures/${procedure.folio}/continue`);
    } catch (error) {
      // Handle navigation error silently
    }
  };

  const formatDate = (dateString: string | null | undefined) => {
    if (!dateString) return '--';
    try {
      return new Date(dateString).toLocaleDateString('es-MX', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      });
    } catch {
      return '--';
    }
  };

  const getStatusVariant = (status: string | null | undefined) => {
    switch (status) {
      case 'approved':
        return 'success' as const;
      case 'in_review':
        return 'warning' as const;
      case 'rejected':
        return 'destructive' as const;
      case 'pending_review':
        return 'secondary' as const;
      default:
        return 'secondary' as const;
    }
  };

  const getStatusText = (status: string | null | undefined) => {
    switch (status) {
      case 'approved':
        return tProcedures('status.approved');
      case 'in_review':
        return tProcedures('status.inProgress');
      case 'rejected':
        return tProcedures('status.rejected');
      case 'pending_review':
        return tProcedures('status.pending');
      default:
        return tProcedures('status.noStatus');
    }
  };

  const filterProcedures = (procedures: any[], searchTerm: string) => {
    if (!searchTerm.trim()) return procedures;

    const term = searchTerm.toLowerCase().trim();
    return procedures.filter(
      procedure =>
        (procedure.folio && procedure.folio.toLowerCase().includes(term)) ||
        (procedure.establishment_address &&
          procedure.establishment_address.toLowerCase().includes(term)) ||
        (procedure.full_address &&
          procedure.full_address.toLowerCase().includes(term)) ||
        (procedure.official_applicant_name &&
          procedure.official_applicant_name.toLowerCase().includes(term)) ||
        (procedure.municipality_name &&
          procedure.municipality_name.toLowerCase().includes(term)) ||
        (procedure.street && procedure.street.toLowerCase().includes(term)) ||
        (procedure.scian_code &&
          procedure.scian_code.toLowerCase().includes(term)) ||
        (procedure.scian_name &&
          procedure.scian_name.toLowerCase().includes(term))
    );
  };

  const filteredBusinessProcedures = searchResults
    ? searchResults.businessProcedures
    : filterProcedures(businessProcedures, searchTerm);
  const filteredConstructionProcedures = searchResults
    ? searchResults.constructionProcedures
    : filterProcedures(constructionProcedures, searchTerm);

  const businessTableData = useMemo(() => {
    return filteredBusinessProcedures.map(procedure => {
      let address = '--';
      if (procedure.establishment_address?.trim()) {
        address = procedure.establishment_address.trim();
      } else if (procedure.street || procedure.neighborhood) {
        const parts = [procedure.street, procedure.neighborhood].filter(
          Boolean
        );
        address = parts.join(', ') || '--';
      }

      let scianInfo = '--';
      if (procedure.scian_code?.trim()) {
        scianInfo = procedure.scian_code.trim();
        if (procedure.scian_name?.trim()) {
          scianInfo += ` - ${procedure.scian_name.trim()}`;
        }
      } else if (procedure.business_line) {
        scianInfo = procedure.business_line;
      }

      return {
        id: procedure.folio || '--',
        address: address,
        location: procedure.municipality_name || '--',
        scian: scianInfo,
        createdAt: formatDate(procedure.created_at),
      };
    });
  }, [filteredBusinessProcedures, searchResults]);

  const constructionTableData = useMemo(() => {
    return filteredConstructionProcedures.map(procedure => {
      let address = '--';
      if (procedure.establishment_address) {
        address = procedure.establishment_address;
      } else if (procedure.street || procedure.neighborhood) {
        const parts = [procedure.street, procedure.neighborhood].filter(
          Boolean
        );
        address = parts.join(', ') || '--';
      }

      return {
        id: procedure.folio || '--',
        address: address,
        interestedParty: procedure.official_applicant_name || '--',
        createdAt: formatDate(procedure.created_at),
        updatedAt: formatDate(procedure.updated_at),
      };
    });
  }, [filteredConstructionProcedures, searchResults]);

  const handleViewProcedure = (procedure: AnyProcedureData) => {
    setSelectedProcedure(toProcedureData(procedure));
    setIsProcedureModalOpen(true);
  };

  const handleViewProcedureDetail = (procedure: AnyProcedureData) => {
    if (procedure.folio) {
      const encodedFolio = btoa(procedure.folio);
      navigate(`/procedures/${encodedFolio}/detail`);
    }
  };

  const handleViewFiles = (procedure: AnyProcedureData) => {
    setSelectedProcedureId(procedure.id);
    setIsFilesModalOpen(true);
  };

  const handleContinueProcedure = (procedure: any) => {
    void continueWithClientAPI(procedure);
  };

  const handleViewFilesFromModal = (procedure: any) => {
    setSelectedProcedureId(procedure.id);
    setIsFilesModalOpen(true);
  };

  const handleMoreOptions = (procedure: AnyProcedureData) => {};

  const handleSearch = async () => {
    if (searchTerm.trim()) {
      const filteredBusiness = filterProcedures(businessProcedures, searchTerm);
      const filteredConstruction = filterProcedures(
        constructionProcedures,
        searchTerm
      );

      if (filteredBusiness.length > 0 || filteredConstruction.length > 0) {
        setSearchResults({
          businessProcedures: filteredBusiness,
          constructionProcedures: filteredConstruction,
        });
      } else {
        await searchSpecificProcedures(searchTerm);
      }
    } else {
      setSearchResults(null);
    }
  };

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      handleSearch();
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm]);

  return (
    <div className="p-4">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          {tProcedures('myProcedures')}
        </h1>
      </div>

      <div className="mb-6">
        <div className="relative">
          <Search
            className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
            size={20}
          />
          <input
            type="text"
            placeholder={tProcedures('search.placeholder')}
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        {searchTerm && (
          <div className="mt-2 text-sm text-gray-600">
            {isSearching ? (
              <div className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                {tProcedures('search.searching')}
              </div>
            ) : (
              <>
                {tProcedures('tabs.tab1.label')}:{' '}
                {filteredBusinessProcedures.length} de{' '}
                {searchResults ? 'toda la BD' : businessProcedures.length} |{' '}
                {tProcedures('tabs.tab2.label')}:{' '}
                {filteredConstructionProcedures.length} de{' '}
                {searchResults ? 'toda la BD' : constructionProcedures.length}
                {searchResults && (
                  <span className="text-blue-600 ml-2">
                    ({tProcedures('search.specificDatabaseSearch')})
                  </span>
                )}
                {searchTerm.trim().match(/^(CONS|PROC|TEST)/i) && (
                  <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-md">
                    <p className="text-sm text-blue-800">
                      <strong>
                        {tProcedures('search.tips.title')} "{searchTerm}":
                      </strong>
                      {filteredBusinessProcedures.length === 0 &&
                        filteredConstructionProcedures.length > 0 && (
                          <span className="block mt-1">
                            • {tProcedures('search.tips.inConstruction')}{' '}
                            <strong>
                              "{tProcedures('search.tips.constructionTab')}"
                            </strong>{' '}
                            ({filteredConstructionProcedures.length}{' '}
                            {filteredConstructionProcedures.length !== 1
                              ? tProcedures('search.tips.results')
                              : tProcedures('search.tips.result')}
                            )
                          </span>
                        )}
                      {filteredConstructionProcedures.length === 0 &&
                        filteredBusinessProcedures.length > 0 && (
                          <span className="block mt-1">
                            • {tProcedures('search.tips.inBusiness')}{' '}
                            <strong>
                              "{tProcedures('search.tips.businessTab')}"
                            </strong>{' '}
                            ({filteredBusinessProcedures.length}{' '}
                            {filteredBusinessProcedures.length !== 1
                              ? tProcedures('search.tips.results')
                              : tProcedures('search.tips.result')}
                            )
                          </span>
                        )}
                      {filteredBusinessProcedures.length === 0 &&
                        filteredConstructionProcedures.length === 0 && (
                          <span className="block mt-1">
                            • {tProcedures('search.tips.notFound')}
                          </span>
                        )}
                    </p>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>

      <Tabs
        className="flex gap-4"
        defaultValue={tProcedures('tabs.tab1.label')}
      >
        <TabsList className="flex gap-4 w-full justify-center">
          <TabsTrigger value={tProcedures('tabs.tab1.label')}>
            {tProcedures('tabs.tab1.label')}
            {filteredBusinessProcedures.length > 0 && (
              <Badge variant="secondary" className="ml-2">
                {searchResults
                  ? filteredBusinessProcedures.length
                  : searchTerm
                    ? `${filteredBusinessProcedures.length}/${businessProcedures.length}`
                    : filteredBusinessProcedures.length}
              </Badge>
            )}
          </TabsTrigger>

          <TabsTrigger value={tProcedures('tabs.tab2.label')}>
            {tProcedures('tabs.tab2.label')}
            {filteredConstructionProcedures.length > 0 && (
              <Badge variant="secondary" className="ml-2">
                {searchResults
                  ? filteredConstructionProcedures.length
                  : searchTerm
                    ? `${filteredConstructionProcedures.length}/${constructionProcedures.length}`
                    : filteredConstructionProcedures.length}
              </Badge>
            )}
          </TabsTrigger>
        </TabsList>

        <TabsContent value={tProcedures('tabs.tab1.label')}>
          {businessProceduresAtLimit && (
            <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
              <p className="text-sm text-yellow-800">
                {tProcedures('limits.businessNote')}
                {businessProcedures.length === 100 && (
                  <span className="block mt-1">
                    {tProcedures('limits.maxReached')}
                  </span>
                )}
              </p>
            </div>
          )}
          <Table
            data={businessTableData.map(item => ({
              id: item.id,
              address: item.address,
              location: item.location,
              scian: item.scian,
              createdAt: item.createdAt,
              actions: '',
            }))}
            noDataMessage={
              searchTerm && filteredBusinessProcedures.length === 0
                ? isSearching
                  ? tProcedures('search.searchingBusiness')
                  : `${tProcedures('search.noResultsBusiness')} "${searchTerm}"`
                : tProcedures('tabs.tab1.table.noData')
            }
            columns={[
              {
                id: 'id',
                header: tProcedures('tabs.tab1.table.columns.id'),
              },
              {
                id: 'address',
                header: tProcedures('tabs.tab1.table.columns.address'),
              },
              {
                id: 'location',
                header: tProcedures('tabs.tab1.table.columns.location'),
              },
              {
                id: 'scian',
                header: tProcedures('tabs.tab1.table.columns.scian'),
              },
              {
                id: 'createdAt',
                header: tProcedures('tabs.tab1.table.columns.createdAt'),
              },
              {
                id: 'actions',
                header: tProcedures('tabs.tab1.table.columns.actions'),
                cell: ({ row }) => {
                  const procedure = filteredBusinessProcedures.find(
                    p => p.folio === row.id
                  );
                  if (!procedure) return null;

                  return (
                    <div className="flex gap-2">
                      <Button
                        variant="tertiary"
                        className="px-2 py-1"
                        title={tProcedures('actions.detail')}
                        onClick={() => handleViewProcedureDetail(procedure)}
                      >
                        <Search size={16} />
                      </Button>
                      <Button
                        variant="tertiary"
                        className="px-2 py-1"
                        title={tProcedures('actions.view')}
                        onClick={() => handleViewProcedure(procedure)}
                      >
                        <Eye size={16} />
                      </Button>
                    </div>
                  );
                },
              },
            ]}
          />
        </TabsContent>

        <TabsContent value={tProcedures('tabs.tab2.label')}>
          {constructionProceduresAtLimit && (
            <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
              <p className="text-sm text-yellow-800">
                {tProcedures('limits.constructionNote')}
                {constructionProcedures.length === 100 && (
                  <span className="block mt-1">
                    {tProcedures('limits.maxReached')}
                  </span>
                )}
              </p>
            </div>
          )}
          <Table
            data={constructionTableData.map(item => ({
              id: item.id,
              address: item.address,
              interestedParty: item.interestedParty,
              createdAt: item.createdAt,
              updatedAt: item.updatedAt,
              status: '',
              actions: '',
            }))}
            noDataMessage={
              searchTerm && filteredConstructionProcedures.length === 0
                ? isSearching
                  ? tProcedures('search.searchingConstruction')
                  : `${tProcedures('search.noResultsConstruction')} "${searchTerm}"`
                : tProcedures('tabs.tab2.table.noData')
            }
            columns={[
              {
                id: 'id',
                header: tProcedures('tabs.tab2.table.columns.id'),
              },
              {
                id: 'address',
                header: tProcedures('tabs.tab2.table.columns.address'),
              },
              {
                id: 'interestedParty',
                header: tProcedures('tabs.tab2.table.columns.interestedParty'),
              },
              {
                id: 'createdAt',
                header: tProcedures('tabs.tab2.table.columns.createdAt'),
              },
              {
                id: 'updatedAt',
                header: tProcedures('tabs.tab2.table.columns.updatedAt'),
              },
              {
                id: 'status',
                header: tProcedures('tabs.tab2.table.columns.status'),
                cell: ({ row }) => {
                  const procedure = filteredConstructionProcedures.find(
                    p => p.folio === row.id
                  );
                  return (
                    <Badge variant={getStatusVariant(procedure?.status)}>
                      {getStatusText(procedure?.status)}
                    </Badge>
                  );
                },
              },
              {
                id: 'actions',
                header: tProcedures('tabs.tab2.table.columns.actions'),
                cell: ({ row }) => {
                  const procedure = filteredConstructionProcedures.find(
                    p => p.folio === row.id
                  );
                  if (!procedure) return null;

                  return (
                    <div className="flex gap-2">
                      <Button
                        variant="tertiary"
                        className="px-2 py-1"
                        title={tProcedures('actions.detail')}
                        onClick={() => handleViewProcedureDetail(procedure)}
                      >
                        <Search size={16} />
                      </Button>
                      <Button
                        variant="tertiary"
                        className="px-2 py-1"
                        title={tProcedures('actions.view')}
                        onClick={() => handleViewProcedure(procedure)}
                      >
                        <Eye size={16} />
                      </Button>
                      <Button
                        variant="tertiary"
                        className="px-2 py-1"
                        title={tProcedures('actions.more')}
                        onClick={() => handleMoreOptions(procedure)}
                      >
                        <MoreHorizontal size={16} />
                      </Button>
                    </div>
                  );
                },
              },
            ]}
          />
        </TabsContent>
      </Tabs>

      <ProcedureModal
        isOpen={isProcedureModalOpen}
        onClose={() => {
          setIsProcedureModalOpen(false);
          setSelectedProcedure(null);
        }}
        procedure={selectedProcedure}
        onContinue={handleContinueProcedure}
        onViewFiles={handleViewFilesFromModal}
      />

      <ProcedureFilesModal
        isOpen={isFilesModalOpen}
        onClose={() => {
          setIsFilesModalOpen(false);
          setSelectedProcedureId(null);
        }}
        procedureId={selectedProcedureId}
        authToken={authToken}
      />
    </div>
  );
}
