import type { action, loader } from '@root/app/routes/map';
import { useTranslation } from 'react-i18next';
import { Button } from '../Button/Button';
import { Form, Link, useActionData, useNavigation } from 'react-router';
import { useEffect, useRef, useReducer, type FormEventHandler } from 'react';
import { ArrowLeft, NotepadText, PlusCircle, CheckCircle } from 'lucide-react';
import { Input } from '../Input/Input';
import { Option, Select } from '../Select/Select';
import { RadioGroup } from '../RadioGroup/RadioGroup';
import { Checkbox } from '../Checkbox/Checkbox';
import { ConstructionRequirementsDisplay } from '../ConstructionRequirements/ConstructionRequirements';
import type { ConstructionRequirement } from '../ConstructionRequirements/ConstructionRequirements';
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogDescription,
} from '../Dialog/Dialog';
import { dynamicFieldsSchema } from '@root/app/schemas/requirements';
import { z } from 'zod';

// Type definitions for dynamic fields
type DynamicField = z.infer<typeof dynamicFieldsSchema>[number];

type FieldType = DynamicField['field_type'];

type DynamicFieldOption = {
  label: string;
  value: string;
};

type InputField = {
  name: string;
  type?: FieldType | 'hidden';
  required?: boolean;
  label?: string;
  value?: string;
  defaultValue?: string;
  readOnly?: boolean;
  pattern?: string;
  title?: string;
  onChange?: FormEventHandler<HTMLDivElement>;
  visibilityCondition?: string;
  options?: DynamicFieldOption[];
};

type Section = {
  name: string;
  inputs: InputField[];
};

type LicenseType = 'commercial' | 'construction';

type State = {
  dynamicFields?: InputField[];
  licenseType?: LicenseType;
  section: 'property' | 'requirements';
  showRequirementsModal?: boolean;
  visibilityConditions: Record<string, string>;
};

type Action =
  | { type: 'SET_SECTION'; section: 'property' | 'requirements' }
  | { type: 'SET_LICENSE_TYPE'; licenseType?: LicenseType }
  | { type: 'SET_SHOW_REQUIREMENTS_MODAL'; show: boolean }
  | { type: 'SET_DYNAMIC_FIELDS'; dynamicFields: State['dynamicFields'] }
  | {
      type: 'SET_VISIBILITY_CONDITION';
      visibilityCondition: string;
      value: string;
    };

const getFilteredProps = (
  input: InputField
): Omit<InputField, 'visibilityCondition'> => {
  const { visibilityCondition, ...filteredProps } = input;
  return filteredProps;
};

