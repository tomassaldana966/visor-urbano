import { z } from 'zod';

/*
calle -> street
colonia -> neighborhood
municipio -> municipality_name
id_municipio -> municipality_id
codigo_scian -> scian_code
nombre_scian -> scian_name
superficie_propiedad -> property_area
superficie -> activity_area
nombre -> applicant_name
caracter -> applicant_character
tipo_persona -> person_type
localidad -> locality
actividad -> activity_description
alcohol -> alcohol_sales
url_minimapa -> minimap_url
url_croquis -> minimap_sketch_url
restricciones -> restrictions
camposDinamicos -> dynamic_fields
*/

// Base schema with common fields shared between commercial and construction licenses
const baseRequirementsSchema = z.object({
  dynamic_fields: z.record(z.string()).optional(),
  folio: z.string().optional(),
  locality: z.string().optional(),
  minimap_sketch_url: z.string().optional(),
  minimap_url: z.string().optional(),
  municipality_id: z.string(),
  municipality_name: z.string().optional(),
  neighborhood: z.string().optional(),
  primary_folio: z.string().optional(),
  restrictions: z.record(z.unknown()).optional(),
  street: z.string().optional(),
  entry_date: z.string().optional(), // Auto-generated but can be included
  // Common intent field
  _intent: z.string().optional(),
});

// Commercial license requirements schema
export const commercialRequirementsSchema = baseRequirementsSchema.extend({
  license_type: z.literal('commercial'),
  // Commercial specific fields
  activity_area: z.string(),
  activity_description: z.string(),
  alcohol_sales: z.string(),
  applicant_character: z.string(),
  applicant_name: z.string(),
  person_type: z.string().optional(),
  property_area: z.string().optional(),
  scian_code: z.string().optional(),
  scian_name: z.string().optional(),
  scian: z.string().optional(), // For commercial licenses (SCIAN code)
});

// Construction license requirements schema
export const constructionRequirementsSchema = baseRequirementsSchema.extend({
  license_type: z.literal('construction'),
  // Construction specific fields
  interested_party: z.string().optional(), // For construction licenses
  last_resolution: z.string().optional(), // For construction licenses
  resolution_sense: z.string().optional(), // For construction licenses
  construction_type: z.string().optional(),
});

// Union schema for backwards compatibility
export const requirementsSchema = z.union([
  commercialRequirementsSchema,
  constructionRequirementsSchema,
]);

export const dynamicFieldSchema = z.object({
  affected_field: z.string().nullable(),
  dependency_condition: z.string().nullable(),
  description_rec: z.string().nullable(),
  description: z.string().nullable(),
  field_type: z.enum([
    'radio',
    'text',
    'email',
    'file',
    'textarea',
    'number',
    'date',
    'boolean',
    'select',
    'dropdown',
    'document',
    'input',
    'multifile',
  ]),
  id: z.number().nullable(),
  municipality_id: z.number().nullable(),
  name: z.string(),
  options_description: z.string().nullable(),
  options: z.string().nullable(),
  procedure_type: z.string().nullable(),
  rationale: z.string().nullable(),
  required: z
    .union([z.boolean(), z.number()])
    .nullable()
    .transform(val => {
      if (val === null || val === undefined) return false;
      if (typeof val === 'boolean') return val;
      return Boolean(val);
    }),
  sequence: z.number().nullable(),
  status: z.number().nullable(),
  step: z.number().nullable(),
  trade_condition: z.string().nullable(),
  visible_condition: z.string().nullable(),
  editable: z
    .union([z.boolean(), z.number()])
    .nullable()
    .optional()
    .transform(val => {
      if (val === null || val === undefined) return true; // Default to true for editable
      if (typeof val === 'boolean') return val;
      return Boolean(val);
    }),
  static_field: z
    .union([z.boolean(), z.number()])
    .nullable()
    .optional()
    .transform(val => {
      if (val === null || val === undefined) return false;
      if (typeof val === 'boolean') return val;
      return Boolean(val);
    }),
  created_at: z.string().optional(),
  updated_at: z.string().optional(),
  deleted_at: z.string().optional(),
  required_official: z
    .union([z.boolean(), z.number()])
    .nullable()
    .optional()
    .transform(val => {
      if (val === null || val === undefined) return false;
      if (typeof val === 'boolean') return val;
      return Boolean(val);
    }),
  value: z.string().nullable().optional(),
});

export const dynamicFieldsSchema = z.array(dynamicFieldSchema);

// Export types
export type CommercialRequirements = z.infer<
  typeof commercialRequirementsSchema
>;
export type ConstructionRequirements = z.infer<
  typeof constructionRequirementsSchema
>;
export type Requirements = z.infer<typeof requirementsSchema>;
export type DynamicField = z.infer<typeof dynamicFieldSchema>;
export type DynamicFields = z.infer<typeof dynamicFieldsSchema>;
