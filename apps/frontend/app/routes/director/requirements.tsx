import type { LoaderFunctionArgs, ActionFunctionArgs } from 'react-router';
import React, { useState, useEffect } from 'react';
import {
  useLoaderData,
  Form,
  useActionData,
  useNavigation,
} from 'react-router';
import { useTranslation } from 'react-i18next';
import { z } from 'zod';
import { zx } from 'zodix';
import { requireAuth, getAccessToken } from '../../utils/auth/auth.server';
import { checkDirectorPermissions } from '../../utils/auth/director';
import { DataTable } from '../../components/Director/Charts/DataTable';
import {
  getFields,
  createField,
  updateField,
} from '../../utils/api/api.server';
import { dynamicFieldSchema } from '../../schemas/requirements';
import { Select, Option } from '../../components/Select/Select';
import { Input } from '../../components/Input/Input';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../../components/Dialog/Dialog';
import {
  FileText,
  Plus,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Filter,
  X,
} from 'lucide-react';

type DynamicField = z.infer<typeof dynamicFieldSchema>;

// Form validation schemas
const createRequirementSchema = z.object({
  _intent: z.literal('create'),
  field_type: z.enum(['input', 'file', 'boolean', 'select', 'radio']),
  description: z.string().min(1, 'validation.titleRequired'),
  description_rec: z.string().optional(),
  rationale: z.string().optional(),
  options: z.string().optional(),
  options_description: z.string().optional(),
  step: z.string().transform(val => (val ? parseInt(val, 10) : null)),
  sequence: z
    .string()
    .optional()
    .transform(val => (val ? parseInt(val, 10) : null)),
  procedure_type: z.string().min(1, 'validation.procedureTypeRequired'),
  required: z.string(),
  // Advanced conditional parameters
  property_condition: z.string().optional(),
  property_meters: z.string().optional(),
  activity_condition: z.string().optional(),
  activity_meters: z.string().optional(),
  applicant_character_condition: z.string().optional(),
  person_type_condition: z.string().optional(),
  alcohol_condition: z.string().optional(),
  all_conditions: z.string().optional(),
  check_dependency: z.string().optional(),
  selected_dependency: z.string().optional(),
});

const editRequirementSchema = z.object({
  _intent: z.literal('edit'),
  id: z.string().transform(val => parseInt(val, 10)),
  field_type: z.enum(['input', 'file', 'boolean', 'select', 'radio']),
  description: z.string().min(1, 'validation.titleRequired'),
  description_rec: z.string().optional(),
  rationale: z.string().optional(),
  options: z.string().optional(),
  options_description: z.string().optional(),
  step: z.string().transform(val => (val ? parseInt(val, 10) : null)),
  sequence: z
    .string()
    .optional()
    .transform(val => (val ? parseInt(val, 10) : null)),
  procedure_type: z.string().min(1, 'validation.procedureTypeRequired'),
  required: z.string(),
});

const toggleStatusSchema = z.object({
  _intent: z.literal('toggleStatus'),
  id: z.string().transform(val => parseInt(val, 10)),
  status: z.string().transform(val => parseInt(val, 10)),
});

const requirementFormSchema = z.discriminatedUnion('_intent', [
  createRequirementSchema,
  editRequirementSchema,
  toggleStatusSchema,
]);

