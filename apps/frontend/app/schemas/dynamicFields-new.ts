import { z } from 'zod';

// Schema for dynamic field definition (Spanish field names - legacy)
export const dynamicFieldSchema = z.object({
  id: z.number(),
  name: z.string(),
  type: z.enum(['input', 'file', 'multifile', 'radio', 'select', 'textarea']),
  description: z.string(),
  description_rec: z.string().nullable().optional(),
  fundamento: z.string().nullable().optional(),
  opciones: z.string().nullable().optional(), // Options separated by |
  opciones_desc: z.string().nullable().optional(), // Option descriptions
  secuencia: z.number(),
  requerido: z.boolean(),
  requerido_funcionario: z.boolean().optional(),
  condicion_visible: z.string().nullable().optional(),
  condicion_dependencia: z.string().nullable().optional(),
  condicion_giro: z.string().nullable().optional(),
  campo_afectado: z.string().nullable().optional(),
  tipo_tramite: z.string().nullable().optional(),
  status: z.number(),
  step: z.number().min(1).max(4), // 1-4 sections
  id_municipio: z.number(),
  campo_estatico: z.boolean().optional(),
  value: z.string().nullable().optional(), // Current value from responses
  created_at: z.string().optional(),
  updated_at: z.string().optional(),
});

// Schema for dynamic field definition from API (English field names)
export const apiDynamicFieldSchema = z
  .object({
    id: z.number(),
    name: z.string(),
    field_type: z.string(), // Maps to 'type'
    description: z.string(),
    description_rec: z.string().nullable().optional(),
    rationale: z.string().nullable().optional(), // Maps to 'fundamento'
    options: z.string().nullable().optional(), // Maps to 'opciones'
    options_description: z.string().nullable().optional(), // Maps to 'opciones_desc'
    sequence: z.number(), // Maps to 'secuencia'
    required: z.number(), // Maps to 'requerido' (0/1 instead of boolean)
    visible_condition: z.string().nullable().optional(),
    affected_field: z.string().nullable().optional(),
    procedure_type: z.string().nullable().optional(),
    dependency_condition: z.string().nullable().optional(),
    trade_condition: z.string().nullable().optional(),
    status: z.number(),
    step: z.number().min(1).max(4),
    municipality_id: z.number(), // Maps to 'id_municipio'
    value: z.string().nullable().optional(),
  })
  .transform(data => ({
    // Transform API response to match the expected format
    id: data.id,
    name: data.name,
    type: data.field_type as
      | 'input'
      | 'file'
      | 'multifile'
      | 'radio'
      | 'select'
      | 'textarea',
    description: data.description,
    description_rec: data.description_rec,
    fundamento: data.rationale,
    opciones: data.options,
    opciones_desc: data.options_description,
    secuencia: data.sequence,
    requerido: data.required === 1, // Convert 0/1 to boolean
    condicion_visible: data.visible_condition,
    campo_afectado: data.affected_field,
    tipo_tramite: data.procedure_type,
    condicion_dependencia: data.dependency_condition,
    condicion_giro: data.trade_condition,
    status: data.status,
    step: data.step,
    id_municipio: data.municipality_id,
    value: data.value,
  }));

// Schema for static field definition
export const staticFieldSchema = z.object({
  id: z.number(),
  name: z.string(),
  type: z.string(),
  description: z.string(),
  value: z.string().nullable().optional(),
});

// Schema for license information
export const licenseInfoSchema = z.object({
  hora_a: z.string().nullable().optional(),
  hora_c: z.string().nullable().optional(),
  superficie_autorizada: z.string().nullable().optional(),
});

// Schema for the API response format
export const apiDynamicFieldsResponseSchema = z
  .object({
    dynamic_fields: z.array(apiDynamicFieldSchema),
    static_fields: z.array(staticFieldSchema),
  })
  .transform(data => {
    // Transform to the expected tuple format
    return [
      data.dynamic_fields, // Already transformed by apiDynamicFieldSchema
      data.static_fields,
      [], // Empty license info array for now
    ] as const;
  });

// Schema for the complete dynamic fields response (legacy tuple format)
export const dynamicFieldsResponseSchema = z.tuple([
  z.array(dynamicFieldSchema), // campos_dinamicos
  z.array(staticFieldSchema), // campos_estaticos
  z.array(licenseInfoSchema), // licencias
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
