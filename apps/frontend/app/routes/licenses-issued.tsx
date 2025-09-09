import type { LoaderFunctionArgs, ActionFunctionArgs } from 'react-router';
import {
  useLoaderData,
  Link,
  useFetcher,
  useRevalidator,
  useNavigate,
} from 'react-router';
import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  checkDirectorPermissions,
  checkAdminPermissions,
} from '../utils/auth/director';
import {
  downloadLicensePdf,
  exportBusinessLicenses,
  getLicenseStatusHistory,
  type BusinessLicense,
} from '../utils/api/api.client';

// Import server-side functions from server-specific file
export { loader, action } from './licenses-issued.server';
import type { loader } from './licenses-issued.server';

// Interface for the mapped license data used in the UI
interface MappedLicense {
  // Core BusinessLicense properties
  id?: number;
  license_folio: string;
  commercial_activity: string;
  industry_classification_code: string;
  municipality_id?: number;
  license_status?: string | null;
  license_type?: string | null;
  payment_status?: number;
  scanned_pdf?: string | null;
  opening_time?: string;
  closing_time?: string;
  reason?: string | null;
  reason_file?: string | null;
  status_change_date?: string | null;
  secondary_folio?: string | null;

  // Owner information from BusinessLicense
  owner?: string;
  owner_last_name_p?: string | null;
  owner_last_name_m?: string | null;
  // Contact information
  owner_phone?: string | null;
  owner_email?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
  authorized_area?: string;
  national_id?: string | null;
  license_year?: number;
  license_category?: number | null;

  // Additional data from procedure joins
  procedure_applicant_name?: string | null;
  procedure_street?: string | null;
  procedure_neighborhood?: string | null;
  procedure_scian_name?: string | null;
  procedure_establishment_name?: string | null;
  procedure_establishment_address?: string | null;
  procedure_establishment_phone?: string | null;
  user_email?: string | null; // Email del usuario que hizo el trámite

  // New establishment fields stored directly in BusinessLicense
  establishment_name?: string | null;
  establishment_address?: string | null;
  establishment_phone?: string | null;
  establishment_email?: string | null;
  procedure_id?: number | null;
  requirements_query_id?: number | null;

  // Mapped properties for UI display
  business_name: string;
  business_line: string;
  owner_first_name: string;
  issue_date: string;
  street: string;
  neighborhood: string;
}
import {
  FileText,
  User,
  Calendar,
  MapPin,
  Eye,
  Download,
  Edit,
  DollarSign,
  Building,
  Clock,
  Search,
  Filter,
  ExternalLink,
  CheckCircle,
  XCircle,
  AlertCircle,
  ChevronRight,
  ChevronDown,
  MoreVertical,
  RotateCcw,
  TrendingUp,
} from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

export const handle = {
  title: 'nav:issuedLicenses',
  breadcrumb: 'nav:issuedLicenses',
};

