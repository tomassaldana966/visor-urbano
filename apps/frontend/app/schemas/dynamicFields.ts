import { z } from 'zod';

// Schema for dynamic field definition (Spanish field names - legacy)
export const dynamicFieldSchema = z.object({
  id: z.number(),
  name: z.string(),
  field_type: z.enum([
    'input',
    'file',
    'multifile',
    'radio',
    'select',
    'dropdown',
    'textarea',
  ]),
  description: z.string().nullable().optional(),
  description_rec: z.string().nullable().optional(),
  rationale: z.string().nullable().optional(),
  options: z.string().nullable().optional(),
  options_description: z.string().nullable().optional(),
  step: z.number().min(1).max(4).optional(),
  sequence: z.number().optional(),
  required: z.boolean().optional(),
  visible_condition: z.string().nullable().optional(),
  affected_field: z.string().nullable().optional(),
  procedure_type: z.string().nullable().optional(),
  dependency_condition: z.string().nullable().optional(),
  trade_condition: z.string().nullable().optional(),
  status: z.number().optional(),
  municipality_id: z.number().optional(),
  editable: z.boolean().optional(),
  static_field: z.boolean().optional(),
  created_at: z.string().optional(),
  updated_at: z.string().optional(),
  deleted_at: z.string().optional(),
  required_official: z.boolean().optional(),
  value: z.string().nullable().optional(),
});

// Schema for static field definition
export const staticFieldSchema = z
  .object({
    id: z.number(),
    name: z.string(),
    field_type: z.string(), // Changed from 'type' to 'field_type' to match API response
    description: z.string(),
    description_rec: z.string().nullable().optional(),
    rationale: z.string().nullable().optional(),
    options: z.string().nullable().optional(),
    options_description: z.string().nullable().optional(),
    sequence: z.number().optional(),
    required: z.boolean().optional(), // Changed from number to boolean
    visible_condition: z.string().nullable().optional(),
    affected_field: z.string().nullable().optional(),
    procedure_type: z.string().nullable().optional(),
    dependency_condition: z.string().nullable().optional(),
    trade_condition: z.string().nullable().optional(),
    status: z.number().optional(),
    step: z.number().optional(),
    municipality_id: z.number(),
    value: z.string().nullable().optional(),
  })
  .transform(field => ({
    ...field,
    // Add 'type' field for backwards compatibility
    type: field.field_type,
  }));

// Schema for license information
export const licenseInfoSchema = z.object({
  hora_a: z.string().nullable().optional(),
  hora_c: z.string().nullable().optional(),
  superficie_autorizada: z.string().nullable().optional(),
});

// Schema for the API response format
export const apiDynamicFieldsResponseSchema = z
  .object({
    dynamic_fields: z.array(dynamicFieldSchema),
    static_fields: z.array(staticFieldSchema),
  })
  .transform(data => {
    // Transform to the expected tuple format
    return [
      data.dynamic_fields, // Already transformed by apiDynamicFieldSchema
      data.static_fields,
      [], // Empty license info array for now
    ] as [typeof data.dynamic_fields, typeof data.static_fields, never[]];
  });

// Schema for the complete dynamic fields response (legacy tuple format)
export const dynamicFieldsResponseSchema = z.tuple([
  z.array(dynamicFieldSchema),
  z.array(staticFieldSchema),
  z.array(licenseInfoSchema),
]);

// Schema for validation capture request
export const validationCaptureSchema = z.object({
  folio: z.string(),
  step: z.number().min(1).max(4),
  fields: z.record(z.unknown()),
});

// Type exports
export type DynamicField = z.infer<typeof dynamicFieldSchema>;
export type StaticField = z.infer<typeof staticFieldSchema>;
export type LicenseInfo = z.infer<typeof licenseInfoSchema>;
export type DynamicFieldsResponse = z.infer<typeof dynamicFieldsResponseSchema>;
export type ValidationCapture = z.infer<typeof validationCaptureSchema>;
export type ApiDynamicFieldsResponse = z.infer<
  typeof apiDynamicFieldsResponseSchema
>;

// Helper functions for field validation and processing
export const getFieldValidation = (field: DynamicField) => {
  const validations: any = {};

  // Required validation
  if (field.required) {
    validations.required = 'Este campo es requerido';
  }

  return validations;
};

// Parse field options from string format
export const parseFieldOptions = (
  field: DynamicField
): Array<{ value: string; label: string }> => {
  if (!field.options) return [];

  // Detect separator - check if pipe exists, otherwise use comma
  const hasPipe = field.options.includes('|');
  const separator = hasPipe ? '|' : ',';

  // Split by detected separator
  const options = field.options.split(separator);
  const descriptions = field.options_description
    ? field.options_description.split(separator)
    : [];

  const result = options.map((option, index) => ({
    value: descriptions[index]?.trim() || option.trim(), // Use descriptions as values (what gets sent to backend)
    label: option.trim(), // Use options as labels (what user sees)
  }));

  return result;
};

// Check if field should be visible based on conditions
export const isFieldVisible = (
  field: DynamicField,
  formValues: Record<string, unknown>
): boolean => {
  if (!field.visible_condition) return true;

  // Simple condition parser - can be expanded for more complex conditions
  try {
    // Example condition: "field_name=value"
    const [fieldName, expectedValue] = field.visible_condition.split('=');
    return formValues[fieldName?.trim()] === expectedValue?.trim();
  } catch {
    return true; // Show field if condition parsing fails
  }
};
