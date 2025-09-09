import { z } from 'zod';

export const geoCodeResultSchema = z.object({
  address_components: z.array(
    z.object({
      long_name: z.string(),
      short_name: z.string(),
      types: z.array(z.string()),
    })
  ),
  formatted_address: z.string(),
  geometry: z.object({
    bounds: z.object({
      northeast: z.object({
        lat: z.number(),
        lng: z.number(),
      }),
      southwest: z.object({
        lat: z.number(),
        lng: z.number(),
      }),
    }),
    location: z.object({
      lat: z.number(),
      lng: z.number(),
    }),
    location_type: z.string(),
    viewport: z.object({
      northeast: z.object({
        lat: z.number(),
        lng: z.number(),
      }),
      southwest: z.object({
        lat: z.number(),
        lng: z.number(),
      }),
    }),
  }),
  partial_match: z.boolean(),
  place_id: z.string(),
  types: z.array(z.string()),
});

export type GeoCodeResult = z.infer<typeof geoCodeResultSchema>;
