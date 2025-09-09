import type { LoaderFunctionArgs, ActionFunctionArgs } from 'react-router';
import { useState } from 'react';
import * as React from 'react';
import {
  useLoaderData,
  Form,
  useActionData,
  useNavigation,
} from 'react-router';
import { useTranslation } from 'react-i18next';
import { requireAccessToken, requireAuth } from '../../utils/auth/auth.server';
import { checkDirectorPermissions } from '../../utils/auth/director';
import { DataTable } from '../../components/Director/Charts/DataTable';
import {
  Building,
  Plus,
  CheckCircle,
  XCircle,
  AlertTriangle,
  EyeOff,
} from 'lucide-react';
import {
  getAllBusinessTypes,
  createBusinessType,
  updateBusinessTypeStatus,
  updateBusinessTypeCertificate,
  updateBusinessTypeImpact,
} from '../../utils/api/business_types';
import { createBusinessTypeSchema } from '../../schemas/business-types';
import {
  Dialog,
  DialogTrigger,
  DialogContent,
} from '../../components/Dialog/Dialog';
import { Input } from '../../components/Input/Input';
import { Button } from '../../components/Button/Button';
import { Select, Option } from '../../components/Select/Select';

export const handle = {
  title: 'director:navigation.businessTypes',
  breadcrumb: 'director:navigation.businessTypes',
};

interface BusinessType {
  id: number;
  name: string;
  code: string;
  description: string;
  impact_level: number;
  requires_certificate: boolean;
  is_disabled: boolean;
  related_keywords: string[];
  status: 'active' | 'inactive' | 'disabled';
}

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireAuth(request);
  const accessToken = await requireAccessToken(request);

  if (!checkDirectorPermissions(user)) {
    throw new Response('Acceso no autorizado', { status: 403 });
  }

  const apiBusinessTypes = await getAllBusinessTypes(accessToken);

  const businessTypes = apiBusinessTypes.map(bt => ({
    id: bt.business_type_id,
    name: bt.name ?? '',
    code: bt.code ?? '',
    description: bt.description ?? '',
    impact_level: bt.impact_level ?? 0,
    requires_certificate: bt.has_certificate,
    is_disabled: bt.is_disabled,
    related_keywords: bt.related_words
      ? bt.related_words.split(',').map(w => w.trim())
      : [],
    status: (bt.is_disabled ? 'disabled' : 'active') as
      | 'active'
      | 'inactive'
      | 'disabled',
  }));

  return { user, businessTypes };
}

