import { z } from 'zod';
import { municipalitySignatureSchema } from './municipality-signatures';

export const municipalitySchema = z.object({
  id: z.number(),
  name: z.string(),
  image: z.string().nullable(),
  director: z.string().nullable(),
  director_signature: z.string().nullable(),
  process_sheet: z.number().nullable(),
  solving_days: z.number().nullable(),
  issue_license: z.number().nullable(),
  address: z.string().nullable(),
  phone: z.string().nullable(),
  email: z.string().nullable(),
  website: z.string().nullable(),
  responsible_area: z.string().nullable(),
  window_license_generation: z.number().nullable(),
  license_restrictions: z.string().nullable(),
  license_price: z.string().nullable(),
  initial_folio: z.number().nullable(),
  has_zoning: z.boolean().nullable(),

  // License configuration fields
  allow_online_procedures: z.boolean().nullable(),
  allow_window_reviewer_licenses: z.boolean().nullable(),
  low_impact_license_cost: z.string().nullable(),
  license_additional_text: z.string().nullable(),
  theme_color: z.string().nullable(),
  signatures: z.array(municipalitySignatureSchema).default([]),

  created_at: z.string().nullable(),
  updated_at: z.string().nullable(),
  deleted_at: z.string().nullable(),
});

// Schema for municipality settings update
export const municipalitySettingsUpdateSchema = z.object({
  name: z.string().min(1, 'El nombre es requerido'),
  director: z.string().min(1, 'El director es requerido'),
  address: z.string().min(1, 'La dirección es requerida'),
  phone: z.string().min(1, 'El teléfono es requerido'),
  email: z.string().email('Email inválido').optional().or(z.literal('')),
  website: z.string().url('URL inválida').optional().or(z.literal('')),
  responsible_area: z.string().min(1, 'El área responsable es requerida'),
  solving_days: z
    .number()
    .min(1, 'Los días para solventar deben ser mayor a 0')
    .optional(),
  initial_folio: z
    .number()
    .min(1, 'El folio inicial debe ser mayor a 0')
    .optional(),
  low_impact_license_cost: z.string().optional(),
  license_additional_text: z.string().optional(),
  allow_online_procedures: z.boolean().optional(),
  allow_window_reviewer_licenses: z.boolean().optional(),
  theme_color: z
    .string()
    .regex(/^#[0-9A-Fa-f]{6}$/, 'Color hexadecimal inválido')
    .optional()
    .or(z.literal('')),
});

export type Municipality = z.infer<typeof municipalitySchema>;
export type MunicipalitySettingsUpdate = z.infer<
  typeof municipalitySettingsUpdateSchema
>;