export function PropertyInfo({
  property,
  onDrawClick,
}: {
  property: Awaited<Awaited<ReturnType<typeof loader>>['property']>;
  onDrawClick?: () => void;
}) {
  const { t: tMap } = useTranslation('map');

  const processFieldsForType = (rawFields: DynamicField[]): InputField[] => {
    if (!rawFields || rawFields.length === 0) {
      return [];
    }

    // Helper function to detect separator and split options
    const splitOptions = (
      optionsString: string | null | undefined
    ): string[] => {
      if (!optionsString) return [];

      // Check if it contains pipes or commas to determine separator
      const hasPipes = optionsString.includes('|');
      const hasCommas = optionsString.includes(',');

      if (hasPipes && !hasCommas) {
        return optionsString.split('|');
      } else if (hasCommas && !hasPipes) {
        return optionsString.split(',');
      } else if (hasPipes && hasCommas) {
        // If both exist, count which appears more frequently
        const pipeCount = (optionsString.match(/\|/g) || []).length;
        const commaCount = (optionsString.match(/,/g) || []).length;
        return pipeCount >= commaCount
          ? optionsString.split('|')
          : optionsString.split(',');
      } else {
        // No separators found, return as single option
        return [optionsString];
      }
    };

    // Helper function to determine if this is a construction field
    const isConstructionField = (procedureType: string | null): boolean => {
      return procedureType === 'permits_building_license';
    };

    const parseResult = dynamicFieldsSchema.safeParse(rawFields);

    if (!parseResult.success) {
      // Try to transform document type to file and retry
      const transformedFields = rawFields.map(field => ({
        ...field,
        field_type:
          field.field_type === 'document'
            ? ('file' as const)
            : field.field_type,
      }));

      const retryResult = dynamicFieldsSchema.safeParse(transformedFields);
      if (retryResult.success) {
        return retryResult.data.map((data): InputField => {
          const options = splitOptions(data.options);
          const optionsValues = splitOptions(data.options_description);

          // Determine label and value based on field type
          const isConstruction = isConstructionField(data.procedure_type);
          return {
            name: `dynamicFields.${data.name}`,
            type: data.field_type,
            required: data.required ?? false,
            label: data.description ?? undefined,
            visibilityCondition: data.visible_condition ?? undefined,
            onChange: (e: React.FormEvent<HTMLDivElement>) => {
              dispatch({
                type: 'SET_VISIBILITY_CONDITION',
                visibilityCondition: data.visible_condition ?? '',
                value: (e.target as HTMLInputElement).value,
              });
            },
            options:
              options.length > 0
                ? options.map(
                    (option, index): DynamicFieldOption => ({
                      // For construction fields: label from options_description, value from options
                      // For commercial fields: label from options, value from options_description
                      label: isConstruction
                        ? (optionsValues[index]?.trim() ?? option.trim())
                        : option.trim(),
                      value: isConstruction
                        ? option.trim()
                        : (optionsValues[index]?.trim() ?? option.trim()),
                    })
                  )
                : undefined,
          };
        });
      }

      return [];
    }

    return (
      parseResult.data?.map((data): InputField => {
        const options = splitOptions(data.options);
        const optionsValues = splitOptions(data.options_description);

        // Determine label and value based on field type
        const isConstruction = isConstructionField(data.procedure_type);

        return {
          name: `dynamicFields.${data.name}`,
          type: data.field_type,
          required: data.required ?? false,
          label: data.description ?? undefined,
          visibilityCondition: data.visible_condition ?? undefined,
          onChange: (e: React.FormEvent<HTMLDivElement>) => {
            dispatch({
              type: 'SET_VISIBILITY_CONDITION',
              visibilityCondition: data.visible_condition ?? '',
              value: (e.target as HTMLInputElement).value,
            });
          },
          options:
            options.length > 0
              ? options.map(
                  (option, index): DynamicFieldOption => ({
                    // For construction fields: label from options_description, value from options
                    // For commercial fields: label from options, value from options_description
                    label: isConstruction
                      ? (optionsValues[index]?.trim() ?? option.trim())
                      : option.trim(),
                    value: isConstruction
                      ? option.trim()
                      : (optionsValues[index]?.trim() ?? option.trim()),
                  })
                )
              : undefined,
        };
      }) ?? []
    );
  };

  function reducer(state: State, action: Action): State {
    switch (action.type) {
      case 'SET_SECTION':
        return { ...state, section: action.section };
      case 'SET_LICENSE_TYPE': {
        // Filter dynamic fields based on the new license type and only show step 1
        const filteredFields =
          action.licenseType === 'construction'
            ? (property?.dynamicFields || []).filter(
                (field: DynamicField) =>
                  field.procedure_type === 'permits_building_license' &&
                  field.step === 1
              )
            : (property?.dynamicFields || []).filter(
                (field: DynamicField) =>
                  field.procedure_type === 'business_license' &&
                  field.step === 1
              );

        return {
          ...state,
          licenseType: action.licenseType,
          visibilityConditions: {},
          dynamicFields: processFieldsForType(filteredFields),
        };
      }
      case 'SET_SHOW_REQUIREMENTS_MODAL':
        return { ...state, showRequirementsModal: action.show };
      case 'SET_VISIBILITY_CONDITION':
        return {
          ...state,
          visibilityConditions: {
            ...state.visibilityConditions,
            [action.visibilityCondition]: action.value,
          },
        };
      case 'SET_DYNAMIC_FIELDS':
        return { ...state, dynamicFields: action.dynamicFields };
      default:
        return state;
    }
  }

  const [state, dispatch] = useReducer(reducer, {
    section: 'property',
    visibilityConditions: {},
    showRequirementsModal: false, // Initialize explicitly
    dynamicFields: (() => {
      if (!property?.dynamicFields || property.dynamicFields.length === 0) {
        return [];
      }

      // Initially show commercial fields as default
      const defaultFields = (property.dynamicFields || []).filter(
        (field: DynamicField) =>
          field.procedure_type === 'business_license' ||
          field.procedure_type === 'oficial' ||
          field.procedure_type === 'business_license'
      );
      return processFieldsForType(defaultFields);
    })(),
  });

  const formRef = useRef<HTMLFormElement>(null);
  const actionData = useActionData<typeof action>();
  const navigation = useNavigation();

  useEffect(() => {
    if (navigation.state === 'idle') {
      const link = document.createElement('a');

      link.target = '_blank';
      link.rel = 'noopener noreferrer';

      // Only auto-download if there's a URL but no requirements data to show in modal
      if (actionData?.requirements?.url && !actionData?.requirements?.data) {
        link.href = actionData.requirements.url;
      }

      if (property && actionData?.technicalSheetURL) {
        link.href = actionData.technicalSheetURL;
      }

      document.body.appendChild(link);

      if (link.href) {
        link.click();
      }

      document.body.removeChild(link);
    }
  }, [actionData, property]);

  // Handle requirements response for both commercial and construction licenses
  useEffect(() => {
    if (
      navigation.state === 'idle' &&
      actionData?.success &&
      actionData?.requirements
    ) {
      dispatch({ type: 'SET_SHOW_REQUIREMENTS_MODAL', show: true });
    }
  }, [actionData, navigation.state]);

  if (!property) {
    return (
      <div className="flex flex-col gap-4">
        <p>{tMap('noProperty.paragraph')}</p>
        <Button onClick={onDrawClick}>{tMap('noProperty.drawCTA')}</Button>
      </div>
    );
  }

  const propertyFields = [
    {
      key: 'municipality',
      label: tMap('property.municipality'),
      value: property?.municipality,
    },
    {
      key: 'locality',
      label: tMap('property.locality'),
      value: property?.locality,
    },
    {
      key: 'postalCode',
      label: tMap('property.postalCode'),
      value: property?.postalCode,
    },
    {
      key: 'neighborhood',
      label: tMap('property.colony'),
      value: property?.neighborhood,
    },
    {
      key: 'street',
      label: tMap('property.address'),
      value: property?.street,
    },
    {
      key: 'area',
      label: tMap('property.area'),
      value: property.area?.value ? (
        <>
          {property.area.value}
          {property.area.sup ? <sup>{property.area.sup}</sup> : null}
        </>
      ) : null,
    },
    {
      key: 'areaBuilt',
      label: tMap('property.constructionArea'),
      value: property.areaBuilt?.value ? (
        <>
          {property.areaBuilt.value}
          {property.areaBuilt.sup ? <sup>{property.areaBuilt.sup}</sup> : null}
        </>
      ) : null,
    },
    {
      key: 'technicalSheet',
      value: property ? (
        <Form method="POST">
          <input type="hidden" name="address" value={property.address} />
          <input
            type="hidden"
            name="square_meters"
            value={btoa(
              JSON.stringify({
                area: property.area?.raw,
                construccion: property.areaBuilt?.raw,
              })
            )}
          />
          <input
            type="hidden"
            name="coordinates"
            value={btoa(JSON.stringify(property.coordinates))}
          />
          <input
            type="hidden"
            name="image"
            value={property.minimapURL?.toString()}
          />
          <input
            type="hidden"
            name="municipality_id"
            value={property.municipalityId}
          />
          <input type="hidden" name="technical_sheet_download_id" value="2" />
          <Button
            className="w-full"
            type="submit"
            name="_intent"
            value="downloadTechnicalSheet"
          >
            {tMap('property.downloadTechnicalSheet')}
          </Button>
        </Form>
      ) : null,
    },
    {
      key: 'requirements',
      value: (
        <Button
          className="w-full"
          type="button"
          onClick={() => {
            dispatch({ type: 'SET_SECTION', section: 'requirements' });
          }}
        >
          <PlusCircle size={16} />
          {tMap('property.requirements.ctas.open')}
        </Button>
      ),
    },
    {
      key: 'minimapURL',
      value: property.minimapURL ? (
        <img
          src={
            typeof property.minimapURL === 'string'
              ? property.minimapURL
              : property.minimapURL?.toString()
          }
          alt={`Minimap showing property in ${property?.municipality}`}
        />
      ) : null,
    },
    {
      key: 'downloadURL',
      value: property.downloadURL ? (
        <div className="flex flex-col gap-2">
          <Button asChild>
            <Link
              to={property.downloadURL.toString()}
              target="_blank"
              rel="noreferrer noopener"
            >
              {tMap('property.downloadBlueprint.cta')}
            </Link>
          </Button>
          <small>{tMap('property.downloadBlueprint.disclaimer')}</small>
        </div>
      ) : null,
    },
  ].filter(field => field?.value !== null);

  const commercialLicenseSections: Section[] = [
    {
      name: 'general',
      inputs: [
        {
          name: 'municipality_id',
          type: 'hidden',
          value: `${property.municipalityId}`,
        },
        {
          name: 'license_type',
          type: 'hidden',
          value: 'commercial',
        },
        {
          name: 'minimap_sketch_url',
          type: 'hidden',
          value:
            typeof property.minimapURL === 'string'
              ? property.minimapURL
              : property.minimapURL?.toString(),
        },
        {
          name: 'minimap_url',
          type: 'hidden',
          value:
            typeof property.minimapURL === 'string'
              ? property.minimapURL
              : property.minimapURL?.toString(),
        },
        {
          name: 'property_area',
          type: 'hidden',
          value: `${(property.area?.raw ?? 0) * 1000}`,
        },
        {
          name: 'applicant_name',
          required: true,
        },
        {
          name: 'street',
          defaultValue: property.street,
          readOnly: true,
        },
        {
          name: 'neighborhood',
          defaultValue: property.neighborhood,
          readOnly: true,
        },
        {
          name: 'locality',
          defaultValue: property.locality,
          readOnly: true,
        },
        {
          name: 'municipality_name',
          defaultValue: property.municipality,
          readOnly: true,
        },
        {
          name: 'businessType',
          type: 'select',
          options:
            property.businessTypes?.map(type => ({
              label: type.name ?? '',
              value: `${type.id}|${type.name}`,
            })) ?? [],
          required: true,
        },
        {
          name: 'activity_area',
          pattern: '[0-9]+',
          title: tMap(
            'property.requirements.sections.general.inputs.activity_area.title'
          ),
          required: true,
        },
        {
          name: 'alcohol_sales',
          type: 'select',
          required: true,
          options: [
            {
              value: '0',
              label: tMap(
                'property.requirements.sections.general.inputs.alcohol_sales.options.0'
              ),
            },
            {
              value: '1',
              label: tMap(
                'property.requirements.sections.general.inputs.alcohol_sales.options.1'
              ),
            },
            {
              value: '2',
              label: tMap(
                'property.requirements.sections.general.inputs.alcohol_sales.options.2'
              ),
            },
            {
              value: '3',
              label: tMap(
                'property.requirements.sections.general.inputs.alcohol_sales.options.3'
              ),
            },
            {
              value: '4',
              label: tMap(
                'property.requirements.sections.general.inputs.alcohol_sales.options.4'
              ),
            },
          ],
        },
      ],
    },
    {
      name: 'procedure',
      inputs: state.dynamicFields || [],
    },
  ];

  // Helper function to create sections from dynamic fields
  const createDynamicSection = (
    licenseType: 'commercial' | 'construction'
  ): Section[] => {
    const baseFields: InputField[] = [
      {
        name: 'municipality_id',
        type: 'hidden',
        value: `${property.municipalityId}`,
      },
      {
        name: 'license_type',
        type: 'hidden',
        value: licenseType,
      },
      {
        name: 'street',
        defaultValue: property.street,
        required: true,
      },
      {
        name: 'neighborhood',
        defaultValue: property.neighborhood,
        required: true,
      },
      {
        name: 'municipality_name',
        defaultValue: property.municipality,
        type: 'hidden',
      },
      {
        name: 'interested_party',
        required: true,
      },
    ];

    // Add dynamic fields if available
    const dynamicFields = state.dynamicFields || [];

    return [
      {
        name: licenseType,
        inputs: [...baseFields, ...dynamicFields],
      },
    ];
  };

  return (
    <ul className="flex flex-col gap-4">
      {state.section === 'property'
        ? propertyFields.map(({ key, label, value }) => (
            <li
              key={key}
              className="border-accent border-t-1 py-2 flex flex-col gap-2"
            >
              {label ? <h2 className="font-bold">{label}</h2> : null}
              <span>{value}</span>
            </li>
          ))
        : null}
      {state.section === 'requirements' ? (
        <Form
          className="flex flex-col gap-6 py-4"
          method="POST"
          ref={formRef}
          key={state.licenseType ?? 'no-license'} // Force re-render when license type changes
        >
          <h1 className="font-bold text-xl flex gap-4 items-center">
            <Button
              variant="tertiary"
              type="button"
              onClick={() => {
                if (state.licenseType) {
                  dispatch({
                    type: 'SET_LICENSE_TYPE',
                    licenseType: undefined,
                  });
                  // Reset form when changing license type
                  if (formRef.current) {
                    formRef.current.reset();
                  }
                } else {
                  dispatch({ type: 'SET_SECTION', section: 'property' });
                }
              }}
            >
              <ArrowLeft />
            </Button>
            {tMap('property.requirements.title')}
          </h1>
          {!state.licenseType ? (
            <section className="flex flex-col gap-4">
              <h2 className="font-bold text-lg">
                {tMap('property.requirements.licenseTypeSelection.title')}
              </h2>
              <p className="text-gray-600">
                {tMap('property.requirements.licenseTypeSelection.description')}
              </p>
              <div className="flex flex-col gap-3">
                <Button
                  type="button"
                  onClick={() => {
                    dispatch({
                      type: 'SET_LICENSE_TYPE',
                      licenseType: 'commercial',
                    });
                    // Reset form when selecting license type
                    if (formRef.current) {
                      formRef.current.reset();
                    }
                  }}
                  className="w-full"
                >
                  {tMap(
                    'property.requirements.licenseTypeSelection.options.commercial'
                  )}
                </Button>
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => {
                    dispatch({
                      type: 'SET_LICENSE_TYPE',
                      licenseType: 'construction',
                    });
                    // Reset form when selecting license type
                    if (formRef.current) {
                      formRef.current.reset();
                    }
                  }}
                  className="w-full"
                >
                  {tMap(
                    'property.requirements.licenseTypeSelection.options.construction'
                  )}
                </Button>
              </div>
            </section>
          ) : (
            <>
              {(state.licenseType === 'commercial'
                ? commercialLicenseSections
                : createDynamicSection('construction')
              ).map((section: Section) => (
                <section key={section.name} className="flex flex-col gap-4">
                  <h2 className="font-bold text-lg">
                    {tMap(
                      `property.requirements.sections.${section.name}.title`
                    )}
                  </h2>
                  {section.inputs?.map((input: InputField) => {
                    const visibilityConditions = Object.getOwnPropertyNames(
                      state.visibilityConditions
                    ).map(key => state.visibilityConditions[key]);

                    if (
                      input.visibilityCondition &&
                      !visibilityConditions.includes(input.visibilityCondition)
                    ) {
                      return null;
                    }
                    const defaultValue = actionData?.formData?.[input.name];
                    const label =
                      input.type !== 'hidden'
                        ? tMap(
                            `property.requirements.sections.${section.name}.inputs.${input.name}.label`,
                            {
                              defaultValue: input.label,
                            }
                          )
                        : undefined;

                    switch (input.type) {
                      case 'boolean': {
                        return (
                          <Checkbox
                            key={input.name}
                            label={label ?? input.name}
                            name={input.name}
                            required={input.required}
                          />
                        );
                      }
                      case 'select': {
                        const { options = [], ...props } =
                          getFilteredProps(input);

                        return (
                          <Select {...props} label={label} key={input.name}>
                            {options.map((option: DynamicFieldOption) => (
                              <Option value={option.value} key={option.value}>
                                {option.label}
                              </Option>
                            ))}
                          </Select>
                        );
                      }
                      case 'radio': {
                        const { options = [], ...props } =
                          getFilteredProps(input);

                        return (
                          <RadioGroup
                            {...props}
                            key={input.name}
                            label={label}
                            options={options}
                          />
                        );
                      }
                      case 'hidden': {
                        const props = getFilteredProps(input);

                        return (
                          <input
                            {...props}
                            key={input.name}
                            value={input.value}
                          />
                        );
                      }
                      default: {
                        const props = getFilteredProps(input);

                        return (
                          <Input
                            defaultValue={defaultValue}
                            {...props}
                            key={input.name}
                            label={label}
                          />
                        );
                      }
                    }
                  })}
                </section>
              ))}
              <Button
                className="flex gap-2 items-center"
                type="submit"
                name="_intent"
                value="getRequirements"
              >
                <NotepadText size={16} />
                {tMap('property.requirements.ctas.submit')}
              </Button>
            </>
          )}
        </Form>
      ) : null}
      {/* Requirements Modal - Shows for both commercial and construction licenses */}
      {state.showRequirementsModal &&
        actionData?.success &&
        actionData?.requirements && (
          <Dialog
            open={true}
            onOpenChange={() =>
              dispatch({ type: 'SET_SHOW_REQUIREMENTS_MODAL', show: false })
            }
          >
            <DialogContent className="max-w-6xl max-h-[85vh] overflow-y-auto w-[95vw] sm:w-full p-6">
              <DialogTitle className="text-center pb-4">
                <div className="flex flex-col items-center gap-3">
                  <CheckCircle className="h-10 w-10 text-green-500" />
                  <span className="text-xl font-semibold">
                    {actionData?.requirements?.data?.license_type ===
                    'construction'
                      ? 'Requisitos para Licencia de Construcción'
                      : 'Requisitos para Licencia Comercial'}
                  </span>
                </div>
              </DialogTitle>
              <DialogDescription className="sr-only">
                Detalles de los requisitos para{' '}
                {actionData?.requirements?.data?.license_type === 'construction'
                  ? 'licencia de construcción'
                  : 'licencia comercial'}
              </DialogDescription>
              <div className="space-y-6">
                {actionData?.requirements?.data?.license_type ===
                'construction' ? (
                  <ConstructionRequirementsDisplay
                    requirements={
                      Array.isArray(
                        actionData?.requirements?.data?.requirements
                      )
                        ? (
                            actionData.requirements.data
                              .requirements as unknown[]
                          ).filter(
                            (req): req is ConstructionRequirement =>
                              req != null &&
                              typeof req === 'object' &&
                              'title' in req &&
                              'description' in req &&
                              'department_issued' in req
                          )
                        : []
                    }
                    folio={
                      actionData?.requirements?.data?.folio ??
                      actionData?.requirements?.folio ??
                      ''
                    }
                    municipalityName={property?.municipality ?? ''}
                    address={`${property?.street}, ${property?.neighborhood}`}
                    interestedParty={
                      actionData?.requirements?.data?.interested_party ?? ''
                    }
                  />
                ) : (
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <h3 className="font-semibold mb-2">
                          Información del Trámite
                        </h3>
                        <p>
                          <strong>Folio:</strong>{' '}
                          {actionData?.requirements?.data?.folio ??
                            actionData?.requirements?.folio}
                        </p>
                        <p>
                          <strong>Tipo:</strong> Licencia Comercial
                        </p>
                        <p>
                          <strong>Municipio:</strong> {property?.municipality}
                        </p>
                        <p>
                          <strong>Dirección:</strong> {property?.street},{' '}
                          {property?.neighborhood}
                        </p>
                      </div>
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <h3 className="font-semibold mb-2">Resumen</h3>
                        <p>
                          <strong>Total de requisitos:</strong>{' '}
                          {actionData?.requirements?.data?.total_requirements ??
                            0}
                        </p>
                        <p>
                          <strong>Estado:</strong> Pendiente de documentación
                        </p>
                      </div>
                    </div>
                    <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
                      <div className="flex">
                        <div className="ml-3">
                          <p className="text-sm text-yellow-700">
                            <strong>Próximos pasos:</strong> Deberá completar la
                            documentación requerida y presentarla en las
                            oficinas municipales correspondientes para continuar
                            con el proceso de licencia comercial.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                <div className="flex flex-wrap gap-3 justify-center pt-6 border-t border-gray-200">
                  {actionData?.requirements?.data?.url && (
                    <Button
                      variant="secondary"
                      onClick={() => {
                        const pdfUrl = `/${actionData.requirements.data.url}`;
                        window.open(pdfUrl, '_blank');
                      }}
                      className="flex items-center gap-2"
                    >
                      <NotepadText size={16} />
                      Ver PDF
                    </Button>
                  )}
                  <Button
                    variant="tertiary"
                    onClick={() =>
                      dispatch({
                        type: 'SET_SHOW_REQUIREMENTS_MODAL',
                        show: false,
                      })
                    }
                  >
                    Cerrar
                  </Button>
                  <Button
                    asChild
                    variant="primary"
                    className="flex items-center gap-2"
                  >
                    <Link
                      to={`/procedures/new/?folio=${actionData.requirements.data.folio}`}
                      target="_blank"
                    >
                      <PlusCircle size={16} />
                      Tramitar Licencia
                    </Link>
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        )}
    </ul>
  );
}
