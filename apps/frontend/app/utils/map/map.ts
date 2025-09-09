import { formatNumberToArea } from '@root/app/components/OpenLayerMap/utils';
import proj4 from 'proj4';
import {
  bbox,
  buffer,
  area as turfArea,
  polygon,
  simplify,
  centroid,
} from '@turf/turf';
import { z } from 'zod';
import Polygon from 'ol/geom/Polygon';
import MultiPolygon from 'ol/geom/MultiPolygon';

interface WFSBaseParams {
  geoServerURL?: string;
}

interface WMSGetMapParams extends WFSBaseParams {
  BBOX: `${number},${number},${number},${number}`;
  cql_filter: string;
  CRS: 'EPSG:4326';
  exceptions: 'application/vnd.ogc.se_inimage';
  FORMAT: 'image/png8';
  height: number;
  layers: string;
  request: 'GetMap';
  service: 'WMS';
  styles: string;
  version: '1.3.0';
  width: number;
}

export interface WMSGetFeatureInfoParams extends WFSBaseParams {
  BBOX: string;
  CRS: 'EPSG:4326';
  FEATURE_COUNT: number;
  FORMAT: 'image/png';
  HEIGHT: number;
  I: number;
  INFO_FORMAT: 'application/json';
  J: number;
  LAYERS: string;
  QUERY_LAYERS: string;
  REQUEST: 'GetFeatureInfo';
  SERVICE: 'WMS';
  SRS?: string;
  STYLES: '';
  TILED: 'true';
  TILESORIGIN: '-180,-90';
  TRANSPARENT: 'true';
  VERSION: '1.3.0';
  WIDTH: number;
}

interface WFSGetFeatureBaseParams extends WFSBaseParams {
  service: 'WFS';
  request: 'GetFeature';
  version: '2.0.0';
  count?: number;
  typename: string;
  outputFormat: string;
  cql_filter: string;
}

interface WFSGetFeatureShapeZipParams extends WFSGetFeatureBaseParams {
  typename: string;
  outputFormat: 'shape-zip';
  format_options: string;
  cql_filter: string;
}

interface WFSGetFeatureJsonParams extends WFSGetFeatureBaseParams {
  typename: string;
  outputFormat: 'application/json';
  cql_filter: string;
}

export type MapServiceSearchParams =
  | WMSGetMapParams
  | WMSGetFeatureInfoParams
  | WFSGetFeatureShapeZipParams
  | WFSGetFeatureJsonParams;

function generateGeoServerURL(paramsFromArgs: MapServiceSearchParams) {
  const url = new URL(
    `${paramsFromArgs.geoServerURL ?? process.env.GEOSERVER_URL}/ows`
  );

  const params = new URLSearchParams();

  for (const [key, value] of Object.entries(paramsFromArgs)) {
    if (key !== 'geoServerURL') {
      params.append(key, String(value));
    }
  }

  url.search = params.toString();

  return url;
}

export async function fetchGeoServer(params: MapServiceSearchParams) {
  const url = generateGeoServerURL(params);

  return fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(
          `GeoServer request failed with status ${response.status}: ${response.statusText}`
        );
      }
      return response.json();
    })
    .catch(error => {
      return {};
    });
}

function urlMinimap(
  bbox: number[],
  id: string | null,
  overridePolygon?: number[][] | null
) {
  if (!id) {
    return '';
  }

  let cqlFilter = `INCLUDE;fid=${id}`;

  if (overridePolygon && overridePolygon.length > 0) {
    const wktCoordinates = overridePolygon
      .map(coord => `${coord[0]} ${coord[1]}`)
      .join(',');
    const wktPolygon = `POLYGON((${wktCoordinates}))`;
    cqlFilter = `INCLUDE;INTERSECTS(geom,${wktPolygon})`;
  }

  return generateGeoServerURL({
    service: 'WMS',
    version: '1.3.0',
    request: 'GetMap',
    FORMAT: 'image/png8',
    layers: `${process.env.MAP_CROQUIS_BASE},${process.env.MAP_PREDIOS_LAYER}`,
    exceptions: 'application/vnd.ogc.se_inimage',
    CRS: 'EPSG:4326',
    width: 600,
    height: 600,
    styles: `${process.env.MAP_CROQUIS_BASE_STYLE},${process.env.MAP_CROQUIS_PREDIO_STYLE}`,
    cql_filter: cqlFilter,
    BBOX: `${bbox[1]},${bbox[0]},${bbox[3]},${bbox[2]}`,
  });
}