// Action function to handle form submissions
export async function action({ request }: ActionFunctionArgs) {
  const authToken = await getAccessToken(request);

  if (!authToken) {
    return {
      success: false,
      error: 'messages.tokenUnavailable',
    };
  }

  const user = await requireAuth(request);

  if (!checkDirectorPermissions(user)) {
    return {
      success: false,
      error: 'messages.accessDenied',
    };
  }

  try {
    // Use zodix to validate form data
    const result = await zx.parseFormSafe(request, requirementFormSchema);

    if (!result.success) {
      return {
        success: false,
        error: 'messages.formInvalid',
        fieldErrors: result.error.flatten().fieldErrors,
      };
    }

    const data = result.data;

    if (data._intent === 'create') {
      // Build visible condition string if conditional requirements
      let visibleCondition = '';
      if (data.required === 'conditional') {
        const conditions: string[] = [];
        const conditionOperator = data.all_conditions === 'true' ? '&&' : '||';

        if (data.property_condition !== '0' && data.property_meters) {
          conditions.push(
            `(/superficie_propiedad ${data.property_condition} ${data.property_meters})`
          );
        }

        if (data.activity_condition !== '0' && data.activity_meters) {
          conditions.push(
            `(/superficie_actividad ${data.activity_condition} ${data.activity_meters})`
          );
        }

        if (data.applicant_character_condition) {
          const characterArray = data.applicant_character_condition
            .split(',')
            .filter(Boolean);
          if (characterArray.length > 0) {
            const characterConditions = characterArray
              .map(char => `/caracter_solicitante == '${char.trim()}'`)
              .join(' || ');
            conditions.push(`(${characterConditions})`);
          }
        }

        if (data.person_type_condition) {
          const typeArray = data.person_type_condition
            .split(',')
            .filter(Boolean);
          if (typeArray.length > 0) {
            const typeConditions = typeArray
              .map(type => `/tipo_persona == '${type.trim()}'`)
              .join(' || ');
            conditions.push(`(${typeConditions})`);
          }
        }

        if (data.alcohol_condition !== '0') {
          const alcoholOp = data.alcohol_condition === '5' ? '<=' : '==';
          conditions.push(
            `(/check_alcohol ${alcoholOp} '${data.alcohol_condition}')`
          );
        }

        if (conditions.length > 0) {
          const conditionString = conditions.join(` ${conditionOperator} `);
          visibleCondition = btoa(
            unescape(encodeURIComponent(conditionString))
          );
        }
      }

      // Generate unique field name based on description
      const fieldName = data.description
        ? data.description.replace(/[^a-zA-Z0-9]/g, '').toLowerCase() +
          'visor' +
          Date.now()
        : 'field' + Date.now();

      // Validate form data
      const fieldData = {
        name: fieldName,
        field_type: data.field_type as DynamicField['field_type'],
        description: data.description ?? null,
        description_rec: data.description_rec ?? null,
        rationale: data.rationale ?? null,
        options: data.options ?? null,
        options_description: data.options_description ?? null,
        step: data.step,
        sequence: data.sequence,
        procedure_type: data.procedure_type ?? null,
        visible_condition: visibleCondition || null,
        affected_field: null,
        dependency_condition:
          data.check_dependency === 'true' && data.selected_dependency
            ? data.selected_dependency
            : null,
        trade_condition: null,
        required: data.required === 'true' || data.required === 'conditional',
        required_official: true,
        editable: true,
        static_field: false,
        status: 1,
        municipality_id: null,
      };

      // Create field using API
      const newField = await createField(authToken, fieldData);

      return {
        success: true,
        message: 'messages.success',
        field: newField,
      };
    }

    if (data._intent === 'toggleStatus') {
      const updatedField = await updateField(authToken, data.id, {
        status: data.status,
      });

      return {
        success: true,
        message: 'messages.statusUpdated',
        field: updatedField,
      };
    }

    return { success: false, error: 'messages.unknownError' };
  } catch (error) {
    console.error(
      'Error in requirements action:',
      JSON.stringify(error, null, 2)
    );

    if (error instanceof z.ZodError) {
      return {
        success: false,
        error: 'messages.formInvalid',
        fieldErrors: error.flatten().fieldErrors,
      };
    }

    return {
      success: false,
      error: error instanceof Error ? error.message : 'messages.unknownError',
    };
  }
}

