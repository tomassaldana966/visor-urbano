import { useState, useEffect } from 'react';
import type { LoaderFunctionArgs } from 'react-router';
import { useLoaderData, useParams, Link, useNavigate } from 'react-router';
import { useTranslation } from 'react-i18next';
import { requireUser } from '../../utils/auth/utils';
import {
  getProcedureByFolio,
  getDynamicFieldsByFolio,
} from '../../utils/api/api.server';

// Define LicenseStatus type locally since we can't import from server
type LicenseStatus = {
  folio: string;
  procedure_status: number;
  license_exists: boolean;
  license_paid: boolean;
  license_file_exists: boolean;
  can_download: boolean;
};
import { getWorkflowStatusFromBackend } from '../../utils/api/workflow';
import { WorkflowIndicator } from '../../components/Procedures/WorkflowIndicator';
import { Button } from '../../components/Button/Button';
import { StatusBadge } from '../../components/Procedures';
import {
  dynamicFieldsResponseSchema,
  type DynamicField,
} from '../../schemas/dynamicFields';
import {
  FileText,
  MapPin,
  User,
  Building,
  Calendar,
  CheckCircle,
  Download,
  Eye,
  ArrowLeft,
  AlertCircle,
  X,
} from 'lucide-react';
import { useProcedurePDF } from '../../hooks/useProcedurePDF';
import { getFileDownloadUrl, parseFileValue } from '../../utils/fileDownload';
import { encodeFolio } from '../../utils/folio';
export const handle = {
  title: 'procedures:detail.title',
  breadcrumb: 'procedures:detail.breadcrumb',
};

export async function loader({ request, params }: LoaderFunctionArgs) {
  const user = await requireUser(request);
  const { folio } = params;

  if (!folio) {
    throw new Response('Folio not provided', { status: 400 });
  }

  try {
    const authToken = user.access_token;
    if (!authToken) {
      throw new Response('Authentication required', { status: 401 });
    }

    let decodedFolio: string;
    try {
      decodedFolio = atob(folio);
    } catch {
      decodedFolio = folio;
    }

    const [procedure, rawDynamicFieldsResponse, workflowStatus] =
      await Promise.all([
        getProcedureByFolio(authToken, decodedFolio),
        getDynamicFieldsByFolio(authToken, decodedFolio),
        getWorkflowStatusFromBackend(authToken, decodedFolio),
      ]);

    let normalizedResponse = rawDynamicFieldsResponse;
    try {
      if (
        Array.isArray(rawDynamicFieldsResponse) &&
        rawDynamicFieldsResponse.length >= 1
      ) {
        const transformedDynamicFields = Array.isArray(
          rawDynamicFieldsResponse[0]
        )
          ? rawDynamicFieldsResponse[0].map((field: any) => ({
              ...field,
              required: field.required === 1 || field.required === true,
              status: Number(field.status || 0),
              step: Number(field.step || 1),
              municipality_id: Number(field.municipality_id || 0),
            }))
          : rawDynamicFieldsResponse[0];
        normalizedResponse = [
          transformedDynamicFields,
          ...rawDynamicFieldsResponse.slice(1),
        ] as typeof rawDynamicFieldsResponse;
      }
    } catch {
      normalizedResponse = rawDynamicFieldsResponse;
    }

    const fieldsResult =
      dynamicFieldsResponseSchema.safeParse(normalizedResponse);

    if (!fieldsResult.success) {
      return {
        user,
        procedure,
        folio: decodedFolio,
        dynamicFields: [],
        staticFields: [],
        licenseInfo: null,
        workflowStatus: null,
      };
    }

    const [dynamicFields, staticFields, licenseInfo] = fieldsResult.data;

    return {
      user,
      procedure,
      folio: decodedFolio,
      dynamicFields,
      staticFields,
      licenseInfo,
      workflowStatus,
    };
  } catch {
    throw new Response('Procedure not found', { status: 404 });
  }
}