export async function getPropertyData(
  response: Record<string, unknown>,
  overridePolygon?: number[][] | null
) {
  const schema = z.object({
    type: z.string(),
    features: z
      .array(
        z.object({
          type: z.literal('Feature').optional(),
          id: z.string(),
          geometry: z.union([
            z.object({
              type: z.literal('Polygon'),
              coordinates: z.array(z.array(z.array(z.number()))),
            }),
            z.object({
              type: z.literal('MultiPolygon'),
              coordinates: z.array(z.array(z.array(z.array(z.number())))),
            }),
          ]),
          geometry_name: z.string(),
          properties: z
            .object({
              AGUA_POT: z.string(),
              ALUMBRADO: z.string(),
              BASURA: z.string(),
              CAL_POS: z.string(),
              CLAS_EQUIP: z.string(),
              CLAS_TEN: z.string(),
              CP: z.string(),
              CVE_CAT: z.string(),
              CVE_STD: z.string(),
              DRENAJE: z.string(),
              ENCARGADO: z.string(),
              fid: z.number(),
              FOLIO_REAL: z.string(),
              FUENTE: z.string(),
              LAT: z.string(),
              LON: z.string(),
              LUZ: z.string(),
              municipio_id: z.number(),
              NOM_AH: z.string(),
              NOM_ENT: z.string(),
              NOM_EQUIP: z.string(),
              NOM_LOC: z.string(),
              NOM_MUN: z.string(),
              NOM_REG: z.string(),
              NOM_VIAL: z.string(),
              NOM_ZNA: z.string(),
              NUM_EXT: z.string(),
              NUM_INT: z.string(),
              OBJECTID: z.number(),
              PAVIMENTO: z.string(),
              SUP_CONST: z.number().nullable(),
              SUP_TOT: z.number().nullable(),
              TIPO_ASEN: z.string(),
              TIPO_EQUIP: z.string(),
              TIPO_TEN: z.string(),
              TIPO_VIAL: z.string(),
              TOT_PROP: z.string(),
            })
            .optional(),
          bbox: z.array(z.number()),
        })
      )
      .optional(),
    totalFeatures: z.number(),
    numberMatched: z.number(),
    numberReturned: z.number(),
    timeStamp: z.string(),
    crs: z
      .object({
        type: z.string(),
        properties: z.object({
          name: z.string(),
        }),
      })
      .optional()
      .nullable(),
    bbox: z.array(z.number()).optional(),
  });

  const result = schema.safeParse(response);

  if (result.success) {
    const feature = result.data.features?.[0];

    let responseData = result.data;

    if (overridePolygon) {
      const polygonFeature = polygon([overridePolygon]);
      const polygonBbox = bbox(polygonFeature);

      if (!responseData.crs) {
        responseData = {
          ...responseData,
          crs: {
            type: 'name',
            properties: {
              name: 'EPSG:4326',
            },
          },
        };
      }

      if (!responseData.bbox) {
        responseData = {
          ...responseData,
          bbox: polygonBbox,
        };
      }

      if (!responseData.features || responseData.features.length === 0) {
        responseData = {
          ...responseData,
          totalFeatures: 1,
          numberMatched: 1,
          numberReturned: 1,
          features: [],
        };
      }
    }

    let propertyGeom: number[][] = [];
    let coordinates: number[][] = [];
    let olGeom;
    let modifiedResponse = responseData;

    if (overridePolygon) {
      const transformedCoordinates = overridePolygon.map(coord =>
        proj4('EPSG:4326', process.env.MAP_LOCAL_SRS ?? 'EPSG:32613', coord)
      );

      coordinates = transformedCoordinates;
      propertyGeom = overridePolygon;

      const defaultProperties = {
        AGUA_POT: '',
        ALUMBRADO: '',
        BASURA: '',
        CAL_POS: '',
        CLAS_EQUIP: '',
        CLAS_TEN: '',
        CP: '',
        CVE_CAT: '',
        CVE_STD: '',
        DRENAJE: '',
        ENCARGADO: '',
        fid: 0,
        FOLIO_REAL: '',
        FUENTE: '',
        LAT: '',
        LON: '',
        LUZ: '',
        municipio_id: 0,
        NOM_AH: '',
        NOM_ENT: '',
        NOM_EQUIP: '',
        NOM_LOC: '',
        NOM_MUN: '',
        NOM_REG: '',
        NOM_VIAL: '',
        NOM_ZNA: '',
        NUM_EXT: '',
        NUM_INT: '',
        OBJECTID: 0,
        PAVIMENTO: '',
        SUP_CONST: null,
        SUP_TOT: null,
        TIPO_ASEN: '',
        TIPO_EQUIP: '',
        TIPO_TEN: '',
        TIPO_VIAL: '',
        TOT_PROP: '',
      };

      const modifiedFeature = {
        type: 'Feature' as const,
        id: feature?.id ?? 'uploaded-polygon',
        geometry_name: feature?.geometry_name ?? 'geom',
        bbox: feature?.bbox ?? [],
        properties: feature?.properties ?? defaultProperties,
        geometry: {
          type: 'Polygon' as const,
          coordinates: [transformedCoordinates],
        },
      };

      modifiedResponse = {
        ...responseData,
        features: [modifiedFeature],
      };

      olGeom = new Polygon([transformedCoordinates]);
    } else if (feature && feature.geometry) {
      const geom = simplify(feature.geometry, {
        tolerance: 2,
        highQuality: false,
      });

      if (geom.type === 'Polygon') {
        coordinates = geom.coordinates[0];
        olGeom = new Polygon(geom.coordinates);
      } else if (geom.type === 'MultiPolygon') {
        coordinates = geom.coordinates[0][0];
        olGeom = new MultiPolygon(geom.coordinates);
      }

      coordinates.forEach(vert => {
        propertyGeom.push(
          proj4(process.env.MAP_LOCAL_SRS ?? 'EPSG:32613', 'EPSG:4326', vert)
        );
      });
    } else {
      throw new Error('Feature or feature geometry is undefined.');
    }

    if (propertyGeom.length === 0) {
      throw new Error('Invalid geometry: propertyGeom is empty.');
    }

    const propertyPolygon = polygon([propertyGeom]);

    const area = formatNumberToArea(turfArea(propertyPolygon));

    const areaBuilt = formatNumberToArea(feature?.properties?.SUP_CONST);

    const buffered = buffer(propertyPolygon, 50, { units: 'meters' });

    if (!buffered) {
      throw new Error('Buffering failed for feature geometry');
    }

    const boundingBox = bbox(buffered);

    const downloadURL = generateGeoServerURL({
      service: 'WFS',
      request: 'GetFeature',
      version: '2.0.0',
      typename: `${process.env.MAP_PREDIOS_LAYER}`,
      outputFormat: 'shape-zip',
      format_options: 'filename:extract.zip',
      cql_filter: `${process.env.MAP_PREDIOS_LAYER_ID}=${feature?.properties?.fid}`,
    });

    const minimapURL = urlMinimap(
      boundingBox,
      `${feature?.properties?.fid}`,
      overridePolygon
    );

    const municipality = feature?.properties?.NOM_MUN;

    const locality = feature?.properties?.NOM_LOC;

    const postalCode = feature?.properties?.CP;

    const neighborhood = feature?.properties?.NOM_AH;

    const street = feature?.properties?.NOM_VIAL;

    const address = `${street} ${feature?.properties?.NUM_EXT}, ${neighborhood}, ${locality}, ${postalCode}`;

    return {
      ...modifiedResponse,
      address,
      area,
      areaBuilt,
      boundingBox,
      coordinates: propertyGeom,
      downloadURL,
      id: feature?.id,
      locality,
      minimapURL,
      municipality,
      municipalityId: feature?.properties?.municipio_id,
      neighborhood,
      postalCode,
      street,
    };
  } else {
    throw new Error(`Error validating response: ${result.error}`);
  }
}

export function getPolygonCenter(polygonCoordinates: number[][]) {
  try {
    const polygonFeature = polygon([polygonCoordinates]);
    const center = centroid(polygonFeature);
    return center.geometry.coordinates;
  } catch (error) {
    console.error('Error calculating polygon center:', error);
    return null;
  }
}

export function encodePolygonToBase64(coordinates: number[][]): string {
  try {
    const jsonString = JSON.stringify(coordinates);
    return btoa(jsonString);
  } catch (error) {
    console.error('Error encoding polygon to base64:', error);
    return '';
  }
}

export function decodePolygonFromBase64(
  base64String: string
): number[][] | null {
  try {
    const jsonString = atob(base64String);
    return JSON.parse(jsonString);
  } catch (error) {
    console.error('Error decoding polygon from base64:', error);
    return null;
  }
}