// Field type badge component
const FieldTypeBadge = ({ type }: { type: DynamicField['field_type'] }) => {
  const { t } = useTranslation('requirements');

  const typeConfig: Record<string, { color: string; label: string }> = {
    input: { color: 'bg-blue-100 text-blue-800', label: t('fieldTypes.input') },
    boolean: {
      color: 'bg-indigo-100 text-indigo-800',
      label: t('fieldTypes.boolean'),
    },
    select: {
      color: 'bg-yellow-100 text-yellow-800',
      label: t('fieldTypes.select'),
    },
    radio: {
      color: 'bg-indigo-100 text-indigo-800',
      label: t('fieldTypes.radio'),
    },
    file: {
      color: 'bg-red-100 text-red-800',
      label: t('fieldTypes.file'),
    },
  };

  const config = typeConfig[type] ?? {
    color: 'bg-gray-100 text-gray-800',
    label: type,
  };

  return (
    <span
      className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${config.color}`}
    >
      {config.label}
    </span>
  );
};

// Status badge component
const StatusBadge = ({ status }: { status: DynamicField['status'] }) => {
  const { t } = useTranslation('requirements');
  const isActive = status === 1;
  const statusConfig = {
    active: {
      icon: CheckCircle,
      color: 'text-green-600 bg-green-100',
      label: t('status.active'),
    },
    inactive: {
      icon: XCircle,
      color: 'text-red-600 bg-red-100',
      label: t('status.inactive'),
    },
  };

  const config = statusConfig[isActive ? 'active' : 'inactive'];
  const Icon = config.icon;

  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${config.color}`}
    >
      <Icon size={12} />
      {config.label}
    </span>
  );
};

export const handle = {
  title: 'Requisitos',
  breadcrumb: 'Requisitos',
};

export async function loader({ request }: LoaderFunctionArgs) {
  const authToken = await getAccessToken(request);

  if (!authToken) {
    throw new Response('Token de acceso no disponible', { status: 401 });
  }

  const user = await requireAuth(request);

  if (!checkDirectorPermissions(user)) {
    throw new Response('Acceso no autorizado', { status: 403 });
  }

  try {
    const requirements = await getFields(authToken);
    return { user, requirements };
  } catch (error) {
    console.error('Error loading requirements:', error);
    return { user, requirements: [] };
  }
}

