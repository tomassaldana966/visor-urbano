import { z } from 'zod';
import { PolygonSchema } from './zoning-impact-levels';

export const CreateImpactLevelFormSchema = z.object({
  _intent: z.literal('create'),
  impact_level: z
    .string()
    .transform(val => Number(val))
    .pipe(z.number().min(1).max(5)),
  municipality_id: z
    .string()
    .transform(val => Number(val))
    .pipe(z.number().positive()),
  geom: z
    .string()
    .transform(val => JSON.parse(val))
    .pipe(PolygonSchema),
});

export const UpdateImpactLevelFormSchema = z.object({
  _intent: z.literal('update'),
  id: z
    .string()
    .transform(val => Number(val))
    .pipe(z.number().positive()),
  impact_level: z
    .string()
    .transform(val => Number(val))
    .pipe(z.number().min(1).max(5))
    .optional(),
  geom: z
    .string()
    .transform(val => JSON.parse(val))
    .pipe(PolygonSchema)
    .optional(),
});

export const DeleteImpactLevelFormSchema = z.object({
  _intent: z.literal('delete'),
  id: z
    .string()
    .transform(val => Number(val))
    .pipe(z.number().positive()),
});

export const ImpactMapFormSchema = z.discriminatedUnion('_intent', [
  CreateImpactLevelFormSchema,
  UpdateImpactLevelFormSchema,
  DeleteImpactLevelFormSchema,
]);

export type CreateImpactLevelForm = z.infer<typeof CreateImpactLevelFormSchema>;
export type UpdateImpactLevelForm = z.infer<typeof UpdateImpactLevelFormSchema>;
export type DeleteImpactLevelForm = z.infer<typeof DeleteImpactLevelFormSchema>;
export type ImpactMapForm = z.infer<typeof ImpactMapFormSchema>;
