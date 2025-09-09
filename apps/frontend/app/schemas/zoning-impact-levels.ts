import { z } from 'zod';

export const PolygonSchema = z.object({
  type: z.literal('Polygon'),
  coordinates: z.array(z.array(z.array(z.number()))),
});

export const ZoningImpactLevelSchema = z.object({
  id: z.number(),
  impact_level: z.number(),
  municipality_id: z.number(),
  geom: PolygonSchema.nullable(),
});

export const ZoningImpactLevelsArraySchema = z.array(ZoningImpactLevelSchema);

export const CreateZoningImpactLevelSchema = z.object({
  impact_level: z.number(),
  municipality_id: z.number(),
  geom: PolygonSchema.optional(),
});

export const UpdateZoningImpactLevelSchema = z.object({
  impact_level: z.number().optional(),
  municipality_id: z.number().optional(),
  geom: PolygonSchema.optional(),
});

export const ZoningImpactLevelQuerySchema = z.object({
  municipality_id: z.number(),
});