export default function DirectorRequirements() {
  const { user, requirements } = useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();
  const navigation = useNavigation();
  const { t } = useTranslation('requirements');
  const { t: tCommon } = useTranslation('common');
  const [showAddModal, setShowAddModal] = useState(false);
  const [filterByType, setFilterByType] = useState<string>('all');
  const [isMobile, setIsMobile] = useState(false);
  const [selectedFieldType, setSelectedFieldType] = useState<string>('');
  const [selectedRequired, setSelectedRequired] = useState<string>('');
  const [dynamicOptions, setDynamicOptions] = useState<
    Array<{ id: string; value: string; description: string }>
  >([]);

  // Additional state for advanced conditional logic (Angular equivalent)
  const [propertyCondition, setPropertyCondition] = useState<string>('0');
  const [propertyMeters, setPropertyMeters] = useState<string>('');
  const [activityCondition, setActivityCondition] = useState<string>('0');
  const [activityMeters, setActivityMeters] = useState<string>('');
  const [applicantCharacterCondition, setApplicantCharacterCondition] =
    useState<string[]>([]);
  const [personTypeCondition, setPersonTypeCondition] = useState<string[]>([]);
  const [alcoholCondition, setAlcoholCondition] = useState<string>('0');
  const [allConditions, setAllConditions] = useState<string>('false');
  const [checkDependency, setCheckDependency] = useState<boolean>(false);
  const [selectedDependency, setSelectedDependency] = useState<string>('');
  const [availableGiros, setAvailableGiros] = useState<any[]>([]);
  const [selectedGiros, setSelectedGiros] = useState<string[]>([]);
  const [dependenciesList, setDependenciesList] = useState<any[]>([]);

  const isSubmitting = navigation.state === 'submitting';

  // Handle successful form submission
  React.useEffect(() => {
    if (actionData?.success) {
      setShowAddModal(false);
      setSelectedFieldType('');
      setSelectedRequired('');
      setDynamicOptions([]);
      // Reset advanced conditional fields
      setPropertyCondition('0');
      setPropertyMeters('');
      setActivityCondition('0');
      setActivityMeters('');
      setApplicantCharacterCondition([]);
      setPersonTypeCondition([]);
      setAlcoholCondition('0');
      setAllConditions('false');
      setCheckDependency(false);
      setSelectedDependency('');
      setSelectedGiros([]);
    }
  }, [actionData]);

  // Reset field type when Add modal opens/closes
  React.useEffect(() => {
    if (!showAddModal) {
      setDynamicOptions([]);
      setSelectedFieldType('');
      setSelectedRequired('');
      // Reset advanced conditional fields
      setPropertyCondition('0');
      setPropertyMeters('');
      setActivityCondition('0');
      setActivityMeters('');
      setApplicantCharacterCondition([]);
      setPersonTypeCondition([]);
      setAlcoholCondition('0');
      setAllConditions('false');
      setCheckDependency(false);
      setSelectedDependency('');
      setSelectedGiros([]);
    }
  }, [showAddModal]);

  // Dynamic options management functions
  const addDynamicOption = () => {
    const newOption = {
      id: `option-${Date.now()}`,
      value: '',
      description: '',
    };
    setDynamicOptions([...dynamicOptions, newOption]);
  };

  const removeDynamicOption = (id: string) => {
    setDynamicOptions(dynamicOptions.filter(option => option.id !== id));
  };

  const updateDynamicOption = (
    id: string,
    field: 'value' | 'description',
    newValue: string
  ) => {
    setDynamicOptions(
      dynamicOptions.map(option =>
        option.id === id ? { ...option, [field]: newValue } : option
      )
    );
  };

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);

    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES');
  };

  const handleStatusToggle = async (
    requirementId: number,
    currentStatus: number | null | undefined
  ) => {
    const newStatus = currentStatus === 1 ? 0 : 1;

    // Create a form and submit it
    const form = document.createElement('form');
    form.method = 'post';
    form.style.display = 'none';

    const intentInput = document.createElement('input');
    intentInput.type = 'hidden';
    intentInput.name = '_intent';
    intentInput.value = 'toggleStatus';
    form.appendChild(intentInput);

    const idInput = document.createElement('input');
    idInput.type = 'hidden';
    idInput.name = 'id';
    idInput.value = requirementId.toString();
    form.appendChild(idInput);

    const statusInput = document.createElement('input');
    statusInput.type = 'hidden';
    statusInput.name = 'status';
    statusInput.value = newStatus.toString();
    form.appendChild(statusInput);

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
  };

  const filteredRequirements =
    filterByType === 'all'
      ? requirements
      : requirements.filter(req => req.field_type === filterByType);

  const desktopColumns = [
    {
      key: 'name' as keyof DynamicField,
      label: t('table.columns.requirementTitle'),
      sortable: true,
      render: (value: string) => (
        <div
          className="font-medium text-gray-900 text-sm min-w-0"
          title={value}
        >
          <div className="whitespace-normal break-words leading-tight">
            {value}
          </div>
        </div>
      ),
    },
    {
      key: 'field_type' as keyof DynamicField,
      label: t('table.columns.fieldType'),
      sortable: true,
      render: (value: DynamicField['field_type']) => (
        <FieldTypeBadge type={value} />
      ),
    },
    {
      key: 'required' as keyof DynamicField,
      label: t('table.columns.required'),
      sortable: true,
      render: (value: boolean | null | undefined) => {
        const isRequired = Boolean(value);
        const config = isRequired
          ? { label: t('status.yes'), color: 'bg-red-100 text-red-800' }
          : { label: t('status.no'), color: 'bg-gray-100 text-gray-800' };

        return (
          <span
            className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${config.color}`}
          >
            {config.label}
          </span>
        );
      },
    },
    {
      key: 'procedure_type' as keyof DynamicField,
      label: t('table.columns.procedureType'),
      render: (value: string | null) => (
        <span className="text-sm text-gray-600">
          {value ?? t('table.noSpecified')}
        </span>
      ),
    },
    {
      key: 'status' as keyof DynamicField,
      label: t('table.columns.status'),
      sortable: false,
      render: (value: DynamicField['status'], requirement: DynamicField) => (
        <div className="flex justify-center w-16">
          <input
            type="checkbox"
            checked={value === 1}
            onChange={() => handleStatusToggle(requirement.id ?? 0, value)}
            className="rounded border-gray-300 text-green-600 focus:ring-green-500 focus:ring-2"
            disabled={false}
          />
        </div>
      ),
    },
  ];

  const mobileColumns = [
    {
      key: 'name' as keyof DynamicField,
      label: t('table.requirement'),
      sortable: true,
      render: (value: string, requirement: DynamicField) => (
        <div className="space-y-2">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <FileText className="text-blue-600" size={16} />
            </div>
            <div className="min-w-0 flex-1">
              <div className="font-medium text-gray-900 text-sm">{value}</div>
              <div className="text-xs text-gray-500 mt-1">
                <FieldTypeBadge type={requirement.field_type} />
              </div>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span
                className={`inline-flex px-1.5 py-0.5 rounded-full text-xs font-medium ${
                  requirement.required
                    ? 'bg-red-100 text-red-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {requirement.required
                  ? t('status.required')
                  : t('status.optional')}
              </span>
              <input
                type="checkbox"
                checked={requirement.status === 1}
                onChange={() =>
                  handleStatusToggle(requirement.id ?? 0, requirement.status)
                }
                className="rounded border-gray-300 text-green-600 focus:ring-green-500 focus:ring-2"
                disabled={false}
              />
            </div>
          </div>
          <div className="text-xs text-gray-500">
            {requirement.procedure_type ?? t('table.noSpecified')}
          </div>
          {requirement.visible_condition && (
            <div className="text-xs text-gray-600">
              <strong>{t('table.condition')}:</strong>{' '}
              {requirement.visible_condition}
            </div>
          )}
        </div>
      ),
    },
  ];

  const requirementColumns = isMobile ? mobileColumns : desktopColumns;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b border-gray-200">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <span>Administrador</span>
              <span>/</span>
              <span className="text-gray-900 font-medium">
                {t('breadcrumb')}
              </span>
            </div>
            <button
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
            >
              <Plus size={16} />
              {t('addRequirement')}
            </button>
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{t('title')}</h1>
            <p className="text-gray-600 mt-1">{t('description')}</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                  <FileText className="text-blue-600" size={16} />
                </div>
                <div>
                  <div className="text-xs text-gray-600">
                    {t('stats.total')}
                  </div>
                  <div className="text-lg font-bold text-gray-900">
                    {requirements.length}
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                  <AlertTriangle className="text-red-600" size={16} />
                </div>
                <div>
                  <div className="text-xs text-gray-600">
                    {t('stats.mandatory')}
                  </div>
                  <div className="text-lg font-bold text-gray-900">
                    {requirements.filter(r => r.required).length}
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                  <CheckCircle className="text-green-600" size={16} />
                </div>
                <div>
                  <div className="text-xs text-gray-600">
                    {t('stats.active')}
                  </div>
                  <div className="text-lg font-bold text-gray-900">
                    {requirements.filter(r => r.status === 1).length}
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Filter className="text-purple-600" size={16} />
                </div>
                <div>
                  <div className="text-xs text-gray-600">
                    {t('stats.types')}
                  </div>
                  <div className="text-lg font-bold text-gray-900">
                    {new Set(requirements.map(r => r.field_type)).size}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
              <Select
                value={filterByType}
                onValueChange={setFilterByType}
                label={t('filters.filterByType')}
              >
                <Option value="all">{t('filters.allTypes')}</Option>
                <Option value="input">{t('filters.freeText')}</Option>
                <Option value="boolean">{t('filters.yesNo')}</Option>
                <Option value="select">{t('filters.dropdown')}</Option>
                <Option value="radio">{t('filters.optionSelection')}</Option>
                <Option value="file">{t('filters.document')}</Option>
              </Select>
            </div>
          </div>

          <DataTable
            data={filteredRequirements}
            columns={requirementColumns}
            title={`${t('table.title')} (${filteredRequirements.length})`}
            exportable={false}
            searchable={true}
            filterable={false}
            itemsPerPage={15}
          />
        </div>
      </div>

      {/* Add Modal - Enhanced with Angular component fields */}
      <Dialog
        open={showAddModal}
        onOpenChange={open => !open && setShowAddModal(false)}
      >
        <DialogContent className="sm:max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{t('modal.title')}</DialogTitle>
          </DialogHeader>

          <Form method="post" className="space-y-4">
            <input type="hidden" name="_intent" value="create" />

            {/* Field Type Selection */}
            <div>
              <Select
                name="field_type"
                label={t('modal.fieldType.label')}
                placeholder={t('modal.fieldType.placeholder')}
                value={selectedFieldType}
                onValueChange={setSelectedFieldType}
                required
              >
                {selectedRequired !== 'conditional' && (
                  <Option value="file">{t('fieldTypes.file')}</Option>
                )}
                <Option value="input">{t('fieldTypes.input')}</Option>
                <Option value="boolean">{t('fieldTypes.boolean')}</Option>
                <Option value="select">{t('fieldTypes.select')}</Option>
                <Option value="radio">{t('fieldTypes.radio')}</Option>
              </Select>
            </div>

            {/* Basic Information */}
            <Input
              name="description"
              type="text"
              label={t('modal.description.label')}
              placeholder={t('modal.description.placeholder')}
              required
            />

            <Input
              name="description_rec"
              type="text"
              label={t('modal.detailedDescription.label')}
              placeholder={t('modal.detailedDescription.placeholder')}
            />

            {/* Conditional "Fundamento legal" field - only for file types */}
            {selectedFieldType === 'file' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('modal.rationale.label')}
                </label>
                <textarea
                  name="rationale"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows={3}
                  placeholder={t('modal.rationale.placeholder')}
                />
              </div>
            )}

            {/* Conditional options section - only for select/radio types */}
            {(selectedFieldType === 'select' ||
              selectedFieldType === 'radio') && (
              <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                <div className="mb-4">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    {t('modal.options.title')}
                  </h3>
                  <button
                    type="button"
                    onClick={addDynamicOption}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                  >
                    {t('modal.options.add')}
                  </button>
                </div>

                {dynamicOptions.length === 0 && (
                  <div className="text-gray-500 text-sm italic mb-4">
                    {t('modal.options.empty')}
                  </div>
                )}

                <div className="space-y-3 max-h-60 overflow-y-auto">
                  {dynamicOptions.map(option => (
                    <div
                      key={option.id}
                      className="flex gap-3 items-center bg-white p-3 rounded-lg border border-gray-200"
                    >
                      <div className="flex-1">
                        <input
                          type="text"
                          placeholder={t('modal.options.placeholder')}
                          value={option.value}
                          onChange={e =>
                            updateDynamicOption(
                              option.id,
                              'value',
                              e.target.value
                            )
                          }
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                      <button
                        type="button"
                        onClick={() => removeDynamicOption(option.id)}
                        className="text-red-600 hover:text-red-800 p-2 hover:bg-red-50 rounded-lg transition-colors"
                        title={t('modal.options.remove')}
                      >
                        <X size={16} />
                      </button>
                    </div>
                  ))}
                </div>

                {/* Hidden inputs to pass data to the form */}
                <input
                  type="hidden"
                  name="options"
                  value={dynamicOptions.map(opt => opt.value).join('|')}
                />
                <input
                  type="hidden"
                  name="options_description"
                  value={dynamicOptions
                    .map((opt, index) => (index + 1).toString())
                    .join('|')}
                />
              </div>
            )}

            {/* Required Selection */}
            <div>
              <Select
                name="required"
                label={t('modal.required.label')}
                placeholder={t('modal.required.placeholder')}
                value={selectedRequired}
                onValueChange={setSelectedRequired}
                required
              >
                <Option value="true">{t('modal.required.always')}</Option>
                {selectedFieldType === 'file' && (
                  <Option value="conditional">
                    {t('modal.required.conditional')}
                  </Option>
                )}
              </Select>
            </div>

            {/* Advanced conditional parameters - only show for file types and conditional requirement */}
            {selectedFieldType === 'file' &&
              selectedRequired === 'conditional' && (
                <div className="border border-gray-200 rounded-lg p-4 bg-gray-50 space-y-4">
                  <div className="mb-4">
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      {t('modal.conditionalParams.title')}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {t('modal.conditionalParams.note')}
                    </p>
                  </div>

                  {/* Property area condition */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {t('modal.conditionalParams.propertyArea')}
                    </label>
                    <div className="grid grid-cols-2 gap-4">
                      <Select
                        value={propertyCondition}
                        onValueChange={setPropertyCondition}
                        placeholder={t(
                          'modal.conditionalParams.conditions.notApply'
                        )}
                      >
                        <Option value="0">
                          {t('modal.conditionalParams.conditions.notApply')}
                        </Option>
                        <Option value=">=">
                          {t('modal.conditionalParams.conditions.greaterEqual')}
                        </Option>
                        <Option value="<=">
                          {t('modal.conditionalParams.conditions.lessEqual')}
                        </Option>
                      </Select>
                      {propertyCondition !== '0' && (
                        <Input
                          type="number"
                          placeholder={t(
                            'modal.conditionalParams.conditions.placeholder'
                          )}
                          value={propertyMeters}
                          onChange={e => setPropertyMeters(e.target.value)}
                          required={propertyCondition !== '0'}
                        />
                      )}
                    </div>
                  </div>

                  {/* Activity area condition */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {t('modal.conditionalParams.activityArea')}
                    </label>
                    <div className="grid grid-cols-2 gap-4">
                      <Select
                        value={activityCondition}
                        onValueChange={setActivityCondition}
                        placeholder={t(
                          'modal.conditionalParams.conditions.notApply'
                        )}
                      >
                        <Option value="0">
                          {t('modal.conditionalParams.conditions.notApply')}
                        </Option>
                        <Option value=">=">
                          {t('modal.conditionalParams.conditions.greaterEqual')}
                        </Option>
                        <Option value="<=">
                          {t('modal.conditionalParams.conditions.lessEqual')}
                        </Option>
                      </Select>
                      {activityCondition !== '0' && (
                        <Input
                          type="number"
                          placeholder={t(
                            'modal.conditionalParams.conditions.placeholder'
                          )}
                          value={activityMeters}
                          onChange={e => setActivityMeters(e.target.value)}
                          required={activityCondition !== '0'}
                        />
                      )}
                    </div>
                  </div>

                  {/* Applicant character condition */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {t('modal.conditionalParams.applicantCharacter')}
                    </label>
                    <div className="space-y-2">
                      {[
                        {
                          key: 'Propietario',
                          label: t('modal.conditionalParams.characters.owner'),
                        },
                        {
                          key: 'Arrendatario',
                          label: t('modal.conditionalParams.characters.tenant'),
                        },
                        {
                          key: 'Carta poder',
                          label: t(
                            'modal.conditionalParams.characters.powerOfAttorney'
                          ),
                        },
                      ].map(character => (
                        <label
                          key={character.key}
                          className="flex items-center"
                        >
                          <input
                            type="checkbox"
                            checked={applicantCharacterCondition.includes(
                              character.key
                            )}
                            onChange={e => {
                              if (e.target.checked) {
                                setApplicantCharacterCondition(prev => [
                                  ...prev,
                                  character.key,
                                ]);
                              } else {
                                setApplicantCharacterCondition(prev =>
                                  prev.filter(c => c !== character.key)
                                );
                              }
                            }}
                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">
                            {character.label}
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Person type condition */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {t('modal.conditionalParams.personType')}
                    </label>
                    <div className="space-y-2">
                      {[
                        {
                          key: 'Física',
                          label: t(
                            'modal.conditionalParams.personTypes.individual'
                          ),
                        },
                        {
                          key: 'Moral',
                          label: t('modal.conditionalParams.personTypes.legal'),
                        },
                      ].map(type => (
                        <label key={type.key} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={personTypeCondition.includes(type.key)}
                            onChange={e => {
                              if (e.target.checked) {
                                setPersonTypeCondition(prev => [
                                  ...prev,
                                  type.key,
                                ]);
                              } else {
                                setPersonTypeCondition(prev =>
                                  prev.filter(t => t !== type.key)
                                );
                              }
                            }}
                            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          />
                          <span className="ml-2 text-sm text-gray-700">
                            {type.label}
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Alcohol condition */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {t('modal.conditionalParams.alcoholSales')}
                    </label>
                    <Select
                      value={alcoholCondition}
                      onValueChange={setAlcoholCondition}
                      placeholder={t(
                        'modal.conditionalParams.conditions.notApply'
                      )}
                    >
                      <Option value="0">
                        {t('modal.conditionalParams.conditions.notApply')}
                      </Option>
                      <Option value="1">
                        {t(
                          'modal.conditionalParams.alcoholTypes.lowGradeClosed'
                        )}
                      </Option>
                      <Option value="2">
                        {t('modal.conditionalParams.alcoholTypes.lowGradeOpen')}
                      </Option>
                      <Option value="3">
                        {t(
                          'modal.conditionalParams.alcoholTypes.highGradeClosed'
                        )}
                      </Option>
                      <Option value="4">
                        {t(
                          'modal.conditionalParams.alcoholTypes.highGradeOpen'
                        )}
                      </Option>
                      <Option value="5">
                        {t('modal.conditionalParams.alcoholTypes.anyOfAbove')}
                      </Option>
                    </Select>
                  </div>

                  {/* All conditions toggle */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {t('modal.conditionalParams.applicationRule')}
                    </label>
                    <div className="space-y-2">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="allConditions"
                          value="true"
                          checked={allConditions === 'true'}
                          onChange={e => setAllConditions(e.target.value)}
                          className="text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">
                          {t('modal.conditionalParams.allConditions')}
                        </span>
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="allConditions"
                          value="false"
                          checked={allConditions === 'false'}
                          onChange={e => setAllConditions(e.target.value)}
                          className="text-blue-600 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-700">
                          {t('modal.conditionalParams.anyCondition')}
                        </span>
                      </label>
                    </div>
                  </div>

                  {/* Dependencies */}
                  <div>
                    <label className="flex items-center mb-2">
                      <input
                        type="checkbox"
                        checked={checkDependency}
                        onChange={e => setCheckDependency(e.target.checked)}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm font-medium text-gray-700">
                        {t('modal.conditionalParams.dependency.label')}
                      </span>
                    </label>
                    {checkDependency && (
                      <Select
                        value={selectedDependency}
                        onValueChange={setSelectedDependency}
                        placeholder={t(
                          'modal.conditionalParams.dependency.placeholder'
                        )}
                      >
                        <Option value="1">
                          {t('dependencies.dependency1')}
                        </Option>
                        <Option value="2">
                          {t('dependencies.dependency2')}
                        </Option>
                      </Select>
                    )}
                  </div>

                  {/* Hidden inputs for form submission */}
                  <input
                    type="hidden"
                    name="property_condition"
                    value={propertyCondition}
                  />
                  <input
                    type="hidden"
                    name="property_meters"
                    value={propertyMeters}
                  />
                  <input
                    type="hidden"
                    name="activity_condition"
                    value={activityCondition}
                  />
                  <input
                    type="hidden"
                    name="activity_meters"
                    value={activityMeters}
                  />
                  <input
                    type="hidden"
                    name="applicant_character_condition"
                    value={applicantCharacterCondition.join(',')}
                  />
                  <input
                    type="hidden"
                    name="person_type_condition"
                    value={personTypeCondition.join(',')}
                  />
                  <input
                    type="hidden"
                    name="alcohol_condition"
                    value={alcoholCondition}
                  />
                  <input
                    type="hidden"
                    name="all_conditions"
                    value={allConditions}
                  />
                  <input
                    type="hidden"
                    name="check_dependency"
                    value={checkDependency.toString()}
                  />
                  <input
                    type="hidden"
                    name="selected_dependency"
                    value={selectedDependency}
                  />
                </div>
              )}

            {/* Remaining basic fields */}
            <div>
              <Select
                name="step"
                label={t('modal.step.label')}
                placeholder={t('modal.step.placeholder')}
                required
              >
                <Option value="1">{t('modal.step.applicant')}</Option>
                <Option value="2">{t('modal.step.owner')}</Option>
                <Option value="3">{t('modal.step.property')}</Option>
                <Option value="4">{t('modal.step.establishment')}</Option>
              </Select>
            </div>

            <div>
              <Select
                name="procedure_type"
                label={t('modal.procedureType.label')}
                placeholder={t('modal.procedureType.placeholder')}
                required
              >
                {selectedFieldType !== 'file' && (
                  <Option value="consulta_requisitos">
                    {t('modal.procedureType.requirementsConsultation')}
                  </Option>
                )}
                <Option value="solicitud_licencia">
                  {t('modal.procedureType.licenseApplication')}
                </Option>
                <Option value="oficial">
                  {t('modal.procedureType.official')}
                </Option>
              </Select>
            </div>

            <DialogFooter className="gap-3 pt-4">
              <button
                type="button"
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                {t('modal.actions.cancel')}
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {isSubmitting
                  ? t('modal.actions.creating')
                  : t('modal.actions.create')}
              </button>
            </DialogFooter>
          </Form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
