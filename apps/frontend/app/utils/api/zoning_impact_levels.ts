import { z } from 'zod';
import { requestAPI } from './base';

const PolygonSchema = z.object({
  type: z.literal('Polygon'),
  coordinates: z.array(z.array(z.array(z.number()))),
});

const ZoningImpactLevelSchema = z.object({
  id: z.number(),
  impact_level: z.number(),
  municipality_id: z.number(),
  geom: PolygonSchema.nullable(),
});

const ZoningImpactLevelsArraySchema = z.array(ZoningImpactLevelSchema);

export type ZoningImpactLevel = z.infer<typeof ZoningImpactLevelSchema>;
export type Polygon = z.infer<typeof PolygonSchema>;

export interface CreateZoningImpactLevelData {
  impact_level: number;
  municipality_id: number;
  geom?: Polygon;
}

export interface UpdateZoningImpactLevelData {
  impact_level?: number;
  municipality_id?: number;
  geom?: Polygon;
}

export async function getZoningImpactLevels(
  municipality_id: number,
  authToken: string
): Promise<ZoningImpactLevel[]> {
  return requestAPI({
    endpoint: 'v1/zoning_impact_levels/',
    method: 'GET',
    authToken,
    data: { municipality_id },
  }).then(response => {
    const result = ZoningImpactLevelsArraySchema.safeParse(response);
    if (result.success) {
      return result.data;
    }
    throw new Error('Invalid response format for zoning impact levels');
  });
}

export async function getZoningImpactLevel(
  id: number,
  authToken: string
): Promise<ZoningImpactLevel> {
  return requestAPI({
    endpoint: `v1/zoning_impact_levels/${id}`,
    method: 'GET',
    authToken,
  }).then(response => {
    const result = ZoningImpactLevelSchema.safeParse(response);
    if (result.success) {
      return result.data;
    }
    throw new Error('Invalid response format for zoning impact level');
  });
}

export async function createZoningImpactLevel(
  data: CreateZoningImpactLevelData,
  authToken: string
): Promise<ZoningImpactLevel> {
  return requestAPI({
    endpoint: 'v1/zoning_impact_levels/',
    method: 'POST',
    authToken,
    data,
  }).then(response => {
    const result = ZoningImpactLevelSchema.safeParse(response);
    if (result.success) {
      return result.data;
    }
    throw new Error('Invalid response format for created zoning impact level');
  });
}

export async function updateZoningImpactLevel(
  id: number,
  data: UpdateZoningImpactLevelData,
  authToken: string
): Promise<ZoningImpactLevel> {
  return requestAPI({
    endpoint: `v1/zoning_impact_levels/${id}`,
    method: 'PATCH',
    authToken,
    data,
  }).then(response => {
    const result = ZoningImpactLevelSchema.safeParse(response);
    if (result.success) {
      return result.data;
    }
    throw new Error('Invalid response format for updated zoning impact level');
  });
}

export async function deleteZoningImpactLevel(
  id: number,
  authToken: string
): Promise<void> {
  return requestAPI({
    endpoint: `v1/zoning_impact_levels/${id}`,
    method: 'DELETE',
    authToken,
  });
}
