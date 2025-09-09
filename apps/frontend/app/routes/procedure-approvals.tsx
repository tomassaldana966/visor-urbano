import type { LoaderFunctionArgs } from 'react-router';
import React, { useState } from 'react';
import { Link, useLoaderData, useSearchParams } from 'react-router';
import { useTranslation } from 'react-i18next';
import {
  AlertCircle,
  AlertTriangle,
  Award,
  Building,
  CheckCircle,
  CheckSquare,
  Clock,
  Construction,
  Edit,
  Eye,
  FileCheck,
  FileText,
  Search,
  Upload,
  XCircle,
  Gavel,
  X,
  Paperclip,
} from 'lucide-react';

import { Button } from '../components/Button/Button';
import { IssueLicenseModal } from '../components/IssueLicenseModal/IssueLicenseModal';
import { Select, Option } from '../components/Select/Select';
import { Modal } from '../components/Modal/Modal';
import {
  checkDirectorPermissions,
  checkElaborateResolutionPermissions,
  checkEnhancedElaborateResolutionPermissions,
} from '../utils/auth/director';
import { encodeFolio } from '../utils/folio';
import type {
  ProcedureApproval,
  LoaderData,
  TabFilter,
  ActionItem,
  StatusDisplay,
} from '../types/procedure-approvals';
import type { AuthUser } from '../utils/auth/auth.server';
import { requestAPI } from '../utils/api/base';

export const handle = {
  title: 'procedureApprovals:title',
  breadcrumb: 'procedureApprovals:breadcrumb',
};

export async function loader({
  request,
}: LoaderFunctionArgs): Promise<LoaderData> {
  const { getProcedures } = await import('../utils/api/api.server');
  const { getAccessToken, requireAuth } = await import(
    '../utils/auth/auth.server'
  );
  const { checkProcedureApprovalPermissions, checkDirectorPermissions } =
    await import('../utils/auth/director');

  const user = await requireAuth(request);
  const accessToken = await getAccessToken(request);

  if (!user.role_id || user.role_id <= 1) {
    throw new Response('procedureApprovals:errors.accessDenied', {
      status: 403,
    });
  }

  const hasProcedureApprovalPermissions =
    checkProcedureApprovalPermissions(user);

  if (!hasProcedureApprovalPermissions) {
    throw new Response('procedureApprovals:errors.insufficientPermissions', {
      status: 403,
    });
  }

  if (!accessToken) {
    throw new Response('procedureApprovals:errors.tokenRequired', {
      status: 401,
    });
  }

  const url = new URL(request.url);
  const page = parseInt(url.searchParams.get('page') || '1');
  const per_page = parseInt(url.searchParams.get('per_page') || '20');
  const tab_filter = url.searchParams.get('tab_filter') as TabFilter;
  const folio = url.searchParams.get('folio') || undefined;

  try {
    const allProceduresParams = {
      per_page: 1000,
    };
    const allProcedures = await getProcedures(accessToken, allProceduresParams);

    const allProceduresForCounts = allProcedures.filter(
      procedure => procedure.municipality_id === user.municipality_id
    );

    const filteredParams: Record<string, unknown> = {
      folio,
      per_page: 1000,
    };

    const allFilteredProcedures = await getProcedures(
      accessToken,
      filteredParams
    );

    let procedureApprovals = allFilteredProcedures.filter(
      procedure => procedure.municipality_id === user.municipality_id
    );

    if (tab_filter) {
      procedureApprovals = procedureApprovals.filter(procedure => {
        switch (tab_filter) {
          case 'business_licenses':
            return (
              procedure.procedure_type?.includes('business') ||
              procedure.procedure_type?.includes('comercial')
            );
          case 'permits_building_license':
            return (
              procedure.procedure_type?.includes('building') ||
              procedure.procedure_type?.includes('construccion')
            );
          case 'en_revisiones':
            return (
              procedure.status === 1 && // pending_review status
              procedure.sent_to_reviewers === 1
            );
          case 'prevenciones':
            return procedure.status === 3; // prevention status
          case 'desechados':
            return procedure.status === 2; // rejected status (corrected from 3)
          case 'aprobados':
            return procedure.status === 2 && !procedure.license_pdf; // approved but no license issued
          case 'en_ventanilla':
            return (
              procedure.step_one === 1 &&
              procedure.step_two === 1 &&
              !procedure.director_approval
            );
          default:
            return true;
        }
      });
    }

    const startIndex = (page - 1) * per_page;
    const endIndex = startIndex + per_page;
    const paginatedProcedures = procedureApprovals.slice(startIndex, endIndex);

    return {
      user,
      procedureApprovals: paginatedProcedures,
      allProceduresForCounts,
      accessToken,
      pagination: {
        page,
        per_page,
        total: procedureApprovals.length,
      },
      filters: {
        tab_filter,
        folio,
      },
    };
  } catch (error) {
    if (
      error instanceof Error &&
      (error.message.includes('401') || error.message.includes('Unauthorized'))
    ) {
      throw new Response('procedureApprovals:errors.authenticationExpired', {
        status: 401,
      });
    }

    throw new Response('procedureApprovals:errors.loadError', {
      status: 500,
    });
  }
}