export async function action({ request }: ActionFunctionArgs) {
  const user = await requireAuth(request);
  const accessToken = await requireAccessToken(request);

  if (!checkDirectorPermissions(user)) {
    throw new Response('Acceso no autorizado', { status: 403 });
  }

  const formData = await request.formData();
  const intent = formData.get('intent');

  if (intent === 'create') {
    const data = {
      name: formData.get('name') as string,
      description: formData.get('description') as string,
      is_active: formData.get('is_active') === 'true',
      code: formData.get('code') as string,
      related_words: formData.get('related_words') as string,
    };

    const validationResult = createBusinessTypeSchema.safeParse(data);

    if (!validationResult.success) {
      return {
        success: false,
        errors: validationResult.error.errors,
      };
    }

    try {
      await createBusinessType(validationResult.data, accessToken);
      return { success: true };
    } catch (error) {
      console.error('Error creating business type:', error);
      return {
        success: false,
        error:
          'Error al crear el giro comercial. Por favor, intenta nuevamente.',
      };
    }
  }

  if (intent === 'update-status') {
    const business_type_id = Number(formData.get('business_type_id'));
    const status = formData.get('status') === 'true' ? 1 : 0;

    try {
      await updateBusinessTypeStatus(status, { business_type_id }, accessToken);
      return { success: true };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  if (intent === 'update-certificate') {
    const business_type_id = Number(formData.get('business_type_id'));
    const status = formData.get('status') === 'true' ? 1 : 0;
    try {
      await updateBusinessTypeCertificate(
        status,
        { business_type_id, status: status === 1 },
        accessToken
      );
      return { success: true };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  if (intent === 'update-impact') {
    const business_type_id = Number(formData.get('business_type_id'));
    const impact_level = Number(formData.get('impact_level'));

    try {
      await updateBusinessTypeImpact(
        {
          business_type_id,
          impact_level,
        },
        accessToken
      );
      return { success: true };
    } catch (error) {
      return { success: false, error: (error as Error).message };
    }
  }

  return {
    success: false,
    error: 'Acción no válida',
  };
}

export const ImpactLevelBadge = ({ level }: { level: number }) => {
  const { t } = useTranslation('business-types');

  const levelConfig = {
    1: { color: 'bg-green-100 text-green-800', label: t('impactBadges.low') },
    2: {
      color: 'bg-yellow-100 text-yellow-800',
      label: t('impactBadges.medium'),
    },
    3: {
      color: 'bg-orange-100 text-orange-800',
      label: t('impactBadges.high'),
    },
    4: { color: 'bg-red-100 text-red-800', label: t('impactBadges.veryHigh') },
  };

  const config =
    levelConfig[level as keyof typeof levelConfig] || levelConfig[1];

  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${config.color}`}
    >
      <AlertTriangle size={12} />
      {config.label} ({level})
    </span>
  );
};

export const StatusBadge = ({ status }: { status: BusinessType['status'] }) => {
  const { t } = useTranslation('business-types');

  const statusConfig = {
    active: {
      icon: CheckCircle,
      color: 'text-green-600 bg-green-100',
      label: t('statusBadges.active'),
    },
    inactive: {
      icon: XCircle,
      color: 'text-gray-600 bg-gray-100',
      label: t('statusBadges.inactive'),
    },
    disabled: {
      icon: EyeOff,
      color: 'text-red-600 bg-red-100',
      label: t('statusBadges.disabled'),
    },
  };

  const config = statusConfig[status];
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

export default function DirectorBusinessTypes() {
  const { businessTypes } = useLoaderData<typeof loader>();
  const actionData = useActionData<{
    success: boolean;
    errors?: any[];
    error?: string;
  }>();
  const navigation = useNavigation();
  const { t } = useTranslation('business-types');
  const [showAddModal, setShowAddModal] = useState(false);
  const [filterByStatus, setFilterByStatus] = useState<string>('all');

  const isSubmitting = navigation.state === 'submitting';

  React.useEffect(() => {
    if (actionData?.success) {
      setShowAddModal(false);
    }
  }, [actionData]);

  let filteredBusinessTypes = businessTypes;
  if (filterByStatus !== 'all') {
    filteredBusinessTypes = filteredBusinessTypes.filter(
      bt => bt.status === (filterByStatus as BusinessType['status'])
    );
  }

  const businessTypeColumns = [
    {
      key: 'code' as keyof BusinessType,
      label: t('codeColumnHeader'),
      sortable: true,
      render: (value: string) => (
        <span className="font-mono text-sm text-gray-700">{value}</span>
      ),
    },
    {
      key: 'name' as keyof BusinessType,
      label: t('businessTypeColumnHeader'),
      sortable: true,
      render: (value: string, businessType: BusinessType) => (
        <div className="min-w-0 max-w-xs">
          <div className="font-medium text-gray-900 text-sm">{value}</div>
          <div className="text-xs text-gray-500 line-clamp-2">
            {businessType.description}
          </div>
        </div>
      ),
    },
    {
      key: 'impact_level' as keyof BusinessType,
      label: t('impactColumnHeader'),
      sortable: false,
      render: (value: number, businessType: BusinessType) => (
        <Form method="post" className="inline">
          <input type="hidden" name="intent" value="update-impact" />
          <input
            type="hidden"
            name="business_type_id"
            value={businessType.id}
          />
          <input type="hidden" name="impact_level" value={value} />
          <Select
            value={value.toString()}
            onValueChange={selectedValue => {
              const form = document
                .querySelector(
                  `input[name="business_type_id"][value="${businessType.id}"]`
                )
                ?.closest('form') as HTMLFormElement;
              const impactInput = form?.querySelector(
                'input[name="impact_level"]'
              ) as HTMLInputElement;
              if (impactInput) {
                impactInput.value = selectedValue;
              }
              form?.requestSubmit();
            }}
          >
            <Option value="1">{t('impactLevels.1')}</Option>
            <Option value="2">{t('impactLevels.2')}</Option>
            <Option value="3">{t('impactLevels.3')}</Option>
            <Option value="4">{t('impactLevels.4')}</Option>
            <Option value="5">{t('impactLevels.5')}</Option>
          </Select>
        </Form>
      ),
    },
    {
      key: 'requires_certificate' as keyof BusinessType,
      label: t('certificateColumnHeader'),
      sortable: false,
      render: (value: boolean, businessType: BusinessType) => (
        <Form method="post" className="inline">
          <input type="hidden" name="intent" value="update-certificate" />
          <input
            type="hidden"
            name="business_type_id"
            value={businessType.id}
          />
          <input type="hidden" name="status" value={(!value).toString()} />
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              checked={value}
              onChange={e => {
                e.target.form?.requestSubmit();
              }}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 focus:ring-2"
            />
            <span className="ml-1 text-xs text-gray-600">
              {value
                ? t('checkboxLabels.required')
                : t('checkboxLabels.notRequired')}
            </span>
          </label>
        </Form>
      ),
    },
    {
      key: 'is_disabled' as keyof BusinessType,
      label: t('statusColumnHeader'),
      sortable: false,
      render: (value: boolean, businessType: BusinessType) => (
        <Form method="post" className="inline">
          <input type="hidden" name="intent" value="update-status" />
          <input
            type="hidden"
            name="business_type_id"
            value={businessType.id}
          />
          <input type="hidden" name="status" value={(!value).toString()} />
          <label className="inline-flex items-center">
            <input
              type="checkbox"
              checked={!value}
              onChange={e => {
                e.target.form?.requestSubmit();
              }}
              className="rounded border-gray-300 text-green-600 focus:ring-green-500 focus:ring-2"
            />
            <span
              className={`ml-1 text-xs ${!value ? 'text-green-600' : 'text-red-600'}`}
            >
              {!value
                ? t('checkboxLabels.enabled')
                : t('checkboxLabels.disabled')}
            </span>
          </label>
        </Form>
      ),
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b border-gray-200 px-4 md:px-6 lg:px-8 py-4 md:py-6">
        <div className="flex flex-col space-y-3 md:flex-row md:items-center md:justify-between md:space-y-0">
          <div className="flex items-center text-sm text-gray-500">
            <Building className="w-4 h-4 mr-1" />
            <span>{t('breadcrumbAdmin')}</span>
            <span className="mx-2">&gt;</span>
            <span>{t('breadcrumbBusinessTypes')}</span>
          </div>

          <div className="flex flex-col md:flex-row md:items-center md:justify-between w-full md:w-auto">
            <div className="mb-3 md:mb-0 md:mr-4">
              <h1 className="text-xl md:text-2xl font-semibold text-gray-900 flex items-center">
                <Building className="w-5 h-5 mr-2 text-gray-600" />
                {t('pageTitle')}
              </h1>
            </div>

            <Dialog onOpenChange={setShowAddModal} open={showAddModal}>
              <DialogTrigger asChild>
                <Button
                  onClick={() => setShowAddModal(true)}
                  variant="primary"
                  className="flex items-center justify-center gap-2 text-sm whitespace-nowrap"
                >
                  <Plus size={16} />
                  <span className="hidden sm:inline">
                    {t('addBusinessType')}
                  </span>
                  <span className="sm:hidden">{t('addBusinessType')}</span>
                </Button>
              </DialogTrigger>

              <DialogContent className="p-0 max-w-lg w-full">
                <div className="p-6 max-h-[90vh] overflow-y-auto">
                  <h3 className="text-lg font-semibold mb-4">
                    {t('addBusinessTypeModal')}
                  </h3>
                  <Form
                    method="post"
                    className="space-y-4"
                    key={showAddModal ? 'open' : 'closed'}
                  >
                    <input type="hidden" name="intent" value="create" />

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Input
                          name="name"
                          label={t('businessTypeName')}
                          placeholder={t('businessTypeNamePlaceholder')}
                          required
                        />
                      </div>
                      <div>
                        <Input
                          name="code"
                          label={t('businessTypeCode')}
                          placeholder={t('businessTypeCodePlaceholder')}
                          required
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        {t('description')}
                        <textarea
                          name="description"
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          rows={3}
                          placeholder={t('descriptionPlaceholder')}
                          required
                        />
                      </label>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        {t('relatedWords')}
                        <textarea
                          name="related_words"
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          rows={2}
                          placeholder={t('relatedWordsPlaceholder')}
                          required
                        />
                      </label>
                    </div>

                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        name="is_active"
                        value="true"
                        defaultChecked
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-sm font-medium text-gray-700">
                        {t('isActive')}
                      </span>
                    </label>

                    {(actionData?.errors || actionData?.error) && (
                      <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                        <div className="text-red-800 text-sm">
                          {actionData.errors ? (
                            actionData.errors.map(
                              (error: any, index: number) => (
                                <div
                                  key={`error-${index}-${error.code ?? error.message}`}
                                >
                                  {error.message}
                                </div>
                              )
                            )
                          ) : (
                            <div>{actionData.error}</div>
                          )}
                        </div>
                      </div>
                    )}

                    <div className="flex justify-end gap-3 mt-6">
                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => setShowAddModal(false)}
                        disabled={isSubmitting}
                      >
                        {t('cancel')}
                      </Button>
                      <Button
                        type="submit"
                        variant="primary"
                        disabled={isSubmitting}
                      >
                        {isSubmitting ? t('creating') : t('createBusinessType')}
                      </Button>
                    </div>
                  </Form>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </div>

      <div className="px-4 md:px-6 lg:px-8 py-4 md:py-6 space-y-4 md:space-y-6">
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4">
          <div className="bg-white p-3 md:p-4 rounded-lg border border-gray-200 text-center">
            <div className="text-lg md:text-xl font-bold text-gray-900">
              {businessTypes.length}
            </div>
            <div className="text-xs md:text-sm text-gray-600">
              {t('totalBusinessTypes')}
            </div>
          </div>

          <div className="bg-white p-3 md:p-4 rounded-lg border border-gray-200 text-center">
            <div className="text-lg md:text-xl font-bold text-green-600">
              {businessTypes.filter(bt => !bt.is_disabled).length}
            </div>
            <div className="text-xs md:text-sm text-gray-600">
              {t('enabled')}
            </div>
          </div>

          <div className="bg-white p-3 md:p-4 rounded-lg border border-gray-200 text-center">
            <div className="text-lg md:text-xl font-bold text-blue-600">
              {businessTypes.filter(bt => bt.requires_certificate).length}
            </div>
            <div className="text-xs md:text-sm text-gray-600">
              {t('withCertificate')}
            </div>
          </div>
        </div>
        <div className="bg-white p-3 md:p-4 rounded-lg border border-gray-200">
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
            <div className="flex-1 flex items-center gap-2">
              <label
                htmlFor="filterByStatus"
                className="text-sm font-medium text-gray-700 whitespace-nowrap"
              >
                {t('statusFilter')}
              </label>
              <Select value={filterByStatus} onValueChange={setFilterByStatus}>
                <Option value="all">{t('statusAll')}</Option>
                <Option value="active">{t('statusActive')}</Option>
                <Option value="inactive">{t('statusInactive')}</Option>
                <Option value="disabled">{t('statusDisabled')}</Option>
              </Select>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="overflow-x-auto">
            <DataTable
              data={filteredBusinessTypes}
              columns={businessTypeColumns}
              title={`${t('businessTypesListTitle')} (${filteredBusinessTypes.length})`}
              exportable={true}
              searchable={true}
              filterable={false}
              itemsPerPage={15}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