// License Row Component with expandable functionality
function LicenseRow({
  license,
  index,
  t,
  authToken,
  revalidator,
}: {
  license: MappedLicense; // Using the MappedLicense interface
  index: number;
  t: any;
  authToken: string;
  revalidator: any;
}) {
  const fetcher = useFetcher();
  const navigate = useNavigate();
  const [isExpanded, setIsExpanded] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showNoReceiptModal, setShowNoReceiptModal] = useState(false);
  const [showNoLicenseModal, setShowNoLicenseModal] = useState(false);
  const [isPaid, setIsPaid] = useState(license.payment_status === 1);
  const [paymentReceipt, setPaymentReceipt] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [selectedStatus, setSelectedStatus] = useState('');
  const [statusReason, setStatusReason] = useState('');
  const [statusFile, setStatusFile] = useState<File | null>(null);
  const [updatingStatus, setUpdatingStatus] = useState(false);
  const [showHistoryModal, setShowHistoryModal] = useState(false);
  const [historyData, setHistoryData] = useState<any>(null);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const handlePaymentToggle = async (newPaymentStatus: boolean) => {
    if (newPaymentStatus && !isPaid) {
      // If trying to mark as paid, show modal to upload receipt
      setShowPaymentModal(true);
    } else if (!newPaymentStatus && isPaid) {
      const formData = new FormData();
      formData.append('_intent', 'updatePayment');
      formData.append('licenseFolio', license.license_folio);
      formData.append('paymentStatus', '0'); // Mark as unpaid

      fetcher.submit(formData, { method: 'POST' });
    }
  };

  const handlePaymentSubmit = async () => {
    if (!paymentReceipt) return;

    setUploading(true);

    const formData = new FormData();
    formData.append('_intent', 'uploadReceipt');
    formData.append('licenseFolio', license.license_folio);
    formData.append('receiptFile', paymentReceipt);

    fetcher.submit(formData, {
      method: 'POST',
      encType: 'multipart/form-data',
    });

    setIsPaid(true);
    setShowPaymentModal(false);
    setPaymentReceipt(null);
    setUploading(false);
  };

  // Handle fetcher responses
  useEffect(() => {
    if (fetcher.data && fetcher.state === 'idle') {
      if (fetcher.data.success) {
        if (fetcher.data.action === 'updatePayment') {
          // Payment status updated successfully
          setIsPaid(fetcher.data.paymentStatus === 1);
        } else if (fetcher.data.action === 'uploadReceipt') {
          // Receipt uploaded and payment marked as paid
          setIsPaid(true);
          setShowPaymentModal(false);
          setPaymentReceipt(null);
        }
        // Revalidate data to refresh the entire list
        revalidator.revalidate();
      } else if (fetcher.data.error) {
        // Handle error - you could add toast notification here
        console.error('Payment update error:', fetcher.data.error);
      }
      setUploading(false);
    }
  }, [fetcher.data, fetcher.state, revalidator]);

  const handleDownloadLicense = async () => {
    if (!license.scanned_pdf) {
      setShowNoLicenseModal(true);
      return;
    }

    try {
      setDownloading(true);
      const blob = await downloadLicensePdf(authToken, license.license_folio);

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `license_${license.license_folio}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading license:', error);
      setShowNoLicenseModal(true);
    } finally {
      setDownloading(false);
    }
  };

  const handleViewHistory = async () => {
    try {
      setLoadingHistory(true);
      const history = await getLicenseStatusHistory(
        authToken,
        license.license_folio
      );

      setHistoryData(history);
      setShowHistoryModal(true);
    } catch (error) {
      console.error('Error loading license history:', error);
      // Could add toast notification here
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleViewDetail = () => {
    // Encode the folio in base64
    const encodedFolio = btoa(license.license_folio);
    // Navigate to the procedure detail page
    navigate(`/procedures/${encodedFolio}/detail`);
  };

  const getPaymentStatusBadge = (status: string | number) => {
    // Handle both string and number status
    const isPaid =
      status === 1 ||
      status === '1' ||
      (typeof status === 'string' && status.toLowerCase() === 'pagado');
    const isPending =
      status === 0 ||
      status === '0' ||
      (typeof status === 'string' && status.toLowerCase() === 'pendiente');

    if (isPaid) {
      return (
        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
          <CheckCircle className="h-2.5 w-2.5 mr-1" />
          {t('licenses:status.paid')}
        </span>
      );
    } else if (isPending) {
      return (
        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
          <AlertCircle className="h-2.5 w-2.5 mr-1" />
          {t('licenses:status.pending')}
        </span>
      );
    } else {
      return (
        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
          <XCircle className="h-2.5 w-2.5 mr-1" />
          {t('licenses:status.unpaid')}
        </span>
      );
    }
  };

  const getLicenseStatusBadge = (status: string) => {
    const statusLower = status?.toLowerCase() || '';
    if (statusLower === 'activa' || statusLower === 'vigente') {
      return (
        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
          {t('licenses:status.active')}
        </span>
      );
    } else if (statusLower === 'pendiente' || statusLower === 'nueva') {
      return (
        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
          {t('licenses:status.new')}
        </span>
      );
    } else if (statusLower === 'aprobada') {
      return (
        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-800">
          {t('licenses:status.approved')}
        </span>
      );
    } else {
      return (
        <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
          {status || t('common:na')}
        </span>
      );
    }
  };

  const getLicenseTypeBadge = (type: string) => {
    const typeLower = type?.toLowerCase() || '';
    let badgeClass = 'bg-blue-100 text-blue-800';

    if (typeLower.includes('comercial')) {
      badgeClass = 'bg-blue-100 text-blue-800';
    } else if (typeLower.includes('industrial')) {
      badgeClass = 'bg-purple-100 text-purple-800';
    } else if (typeLower.includes('servicios')) {
      badgeClass = 'bg-green-100 text-green-800';
    } else if (typeLower.includes('giro')) {
      badgeClass = 'bg-indigo-100 text-indigo-800';
    }

    return (
      <span
        className={`inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium ${badgeClass}`}
      >
        {type === 'Comercial'
          ? t('licenses:type.commercial')
          : type === 'Industrial'
            ? t('licenses:type.industrial')
            : type?.includes('Giro')
              ? t('licenses:type.giro')
              : t('licenses:type.renewal')}
      </span>
    );
  };

  const handleDownloadReceipt = async () => {
    try {
      setDownloading(true);

      // Get API URL from window environment or fallback
      const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';

      // Base64-encode the folio to handle special characters like "/"
      const encodedFolio = btoa(license.license_folio);

      // Make direct fetch call to download endpoint
      const response = await fetch(
        `${API_URL}/v1/business_licenses/${encodedFolio}/download_receipt`,
        {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      if (!response.ok) {
        if (response.status === 404) {
          setShowNoReceiptModal(true);
          return;
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Get the blob and create download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `receipt_${license.license_folio}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading receipt:', error);
      setShowNoReceiptModal(true);
    } finally {
      setDownloading(false);
    }
  };

  const handleStatusUpdate = async () => {
    if (!selectedStatus) return;

    setUpdatingStatus(true);
    const formData = new FormData();
    formData.append('_intent', 'updateStatus');
    formData.append('licenseFolio', license.license_folio);
    formData.append('licenseStatus', selectedStatus);

    if (statusReason.trim()) {
      formData.append('reason', statusReason.trim());
    }

    if (statusFile) {
      formData.append('statusFile', statusFile);
    }

    try {
      fetcher.submit(formData, { method: 'POST' });
      setShowStatusModal(false);
      setSelectedStatus('');
      setStatusReason('');
      setStatusFile(null);
      revalidator.revalidate();
    } catch (error) {
      console.error('Error updating status:', error);
    } finally {
      setUpdatingStatus(false);
    }
  };

  return (
    <>
      {/* Main Row */}
      <tr className="hover:bg-gray-50 border-b border-gray-200">
        {/* Expand Button */}
        <td className="w-8 px-1 py-3">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-gray-400 hover:text-gray-600"
          >
            {isExpanded ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </button>
        </td>

        {/* Folio licencia */}
        <td className="w-20 px-2 py-3">
          <div className="text-xs font-medium text-gray-900 truncate">
            {license.license_folio || `08${184 + index}`}
          </div>
        </td>

        {/* Folio lista requisitos - Hidden on small screens */}
        <td className="w-20 px-2 py-3 hidden sm:table-cell">
          <div className="text-xs text-gray-900 truncate">
            {license.license_folio
              ? `${license.license_folio.split('-')[0]}-${license.license_folio.split('-')[1]}`
              : `1-${23 + index}/25`}
          </div>
        </td>

        {/* Actividad comercial */}
        <td className="w-28 sm:w-32 px-2 py-3">
          <div className="text-xs font-medium text-gray-900 truncate">
            {license.business_line ||
              license.business_name ||
              t('licenses:notAvailable')}
          </div>
        </td>

        {/* Solicitante/Titular - Hidden on mobile */}
        <td className="w-32 px-2 py-3 hidden md:table-cell">
          <div className="text-xs text-gray-900">
            {[
              license.owner_first_name,
              license.owner_last_name_p,
              license.owner_last_name_m,
            ]
              .filter(Boolean)
              .join(' ') || t('licenses:notAvailable')}
          </div>
        </td>

        {/* Tipo licencia - Hidden on small screens */}
        <td className="w-20 px-2 py-3 hidden sm:table-cell">
          <div className="text-xs">
            {getLicenseTypeBadge(license.license_type || 'Refrendo')}
          </div>
        </td>

        {/* Estatus licencia */}
        <td className="w-20 px-2 py-3">
          <div className="text-xs">
            {getLicenseStatusBadge(license.license_status || 'Vigente')}
          </div>
        </td>

        {/* Fecha de emisión - Hidden on mobile */}
        <td className="w-20 px-2 py-3 hidden md:table-cell">
          <div className="text-xs text-gray-900 truncate">
            {license.issue_date
              ? format(new Date(license.issue_date), 'dd/MM/yy', { locale: es })
              : t('licenses:notAvailable')}
          </div>
        </td>

        {/* Estatus pago - Hidden on tablet and smaller */}
        <td className="w-20 px-2 py-3 hidden lg:table-cell">
          <div className="flex items-center justify-center">
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={isPaid}
                onChange={e => handlePaymentToggle(e.target.checked)}
                className="sr-only"
                disabled={fetcher.state === 'submitting' || uploading}
              />
              <div
                className={`w-11 h-6 rounded-full shadow-inner transition-colors duration-200 ease-in-out ${
                  isPaid ? 'bg-green-400' : 'bg-gray-300'
                } ${fetcher.state === 'submitting' || uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <div
                  className={`inline-block w-4 h-4 rounded-full bg-white shadow transform transition-transform duration-200 ease-in-out ${
                    isPaid ? 'translate-x-6' : 'translate-x-1'
                  } mt-1`}
                />
              </div>
            </label>
          </div>
        </td>

        {/* Acciones */}
        <td className="w-16 px-1 py-3">
          <div className="flex items-center justify-center space-x-1">
            {/* PDF/Receipt Download Button */}
            <button
              onClick={handleDownloadReceipt}
              disabled={downloading}
              className="text-blue-600 hover:text-blue-900 p-1 rounded bg-blue-50 hover:bg-blue-100 transition-colors disabled:opacity-50"
              title={t('licenses:actions.downloadReceipt')}
            >
              <FileText className="h-3 w-3" />
            </button>

            {/* View/Info Button */}
            <button
              onClick={handleDownloadLicense}
              disabled={downloading}
              className="text-green-600 hover:text-green-900 p-1 rounded bg-green-50 hover:bg-green-100 transition-colors disabled:opacity-50"
              title={t('licenses:actions.viewLicense')}
            >
              <Eye className="h-3 w-3" />
            </button>

            {/* More Actions Dropdown */}
            <div className="relative">
              <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="text-gray-600 hover:text-gray-900 p-1 rounded bg-gray-50 hover:bg-gray-100 transition-colors"
                title={t('licenses:actions.moreActions')}
              >
                <MoreVertical className="h-3 w-3" />
              </button>

              {showDropdown && (
                <div className="absolute right-0 mt-2 w-44 bg-white rounded-md shadow-lg border border-gray-200 z-10">
                  <div className="py-1">
                    <button
                      className="flex items-center w-full px-3 py-2 text-xs text-gray-700 hover:bg-gray-100"
                      onClick={() => {
                        setShowStatusModal(true);
                        setShowDropdown(false);
                      }}
                    >
                      <RotateCcw className="h-3 w-3 mr-2" />
                      {t('licenses:actions.changeStatus')}
                    </button>
                    <button
                      className="flex items-center w-full px-3 py-2 text-xs text-gray-700 hover:bg-gray-100"
                      onClick={() => {
                        handleViewDetail();
                        setShowDropdown(false);
                      }}
                    >
                      <Eye className="h-3 w-3 mr-2" />
                      {t('licenses:actions.viewDetail')}
                    </button>
                    <button
                      className="flex items-center w-full px-3 py-2 text-xs text-gray-700 hover:bg-gray-100"
                      onClick={() => {
                        handleViewHistory();
                        setShowDropdown(false);
                      }}
                      disabled={loadingHistory}
                    >
                      <TrendingUp className="h-3 w-3 mr-2" />
                      {loadingHistory
                        ? t('licenses:modals.history.loading')
                        : t('licenses:actions.viewHistory')}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </td>
      </tr>

      {/* Expanded Row */}
      {isExpanded && (
        <tr className="bg-gray-50">
          <td colSpan={10} className="px-3 py-3">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
              {/* Mobile info - Show when columns are hidden */}
              <div className="md:hidden">
                <div className="space-y-1.5">
                  <div>
                    <span className="font-medium text-gray-600">
                      {t('licenses:details.applicant')}:{' '}
                    </span>
                    <span className="text-gray-900">
                      {[
                        license.owner_first_name,
                        license.owner_last_name_p,
                        license.owner_last_name_m,
                      ]
                        .filter(Boolean)
                        .join(' ') || t('licenses:notAvailable')}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-600">
                      {t('licenses:details.type')}:{' '}
                    </span>
                    {getLicenseTypeBadge(license.license_type || 'Refrendo')}
                  </div>
                  <div>
                    <span className="font-medium text-gray-600">
                      {t('licenses:details.issueDate')}:{' '}
                    </span>
                    <span className="text-gray-900">
                      {license.issue_date
                        ? format(new Date(license.issue_date), 'dd/MM/yyyy', {
                            locale: es,
                          })
                        : t('licenses:notAvailable')}
                    </span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-600">
                      {t('licenses:details.paymentStatus')}:{' '}
                    </span>
                    {getPaymentStatusBadge(
                      license.payment_status || 'Sin pagar'
                    )}
                  </div>
                </div>
              </div>

              {/* Additional Details */}
              <div>
                <h4 className="font-medium text-gray-900 mb-1.5">
                  {t('licenses:details.businessDetails')}
                </h4>
                <div className="space-y-1">
                  <div>
                    <span className="text-gray-600">
                      {t('licenses:details.businessName')}:{' '}
                    </span>
                    <span className="text-gray-900">
                      {license.business_name ||
                        license.commercial_activity ||
                        t('licenses:notAvailable')}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">
                      {t('licenses:details.address')}:{' '}
                    </span>
                    <span className="text-gray-900">
                      {license.street
                        ? `${license.street} ${license.neighborhood || ''}`.trim()
                        : t('licenses:notAvailable')}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">
                      {t('licenses:details.phone')}:{' '}
                    </span>
                    <span className="text-gray-900">
                      {license.owner_phone || t('licenses:notAvailable')}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">
                      {t('licenses:details.email')}:{' '}
                    </span>
                    <span className="text-gray-900">
                      {license.owner_email || t('licenses:notAvailable')}
                    </span>
                  </div>
                </div>
              </div>

              {/* Schedule and Details */}
              <div>
                <h4 className="font-medium text-gray-900 mb-1.5">
                  {t('licenses:details.operatingHours')}
                </h4>
                <div className="space-y-1">
                  <div>
                    <span className="text-gray-600">
                      {t('licenses:details.schedule')}:{' '}
                    </span>
                    <span className="text-gray-900">
                      {license.opening_time && license.closing_time
                        ? `${license.opening_time} - ${license.closing_time}`
                        : t('licenses:notAvailable')}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600">
                      {t('licenses:details.days')}:{' '}
                    </span>
                    <span className="text-gray-900">
                      {t('licenses:details.mondayToSunday')}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </td>
        </tr>
      )}

      {/* Payment Receipt Modal */}
      {showPaymentModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <div className="flex items-center justify-between mb-4">
              {' '}
              <h3 className="text-lg font-medium text-gray-900">
                {t('licenses:modals.paymentReceipt.title')}
              </h3>
              <button
                onClick={() => setShowPaymentModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <span className="sr-only">{t('common:actions.close')}</span>
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <div className="space-y-4">
              <p className="text-sm text-gray-600">
                {t('licenses:modals.paymentReceipt.description')}
              </p>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('licenses:modals.paymentReceipt.uploadLabel')}
                </label>
                <div className="flex items-center space-x-2">
                  <div className="flex-1">
                    <input
                      type="file"
                      accept=".pdf,.jpg,.jpeg,.png"
                      onChange={e =>
                        setPaymentReceipt(e.target.files?.[0] || null)
                      }
                      className="hidden"
                      id="payment-receipt"
                    />
                    <label
                      htmlFor="payment-receipt"
                      className="block w-full border border-gray-300 rounded-md px-3 py-2 text-sm text-gray-700 cursor-pointer hover:bg-gray-50"
                    >
                      {paymentReceipt
                        ? paymentReceipt.name
                        : t('licenses:modals.paymentReceipt.noFileChosen')}
                    </label>
                  </div>
                  <label
                    htmlFor="payment-receipt"
                    className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm font-medium cursor-pointer"
                  >
                    {t('licenses:modals.paymentReceipt.chooseFile')}
                  </label>
                </div>
              </div>
            </div>

            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => setShowPaymentModal(false)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                {t('common:actions.close')}
              </button>
              <button
                onClick={handlePaymentSubmit}
                disabled={!paymentReceipt || uploading}
                className="px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {uploading
                  ? t('licenses:modals.paymentReceipt.sending')
                  : t('licenses:modals.paymentReceipt.send')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* No Receipt Modal */}
      {showNoReceiptModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex items-center space-x-3 mb-4">
              <div className="flex-shrink-0">
                <AlertCircle className="h-6 w-6 text-yellow-600" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  {t('licenses:modals.noReceipt.title')}
                </h3>
              </div>
            </div>

            <div className="mb-6">
              <p className="text-sm text-gray-600">
                {t('licenses:modals.noReceipt.description')}
              </p>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setShowNoReceiptModal(false)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                {t('licenses:modals.noReceipt.understood')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* No License Modal */}
      {showNoLicenseModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex items-center space-x-3 mb-4">
              <div className="flex-shrink-0">
                <AlertCircle className="h-6 w-6 text-yellow-600" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  {t('licenses:modals.noLicense.title')}
                </h3>
              </div>
            </div>

            <div className="mb-6">
              <p className="text-sm text-gray-600">
                {t('licenses:modals.noLicense.description')}
              </p>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setShowNoLicenseModal(false)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              >
                {t('licenses:modals.noLicense.understood')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Status Update Modal */}
      {showStatusModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="flex items-center space-x-3 mb-4">
              <div className="flex-shrink-0">
                <RotateCcw className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  {t('licenses:modals.statusUpdate.title')}
                </h3>
              </div>
            </div>

            <div className="space-y-4">
              {/* Current Status Display */}
              <div className="text-sm">
                <p className="text-gray-600">
                  {t('licenses:modals.statusUpdate.currentStatus')}:{' '}
                  <span className="font-medium">
                    {license.license_status || 'Vigente'}
                  </span>
                </p>
                {license.reason && (
                  <p className="text-gray-600">
                    {t('licenses:modals.statusUpdate.reason')}: {license.reason}
                  </p>
                )}
                {license.status_change_date && (
                  <p className="text-gray-600">
                    {t('licenses:modals.statusUpdate.statusChangeDate')}:{' '}
                    {license.status_change_date.slice(0, 10)}
                  </p>
                )}
                {license.reason_file && (
                  <p className="text-gray-600">
                    {t('licenses:modals.statusUpdate.file')}:{' '}
                    <button
                      onClick={() =>
                        window.open(
                          `${(window as any).ENV?.API_URL || 'http://localhost:8000'}/${license.reason_file}`,
                          '_blank'
                        )
                      }
                      className="text-blue-600 hover:underline"
                    >
                      {t('licenses:modals.statusUpdate.download')}
                    </button>
                  </p>
                )}
              </div>

              {/* Status Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('licenses:modals.statusUpdate.newStatus')} *
                </label>
                <select
                  value={selectedStatus}
                  onChange={e => setSelectedStatus(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500"
                  required
                >
                  <option value="">
                    {t('licenses:modals.statusUpdate.selectStatus')}
                  </option>
                  <option value="Cancelada">
                    {t('licenses:statusOptions.cancelled')}
                  </option>
                  <option value="Suspendida">
                    {t('licenses:statusOptions.suspended')}
                  </option>
                  <option value="Vigente">
                    {t('licenses:statusOptions.active')}
                  </option>
                  <option value="Baja">
                    {t('licenses:statusOptions.discharged')}
                  </option>
                  <option value="Sanción">
                    {t('licenses:statusOptions.sanction')}
                  </option>
                  <option value="Adeudo">
                    {t('licenses:statusOptions.debt')}
                  </option>
                  <option value="Renovar">
                    {t('licenses:statusOptions.renew')}
                  </option>
                </select>
              </div>

              {/* Reason/Motivo */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('licenses:modals.statusUpdate.reasonLabel')}
                </label>
                <textarea
                  value={statusReason}
                  onChange={e => setStatusReason(e.target.value)}
                  placeholder={t(
                    'licenses:modals.statusUpdate.reasonPlaceholder'
                  )}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500"
                  rows={3}
                />
              </div>

              {/* File Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('licenses:modals.statusUpdate.uploadFile')}
                </label>
                <input
                  type="file"
                  onChange={e => setStatusFile(e.target.files?.[0] || null)}
                  accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500"
                />
                {statusFile && (
                  <p className="text-xs text-gray-500 mt-1">
                    {t('licenses:modals.statusUpdate.fileSelected')}:{' '}
                    {statusFile.name}
                  </p>
                )}
              </div>
            </div>

            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => {
                  setShowStatusModal(false);
                  setSelectedStatus('');
                  setStatusReason('');
                  setStatusFile(null);
                }}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                disabled={updatingStatus}
              >
                {t('common:actions.cancel')}
              </button>
              <button
                onClick={handleStatusUpdate}
                disabled={!selectedStatus || updatingStatus}
                className="px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {updatingStatus
                  ? t('licenses:modals.statusUpdate.updating')
                  : t('licenses:modals.statusUpdate.add')}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* History Modal */}
      {showHistoryModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full mx-4 max-h-[90vh] flex flex-col">
            {/* Modal Header */}
            <div className="bg-green-500 text-white p-4 rounded-t-lg">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium">
                  {t('licenses:modals.history.title')}
                </h3>
                <button
                  onClick={() => setShowHistoryModal(false)}
                  className="text-white hover:text-gray-200"
                >
                  <span className="sr-only">{t('common:actions.close')}</span>
                  <svg
                    className="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="flex-1 overflow-y-auto p-6">
              {loadingHistory ? (
                <div className="animate-pulse space-y-4">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-4 bg-gray-200 rounded w-full"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                  <div className="h-32 bg-gray-200 rounded"></div>
                </div>
              ) : historyData ? (
                <div className="space-y-6">
                  {/* General License Data */}
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-medium text-gray-600">
                          {t('licenses:modals.history.folioLicense')}:
                        </span>
                        <span className="ml-2 text-gray-900">
                          {license.license_folio}
                        </span>
                      </div>
                      <div>
                        <span className="font-medium text-gray-600">
                          {t('licenses:modals.history.folioList')}:
                        </span>
                        <span className="ml-2 text-gray-900">
                          {license.license_folio
                            ? `${license.license_folio.split('-')[0]}-${license.license_folio.split('-')[1]}`
                            : 'N/A'}
                        </span>
                      </div>
                      <div>
                        <span className="font-medium text-gray-600">
                          {t('licenses:modals.history.applicant')}:
                        </span>
                        <span className="ml-2 text-gray-900">
                          {[
                            license.owner_first_name,
                            license.owner_last_name_p,
                            license.owner_last_name_m,
                          ]
                            .filter(Boolean)
                            .join(' ') || t('licenses:notAvailable')}
                        </span>
                      </div>
                      <div>
                        <span className="font-medium text-gray-600">
                          {t('licenses:modals.history.status')}:
                        </span>
                        <span className="ml-2">
                          {getLicenseStatusBadge(
                            historyData.current_status ||
                              license.license_status ||
                              'Vigente'
                          )}
                        </span>
                      </div>
                      <div className="md:col-span-2">
                        <span className="font-medium text-gray-600">
                          {t('licenses:modals.history.type')}:
                        </span>
                        <span className="ml-2">
                          {getLicenseTypeBadge(
                            license.license_type || 'Refrendo'
                          )}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Status History Table */}
                  <div className="bg-white">
                    <div className="overflow-x-auto">
                      <table className="w-full border-collapse border border-gray-300">
                        <thead>
                          <tr className="bg-gray-100">
                            <th className="border border-gray-300 px-4 py-3 text-left text-sm font-medium text-gray-700">
                              {t('licenses:modals.history.previousStatus')}
                            </th>
                            <th className="border border-gray-300 px-4 py-3 text-left text-sm font-medium text-gray-700">
                              {t('licenses:modals.history.newStatus')}
                            </th>
                            <th className="border border-gray-300 px-4 py-3 text-left text-sm font-medium text-gray-700">
                              {t('licenses:modals.history.changeDate')}
                            </th>
                            <th className="border border-gray-300 px-4 py-3 text-left text-sm font-medium text-gray-700">
                              {t('licenses:modals.history.user')}
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          {historyData.status_history &&
                          historyData.status_history.length > 0 ? (
                            historyData.status_history.map(
                              (entry: any, index: number) => (
                                <tr
                                  key={entry.id || index}
                                  className="hover:bg-gray-50"
                                >
                                  <td className="border border-gray-300 px-4 py-3 text-sm text-gray-900">
                                    {entry.previous_status || 'N/A'}
                                  </td>
                                  <td className="border border-gray-300 px-4 py-3 text-sm text-gray-900">
                                    {entry.new_status}
                                  </td>
                                  <td className="border border-gray-300 px-4 py-3 text-sm text-gray-900">
                                    {entry.changed_at
                                      ? format(
                                          new Date(entry.changed_at),
                                          'dd/MM/yyyy HH:mm',
                                          { locale: es }
                                        )
                                      : 'N/A'}
                                  </td>
                                  <td className="border border-gray-300 px-4 py-3 text-sm text-gray-900">
                                    {entry.changed_by_user ? (
                                      <div>
                                        <div className="font-medium">
                                          {entry.changed_by_user.name}
                                        </div>
                                        <div className="text-xs text-gray-500">
                                          {entry.changed_by_user.role_name}
                                        </div>
                                      </div>
                                    ) : (
                                      'N/A'
                                    )}
                                  </td>
                                </tr>
                              )
                            )
                          ) : (
                            <tr>
                              <td
                                colSpan={4}
                                className="border border-gray-300 px-4 py-8 text-center text-gray-500"
                              >
                                Sin datos
                              </td>
                            </tr>
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center text-gray-500">
                  {t('licenses:modals.history.errorLoading')}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default function LicensesIssued() {
  const { licenses, pagination, municipalityName, error, authToken } =
    useLoaderData<typeof loader>();
  const { t } = useTranslation(['licenses', 'common']);
  const revalidator = useRevalidator();

  // Map BusinessLicense data to match the expected UI format
  const mappedLicenses = licenses.map(license => ({
    ...license,
    // Map fields to match expected UI format - prioritize new establishment fields
    business_name:
      license.establishment_name ||
      license.procedure_establishment_name ||
      license.commercial_activity ||
      license.procedure_scian_name ||
      t('licenses:notAvailable'),
    business_line:
      license.commercial_activity ||
      license.procedure_scian_name ||
      t('licenses:notAvailable'),
    // Extract owner information - use available data
    owner_first_name:
      license.owner ||
      license.procedure_applicant_name ||
      t('licenses:notAvailable'),
    // Format issue date from created_at if available
    issue_date: license.created_at || new Date().toISOString(),
    // Address data - prioritize new establishment address field
    street:
      license.establishment_address ||
      license.procedure_establishment_address ||
      license.procedure_street ||
      license.authorized_area ||
      '',
    neighborhood: license.procedure_neighborhood || '',
    // Contact information - prioritize new establishment fields
    owner_phone:
      license.establishment_phone ||
      license.procedure_establishment_phone ||
      license.owner_phone ||
      '',
    owner_email:
      license.establishment_email ||
      license.owner_email ||
      license.user_email ||
      '', // Usa email del establecimiento primero, luego usuario
    // Use actual payment_status from backend, default to 0 (unpaid) if not available
    payment_status: license.payment_status ?? 0,
  }));

  // Filter states
  const [searchTerm, setSearchTerm] = useState('');

  // For client-side filtering (if needed on the displayed page)
  const filteredLicenses = mappedLicenses.filter((license: any) => {
    if (!searchTerm) return true;

    const matchesSearch =
      license.business_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      license.license_folio?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      `${license.owner_first_name || ''} ${license.owner_last_name_p || ''} ${license.owner_last_name_m || ''}`
        .toLowerCase()
        .includes(searchTerm.toLowerCase());

    return matchesSearch;
  });

  // Update stats based on current page results
  const filteredStats = {
    total: filteredLicenses.length,
    active: filteredLicenses.filter((l: any) => {
      const status = l.license_status?.toLowerCase();
      return status === 'active' || status === 'vigente' || status === 'activa';
    }).length,
    pending: filteredLicenses.filter((l: any) => {
      const status = l.license_status?.toLowerCase();
      return (
        status === 'pending' ||
        status === 'pendiente' ||
        status === 'nueva' ||
        status === 'documentación pendiente' ||
        status === 'en proceso'
      );
    }).length,
    paid: filteredLicenses.filter((l: any) => l.payment_status === 1).length,
  };

  // Calculate display range for pagination info
  const displayStart =
    pagination.total === 0
      ? 0
      : (pagination.page - 1) * pagination.per_page + 1;
  const displayEnd = Math.min(
    pagination.page * pagination.per_page,
    pagination.total
  );

  // Export function
  const handleExport = async () => {
    try {
      // Get municipality_id from the first license or a default value
      const municipalityId = mappedLicenses[0]?.municipality_id || 1;

      const blob = await exportBusinessLicenses({
        municipality_id: municipalityId,
        authToken,
      });

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `business_licenses_${new Date().toISOString().split('T')[0]}.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error exporting licenses:', error);
      // You could add a toast notification here
    }
  };

  // Show error message if there was an issue loading data
  if (error) {
    return (
      <div className="p-6 max-w-7xl mx-auto">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <AlertCircle className="h-5 w-5 text-red-600" />
            <p className="text-red-800">{t(error)}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-3 md:p-6 w-full mx-auto">
      {/* Header */}
      <div className="mb-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div className="min-w-0 flex-1">
            <h1 className="text-xl md:text-2xl font-bold text-gray-900 truncate">
              {t('licenses:title.issuedLicenses')}
            </h1>
            <p className="text-gray-600 mt-1 text-sm md:text-base">
              {t('licenses:description.managementAndConsultation', {
                municipalityName,
              })}
            </p>
          </div>
          <div className="flex items-center space-x-2 flex-shrink-0">
            <button
              onClick={handleExport}
              className="bg-blue-600 text-white px-3 md:px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2 text-sm"
            >
              <Download className="h-4 w-4" />
              <span className="hidden sm:inline">{t('common:export')}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 md:gap-4 mb-6">
        <div className="bg-white p-2 md:p-4 rounded-lg border border-gray-200">
          <div className="flex items-center space-x-2">
            <div className="p-1 md:p-2 bg-blue-100 rounded-lg flex-shrink-0">
              <FileText className="h-4 w-4 md:h-5 md:w-5 text-blue-600" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs md:text-sm text-gray-600 truncate">
                {t('licenses:stats.totalLicenses')}
              </p>
              <p className="text-lg md:text-xl font-bold text-gray-900">
                {filteredStats.total}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-2 md:p-4 rounded-lg border border-gray-200">
          <div className="flex items-center space-x-2">
            <div className="p-1 md:p-2 bg-green-100 rounded-lg flex-shrink-0">
              <CheckCircle className="h-4 w-4 md:h-5 md:w-5 text-green-600" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs md:text-sm text-gray-600 truncate">
                {t('licenses:stats.activeLicenses')}
              </p>
              <p className="text-lg md:text-xl font-bold text-green-600">
                {filteredStats.active}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-2 md:p-4 rounded-lg border border-gray-200">
          <div className="flex items-center space-x-2">
            <div className="p-1 md:p-2 bg-yellow-100 rounded-lg flex-shrink-0">
              <AlertCircle className="h-4 w-4 md:h-5 md:w-5 text-yellow-600" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs md:text-sm text-gray-600 truncate">
                {t('licenses:stats.pendingLicenses')}
              </p>
              <p className="text-lg md:text-xl font-bold text-yellow-600">
                {filteredStats.pending}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-2 md:p-4 rounded-lg border border-gray-200">
          <div className="flex items-center space-x-2">
            <div className="p-1 md:p-2 bg-green-100 rounded-lg flex-shrink-0">
              <DollarSign className="h-4 w-4 md:h-5 md:w-5 text-green-600" />
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-xs md:text-sm text-gray-600 truncate">
                {t('licenses:stats.paidLicenses')}
              </p>
              <p className="text-lg md:text-xl font-bold text-green-600">
                {filteredStats.paid}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg border border-gray-200 p-3 md:p-4 mb-6">
        <div className="w-full">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              placeholder={t('licenses:search.placeholder')}
              className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            />
          </div>
        </div>
      </div>

      {/* Show empty state if no licenses */}
      {filteredLicenses.length === 0 ? (
        <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
          <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {licenses.length === 0
              ? t('licenses:empty.noLicensesAvailable')
              : t('licenses:empty.noResultsFound')}
          </h3>
          <p className="text-gray-500">
            {licenses.length === 0
              ? t('licenses:empty.noLicensesDescription')
              : t('licenses:empty.noResultsFound')}
          </p>
        </div>
      ) : (
        <>
          {/* Licenses Table - Legacy Style */}
          <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full table-fixed divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="w-8 px-1 py-3"></th>
                    <th className="w-20 px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {t('licenses:table.folio')}
                    </th>
                    <th className="w-20 px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell">
                      {t('licenses:table.folioList')}
                    </th>
                    <th className="w-28 sm:w-32 px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {t('licenses:table.activity')}
                    </th>
                    <th className="w-32 px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">
                      {t('licenses:table.owner')}
                    </th>
                    <th className="w-20 px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell">
                      {t('licenses:table.type')}
                    </th>
                    <th className="w-20 px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {t('licenses:table.status')}
                    </th>
                    <th className="w-20 px-2 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">
                      {t('licenses:table.date')}
                    </th>
                    <th className="w-20 px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider hidden lg:table-cell">
                      {t('licenses:table.payment')}
                    </th>
                    <th className="w-16 px-1 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {t('licenses:table.actions')}
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredLicenses.map((license: any, index: number) => (
                    <LicenseRow
                      key={`${license.license_folio}-${license.id || index}`}
                      license={license}
                      index={index}
                      t={t}
                      authToken={authToken}
                      revalidator={revalidator}
                    />
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          {/* Pagination */}
          <div className="bg-white px-3 md:px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 mt-6">
            <div className="flex-1 flex justify-between sm:hidden">
              <Link
                to={`?page=${Math.max(1, pagination.page - 1)}`}
                className={`relative inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md ${
                  pagination.page <= 1
                    ? 'text-gray-400 bg-gray-100 cursor-not-allowed'
                    : 'text-gray-700 bg-white hover:bg-gray-50'
                }`}
                aria-disabled={pagination.page <= 1}
              >
                {t('common:previous')}
              </Link>
              <Link
                to={`?page=${Math.min(pagination.total_pages, pagination.page + 1)}`}
                className={`ml-3 relative inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md ${
                  pagination.page >= pagination.total_pages
                    ? 'text-gray-400 bg-gray-100 cursor-not-allowed'
                    : 'text-gray-700 bg-white hover:bg-gray-50'
                }`}
                aria-disabled={pagination.page >= pagination.total_pages}
              >
                {t('common:next')}
              </Link>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-xs md:text-sm text-gray-700">
                  {t('common:pagination.showing')}: {displayStart}-{displayEnd}{' '}
                  {t('common:pagination.of')} {pagination.total}{' '}
                  {t('licenses:table.tableTitle')}
                </p>
              </div>
              <div>
                <nav
                  className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                  aria-label="Pagination"
                >
                  <Link
                    to={`?page=${Math.max(1, pagination.page - 1)}`}
                    className={`relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 text-xs md:text-sm font-medium ${
                      pagination.page <= 1
                        ? 'text-gray-400 bg-gray-100 cursor-not-allowed'
                        : 'text-gray-500 bg-white hover:bg-gray-50'
                    }`}
                    aria-disabled={pagination.page <= 1}
                  >
                    {t('common:previous')}
                  </Link>

                  {/* Page numbers */}
                  {(() => {
                    const pages = [];
                    const startPage = Math.max(1, pagination.page - 2);
                    const endPage = Math.min(
                      pagination.total_pages,
                      pagination.page + 2
                    );

                    for (let i = startPage; i <= endPage; i++) {
                      pages.push(
                        <Link
                          key={i}
                          to={`?page=${i}`}
                          className={`relative inline-flex items-center px-3 md:px-4 py-2 border text-xs md:text-sm font-medium ${
                            i === pagination.page
                              ? 'bg-blue-50 border-blue-500 text-blue-600'
                              : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                          }`}
                        >
                          {i}
                        </Link>
                      );
                    }

                    return pages;
                  })()}

                  <Link
                    to={`?page=${Math.min(pagination.total_pages, pagination.page + 1)}`}
                    className={`relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 text-xs md:text-sm font-medium ${
                      pagination.page >= pagination.total_pages
                        ? 'text-gray-400 bg-gray-100 cursor-not-allowed'
                        : 'text-gray-500 bg-white hover:bg-gray-50'
                    }`}
                    aria-disabled={pagination.page >= pagination.total_pages}
                  >
                    {t('common:next')}
                  </Link>
                </nav>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