const getAvailableActions = (
  procedure: ProcedureApproval,
  user: AuthUser | null,
  onIssueLicense?: (folio: string) => void,
  onResolution?: (folio: string) => void,
  t?: (key: string) => string
): ActionItem[] => {
  const actions = [];

  actions.push({
    type: 'view_detail',
    icon: <Eye className="h-4 w-4" />,
    label: t ? t('procedureApprovals:actionLabels.viewDetail') : 'Ver detalle',
    variant: 'secondary' as const,
    href: `/procedures/${encodeFolio(procedure.folio || '')}/detail`,
  });

  const enhancedPermissions = checkEnhancedElaborateResolutionPermissions(
    procedure,
    user
  );

  if (enhancedPermissions.canElaborate) {
    actions.push({
      type: 'resolution',
      icon: <Gavel className="h-4 w-4" />,
      label: t ? t('procedureApprovals:actionLabels.resolution') : 'Resolución',
      variant: 'primary' as const,
      action: () => onResolution && onResolution(procedure.folio || ''),
    });
  }

  if (
    checkDirectorPermissions(user) &&
    (procedure.status === 1 ||
      procedure.status === 2 ||
      procedure.status === 4 ||
      procedure.director_approval === 1) &&
    !procedure.license_pdf
  ) {
    actions.push({
      type: 'issue_license',
      icon: <Award className="h-4 w-4" />,
      label: t
        ? t('procedureApprovals:actionLabels.issueLicense')
        : 'Emitir licencia',
      variant: 'primary' as const,
      action: () => onIssueLicense && onIssueLicense(procedure.folio || ''),
    });
  }

  if (procedure.license_pdf) {
    actions.push({
      type: 'view_license',
      icon: <FileCheck className="h-4 w-4" />,
      label: t
        ? t('procedureApprovals:actionLabels.viewLicense')
        : 'Ver licencia',
      variant: 'secondary' as const,
      isCustom: true,
      procedure: procedure,
    });
  }

  return actions;
};

