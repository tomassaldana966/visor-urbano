import { z } from 'zod';

export const businessTypeSchema = z.object({
  business_type_id: z.number(),
  municipality_id: z.number(),
  id: z.number(),
  is_disabled: z.boolean(),
  has_certificate: z.boolean(),
  impact_level: z.union([z.number(), z.null()]),
  name: z.union([z.string(), z.null()]),
  description: z.union([z.string(), z.null()]),
  code: z.union([z.string(), z.null()]),
  related_words: z.union([z.string(), z.null()]),
});

export const businessTypesSchema = z.array(businessTypeSchema);

export const createBusinessTypeSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().min(1, 'Description is required'),
  code: z.string().min(1, 'SCIAN code is required'),
  related_words: z.string().min(1, 'Related words are required'),
  is_active: z.boolean().default(true),
});

export const updateBusinessTypeStatusSchema = z.object({
  business_type_id: z.number(),
});

export const updateBusinessTypeCertificateSchema = z.object({
  business_type_id: z.number(),
  status: z.boolean(),
});

export const businessTypeImpactUpdateSchema = z.object({
  business_type_id: z.number(),
  impact_level: z.number(),
});
