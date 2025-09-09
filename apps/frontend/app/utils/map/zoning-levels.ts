import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import Feature from 'ol/Feature';
import Style from 'ol/style/Style';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import Text from 'ol/style/Text';
import { getCenter } from 'ol/extent';
import { Point } from 'ol/geom';
import type { ZoningImpactLevel } from '@root/app/utils/api/zoning_impact_levels';

const impactLevelColors = {
  1: '#4ade80', // green-400 - Mínimo
  2: '#facc15', // yellow-400 - Bajo
  3: '#fb923c', // orange-400 - Medio
  4: '#f87171', // red-400 - Alto
  5: '#dc2626', // red-600 - Máximo
};

export function createHighlightStyle(impactLevel: number): Style {
  return new Style({
    fill: new Fill({
      color: `${impactLevelColors[impactLevel as keyof typeof impactLevelColors] || '#6b7280'}40`, // 25% opacity
    }),
    stroke: new Stroke({
      color:
        impactLevelColors[impactLevel as keyof typeof impactLevelColors] ||
        '#6b7280',
      width: 3,
    }),
  });
}

export function createZoningLevelLayers(
  zoningLevels: ZoningImpactLevel[]
): VectorLayer<VectorSource>[] {
  const layers: VectorLayer<VectorSource>[] = [];

  // Create a separate layer for each zoning level record
  zoningLevels.forEach(level => {
    if (level.geom) {
      try {
        let geoJSONFeatures: Feature[];
        let coordinateSystemUsed = 'unknown';

        // Parse geometry and detect coordinate system
        try {
          // First, try to read the geometry without any projection assumptions
          const rawFeatures = new GeoJSON().readFeatures(level.geom);

          if (rawFeatures.length > 0) {
            const firstGeometry = rawFeatures[0].getGeometry();
            if (firstGeometry) {
              const extent = firstGeometry.getExtent();
              // Get coordinates by examining the extent instead of getFlatCoordinates
              const [minX, minY, maxX, maxY] = extent;
              const sampleCoords = [minX, minY, maxX, maxY];

              // Detect coordinate system based on coordinate ranges
              const hasLargeCoords = sampleCoords.some(
                (coord: number) => Math.abs(coord) > 1000
              );
              const hasLatLonRange = sampleCoords.every(
                (coord: number) => Math.abs(coord) <= 180
              );

              if (hasLatLonRange && !hasLargeCoords) {
                // Looks like WGS84 (lat/lon), transform to map projection

                geoJSONFeatures = new GeoJSON().readFeatures(level.geom, {
                  featureProjection: 'EPSG:32613',
                  dataProjection: 'EPSG:4326',
                });
                coordinateSystemUsed = 'WGS84->UTM';
              } else if (hasLargeCoords) {
                // Looks like UTM coordinates, use as-is

                geoJSONFeatures = rawFeatures;
                coordinateSystemUsed = 'UTM';
              } else {
                // Fallback: try transformation anyway

                try {
                  geoJSONFeatures = new GeoJSON().readFeatures(level.geom, {
                    featureProjection: 'EPSG:32613',
                    dataProjection: 'EPSG:4326',
                  });
                  coordinateSystemUsed = 'Fallback WGS84->UTM';
                } catch {
                  geoJSONFeatures = rawFeatures;
                  coordinateSystemUsed = 'Raw';
                }
              }
            } else {
              throw new Error('No geometry found in feature');
            }
          } else {
            throw new Error('No features parsed from geometry');
          }
        } catch (parseError) {
          console.error(
            `Failed to parse geometry for level ${level.id}:`,
            parseError
          );
          return; // Skip this level
        }

        const features: Feature[] = [];
        geoJSONFeatures.forEach(feature => {
          feature.setProperties({
            id: level.id,
            impact_level: level.impact_level,
            municipality_id: level.municipality_id,
            coordinate_system: coordinateSystemUsed,
          });
          features.push(feature);
        });

        if (features.length > 0) {
          // Create the main geometry layer
          const mainVectorSource = new VectorSource({
            features,
          });

          const mainVectorLayer = new VectorLayer({
            source: mainVectorSource,
            style: new Style({
              fill: new Fill({
                color: `${impactLevelColors[level.impact_level as keyof typeof impactLevelColors] || '#6b7280'}60`,
              }),
              stroke: new Stroke({
                color:
                  impactLevelColors[
                    level.impact_level as keyof typeof impactLevelColors
                  ] || '#6b7280',
                width: 2,
                lineDash: [10, 5],
              }),
            }),
            properties: {
              id: `zoning-impact-level-${level.id}`,
              label: `Nivel de impacto ${level.impact_level} - ID ${level.id} (${coordinateSystemUsed})`,
              type: 'zoning-impact-level',
              impactLevel: level.impact_level,
              dbId: level.id,
              coordinateSystem: coordinateSystemUsed,
            },
          });

          // Create a label layer with the impact level text
          const extent = mainVectorSource.getExtent();
          const center = getCenter(extent);

          const labelFeature = new Feature({
            geometry: new Point(center),
            impact_level: level.impact_level,
          });

          const labelVectorSource = new VectorSource({
            features: [labelFeature],
          });

          const labelVectorLayer = new VectorLayer({
            source: labelVectorSource,
            style: new Style({
              text: new Text({
                text: String(level.impact_level),
                font: 'bold 24px Arial',
                fill: new Fill({
                  color:
                    impactLevelColors[
                      level.impact_level as keyof typeof impactLevelColors
                    ] || '#6b7280',
                }),
                stroke: new Stroke({
                  color: '#ffffff',
                  width: 2,
                }),
                textAlign: 'center',
                textBaseline: 'middle',
              }),
            }),
            properties: {
              id: `zoning-impact-level-label-${level.id}`,
              label: `Label Nivel ${level.impact_level} - ID ${level.id}`,
              type: 'zoning-impact-level-label',
              impactLevel: level.impact_level,
              dbId: level.id,
            },
          });

          layers.push(mainVectorLayer);
          layers.push(labelVectorLayer);
        }
      } catch (error) {
        console.error(
          `Failed to create layer for zoning level ${level.id}:`,
          error
        );
      }
    }
  });

  return layers;
}