export default function ProcedureDetailPage() {
  const {
    user,
    procedure,
    folio,
    dynamicFields,
    staticFields,
    workflowStatus,
  } = useLoaderData<typeof loader>();
  const { t } = useTranslation('procedures');
  const navigate = useNavigate();
  const { generatePDF } = useProcedurePDF();
  const [showDocumentsModal, setShowDocumentsModal] = useState(false);
  const [resolutions, setResolutions] = useState<any[]>([]);
  const [loadingResolutions, setLoadingResolutions] = useState(false);
  const [errorResolutions, setErrorResolutions] = useState<string | null>(null);
  const [downloadingResolutionId, setDownloadingResolutionId] = useState<
    string | number | null
  >(null);
  const [downloadResolutionError, setDownloadResolutionError] = useState<
    string | null
  >(null);
  const [downloadingFiles, setDownloadingFiles] = useState<{
    [id: string]: boolean;
  }>({});
  const [downloadErrors, setDownloadErrors] = useState<{
    [id: string]: string | null;
  }>({});
  const [licenseStatus, setLicenseStatus] = useState<LicenseStatus | null>(
    null
  );
  const [loadingLicenseStatus, setLoadingLicenseStatus] = useState(false);
  const [downloadingLicense, setDownloadingLicense] = useState(false);

  const goBackToProcedures = () => {
    navigate(-1);
  };

  const handleDownloadPDF = async () => {
    try {
      await generatePDF(procedure as any, fieldsBySection);
    } catch (error) {
      throw new Error(
        `Failed to generate PDF: ${error instanceof Error ? error.message : 'Unknown error'}`
      );
    }
  };

  // Handle license download
  const handleDownloadLicense = async () => {
    if (!licenseStatus?.can_download || !user.access_token) return;

    setDownloadingLicense(true);
    try {
      const encodedFolio = btoa(folio);

      // Get API URL from window environment or fallback
      const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';

      // Use the procedures endpoint for users to download their own licenses
      const response = await fetch(
        `${API_URL}/v1/procedures/license/download-by-folio/${encodedFolio}`,
        {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${user.access_token}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error(
          `Download failed: ${response.status} ${response.statusText}`
        );
      }

      // Get the file blob and create download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `licencia_${folio}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading license:', error);
      // Could add error state/toast here if needed
    } finally {
      setDownloadingLicense(false);
    }
  };

  const getTranslatedProcedureType = (
    procedureType: string | null | undefined
  ) => {
    if (!procedureType) return t('detail.status.notSpecified');
    const typeTranslations: Record<string, string> = {
      business_license: t('edit.pdf.procedureTypes.businessLicense'),
      permits_building_license: t('edit.pdf.procedureTypes.buildingLicense'),
    };
    return typeTranslations[procedureType] || procedureType;
  };

  const formatDate = (dateString: string | null | undefined) => {
    if (!dateString) return '--';
    try {
      return new Date(dateString).toLocaleDateString('es-MX', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return '--';
    }
  };

  const transformedStaticFields =
    staticFields?.map(staticField => ({
      ...staticField,
      step: staticField.step || 1,
      sequence: staticField.sequence || 0,
      required:
        typeof staticField.required === 'number'
          ? staticField.required === 1
          : Boolean(staticField.required),
    })) || [];

  const allFieldsMap = new Map<string, any>();
  (dynamicFields || []).forEach(field => {
    if (field.name) {
      allFieldsMap.set(field.name.toLowerCase(), field);
    }
  });
  transformedStaticFields.forEach(field => {
    if (field.name && !allFieldsMap.has(field.name.toLowerCase())) {
      allFieldsMap.set(field.name.toLowerCase(), field);
    }
  });
  const allFields = Array.from(allFieldsMap.values());

  const procedureToFieldMapping: Record<string, string> = {
    establishment_name: 'nombre_establecimiento',
    establishment_address: 'direccion_establecimiento',
    establishment_phone: 'telefono_establecimiento',
    establishment_area: 'superficie_establecimiento',
    official_applicant_name: 'nombre_solicitante',
    street: 'calle',
    exterior_number: 'numero_exterior',
    interior_number: 'numero_interior',
    neighborhood: 'colonia',
    municipality_id: 'municipio',
    business_name: 'nombre_negocio',
    business_sector: 'giro_comercial',
    business_activity: 'actividad',
    operating_hours: 'horario_funcionamiento',
    employee_count: 'numero_empleados',
    area: 'superficie',
  };

  const fieldsWithValues = allFields.map(field => {
    let fieldValue = field.value;
    const fieldName = field.name?.toLowerCase();
    if (fieldName) {
      const mappedProcedureField = Object.entries(procedureToFieldMapping).find(
        ([procField, dynamicFieldName]) =>
          dynamicFieldName.toLowerCase() === fieldName
      );
      if (mappedProcedureField) {
        const [procedureFieldName] = mappedProcedureField;
        const procedureValue = (procedure as any)[procedureFieldName];
        if (
          procedureValue !== null &&
          procedureValue !== undefined &&
          procedureValue !== ''
        ) {
          fieldValue = procedureValue;
        }
      }
    }
    return {
      ...field,
      value: fieldValue,
    };
  });

  const allowedFieldTypes = [
    'input',
    'file',
    'multifile',
    'radio',
    'select',
    'textarea',
  ] as const;

  function isValidDynamicField(field: any): field is DynamicField {
    return (
      typeof field === 'object' &&
      field !== null &&
      'field_type' in field &&
      allowedFieldTypes.includes(field.field_type)
    );
  }

  const fieldsBySection = fieldsWithValues.reduce(
    (acc, field) => {
      if (!isValidDynamicField(field)) {
        return acc;
      }
      const sectionId = field.step?.toString() || '1';
      if (!acc[sectionId]) {
        acc[sectionId] = [];
      }
      acc[sectionId].push(field);
      return acc;
    },
    {} as Record<string, DynamicField[]>
  );

  const getSectionInfo = (sectionId: string) => {
    const sectionMap: Record<
      string,
      { title: string; icon: any; description?: string }
    > = {
      '1': {
        title: t('edit.sections.section1.title'),
        icon: User,
        description: t('edit.sections.section1.description'),
      },
      '2': {
        title: t('edit.sections.section2.title'),
        icon: Building,
        description: t('edit.sections.section2.description'),
      },
      '3': {
        title: t('edit.sections.section3.title'),
        icon: Building,
        description: t('edit.sections.section3.description'),
      },
      '4': {
        title: t('edit.sections.section4.title'),
        icon: FileText,
        description: t('edit.sections.section4.description'),
      },
    };
    return (
      sectionMap[sectionId] || {
        title: `${t('edit.form.section')} ${sectionId}`,
        icon: FileText,
        description: `${t('detail.dynamicFields.noSection')} ${sectionId} ${t('detail.dynamicFields.ofForm')}`,
      }
    );
  };

  const getDocuments = () => {
    const documents: Array<{
      name: string;
      value: string;
      required: boolean;
      description?: string;
    }> = [];
    fieldsWithValues.forEach(field => {
      if (
        (field.field_type === 'file' || field.field_type === 'multifile') &&
        field.value
      ) {
        documents.push({
          name: field.name,
          value: field.value,
          required: field.required || false,
          description: getTranslatedDocumentName(field.name, field.description),
        });
      }
    });
    return documents;
  };

  const formatFieldValue = (field: DynamicField) => {
    if (!field.value || field.value === '') return '--';
    switch (field.field_type) {
      case 'radio':
      case 'select':
        if (field.options && typeof field.options === 'string' && field.value) {
          try {
            const hasPipe = field.options.includes('|');
            const separator = hasPipe ? '|' : ',';
            const options = field.options.split(separator);
            const descriptions = field.options_description
              ? field.options_description.split(separator)
              : [];
            const parsedOptions = options.map((option, index) => ({
              value: descriptions[index]?.trim() || option.trim(),
              label: option.trim(),
            }));
            const selectedOption = parsedOptions.find(
              opt => opt.value === field.value?.toString().trim()
            );
            if (selectedOption) {
              return selectedOption.label;
            }
            const labelMatch = parsedOptions.find(
              opt => opt.label === field.value?.toString().trim()
            );
            if (labelMatch) {
              return labelMatch.label;
            }
          } catch (error) {
            throw new Error(
              `Failed to parse field options: ${error instanceof Error ? error.message : 'Unknown parsing error'}`
            );
          }
        }
        return field.value;
      case 'file':
      case 'multifile':
        if (typeof field.value === 'string' && procedure?.id) {
          const fileInfo = parseFileValue(field.value);
          if (fileInfo) {
            const downloadUrl = getFileDownloadUrl(procedure.id, field.name);
            return (
              <div className="flex items-center space-x-2">
                <FileText size={16} className="text-blue-600" />
                <a
                  href={downloadUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 underline cursor-pointer"
                  title={`${t('detail.sections.documents.download')} ${fileInfo.originalName || fileInfo.filename}`}
                >
                  {fileInfo.originalName || fileInfo.filename}
                </a>
                {fileInfo.size && (
                  <span className="text-xs text-gray-400">
                    ({Math.round(fileInfo.size / 1024)} KB)
                  </span>
                )}
              </div>
            );
          }
          if (field.value.includes('http')) {
            return (
              <div className="flex items-center space-x-2">
                <FileText size={16} className="text-blue-600" />
                <a
                  href={field.value}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 underline cursor-pointer"
                >
                  {t('filesModal.view')}
                </a>
              </div>
            );
          }
          return field.value;
        }
        return field.value;
      case 'textarea':
        return (
          <div className="whitespace-pre-wrap break-words">{field.value}</div>
        );
      default:
        return field.value;
    }
  };

  const DocumentsModal = () => {
    const documents = getDocuments();
    if (!showDocumentsModal) return null;
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[80vh] overflow-hidden">
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div className="flex items-center">
              <FileText className="h-6 w-6 text-blue-600 mr-3" />
              <h2 className="text-xl font-semibold text-gray-900">
                {t('detail.sections.documents.title')}
              </h2>
            </div>
            <button
              onClick={() => setShowDocumentsModal(false)}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X size={24} />
            </button>
          </div>
          <div className="p-6 overflow-y-auto max-h-[calc(80vh-120px)]">
            {documents.length === 0 ? (
              <div className="text-center py-12">
                <FileText size={64} className="mx-auto mb-4 text-gray-300" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {t('detail.sections.documents.noDocuments')}
                </h3>
                <p className="text-gray-500">
                  {t('detail.sections.documents.noDocumentsDescription')}
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {documents.map((doc, index) => {
                  const fileInfo = parseFileValue(doc.value);
                  return (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-4"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center mb-2">
                            <h3 className="text-lg font-semibold text-gray-900">
                              {getTranslatedDocumentName(
                                doc.name,
                                doc.description
                              )}
                              {doc.required && (
                                <span className="text-red-500 ml-1">*</span>
                              )}
                            </h3>
                          </div>
                          {fileInfo ? (
                            <div className="flex items-center space-x-4">
                              <div className="flex items-center space-x-2">
                                <FileText size={16} className="text-blue-600" />
                                <span className="text-sm font-medium text-gray-700">
                                  {fileInfo.originalName || fileInfo.filename}
                                </span>
                              </div>
                              {fileInfo.size && (
                                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                                  {Math.round(fileInfo.size / 1024)} KB
                                </span>
                              )}
                              {fileInfo.contentType && (
                                <span className="text-xs text-gray-500 bg-blue-100 px-2 py-1 rounded">
                                  {fileInfo.contentType
                                    .split('/')[1]
                                    .toUpperCase()}
                                </span>
                              )}
                            </div>
                          ) : (
                            <div className="text-sm text-gray-600">
                              {doc.value}
                            </div>
                          )}
                        </div>
                        {fileInfo && procedure?.id && (
                          <div className="ml-4">
                            <a
                              href={getFileDownloadUrl(procedure.id, doc.name)}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
                            >
                              <Download size={16} className="mr-2" />
                              {t('detail.sections.documents.download')}
                            </a>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
          <div className="flex justify-end p-6 border-t border-gray-200">
            <Button
              variant="secondary"
              onClick={() => setShowDocumentsModal(false)}
            >
              {t('detail.sections.documents.close')}
            </Button>
          </div>
        </div>
      </div>
    );
  };

  const getTranslatedDocumentName = (
    fieldName: string,
    fieldDescription?: string
  ) => {
    const documentNameMap: Record<string, string> = {
      identificacion_oficial:
        'detail.sections.documents.names.identificacionOficial',
      comprobante_domicilio:
        'detail.sections.documents.names.comprobanteDomicilio',
      contrato_arrendamiento:
        'detail.sections.documents.names.contratoArrendamiento',
      licencia_funcionamiento:
        'detail.sections.documents.names.licenciaFuncionamiento',
      carta_poder: 'detail.sections.documents.names.cartaPoder',
      acta_constitutiva: 'detail.sections.documents.names.actaConstitutiva',
      cedula_profesional: 'detail.sections.documents.names.cedulaProfesional',
      planos_arquitectonicos:
        'detail.sections.documents.names.planosArquitectonicos',
      memoria_calculo: 'detail.sections.documents.names.memoriaCalculo',
      estudio_impacto: 'detail.sections.documents.names.estudioImpacto',
    };
    const translationKey = documentNameMap[fieldName];
    if (translationKey) {
      return t(translationKey, fieldDescription || fieldName);
    }
    return (
      fieldDescription ||
      fieldName ||
      t('detail.sections.documents.names.defaultDocument')
    );
  };

  const statusMap: Record<number, string> = {
    0: 'Pendiente',
    1: 'Aprobada',
    2: 'Rechazada',
    3: 'Prevención',
    4: 'Licencia emitida',
  };

  useEffect(() => {
    async function fetchResolutions() {
      setLoadingResolutions(true);
      setErrorResolutions(null);
      try {
        const response = await fetch(
          `/v1/dependency_reviews/resolution_info/${encodeFolio(folio)}`,
          {
            headers: {
              Authorization: `Bearer ${user.access_token}`,
            },
          }
        );
        if (!response.ok) {
          throw new Error(t('detail.sections.resolutions.error'));
        }
        const res = await response.json();
        setResolutions(res.resolutions || []);
      } catch (err: any) {
        setErrorResolutions(t('detail.sections.resolutions.error'));
      } finally {
        setLoadingResolutions(false);
      }
    }
    fetchResolutions();
  }, [folio, user.access_token]);

  // Check license status when component loads
  useEffect(() => {
    async function fetchLicenseStatus() {
      if (procedure.status === 7 && user.access_token) {
        // Only check if procedure status is "License Issued" and we have token
        setLoadingLicenseStatus(true);
        try {
          const encodedFolio = btoa(folio);

          // Get API URL from window environment or fallback
          const API_URL =
            (window as any).ENV?.API_URL || 'http://localhost:8000';

          // Fetch license status directly
          const response = await fetch(
            `${API_URL}/v1/procedures/license/status/${encodedFolio}`,
            {
              method: 'GET',
              headers: {
                Authorization: `Bearer ${user.access_token}`,
              },
            }
          );

          if (response.ok) {
            const status = await response.json();
            setLicenseStatus(status);
          } else {
            // Set default status if there's an error
            setLicenseStatus({
              folio: folio,
              procedure_status: procedure.status || 0,
              license_exists: false,
              license_paid: false,
              license_file_exists: false,
              can_download: false,
            });
          }
        } catch (error) {
          // Set default status if there's an error
          setLicenseStatus({
            folio: folio,
            procedure_status: procedure.status || 0,
            license_exists: false,
            license_paid: false,
            license_file_exists: false,
            can_download: false,
          });
        } finally {
          setLoadingLicenseStatus(false);
        }
      } else {
        // Set a status indicating why we're not fetching
        setLicenseStatus({
          folio: folio,
          procedure_status: procedure.status || 0,
          license_exists: false,
          license_paid: false,
          license_file_exists: false,
          can_download: false,
        });
      }
    }
    fetchLicenseStatus();
  }, [folio, user.access_token, procedure.status]);

  const handleDownloadResolutionFile = async (res: any) => {
    if (!res.resolution_file || !res.id) return;
    setDownloadingFiles(prev => ({ ...prev, [res.id]: true }));
    setDownloadErrors(prev => ({ ...prev, [res.id]: null }));

    try {
      let fileUrl = res.resolution_file;
      if (!fileUrl.startsWith('http')) {
        const API_URL = (window as any).ENV?.API_URL || 'http://localhost:8000';
        fileUrl =
          API_URL.replace(/\/$/, '') +
          '/' +
          res.resolution_file.replace(/^\//, '');
      }
      const response = await fetch(fileUrl, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${user.access_token}`,
        },
      });
      if (!response.ok) {
        let errorMsg = `HTTP error! status: ${response.status}`;
        try {
          const errorText = await response.text();
          errorMsg += ` - ${errorText}`;
        } catch {
          // Ignore error parsing response text
        }
        setDownloadErrors(prev => ({ ...prev, [res.id]: errorMsg }));
        return;
      }
      const blob = await response.blob();
      let filename = `resolucion_${res.id}`;
      const disposition = response.headers.get('Content-Disposition');
      if (disposition && disposition.includes('filename=')) {
        const match = disposition.match(/filename="?([^";]+)"?/);
        if (match && match[1]) filename = match[1];
      } else if (res.resolution_file && res.resolution_file.split) {
        const parts = res.resolution_file.split('/');
        filename = parts[parts.length - 1] || filename;
      }
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error: any) {
      setDownloadErrors(prev => ({
        ...prev,
        [res.id]:
          error?.message || t('detail.sections.resolutions.downloadError'),
      }));
    } finally {
      setDownloadingFiles(prev => ({ ...prev, [res.id]: false }));
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-4">
            <Button variant="secondary" onClick={goBackToProcedures}>
              <ArrowLeft size={16} className="mr-2" />
              {t('detail.backToProcedures')}
            </Button>
          </div>
          <div className="flex items-center space-x-2">
            <Link to={`/procedures/${btoa(folio)}/edit`}>
              <Button variant="outline">
                <FileText size={16} className="mr-2" />
                {t('detail.editProcedure')}
              </Button>
            </Link>
            <Button variant="secondary" onClick={handleDownloadPDF}>
              <Download size={16} className="mr-2" />
              {t('detail.downloadPdf')}
            </Button>
            {/* License Download Button - Only show if license is available */}
            {licenseStatus?.can_download && (
              <Button
                variant="primary"
                onClick={handleDownloadLicense}
                disabled={downloadingLicense}
              >
                {downloadingLicense ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    {t('detail.downloadingLicense')}
                  </>
                ) : (
                  <>
                    <Download size={16} className="mr-2" />
                    {t('detail.downloadLicense')}
                  </>
                )}
              </Button>
            )}
            <Button
              variant="secondary"
              onClick={() => setShowDocumentsModal(true)}
            >
              <Eye size={16} className="mr-2" />
              {t('detail.viewFiles')}
            </Button>
          </div>
        </div>
        <div className="border-b border-gray-200 pb-4 mb-4">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {t('detail.title')}: {folio}
          </h1>
          <div className="flex items-center space-x-4">
            <StatusBadge status={procedure.status} t={t} />
            <span className="text-sm text-gray-500">
              {t('detail.sections.general.procedureType')}:{' '}
              {getTranslatedProcedureType(procedure.procedure_type)}
            </span>
            <span className="text-sm text-gray-500">
              {t('detail.sections.general.created')}:{' '}
              {formatDate(procedure.created_at)}
            </span>
          </div>
        </div>
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3">
            {t('detail.progress.title')}
          </h3>
          <WorkflowIndicator
            procedure={procedure}
            t={t}
            workflowStatus={workflowStatus}
          />
        </div>
      </div>
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center mb-4">
          <FileText className="h-5 w-5 text-blue-600 mr-2" />
          <h2 className="text-xl font-semibold">
            {t('detail.sections.general.title')}
          </h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div>
            <label className="text-sm font-medium text-gray-500">
              {t('detail.sections.general.folio')}
            </label>
            <p className="text-gray-900">{procedure.folio || '--'}</p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-500">
              {t('detail.sections.general.type')}
            </label>
            <p className="text-gray-900">
              {getTranslatedProcedureType(procedure.procedure_type)}
            </p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-500">
              {t('detail.sections.general.licenseStatus')}
            </label>
            <p className="text-gray-900">
              <StatusBadge status={procedure.status} t={t} />
            </p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-500">
              {t('detail.sections.general.startDate')}
            </label>
            <p className="text-gray-900">{formatDate(procedure.created_at)}</p>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-500">
              {t('detail.sections.general.lastUpdate')}
            </label>
            <p className="text-gray-900">{formatDate(procedure.updated_at)}</p>
          </div>
        </div>
      </div>

      {/* Información del Tramitante */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center mb-4">
          <User className="h-5 w-5 text-blue-600 mr-2" />
          <h2 className="text-xl font-semibold">
            {t('detail.sections.applicant.title')}
          </h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {procedure.official_applicant_name && (
            <div>
              <label className="text-sm font-medium text-gray-500">
                {t('detail.sections.applicant.name')}
              </label>
              <p className="text-gray-900">
                {procedure.official_applicant_name}
              </p>
            </div>
          )}

          {/* Show information from form answers */}
          {fieldsWithValues
            .filter(field => {
              const fieldName = field.name?.toLowerCase() || '';
              return [
                'quien_tramita',
                'propietario_rad',
                'arrendatario_rad',
                'carta_poder_rad',
                'nombre_solicitante',
                'applicant_name',
              ].includes(fieldName);
            })
            .map((field, index) => (
              <div key={field.id || index}>
                <label className="text-sm font-medium text-gray-500">
                  {field.description ||
                    field.name ||
                    t('detail.sections.applicant.field')}
                </label>
                <div className="text-gray-900">{formatFieldValue(field)}</div>
              </div>
            ))}

          {!procedure.official_applicant_name &&
            fieldsWithValues.filter(field => {
              const fieldName = field.name?.toLowerCase() || '';
              return [
                'quien_tramita',
                'propietario_rad',
                'arrendatario_rad',
                'carta_poder_rad',
                'nombre_solicitante',
                'applicant_name',
              ].includes(fieldName);
            }).length === 0 && (
              <div className="col-span-full">
                <p className="text-gray-500 italic">
                  {t('detail.sections.applicant.noInfo')}
                </p>
              </div>
            )}
        </div>
      </div>

      {Object.keys(fieldsBySection).length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center mb-6">
            <FileText className="h-6 w-6 text-blue-600 mr-3" />
            <h2 className="text-2xl font-semibold">
              {t('detail.sections.dynamicFields.title')}
            </h2>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {(Object.entries(fieldsBySection) as [string, DynamicField[]][])
              .sort(([a], [b]) => parseInt(a) - parseInt(b))
              .map(([sectionId, fields]) => {
                const sectionInfo = getSectionInfo(sectionId);
                const SectionIcon = sectionInfo.icon;
                return (
                  <div
                    key={sectionId}
                    className="border border-gray-200 rounded-lg p-4"
                  >
                    <div className="flex items-center mb-4">
                      <SectionIcon className="h-5 w-5 text-blue-600 mr-2" />
                      <h3 className="text-lg font-semibold">
                        {sectionInfo.title}
                      </h3>
                    </div>
                    <div className="space-y-3">
                      {fields
                        .filter(field => field.value && field.value !== '')
                        .map((field, index) => (
                          <div key={field.id || index} className="space-y-1">
                            <label className="text-sm font-medium text-gray-700 block">
                              {field.description ||
                                field.name ||
                                `${t('detail.dynamicFields.question')} ${index + 1}`}
                              {field.required && (
                                <span className="text-red-500 ml-1">*</span>
                              )}
                            </label>
                            <div className="text-gray-900">
                              {formatFieldValue(field)}
                            </div>
                          </div>
                        ))}
                      {fields.filter(field => field.value && field.value !== '')
                        .length === 0 && (
                        <p className="text-gray-500 text-sm italic">
                          {t('edit.form.noFieldsInSection')}
                        </p>
                      )}
                    </div>
                  </div>
                );
              })}
          </div>
        </div>
      )}
      {procedure.reason && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center mb-4">
            <AlertCircle className="h-5 w-5 text-yellow-600 mr-2" />
            <h2 className="text-xl font-semibold">
              {t('detail.sections.observations.title')}
            </h2>
          </div>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-gray-900">{procedure.reason}</p>
          </div>
        </div>
      )}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center mb-4">
          <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
          <h2 className="text-xl font-semibold">
            {t('detail.sections.resolutions.title')}
          </h2>
        </div>
        {loadingResolutions ? (
          <div className="text-gray-500">
            {t('detail.sections.resolutions.loading')}
          </div>
        ) : errorResolutions ? (
          <div className="text-red-500">{errorResolutions}</div>
        ) : resolutions.length === 0 ? (
          <div className="text-gray-500">
            {t('detail.sections.resolutions.noResolutions')}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {t('detail.sections.resolutions.table.headers.date')}
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {t('detail.sections.resolutions.table.headers.status')}
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {t('detail.sections.resolutions.table.headers.text')}
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {t('detail.sections.resolutions.table.headers.file')}
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {t('detail.sections.resolutions.table.headers.user')}
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {resolutions.map((res, idx) => (
                  <tr key={res.id || idx}>
                    <td className="px-4 py-2 whitespace-wrap">
                      {formatDate(res.created_at)}
                    </td>
                    <td className="px-4 py-2 whitespace-wrap">
                      {statusMap[res.resolution_status] ||
                        res.resolution_status}
                    </td>
                    <td className="px-4 py-2 whitespace-wrap max-w-xs">
                      {res.resolution_text || '--'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap">
                      {res.resolution_file ? (
                        <>
                          <Button
                            onClick={() => handleDownloadResolutionFile(res)}
                            variant="outline"
                            size="sm"
                            className="px-2 py-1 text-blue-600 bg-blue-50 border-blue-200 hover:bg-blue-100 disabled:opacity-50"
                            disabled={!!downloadingFiles[res.id]}
                            title={t(
                              'detail.sections.resolutions.table.actions.downloadTitle'
                            )}
                          >
                            {downloadingFiles[res.id] ? (
                              <span className="animate-spin mr-2">⏳</span>
                            ) : (
                              <Download size={16} className="mr-1" />
                            )}
                            {t(
                              'detail.sections.resolutions.table.actions.download'
                            )}
                          </Button>
                          {downloadErrors[res.id] && (
                            <span className="ml-2 text-xs text-red-500">
                              {downloadErrors[res.id]}
                            </span>
                          )}
                        </>
                      ) : (
                        '--'
                      )}
                    </td>
                    <td className="px-4 py-2 whitespace-wrap">
                      {res.user_name || '--'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      <DocumentsModal />
    </div>
  );
}
