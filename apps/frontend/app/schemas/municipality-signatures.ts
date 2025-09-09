import { z } from 'zod';

export const municipalitySignatureSchema = z.object({
  id: z.number(),
  municipality_id: z.number(),
  position_title: z.string(),
  signer_name: z.string(),
  signature_image: z.string().nullable(),
  order_index: z.number().min(1).max(4),
  is_active: z.string(),
  created_at: z.string().nullable(),
  updated_at: z.string().nullable(),
});

export const municipalitySignatureCreateSchema = z.object({
  position_title: z.string().min(1, 'El cargo es requerido'),
  signer_name: z.string().min(1, 'El nombre es requerido'),
  order_index: z.number().min(1).max(4),
  is_active: z.string().default('Y'),
});

export const municipalitySignatureUpdateSchema = z.object({
  position_title: z.string().min(1, 'El cargo es requerido').optional(),
  signer_name: z.string().min(1, 'El nombre es requerido').optional(),
  order_index: z.number().min(1).max(4).optional(),
  is_active: z.string().optional(),
});

export type MunicipalitySignature = z.infer<typeof municipalitySignatureSchema>;
export type MunicipalitySignatureCreate = z.infer<
  typeof municipalitySignatureCreateSchema
>;
export type MunicipalitySignatureUpdate = z.infer<
  typeof municipalitySignatureUpdateSchema
>;
