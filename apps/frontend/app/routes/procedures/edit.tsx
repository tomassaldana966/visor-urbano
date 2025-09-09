import { useState } from 'react';
import type { LoaderFunctionArgs, ActionFunctionArgs } from 'react-router';
import { useLoaderData, Link } from 'react-router';
import { useTranslation } from 'react-i18next';
import { requireUser } from '../../utils/auth/utils';
import {
  getProcedureByFolio,
  getDynamicFieldsByFolio,
  validateProcedureCapture,
  updateProcedureByFolio,
  updateProcedureAnswers,
} from '../../utils/api/api.server';
import { submitProcedureForReview } from '../../utils/api/procedures';
import { Button } from '../../components/Button/Button';
import { Accordion } from '../../components/Accordion/Accordion';
import { SectionForm, StatusBadge } from '../../components/Procedures';
import {
  dynamicFieldsResponseSchema,
  type DynamicField,
} from '../../schemas/dynamicFields';
import {
  FileText,
  Download,
  Eye,
  ArrowLeft,
  UserCheck,
  User,
  MapPin,
  Building,
  Send,
  AlertCircle,
  CheckCircle,
  X,
} from 'lucide-react';
import { z } from 'zod';
import { useProcedurePDF } from '../../hooks/useProcedurePDF';

export const handle = {
  title: 'procedures:edit.title',
  breadcrumb: 'procedures:edit.breadcrumb',
};

// Validation schema for step data
const stepValidationSchema = z.object({
  step: z.number().min(1),
  fields: z.record(z.unknown()),
});

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

    // Decode the folio from Base64 since it comes encoded from the URL
    let decodedFolio: string;
    try {
      decodedFolio = atob(folio);
    } catch (error) {
      // If decoding fails, assume it's already decoded
      decodedFolio = folio;
    }

    // Get procedure details and dynamic fields
    const [procedure, dynamicFieldsResponse] = await Promise.all([
      getProcedureByFolio(authToken, decodedFolio),
      getDynamicFieldsByFolio(authToken, decodedFolio),
    ]);

    // Validate the dynamic fields response
    const fieldsResult = dynamicFieldsResponseSchema.safeParse(
      dynamicFieldsResponse
    );

    if (!fieldsResult.success) {
      throw new Response('Invalid fields data', { status: 500 });
    }

    const [dynamicFields, staticFields, licenseInfo] = fieldsResult.data;

    return {
      user,
      procedure,
      folio: decodedFolio,
      dynamicFields,
      staticFields,
      licenseInfo,
    };
  } catch (error) {
    // Check if it's a specific HTTP error (already a Response)
    if (error instanceof Response) {
      throw error;
    }

    // Handle API errors with detailed status information
    if (error instanceof Error) {
      const errorMessage = error.message.toLowerCase();

      // Authentication errors
      if (
        errorMessage.includes('unauthorized') ||
        errorMessage.includes('authentication required') ||
        errorMessage.includes('401')
      ) {
        throw new Response('Authentication required to edit procedures', {
          status: 401,
        });
      }

      // Authorization/Permission errors
      if (
        errorMessage.includes('access denied') ||
        errorMessage.includes('forbidden') ||
        errorMessage.includes('403')
      ) {
        throw new Response(
          'Access denied: You can only edit your own procedures',
          { status: 403 }
        );
      }

      // Procedure not found errors
      if (
        errorMessage.includes('not found') ||
        errorMessage.includes('404') ||
        errorMessage.includes('procedure with folio')
      ) {
        throw new Response(`Procedure not found: ${error.message}`, {
          status: 404,
        });
      }

      // Server/API errors
      if (
        errorMessage.includes('failed to fetch') ||
        errorMessage.includes('500') ||
        errorMessage.includes('internal server error')
      ) {
        const statusMatch = error.message.match(/(\d{3})/);
        const status = statusMatch ? parseInt(statusMatch[1]) : 500;
        throw new Response(
          `Server error while loading procedure: ${error.message}`,
          { status }
        );
      }

      // Schema validation errors
      if (
        errorMessage.includes('invalid fields data') ||
        errorMessage.includes('schema validation') ||
        errorMessage.includes('invalid response format')
      ) {
        throw new Response(`Data validation error: ${error.message}`, {
          status: 500,
        });
      }

      // Network/Connection errors
      if (
        errorMessage.includes('fetch') ||
        errorMessage.includes('network') ||
        errorMessage.includes('connection')
      ) {
        throw new Response(
          `Network error: Unable to connect to server. ${error.message}`,
          { status: 503 }
        );
      }

      // Generic error with the original message
      throw new Response(`Error loading procedure: ${error.message}`, {
        status: 500,
      });
    }

    // Fallback for completely unknown errors
    throw new Response(
      'An unexpected error occurred while loading the procedure',
      { status: 500 }
    );
  }
}