const ApprovalCard = ({
  approval,
  user,
  t,
  onIssueLicense,
  onResolution,
}: {
  approval: ProcedureApproval;
  user: AuthUser | null;
  t: (key: string, options?: Record<string, unknown>) => string;
  onIssueLicense?: (folio: string) => void;
  onResolution?: (folio: string) => void;
}) => {
  const [downloading, setDownloading] = useState(false);

  const handleDownloadLicense = async () => {
    if (!approval.license_pdf) {
      return;
    }

    try {
      setDownloading(true);
      const API_URL =
        (window as { ENV?: { API_URL?: string } }).ENV?.API_URL ||
        'http://localhost:8000';
      const fullUrl = approval.license_pdf.startsWith('http')
        ? approval.license_pdf
        : `${API_URL}${approval.license_pdf.startsWith('/') ? '' : '/'}${approval.license_pdf}`;

      const response = await fetch(fullUrl);

      if (!response.ok) {
        throw new Error(t('procedureApprovals:license.downloadError'));
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `license-${approval.folio || 'unknown'}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      const API_URL =
        (window as { ENV?: { API_URL?: string } }).ENV?.API_URL ||
        'http://localhost:8000';
      const fullUrl = approval.license_pdf.startsWith('http')
        ? approval.license_pdf
        : `${API_URL}${approval.license_pdf.startsWith('/') ? '' : '/'}${approval.license_pdf}`;
      window.open(fullUrl, '_blank');
    } finally {
      setDownloading(false);
    }
  };
  const getStatusDisplay = (): StatusDisplay => {
    switch (approval.status) {
      case 1:
        return {
          label: t('procedureApprovals:statusLabels.pendingReview'),
          color: 'text-blue-600',
          icon: <Clock className="h-4 w-4" />,
        };
      case 2:
        return {
          label: t('procedureApprovals:statusLabels.approved'),
          color: 'text-green-600',
          icon: <CheckCircle className="h-4 w-4" />,
        };
      case 3:
        return {
          label: t('procedureApprovals:statusLabels.rejected'),
          color: 'text-red-600',
          icon: <XCircle className="h-4 w-4" />,
        };
      case 4:
        return {
          label: t('procedureApprovals:statusLabels.approvedByDirector'),
          color: 'text-green-600',
          icon: <CheckCircle className="h-4 w-4" />,
        };
      case 7:
      case 8:
      case 9:
        return {
          label: t('procedureApprovals:statusLabels.licenseIssued'),
          color: 'text-green-600',
          icon: <Award className="h-4 w-4" />,
        };
      default:
        if (
          approval.director_approval === 1 &&
          (approval.sent_to_reviewers === 1 ||
            approval.step_one === 1 ||
            approval.step_two === 1)
        ) {
          return {
            label: t('procedureApprovals:statusLabels.approved'),
            color: 'text-green-600',
            icon: <CheckCircle className="h-4 w-4" />,
          };
        } else if (approval.sent_to_reviewers === 1) {
          return {
            label: t('procedureApprovals:statusLabels.inReview'),
            color: 'text-blue-600',
            icon: <AlertCircle className="h-4 w-4" />,
          };
        } else {
          return {
            label: t('procedureApprovals:statusLabels.new'),
            color: 'text-gray-600',
            icon: <Clock className="h-4 w-4" />,
          };
        }
    }
  };

  const status = getStatusDisplay();
  const actions = getAvailableActions(
    approval,
    user,
    onIssueLicense,
    onResolution,
    t
  );

  return (
    <tr className="border-b border-gray-200 hover:bg-gray-50">
      <TableCell fontMedium whitespaceNowrap truncate>
        {approval.folio}
      </TableCell>
      <TableCell className="min-w-48" truncate>
        {[approval.street, approval.exterior_number]
          .filter(Boolean)
          .join(' ') || t('procedureApprovals:notAvailable')}
      </TableCell>
      <TableCell whitespaceNowrap truncate>
        {approval.municipality_name || t('procedureApprovals:notAvailable')}
      </TableCell>
      <TableCell
        className="w-32 lg:w-40 max-w-xs whitespace-normal break-words leading-relaxed"
        title={
          approval.scian_code
            ? `${approval.scian_code}${approval.scian_name ? ` - ${approval.scian_name}` : ''}`
            : approval.scian_name ||
              approval.business_line ||
              t('procedureApprovals:notAvailable')
        }
      >
        {approval.scian_code
          ? `${approval.scian_code}${approval.scian_name ? ` - ${approval.scian_name}` : ''}`
          : approval.scian_name ||
            approval.business_line ||
            t('procedureApprovals:notAvailable')}
      </TableCell>
      <TableCell whitespaceNowrap truncate>
        {approval.sent_to_reviewers_date || approval.created_at
          ? new Date(
              approval.sent_to_reviewers_date || approval.created_at!
            ).toLocaleDateString('es-MX')
          : t('procedureApprovals:notAvailable')}
      </TableCell>
      <TableCell whitespaceNowrap>
        <div className={`flex items-center space-x-1 ${status.color}`}>
          {status.icon}
          <span className="text-xs font-medium truncate">{status.label}</span>
        </div>
      </TableCell>
      <TableCell whitespaceNowrap fontMedium>
        <div className="flex space-x-1">
          {actions.map((action, index) => {
            if (action.type === 'view_license' && action.isCustom) {
              return (
                <button
                  key={index}
                  onClick={e => {
                    e.preventDefault();
                    e.stopPropagation();
                    handleDownloadLicense();
                  }}
                  disabled={downloading}
                  className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-9 px-3"
                  title={action.label}
                >
                  {action.icon}
                </button>
              );
            }

            if (action.href) {
              return (
                <Button
                  key={index}
                  variant={action.variant}
                  size="sm"
                  asChild
                  title={action.label}
                >
                  <Link to={action.href}>{action.icon}</Link>
                </Button>
              );
            } else {
              return (
                <Button
                  key={index}
                  variant={action.variant}
                  size="sm"
                  title={action.label}
                  onClick={e => {
                    e.preventDefault();
                    e.stopPropagation();
                    action.action && action.action();
                  }}
                >
                  {action.icon}
                </Button>
              );
            }
          })}
        </div>
      </TableCell>
    </tr>
  );
};

interface TableCellProps {
  children: React.ReactNode;
  className?: string;
  truncate?: boolean;
  whitespaceNowrap?: boolean;
  fontMedium?: boolean;
  title?: string;
}

function TableCell({
  children,
  className = '',
  truncate = false,
  whitespaceNowrap = false,
  fontMedium = false,
  title,
}: TableCellProps) {
  const baseClasses = 'px-3 py-4 text-sm text-gray-900';
  const conditionalClasses = [];
  if (whitespaceNowrap) conditionalClasses.push('whitespace-nowrap');
  if (fontMedium) conditionalClasses.push('font-medium');
  const cellClasses = [baseClasses, ...conditionalClasses, className]
    .filter(Boolean)
    .join(' ');

  const content = truncate ? (
    <div className="truncate" title={title}>
      {children}
    </div>
  ) : (
    children
  );

  return <td className={cellClasses}>{content}</td>;
}

export default function ProcedureApprovals() {
  const {
    user,
    procedureApprovals,
    allProceduresForCounts,
    accessToken,
    pagination,
    filters,
  } = useLoaderData<LoaderData>();
  const [searchParams, setSearchParams] = useSearchParams();
  const { t } = useTranslation(['procedureApprovals', 'common']);
  const [searchFolio, setSearchFolio] = useState(filters.folio || '');
  const [issueLicenseModal, setIssueLicenseModal] = useState({
    isOpen: false,
    folio: '',
  });
  const [resolutionModal, setResolutionModal] = useState({
    isOpen: false,
    folio: '',
  });

  const tabs = [
    {
      key: 'all',
      label: t('procedureApprovals:tabs.all'),
      icon: <FileText className="h-4 w-4" />,
      count: allProceduresForCounts.length,
    },
    {
      key: 'business_licenses',
      label: t('procedureApprovals:tabs.businessLicenses'),
      icon: <Building className="h-4 w-4" />,
      count: allProceduresForCounts.filter(
        p =>
          p.procedure_type?.includes('business') ||
          p.procedure_type?.includes('comercial')
      ).length,
    },
    {
      key: 'permits_building_license',
      label: t('procedureApprovals:tabs.buildingLicenses'),
      icon: <Construction className="h-4 w-4" />,
      count: allProceduresForCounts.filter(
        p =>
          p.procedure_type?.includes('building') ||
          p.procedure_type?.includes('construccion')
      ).length,
    },
    {
      key: 'en_revisiones',
      label: t('procedureApprovals:tabs.inReview'),
      icon: <AlertCircle className="h-4 w-4" />,
      count: allProceduresForCounts.filter(
        p =>
          p.status === 1 && // pending_review status (consistent with filter)
          p.sent_to_reviewers === 1
      ).length,
    },
    {
      key: 'prevenciones',
      label: t('procedureApprovals:tabs.preventions'),
      icon: <AlertTriangle className="h-4 w-4" />,
      count: allProceduresForCounts.filter(p => p.status === 3).length, // prevention
    },
    {
      key: 'desechados',
      label: t('procedureApprovals:tabs.rejected'),
      icon: <XCircle className="h-4 w-4" />,
      count: allProceduresForCounts.filter(p => p.status === 2).length, // rejected (corrected)
    },
    {
      key: 'aprobados',
      label: t('procedureApprovals:tabs.approved'),
      icon: <CheckCircle className="h-4 w-4" />,
      count: allProceduresForCounts.filter(
        p => p.status === 2 && !p.license_pdf
      ).length,
    },
    {
      key: 'en_ventanilla',
      label: t('procedureApprovals:tabs.atWindow'),
      icon: <CheckSquare className="h-4 w-4" />,
      count: allProceduresForCounts.filter(
        p => p.step_one === 1 && p.step_two === 1 && !p.director_approval
      ).length,
    },
  ];

  const handleTabChange = (tabKey: string) => {
    const newSearchParams = new URLSearchParams(searchParams);
    if (tabKey === 'all') {
      newSearchParams.delete('tab_filter');
    } else {
      newSearchParams.set('tab_filter', tabKey);
    }
    newSearchParams.set('page', '1');
    setSearchParams(newSearchParams);
  };

  const handleSearch = () => {
    const newSearchParams = new URLSearchParams(searchParams);
    if (searchFolio.trim()) {
      newSearchParams.set('folio', searchFolio.trim());
    } else {
      newSearchParams.delete('folio');
    }
    newSearchParams.set('page', '1');
    setSearchParams(newSearchParams);
  };

  const handlePreviousPage = () => {
    if (pagination.page > 1) {
      const newSearchParams = new URLSearchParams(searchParams);
      newSearchParams.set('page', (pagination.page - 1).toString());
      setSearchParams(newSearchParams);
    }
  };

  const handleNextPage = () => {
    const totalPages = Math.ceil(pagination.total / pagination.per_page);
    if (pagination.page < totalPages) {
      const newSearchParams = new URLSearchParams(searchParams);
      newSearchParams.set('page', (pagination.page + 1).toString());
      setSearchParams(newSearchParams);
    }
  };

  const handleIssueLicense = (folio: string) => {
    setIssueLicenseModal({ isOpen: true, folio });
  };

  const handleResolution = (folio: string) => {
    setResolutionModal({ isOpen: true, folio });
  };

  const handleCloseModal = () => {
    setIssueLicenseModal({ isOpen: false, folio: '' });
  };

  const handleCloseResolutionModal = () => {
    setResolutionModal({ isOpen: false, folio: '' });
  };

  const handleLicenseIssued = () => {
    window.location.reload();
  };

  const handleResolutionSubmitted = () => {
    window.location.reload();
  };

  return (
    <div className="space-y-6 px-3 py-6 max-w-full overflow-hidden lg:px-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {t('procedureApprovals:title')}
          </h1>
          <p className="text-gray-600 mt-1">
            {t('procedureApprovals:subtitle')}
          </p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="flex">
          <input
            type="text"
            placeholder={t('procedureApprovals:searchPlaceholder')}
            value={searchFolio}
            onChange={e => setSearchFolio(e.target.value)}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            onKeyPress={e => e.key === 'Enter' && handleSearch()}
          />
          <Button
            onClick={handleSearch}
            variant="primary"
            className="rounded-l-none"
          >
            <Search className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div className="border-b border-gray-200 p-4">
          <div className="flex flex-col sm:flex-row sm:items-center gap-4">
            <div className="flex-1">
              <Select
                label={t('procedureApprovals:filter.category')}
                placeholder={t('procedureApprovals:filter.selectCategory')}
                value={filters.tab_filter || 'all'}
                onValueChange={handleTabChange}
              >
                {tabs.map(tab => (
                  <Option key={tab.key} value={tab.key}>
                    <div className="flex items-center justify-between w-full">
                      <div className="flex items-center space-x-2">
                        {tab.icon}
                        <span>{tab.label}</span>
                      </div>
                      {tab.count > 0 && (
                        <span className="bg-gray-100 text-gray-600 py-0.5 px-2 rounded-full text-xs">
                          {tab.count}
                        </span>
                      )}
                    </div>
                  </Option>
                ))}
              </Select>
            </div>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                  {t('procedureApprovals:tableHeaders.folio')}
                </th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-48">
                  {t('procedureApprovals:tableHeaders.address')}
                </th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                  {t('procedureApprovals:tableHeaders.municipality')}
                </th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32 lg:w-40 max-w-xs">
                  {t('procedureApprovals:tableHeaders.scian')}
                </th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                  {t('procedureApprovals:tableHeaders.entryDate')}
                </th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                  {t('procedureApprovals:tableHeaders.status')}
                </th>
                <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                  {t('procedureApprovals:tableHeaders.actions')}
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {procedureApprovals.length > 0 ? (
                procedureApprovals.map(approval => (
                  <ApprovalCard
                    key={approval.id}
                    approval={approval}
                    user={user}
                    t={t}
                    onIssueLicense={handleIssueLicense}
                    onResolution={handleResolution}
                  />
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center">
                    <div className="flex flex-col items-center">
                      <FileText className="h-12 w-12 text-gray-400 mb-4" />
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        {t('procedureApprovals:emptyState.title')}
                      </h3>
                      <p className="text-gray-600">
                        {t('procedureApprovals:emptyState.description')}
                      </p>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {pagination.total > pagination.per_page && (
        <div className="flex justify-center">
          <div className="flex space-x-2 items-center">
            <Button
              variant="secondary"
              size="sm"
              disabled={pagination.page <= 1}
              onClick={handlePreviousPage}
            >
              {t('common:pagination.previous')}
            </Button>
            <span className="px-3 py-2 text-sm text-gray-600">
              {t('common:pagination.page')} {pagination.page}{' '}
              {t('common:pagination.of')}{' '}
              {Math.ceil(pagination.total / pagination.per_page)}
            </span>
            <Button
              variant="secondary"
              size="sm"
              disabled={
                pagination.page >=
                Math.ceil(pagination.total / pagination.per_page)
              }
              onClick={handleNextPage}
            >
              {t('common:pagination.next')}
            </Button>
          </div>
        </div>
      )}

      {pagination.total > 0 && (
        <div className="flex justify-center">
          <span className="text-sm text-gray-500">
            {t('procedureApprovals:showingResults', {
              count: procedureApprovals.length,
              total: pagination.total,
            })}
          </span>
        </div>
      )}

      <IssueLicenseModal
        isOpen={issueLicenseModal.isOpen}
        onClose={handleCloseModal}
        folio={issueLicenseModal.folio}
        authToken={accessToken}
        municipalityId={user?.municipality_id}
        onLicenseIssued={handleLicenseIssued}
      />

      <ResolutionModal
        isOpen={resolutionModal.isOpen}
        onClose={handleCloseResolutionModal}
        folio={resolutionModal.folio}
        authToken={accessToken}
        onResolutionSubmitted={handleResolutionSubmitted}
      />
    </div>
  );
}

interface ResolutionModalProps {
  isOpen: boolean;
  onClose: () => void;
  folio: string;
  authToken?: string;
  onResolutionSubmitted?: () => void;
}

function ResolutionModal({
  isOpen,
  onClose,
  folio,
  authToken,
  onResolutionSubmitted,
}: ResolutionModalProps) {
  const { t } = useTranslation(['procedureApprovals', 'common']);
  const [resolutionType, setResolutionType] = useState<
    'approve' | 'prevent' | 'reject' | null
  >(null);
  const [details, setDetails] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  React.useEffect(() => {
    if (isOpen) {
      setResolutionType(null);
      setDetails('');
      setSelectedFile(null);
      setError(null);
      setShowSuccess(false);
    }
  }, [isOpen]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setError(t('procedureApprovals:resolution.errors.fileTooLarge'));
        return;
      }
      const allowedTypes = [
        'application/pdf',
        'image/jpeg',
        'image/png',
        'image/jpg',
      ];
      if (!allowedTypes.includes(file.type)) {
        setError(t('procedureApprovals:resolution.errors.invalidFileType'));
        return;
      }
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleSubmit = async () => {
    if (!resolutionType) {
      setError(t('procedureApprovals:resolution.typeRequired'));
      return;
    }

    if (!details.trim()) {
      setError(t('procedureApprovals:resolution.detailsRequired'));
      return;
    }

    if (!authToken) {
      setError(t('procedureApprovals:resolution.errors.authTokenRequired'));
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      let fileUrl = '';

      if (selectedFile) {
        const formData = new FormData();
        formData.append('files', selectedFile);

        const uploadResponse = await fetch(
          `${API_URL}/v1/dependency_reviews/upload_files/${btoa(folio)}`,
          {
            method: 'POST',
            headers: {
              Authorization: `Bearer ${authToken}`,
            },
            body: formData,
          }
        );

        if (!uploadResponse.ok) {
          throw new Error(
            t('procedureApprovals:resolution.errors.uploadError')
          );
        }

        const uploadResult = await uploadResponse.json();
        if (uploadResult?.files?.length > 0) {
          fileUrl = uploadResult.files[uploadResult.files.length - 1];
        }
      }

      const resolutionStatus =
        resolutionType === 'approve' ? 1 : resolutionType === 'prevent' ? 3 : 2;
      const resolutionData = {
        resolution_status: resolutionStatus,
        resolution_text: details,
        resolution_file: fileUrl || null,
      };

      const resolutionResponse = await fetch(
        `${API_URL}/v1/dependency_reviews/update_resolution/${btoa(folio)}`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${authToken}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(resolutionData),
        }
      );

      if (!resolutionResponse.ok) {
        throw new Error(
          t('procedureApprovals:resolution.errors.submissionError')
        );
      }

      setShowSuccess(true);
      setTimeout(() => {
        onResolutionSubmitted?.();
        onClose();
      }, 2000);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : t('procedureApprovals:resolution.errors.submissionError')
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  if (showSuccess) {
    return (
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        title={t('procedureApprovals:resolution.successTitle')}
        size="md"
      >
        <div className="text-center py-6">
          <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {t('procedureApprovals:resolution.successMessage')}
          </h3>
          <p className="text-gray-600">
            {t('procedureApprovals:resolution.successDescription')}
          </p>
        </div>
      </Modal>
    );
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={t('procedureApprovals:resolution.title')}
      size="lg"
    >
      <div className="space-y-6">
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <Gavel className="h-4 w-4 text-green-500" />
          <span>Folio: {folio}</span>
        </div>
        <div className="space-y-3">
          <label className="block text-sm font-medium text-gray-700">
            {t('procedureApprovals:resolution.type')}
          </label>
          <div className="space-y-2">
            {[
              {
                value: 'approve',
                label: t('procedureApprovals:resolution.types.approve'),
                color: 'green',
              },
              {
                value: 'prevent',
                label: t('procedureApprovals:resolution.types.prevent'),
                color: 'yellow',
              },
              {
                value: 'reject',
                label: t('procedureApprovals:resolution.types.reject'),
                color: 'red',
              },
            ].map(option => (
              <label key={option.value} className="flex items-center">
                <input
                  type="radio"
                  name="resolutionType"
                  value={option.value}
                  checked={resolutionType === option.value}
                  onChange={e => setResolutionType(e.target.value as any)}
                  className={`h-4 w-4 text-${option.color}-600 focus:ring-${option.color}-500 border-gray-300`}
                />
                <span className="ml-2 text-sm text-gray-700">
                  {option.label}
                </span>
              </label>
            ))}
          </div>
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">
            {t('procedureApprovals:resolution.details')}
          </label>
          <textarea
            value={details}
            onChange={e => setDetails(e.target.value)}
            placeholder={t('procedureApprovals:resolution.detailsPlaceholder')}
            className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            disabled={isSubmitting}
          />
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">
            {t('procedureApprovals:resolution.attachFile')}
          </label>
          <div className="flex items-center space-x-3">
            <Paperclip className="h-5 w-5 text-green-500" />
            <input
              type="file"
              onChange={handleFileChange}
              accept=".pdf,.jpg,.jpeg,.png"
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
              disabled={isSubmitting}
            />
          </div>
          {selectedFile && (
            <p className="text-sm text-gray-600">
              {t('procedureApprovals:resolution.fileSelected')}{' '}
              {selectedFile.name} (
              {(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
            </p>
          )}
          <p className="text-xs text-gray-500">
            {t('procedureApprovals:resolution.fileFormats')}
          </p>
        </div>
        {error && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <XCircle className="h-5 w-5 text-red-400" />
              <div className="ml-3">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}
        <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
          <Button variant="secondary" onClick={onClose} disabled={isSubmitting}>
            {t('procedureApprovals:resolution.cancel')}
          </Button>
          <Button
            variant="primary"
            onClick={handleSubmit}
            disabled={isSubmitting || !resolutionType || !details.trim()}
          >
            {isSubmitting ? (
              <>
                <Clock className="h-4 w-4 mr-2 animate-spin" />
                {t('procedureApprovals:resolution.sending')}
              </>
            ) : (
              t('procedureApprovals:resolution.submit')
            )}
          </Button>
        </div>
      </div>
    </Modal>
  );
}
