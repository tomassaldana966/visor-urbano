import { encodePolygonToBase64 } from '@root/app/utils/map/map';

export interface ProcessedFileResult {
  coordinates: number[][];
  polygonBase64: string;
  featureCount: number;
  fileName: string;
}

export interface FileProcessingError {
  message: string;
  details?: string;
}

export async function processUploadedFile(
  file: File
): Promise<ProcessedFileResult | FileProcessingError> {
  try {
    const fileExtension = getFileExtension(file.name);

    switch (fileExtension) {
      case 'geojson':
      case 'json':
        return await processGeoJSONFile(file);
      case 'kml':
        return await processKMLFile(file);
      case 'kmz':
        return await processKMZFile(file);
      case 'zip':
        return await processShapefileZip(file);
      default:
        return {
          message: 'Unsupported file format',
          details: `File extension "${fileExtension}" is not supported. Please upload a GeoJSON, KML, KMZ, or Shapefile (ZIP) file.`,
        };
    }
  } catch (error) {
    return {
      message: 'Error processing file',
      details:
        error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
}

function getFileExtension(fileName: string): string {
  return fileName.split('.').pop()?.toLowerCase() ?? '';
}

async function processGeoJSONFile(
  file: File
): Promise<ProcessedFileResult | FileProcessingError> {
  const text = await file.text();

  try {
    const geoJSON = JSON.parse(text);
    return extractPolygonFromGeoJSON(geoJSON, file.name);
  } catch {
    return {
      message: 'Invalid GeoJSON format',
      details: 'The file does not contain valid JSON.',
    };
  }
}

async function processKMLFile(
  file: File
): Promise<ProcessedFileResult | FileProcessingError> {
  const text = await file.text();

  try {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(text, 'application/xml');

    if (xmlDoc.documentElement.nodeName === 'parsererror') {
      return {
        message: 'Invalid KML format',
        details: 'The file does not contain valid XML.',
      };
    }

    return extractPolygonFromKML(xmlDoc, file.name);
  } catch (error) {
    return {
      message: 'Error parsing KML file',
      details:
        error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
}

async function processKMZFile(
  file: File
): Promise<ProcessedFileResult | FileProcessingError> {
  return {
    message: 'KMZ files not fully supported',
    details: 'Please extract the KMZ file and upload the KML file inside it.',
  };
}

async function processShapefileZip(
  file: File
): Promise<ProcessedFileResult | FileProcessingError> {
  // Shapefile processing would require additional libraries
  // For now, we'll return an error suggesting conversion
  return {
    message: 'Shapefile processing not implemented',
    details:
      'Please convert your Shapefile to GeoJSON format and upload that instead.',
  };
}

function extractPolygonFromGeoJSON(
  geoJSON: unknown,
  fileName: string
): ProcessedFileResult | FileProcessingError {
  if (!geoJSON || typeof geoJSON !== 'object') {
    return {
      message: 'Invalid GeoJSON structure',
      details: 'The file does not contain a valid GeoJSON object.',
    };
  }

  const geojsonObj = geoJSON as Record<string, unknown>;

  if (geojsonObj.type === 'FeatureCollection') {
    const features = geojsonObj.features as Array<unknown>;
    if (!Array.isArray(features) || features.length === 0) {
      return {
        message: 'No features found',
        details: 'The GeoJSON file does not contain any features.',
      };
    }

    // Get the first polygon feature
    const polygonFeature = features.find(feature => {
      const feat = feature as Record<string, unknown>;
      const geometry = feat.geometry as Record<string, unknown>;
      return geometry?.type === 'Polygon';
    });

    if (!polygonFeature) {
      return {
        message: 'No polygon features found',
        details:
          'The GeoJSON file does not contain any polygon features. Only polygon geometries are supported.',
      };
    }

    const feat = polygonFeature as Record<string, unknown>;
    const geometry = feat.geometry as Record<string, unknown>;
    const coordinates = geometry.coordinates as number[][][];

    if (!coordinates?.[0]) {
      return {
        message: 'Invalid polygon coordinates',
        details: 'The polygon feature does not contain valid coordinates.',
      };
    }

    const polygonCoords = coordinates[0];
    const polygonBase64 = encodePolygonToBase64(polygonCoords);

    return {
      coordinates: polygonCoords,
      polygonBase64,
      featureCount: features.length,
      fileName,
    };
  } else if (geojsonObj.type === 'Feature') {
    const geometry = geojsonObj.geometry as Record<string, unknown>;

    if (geometry?.type !== 'Polygon') {
      return {
        message: 'Invalid geometry type',
        details: 'Only polygon geometries are supported.',
      };
    }

    const coordinates = geometry.coordinates as number[][][];
    if (!coordinates?.[0]) {
      return {
        message: 'Invalid polygon coordinates',
        details: 'The polygon feature does not contain valid coordinates.',
      };
    }

    const polygonCoords = coordinates[0];
    const polygonBase64 = encodePolygonToBase64(polygonCoords);

    return {
      coordinates: polygonCoords,
      polygonBase64,
      featureCount: 1,
      fileName,
    };
  }

  return {
    message: 'Unsupported GeoJSON type',
    details: 'Only FeatureCollection and Feature types are supported.',
  };
}

function extractPolygonFromKML(
  xmlDoc: Document,
  fileName: string
): ProcessedFileResult | FileProcessingError {
  try {
    // Find all Polygon elements
    const polygons = xmlDoc.getElementsByTagName('Polygon');

    if (polygons.length === 0) {
      return {
        message: 'No polygons found',
        details: 'The KML file does not contain any polygon geometries.',
      };
    }

    // Get the first polygon
    const firstPolygon = polygons[0];
    const outerBoundary =
      firstPolygon.getElementsByTagName('outerBoundaryIs')[0];

    if (!outerBoundary) {
      return {
        message: 'Invalid polygon structure',
        details: 'The polygon does not have a valid outer boundary.',
      };
    }

    const linearRing = outerBoundary.getElementsByTagName('LinearRing')[0];
    if (!linearRing) {
      return {
        message: 'Invalid polygon structure',
        details: 'The polygon outer boundary does not contain a LinearRing.',
      };
    }

    const coordinates = linearRing.getElementsByTagName('coordinates')[0];
    if (!coordinates) {
      return {
        message: 'No coordinates found',
        details: 'The polygon does not contain coordinate data.',
      };
    }

    const coordText = coordinates.textContent?.trim();
    if (!coordText) {
      return {
        message: 'Empty coordinates',
        details: 'The coordinate data is empty.',
      };
    }

    // Parse KML coordinates (lon,lat,alt format, space-separated)
    const coordPairs = coordText.split(/\s+/).filter(coord => coord.trim());
    const polygonCoords: number[][] = [];

    for (const pair of coordPairs) {
      const parts = pair.split(',');
      if (parts.length >= 2) {
        const lon = parseFloat(parts[0]);
        const lat = parseFloat(parts[1]);

        if (!isNaN(lon) && !isNaN(lat)) {
          // Convert to [lon, lat] format for consistency with GeoJSON
          polygonCoords.push([lon, lat]);
        }
      }
    }

    if (polygonCoords.length < 3) {
      return {
        message: 'Insufficient coordinates',
        details: 'A polygon must have at least 3 coordinate pairs.',
      };
    }

    const polygonBase64 = encodePolygonToBase64(polygonCoords);

    return {
      coordinates: polygonCoords,
      polygonBase64,
      featureCount: polygons.length,
      fileName,
    };
  } catch (error) {
    return {
      message: 'Error parsing KML coordinates',
      details:
        error instanceof Error ? error.message : 'Unknown error occurred',
    };
  }
}