export async function action({ request, params }: ActionFunctionArgs) {
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

    const formData = await request.formData();
    const data = Object.fromEntries(formData);
    const actionType = data._action as string;

    // Decode folio
    let decodedFolio: string;
    try {
      decodedFolio = atob(folio);
    } catch (error) {
      decodedFolio = folio;
    }

    if (actionType === 'validate') {
      // Parse and validate the step data for validation only
      const stepData = stepValidationSchema.parse({
        step: parseInt(data.step as string),
        fields: JSON.parse(data.fields as string),
      });

      // Validate the capture with the API
      const result = await validateProcedureCapture(authToken, {
        folio: decodedFolio,
        ...stepData,
      });

      return {
        success: true,
        step: stepData.step,
        message: 'Section validated successfully',
        data: result,
      };
    } else if (actionType === 'save') {
      // Parse the section data for saving
      const sectionData = JSON.parse(data.sectionData as string);
      const step = parseInt(data.step as string);

      // Get dynamic fields for mapping context
      const dynamicFieldsResponse = await getDynamicFieldsByFolio(
        authToken,
        decodedFolio
      );
      const [dynamicFields, staticFields] = dynamicFieldsResponse;

      // Create a mapping of field IDs to field names from both dynamic and static fields
      const fieldIdToName: Record<string, string> = {};

      // Process dynamic fields
      dynamicFields.forEach(field => {
        if (field.id && field.name) {
          fieldIdToName[field.id.toString()] = field.name;
        }
      });

      // Process static fields
      staticFields.forEach(field => {
        if (field.id && field.name) {
          fieldIdToName[field.id.toString()] = field.name;
        }
      });

      // Transform the form field data to procedure fields
      // Create a mapping function based on field names
      const mapDynamicFieldsToModel = (
        formData: Record<string, any>,
        dynamicFields: any[],
        staticFields: any[]
      ): Record<string, any> => {
        const mappedData: Record<string, any> = {};

        // Common field name mappings from dynamic field names to Procedure model fields
        const fieldMappings: Record<string, string> = {
          // Applicant information
          nombre_solicitante: 'official_applicant_name',
          nombre_propietario: 'official_applicant_name',
          nombre_aplicante: 'official_applicant_name',
          solicitante: 'official_applicant_name',

          // Address information
          calle: 'street',
          direccion: 'street',
          numero_exterior: 'exterior_number',
          numero_interior: 'interior_number',
          colonia: 'neighborhood',
          barrio: 'neighborhood',
          referencia: 'reference',
          municipio: 'municipality_id',

          // Business information
          nombre_negocio: 'business_name',
          giro_comercial: 'business_sector',
          tipo_giro: 'business_sector',
          actividad: 'business_activity',
          descripcion_actividad: 'business_activity',
          superficie: 'area',
          area: 'area',
          horario_funcionamiento: 'operating_hours',
          numero_empleados: 'employee_count',

          // Establishment information (for business licenses)
          nombre_establecimiento: 'establishment_name',
          direccion_establecimiento: 'establishment_address',
          telefono_establecimiento: 'establishment_phone',
          superficie_establecimiento: 'establishment_area',

          // Common fields that might map directly
          folio: 'folio',
          tipo_tramite: 'procedure_type',
          estatus: 'license_status',
          razon: 'reason',
        };

        // Process each form field
        Object.entries(formData).forEach(([fieldId, value]) => {
          const fieldName = fieldIdToName[fieldId];

          if (
            fieldName &&
            value !== null &&
            value !== undefined &&
            value !== ''
          ) {
            // Check if we have a specific mapping for this field name
            const mappedFieldName = fieldMappings[fieldName.toLowerCase()];

            if (mappedFieldName) {
              // Map to the procedure model field
              mappedData[mappedFieldName] = value;
            } else {
              // For unmapped fields, try common patterns or store as-is
              // Check if this field name contains common patterns
              const lowerFieldName = fieldName.toLowerCase();

              if (
                lowerFieldName.includes('nombre') ||
                lowerFieldName.includes('name')
              ) {
                // Check if it's establishment name specifically
                if (lowerFieldName.includes('establecimiento')) {
                  mappedData['establishment_name'] = value;
                } else {
                  mappedData['official_applicant_name'] = value;
                }
              } else if (
                lowerFieldName.includes('direccion') &&
                lowerFieldName.includes('establecimiento')
              ) {
                mappedData['establishment_address'] = value;
              } else if (
                lowerFieldName.includes('telefono') &&
                lowerFieldName.includes('establecimiento')
              ) {
                mappedData['establishment_phone'] = value;
              } else if (
                lowerFieldName.includes('superficie') &&
                lowerFieldName.includes('establecimiento')
              ) {
                mappedData['establishment_area'] = value;
              } else if (
                lowerFieldName.includes('tipo') &&
                lowerFieldName.includes('giro')
              ) {
                mappedData['business_sector'] = value;
              } else if (
                lowerFieldName.includes('descripcion') &&
                lowerFieldName.includes('actividad')
              ) {
                mappedData['business_activity'] = value;
              } else if (
                lowerFieldName.includes('horario') &&
                lowerFieldName.includes('funcionamiento')
              ) {
                mappedData['operating_hours'] = value;
              } else if (
                lowerFieldName.includes('numero') &&
                lowerFieldName.includes('empleados')
              ) {
                mappedData['employee_count'] = value;
              } else if (
                lowerFieldName.includes('calle') ||
                lowerFieldName.includes('street')
              ) {
                mappedData['street'] = value;
              } else if (
                lowerFieldName.includes('colonia') ||
                lowerFieldName.includes('neighborhood')
              ) {
                mappedData['neighborhood'] = value;
              } else if (
                lowerFieldName.includes('municipio') ||
                lowerFieldName.includes('municipality')
              ) {
                // Try to parse as number for municipality_id
                const numValue = parseInt(value as string);
                if (!isNaN(numValue)) {
                  mappedData['municipality_id'] = numValue;
                }
              } else {
                // Store with original field name for debugging/future use
                console.warn(
                  `Unmapped field: ${fieldName} -> storing as dynamic_${fieldName}`
                );
                mappedData[`dynamic_${fieldName}`] = value;
              }
            }
          }
        });

        return mappedData;
      };

      // Map the form data to procedure fields
      const procedureUpdateData = mapDynamicFieldsToModel(
        sectionData,
        dynamicFields,
        staticFields
      );

      try {
        // For dynamic fields (step 2+), use the new answers endpoint
        if (step >= 2) {
          // Convert field IDs back to field names for the API
          const fieldsForApi: Record<string, any> = {};
          Object.entries(sectionData).forEach(([fieldId, value]) => {
            const fieldName = fieldIdToName[fieldId];
            if (
              fieldName &&
              value !== null &&
              value !== undefined &&
              value !== ''
            ) {
              fieldsForApi[fieldName] = value;
            }
          });

          // Use updateProcedureAnswers to save the field answers
          const result = await updateProcedureAnswers(
            authToken,
            decodedFolio,
            fieldsForApi
          );

          const updatedProcedure = await getProcedureByFolio(
            authToken,
            decodedFolio
          );

          return {
            success: true,
            step: step,
            message: 'Section saved successfully',
            procedure: updatedProcedure,
            reload: true,
            savedData: sectionData, // Return original field data for immediate UI update
          };
        } else {
          // For basic procedure data (step 1), use the procedure update endpoint
          const updatedProcedure = await updateProcedureByFolio(
            authToken,
            decodedFolio,
            procedureUpdateData
          );

          return {
            success: true,
            step: step,
            message: 'Section saved successfully',
            procedure: updatedProcedure,
            reload: true,
            savedData: procedureUpdateData,
          };
        }
      } catch (updateError) {
        console.error('Update procedure error:', updateError);
        return {
          success: false,
          step: step,
          error:
            updateError instanceof Error
              ? updateError.message
              : 'Error desconocido al actualizar el procedimiento',
        };
      }
    }

    return {
      success: false,
      error: 'Invalid action type: ' + actionType,
    };
  } catch (error) {
    console.error('Action error:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
}

export default function ProcedureEditPage() {
  const { procedure, folio, dynamicFields, staticFields, licenseInfo, user } =
    useLoaderData<typeof loader>();
  const { t } = useTranslation(['procedures', 'common', 'procedureApprovals']);
  const [expandedSections, setExpandedSections] = useState<string[]>(['1']);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const { generatePDF } = useProcedurePDF();

  const handleSectionToggle = (sectionId: string) => {
    setExpandedSections(prev =>
      prev.includes(sectionId)
        ? prev.filter(id => id !== sectionId)
        : [...prev, sectionId]
    );
  };

  const handleDownloadPDF = async () => {
    try {
      await generatePDF(procedure as any, fieldsBySection);
    } catch (error) {
      console.error('Error downloading PDF:', error);
      // Could add a toast notification here
    }
  };

  const handleSubmitForReview = async () => {
    setIsSubmitting(true);
    setSubmitError(null);

    if (!folio) {
      setSubmitError(t('edit.submitForReview.errors.noFolio'));
      setIsSubmitting(false);
      return;
    }

    if (!user.access_token) {
      setSubmitError(t('edit.submitForReview.errors.noToken'));
      setIsSubmitting(false);
      return;
    }

    const validFolio: string = folio;
    const validToken: string = user.access_token;

    try {
      const result = await submitProcedureForReview(validToken, validFolio);
      setSubmitSuccess(true);
      setShowSubmitModal(false);

      // Optionally reload the page to show updated status
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    } catch (error) {
      console.error('Error submitting procedure for review:', error);

      try {
        const errorData = JSON.parse(
          error instanceof Error ? error.message : '{}'
        );

        if (errorData.type === 'validation' && errorData.missing_fields) {
          const missingFieldsList = errorData.missing_fields
            .map((field: any) => field.description || field.name)
            .join(', ');
          setSubmitError(
            `${t('edit.submitForReview.errors.missingFields')} ${missingFieldsList}`
          );
        } else if (errorData.type === 'validation') {
          setSubmitError(
            errorData.message ||
              t('edit.submitForReview.errors.validationFailed')
          );
        } else if (errorData.type === 'unauthorized') {
          setSubmitError(t('edit.submitForReview.errors.unauthorized'));
        } else if (errorData.type === 'not_found') {
          setSubmitError(t('edit.submitForReview.errors.notFound'));
        } else {
          setSubmitError(t('edit.submitForReview.errors.serverError'));
        }
      } catch {
        setSubmitError(
          error instanceof Error
            ? error.message
            : t('edit.submitForReview.errors.serverError')
        );
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  // Helper function to get translated procedure type
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

  const formatAddress = () => {
    const parts = [
      procedure.street,
      procedure.exterior_number,
      procedure.interior_number && `Int. ${procedure.interior_number}`,
      procedure.neighborhood,
      procedure.municipality,
    ].filter(Boolean);

    return parts.length > 0 ? parts.join(', ') : t('detail.status.noAddress');
  };

  // Combine dynamic and static fields
  // Transform static fields to ensure they match the expected DynamicField structure
  const transformedStaticFields = staticFields.map(staticField => ({
    ...staticField,
    // Ensure required properties are set correctly
    step: staticField.step || 1,
    sequence: staticField.sequence || 0,
    required:
      typeof staticField.required === 'number'
        ? staticField.required === 1
        : Boolean(staticField.required),
  }));

  const allFields = [...dynamicFields, ...transformedStaticFields]; // Create a reverse mapping from procedure model fields to dynamic field names
  const procedureToFieldMapping: Record<string, string> = {
    // Establishment information
    establishment_name: 'nombre_establecimiento',
    establishment_address: 'direccion_establecimiento',
    establishment_phone: 'telefono_establecimiento',
    establishment_area: 'superficie_establecimiento',

    // Applicant information
    official_applicant_name: 'nombre_solicitante',

    // Address information
    street: 'calle',
    exterior_number: 'numero_exterior',
    interior_number: 'numero_interior',
    neighborhood: 'colonia',
    municipality_id: 'municipio',

    // Business information
    business_name: 'nombre_negocio',
    business_sector: 'giro_comercial',
    business_activity: 'actividad',
    operating_hours: 'horario_funcionamiento',
    employee_count: 'numero_empleados',
    area: 'superficie',
  };

  // Populate field values from procedure data
  const fieldsWithValues = allFields.map(field => {
    let fieldValue = field.value;

    // Try to find a value from the procedure data
    const fieldName = field.name?.toLowerCase();
    if (fieldName) {
      // Check if this field maps to a procedure field
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

  // Only allow fields with valid field_type values
  const allowedFieldTypes = [
    'input',
    'file',
    'multifile',
    'radio',
    'select',
    'textarea',
  ] as const;

  function isValidDynamicField(field: any): field is DynamicField {
    const isValid =
      typeof field === 'object' &&
      field !== null &&
      'field_type' in field &&
      allowedFieldTypes.includes(field.field_type);

    return isValid;
  }

  // Group fields by step/section
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

  // Helper function to get section title and icon
  const getSectionInfo = (sectionId: string) => {
    // Map section IDs to meaningful titles and icons based on actual content
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
        description: `Sección ${sectionId} del formulario`,
      }
    );
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-4">
            <Link to="/procedures">
              <Button variant="secondary">
                <ArrowLeft size={16} className="mr-2" />
                {t('edit.actions.backToProcedures')}
              </Button>
            </Link>
          </div>
          <div className="flex items-center space-x-2">
            <Link to={`/procedures/${btoa(folio)}/detail`}>
              <Button variant="outline">
                <Eye size={16} className="mr-2" />
                {t('edit.actions.viewDetails')}
              </Button>
            </Link>
            {/* Show Submit for Review button if procedure is in draft (0), in review (1), or prevention (3) status */}
            {(procedure.status === 0 ||
              procedure.status === 1 ||
              procedure.status === 3) && (
              <Button
                variant="primary"
                onClick={() => setShowSubmitModal(true)}
                disabled={isSubmitting}
              >
                <Send size={16} className="mr-2" />
                {procedure.status === 3
                  ? t('edit.actions.resubmitForReview')
                  : procedure.status === 1
                    ? t('edit.actions.updateSubmission')
                    : t('edit.actions.submitForReview')}
              </Button>
            )}
            <Button variant="secondary" onClick={handleDownloadPDF}>
              <Download size={16} className="mr-2" />
              {t('edit.actions.downloadPdf')}
            </Button>
          </div>
        </div>

        <div className="border-b border-gray-200 pb-4 mb-4">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {t('edit.title')}: {folio}
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

        {/* Basic Info Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <label className="font-medium text-gray-500">
              {t('detail.sections.applicant.name')}
            </label>
            <p className="text-gray-900">
              {(() => {
                return (
                  procedure.official_applicant_name ||
                  procedure.official_applicant_name ||
                  '--'
                );
              })()}
            </p>
          </div>
          <div>
            <label className="font-medium text-gray-500">
              {t('detail.sections.property.address')}
            </label>
            <p className="text-gray-900">{formatAddress()}</p>
          </div>
          <div>
            <label className="font-medium text-gray-500">
              {t('detail.sections.general.lastUpdate')}
            </label>
            <p className="text-gray-900">{formatDate(procedure.updated_at)}</p>
          </div>
        </div>
      </div>

      {/* Dynamic Form Sections */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center mb-6">
          <FileText className="h-6 w-6 text-blue-600 mr-3" />
          <h2 className="text-2xl font-semibold">
            {t('edit.sections.formSections')}
          </h2>
        </div>

        {Object.keys(fieldsBySection).length === 0 ? (
          <div className="text-center py-12">
            <FileText size={64} className="mx-auto mb-4 text-gray-300" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {t('edit.form.noFieldsAvailable')}
            </h3>
            <p className="text-gray-500">
              {t('edit.form.noFieldsDescription')}
            </p>
          </div>
        ) : (
          <Accordion
            type="multiple"
            value={expandedSections}
            onValueChange={setExpandedSections}
            className="space-y-4"
          >
            {Object.entries(fieldsBySection)
              .sort(([a], [b]) => parseInt(a) - parseInt(b))
              .map(([sectionId, fields]) => (
                <SectionForm
                  key={sectionId}
                  sectionId={sectionId}
                  fields={fields}
                  sectionTitle={getSectionInfo(sectionId).title}
                  sectionIcon={getSectionInfo(sectionId).icon}
                  sectionDescription={getSectionInfo(sectionId).description}
                  folio={folio}
                  isExpanded={expandedSections.includes(sectionId)}
                  onToggle={() => handleSectionToggle(sectionId)}
                  t={t}
                  procedureId={procedure.id}
                  authToken={user.access_token}
                />
              ))}
          </Accordion>
        )}
      </div>

      {/* Submit for Review Modal */}
      {showSubmitModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="p-6">
              <div className="flex items-center mb-4">
                <Send className="h-6 w-6 text-blue-600 mr-3" />
                <h3 className="text-lg font-semibold text-gray-900">
                  {t('edit.submitForReview.confirmTitle')}
                </h3>
              </div>

              <p className="text-gray-600 mb-6">
                {t('edit.submitForReview.confirmMessage')}
              </p>

              {submitError && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-center">
                    <AlertCircle className="h-5 w-5 text-red-600 mr-2" />
                    <p className="text-red-700 text-sm">{submitError}</p>
                  </div>
                </div>
              )}

              <div className="flex space-x-3">
                <Button
                  variant="outline"
                  onClick={() => {
                    setShowSubmitModal(false);
                    setSubmitError(null);
                  }}
                  disabled={isSubmitting}
                  className="flex-1"
                >
                  {t('edit.submitForReview.cancelButton')}
                </Button>
                <Button
                  variant="primary"
                  onClick={handleSubmitForReview}
                  disabled={isSubmitting}
                  className="flex-1"
                >
                  {isSubmitting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      {t('edit.submitForReview.submitting')}
                    </>
                  ) : (
                    <>
                      <Send size={16} className="mr-2" />
                      {t('edit.submitForReview.confirmButton')}
                    </>
                  )}
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Success Modal */}
      {submitSuccess && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="p-6 text-center">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
                <CheckCircle className="h-6 w-6 text-green-600" />
              </div>

              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {t('edit.submitForReview.title')}
              </h3>

              <p className="text-gray-600 mb-6">
                {t('edit.submitForReview.success')}
              </p>

              <Button
                variant="primary"
                onClick={() => setSubmitSuccess(false)}
                className="w-full"
              >
                {t('common:ok')}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
