import { z } from 'zod';

export const MapLayerSchema = z.object({
  active: z.boolean(),
  attribution: z.string().nullable(),
  cql_filter: z.string().nullable(),
  editable: z.boolean(),
  format: z.string(),
  id: z.number(),
  label: z.string(),
  layers: z.string(),
  municipality_ids: z.array(z.number()),
  opacity: z.number(),
  order: z.number(),
  projection: z.string(),
  server_type: z
    .enum(['carmentaserver', 'geoserver', 'mapserver', 'qgis'])
    .nullable(),
  type_geom: z.string().nullable(),
  type: z.string(),
  url: z.string(),
  value: z.string(),
  version: z.string(),
  visible: z.boolean(),
});

// Form data schema for parsing HTML form values
export const MapLayerFormSchema = z
  .object({
    label: z.string().min(1, 'El nombre de la capa es requerido'),
    value: z.string().min(1, 'El valor de la capa es requerido'),
    layers: z.string().min(1, 'Las capas son requeridas'),
    type: z.string().min(1, 'El tipo de capa es requerido'),
    server_type: z.string().nullable().optional(),
    url: z.string().url('La URL debe ser válida'),
    format: z.string().min(1, 'El formato es requerido'),
    version: z.string().min(1, 'La versión es requerida'),
    projection: z.string().min(1, 'La proyección es requerida'),
    opacity: z.string().refine(val => {
      const num = Number(val);
      return !isNaN(num) && num >= 0 && num <= 1;
    }, 'La opacidad debe ser un número entre 0 y 1'),
    order: z.string().refine(val => {
      const num = Number(val);
      return !isNaN(num) && num >= 0;
    }, 'El orden debe ser un número mayor o igual a 0'),
    attribution: z.string().nullable().optional(),
    type_geom: z.string().nullable().optional(),
    cql_filter: z.string().nullable().optional(),
    active: z.string().optional(),
    visible: z.string().optional(),
    editable: z.string().optional(),
  })
  .transform(data => ({
    label: data.label,
    value: data.value,
    layers: data.layers,
    type: data.type,
    server_type: data.server_type ?? null,
    url: data.url,
    format: data.format,
    version: data.version,
    projection: data.projection,
    opacity: Number(data.opacity),
    order: Number(data.order),
    attribution: data.attribution ?? null,
    type_geom: data.type_geom ?? null,
    cql_filter: data.cql_filter ?? null,
    active: data.active === 'on',
    visible: data.visible === 'on',
    editable: data.editable === 'on',
  }));

// use MapLayerSchema ignore id
export const MapLayerCreateSchema = MapLayerSchema.omit({
  id: true,
});

// use MapLayerSchema ignore id and make all fields optional for partial updates
export const MapLayerUpdateSchema = MapLayerSchema.omit({
  id: true,
}).partial();

export const MapLayerResponseSchema = MapLayerSchema;

export const MapLayersSchema = z.array(MapLayerSchema);

export type MapLayer = z.infer<typeof MapLayerSchema>;
export type MapLayerForm = z.infer<typeof MapLayerFormSchema>;
export type MapLayerCreate = z.infer<typeof MapLayerCreateSchema>;
export type MapLayerUpdate = z.infer<typeof MapLayerUpdateSchema>;
export type MapLayerResponse = z.infer<typeof MapLayerResponseSchema>;
