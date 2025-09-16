import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile.js';
import OSM from 'ol/source/OSM.js';
import Draw from 'ol/interaction/Draw.js';
import { use, useEffect, useRef, type PropsWithChildren } from 'react';
import 'ol/ol.css';
import './map.css';
import { ChevronRight } from 'lucide-react';
import clsx from 'clsx';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import Feature from 'ol/Feature';
import { useSearchParams } from 'react-router';
import Style from 'ol/style/Style';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import CircleStyle from 'ol/style/Circle.js';
import { Geometry, LineString, Polygon, Point } from 'ol/geom';
import Overlay from 'ol/Overlay';
import type { Coordinate } from 'ol/coordinate';
import { unByKey } from 'ol/Observable';
import type { EventsKey } from 'ol/events';
import { useTranslation } from 'react-i18next';
import { encodePolygonToBase64, fetchGeoServer } from '@root/app/utils/map/map';
import TileWMS from 'ol/source/TileWMS.js';
import type { ServerType } from 'ol/source/wms';
import type { loader } from '@root/app/routes/map';
import { formatArea, formatLength } from './utils';
import proj4 from 'proj4';
import { register } from 'ol/proj/proj4';
import { transform, fromLonLat, toLonLat } from 'ol/proj';

// Define EPSG:32613 (WGS 84 / UTM zone 13N) projection
proj4.defs('EPSG:32613', '+proj=utm +zone=13 +datum=WGS84 +units=m +no_defs');
register(proj4);

function moveHandler({
  map,
  geoServerURL,
  municipioLayer,
  onFeatureLoad,
}: {
  map: Map | null;
  geoServerURL?: string;
  municipioLayer?: string;
  onFeatureLoad?: ({ name }: { name: string }) => void;
}) {
  if (!geoServerURL || !municipioLayer) {
    return;
  }

  const center = map?.getView().getCenter();

  if (center) {
    fetchGeoServer({
      geoServerURL,
      service: 'WFS',
      request: 'GetFeature',
      version: '2.0.0',
      typename: `${municipioLayer}`,
      count: 1,
      outputFormat: 'application/json',
      cql_filter: `CONTAINS(geom, POINT (${encodeURIComponent(center[0])} ${encodeURIComponent(center[1])}))`,
    })
      .then((data: any) => {
        if (
          onFeatureLoad &&
          Array.isArray(data.features) &&
          data.features.length > 0 &&
          data.features[0].properties.nom_mun
        ) {
          onFeatureLoad({ name: data.features[0].properties.nom_mun });
        }

        const layers = getLayerFromFeatures(data.features);

        const mapCurrentLayers = map?.getLayers().getArray();

        layers.forEach(layer => {
          const layerId = layer.get('id');

          const existingLayer = mapCurrentLayers?.find(
            (layer: any) => layer.get('id') === layerId
          );

          if (!existingLayer) {
            map?.addLayer(layer);
          }
        });
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
}

function getLayerFromFeatures(features: Array<unknown>) {
  const layers = features
    .filter(feature => {
      if (!feature || typeof feature !== 'object') return false;
      const f = feature as Record<string, unknown>;
      return f.geometry && typeof f.geometry === 'object';
    })
    .map(feature => {
      try {
        const geoJSONFeatures = new GeoJSON().readFeatures(feature);

        const vectorSource = new VectorSource({
          features: geoJSONFeatures.map(
            geoFeature =>
              new Feature({
                geometry: geoFeature.getGeometry(),
              })
          ),
        });

        const vectorLayer = new VectorLayer({
          source: vectorSource,
          style: new Style({
            fill: new Fill({
              color: 'rgba(0, 0, 0, 0)',
            }),
            stroke: new Stroke({
              color: 'rgba(0, 0, 0, 0.5)',
              width: 1,
            }),
          }),
        });

        const featureWithId = feature as Partial<{ id: string }>;

        if (featureWithId.id) {
          vectorLayer.set('id', featureWithId.id);
        }

        return vectorLayer;
      } catch (error) {
        console.warn('Failed to create layer from feature:', error);
        return null;
      }
    })
    .filter(layer => layer !== null);

  return layers;
}

export function OpenLayerMap({
  center,
  children,
  geoServerURL,
  layers: layersFromProps = [],
  customVectorLayers = [],
  municipioLayer,
  onMapClick,
  onDrawEnd,
  property,
  searchResult,
  states,
  tool,
}: PropsWithChildren<{
  geoServerURL?: string;
  layers?: Awaited<ReturnType<typeof loader>>['layers'];
  customVectorLayers?: VectorLayer<VectorSource>[];
  property?: Awaited<ReturnType<typeof loader>>['property'];
  searchResult?: Awaited<ReturnType<typeof loader>>['searchResult'];
  center?: {
    lat: number;
    lon: number;
  };
  municipioLayer?: string;
  states?: {
    features?: Array<unknown>;
  };
  tool?:
    | 'select'
    | 'draw'
    | 'measure-lineal'
    | 'measure-area'
    | 'clear'
    | 'info';
  onMapClick?: (data: {
    coordinate: Coordinate;
    tool?: string;
    feature?: {
      properties: Record<string, unknown>;
      layerType?: string;
      layerId?: string;
    };
  }) => void;
  onDrawEnd?: (geometry?: {
    type: 'Polygon';
    coordinates: number[][][];
  }) => void;
}>) {
  const { t: tMap } = useTranslation('map');

  const shouldFetch = useRef(false);
  const toolRef = useRef(tool);

  const mapContainer = useRef<HTMLDivElement>(null);
  const mounted = useRef(false);
  const map = useRef<Map>(null);
  const drawSourceRef = useRef<VectorSource>(new VectorSource());
  const measureSourceRef = useRef<VectorSource>(new VectorSource());
  const searchSourceRef = useRef<VectorSource>(new VectorSource());
  const tooltipElement = useRef<HTMLDivElement>(null);
  const tooltip = useRef<Overlay>(null);
  const measureTooltip = useRef<Overlay>(null);
  const measureTooltipElement = useRef<HTMLDivElement>(null);
  const sketch = useRef<Feature<Geometry>>(null);
  const tiles = useRef<Array<TileLayer>>([]);
  const customLayers = useRef<Array<VectorLayer<VectorSource>>>([]);
  const tooltipElements = useRef<HTMLDivElement[]>([]);
  const tooltips = useRef<Overlay[]>([]);
  const measureTooltipElements = useRef<HTMLDivElement[]>([]);
  const measureTooltips = useRef<Overlay[]>([]);
  const propertyID = useRef<string | null>(null);
  const searchResultID = useRef<string | null>(null);

  // Update tool ref when tool prop changes
  useEffect(() => {
    toolRef.current = tool;
  }, [tool]);

  const [searchParams, setSearchParams] = useSearchParams();

  useEffect(() => {
    function onMouseOut() {
      tooltipElement.current?.classList.add('hidden');
    }

    if (!mounted.current && mapContainer.current) {
      const layers = getLayerFromFeatures(states?.features ?? []);

      const view = new View({
        center: center
          ? transform([center.lon, center.lat], 'EPSG:4326', 'EPSG:32613')
          : [0, 0],
        zoom: 7,
        projection: 'EPSG:32613',
      });

      const drawVectorLayer = new VectorLayer({
        source: drawSourceRef.current,
        style: {
          'fill-color': 'rgba(106, 191, 75, 0.4)',
          'stroke-color': '#6abf4b',
          'stroke-width': 2,
          'circle-radius': 7,
          'circle-fill-color': '#6abf4b',
        },
      });

      const measureVectorLayer = new VectorLayer({
        source: measureSourceRef.current,
        style: {
          'fill-color': 'rgba(106, 191, 75, 0.4)',
          'stroke-color': '#6abf4b',
          'stroke-width': 2,
          'circle-radius': 7,
          'circle-fill-color': '#6abf4b',
        },
      });

      const searchVectorLayer = new VectorLayer({
        source: searchSourceRef.current,
        style: {
          'fill-color': 'rgba(34, 197, 94, 0.8)',
          'stroke-color': '#22c55e',
          'stroke-width': 3,
          'circle-radius': 10,
          'circle-fill-color': '#22c55e',
          'circle-stroke-color': '#ffffff',
          'circle-stroke-width': 2,
        },
      });

      tiles.current = layersFromProps
        .map(layer => {
          const tile = new TileLayer({
            properties: {
              id: layer.id,
            },
            source: new TileWMS({
              attributions: layer.attribution ?? undefined,
              url: layer.url,
              params: {
                LAYERS: layer.layers,
                TILED: true,
                FORMAT: layer.format,
                SRS: layer.projection,
                CRS: layer.projection,
                VERSION: layer.version,
                CQL_FILTER: layer.cql_filter,
              },
              serverType: (layer.server_type as ServerType) ?? undefined,
            }),
            visible: layer.visible !== false,
          });

          return tile;
        })
        .filter(layer => layer !== null);

      map.current = new Map({
        target: mapContainer.current,
        layers: [
          new TileLayer({
            source: new OSM(),
          }),
          ...layers,
          ...tiles.current,
          drawVectorLayer,
          measureVectorLayer,
          searchVectorLayer,
        ],
        view,
      });

      const geoJSONFeatures = (states?.features ?? [])
        .filter(feature => {
          if (!feature || typeof feature !== 'object') return false;
          const f = feature as Record<string, unknown>;
          return f.geometry && typeof f.geometry === 'object';
        })
        .map(feature => {
          try {
            return new GeoJSON().readFeatures(feature);
          } catch (error) {
            console.warn('Failed to read GeoJSON feature:', error);
            return [];
          }
        })
        .flat();
/*

      const geometry = geoJSONFeatures[0]?.getGeometry();

      if (geometry) {
        view.fit(geometry.getExtent(), {
          padding: [100, 100, 100, 100],
        });
      }
*/
      map.current.on('pointerdrag', () => {
        shouldFetch.current = true;
      });

      function handleFeatureLoad({ name }: { name: string }) {
        setSearchParams(searchParams => {
          searchParams.set('search', name);
          return searchParams;
        });
      }

      map.current.on('moveend', () => {
        if (shouldFetch.current) {
          moveHandler({
            map: map.current,
            geoServerURL,
            municipioLayer,
            onFeatureLoad: handleFeatureLoad,
          });
        }

        shouldFetch.current = false;
      });

      map.current.on('click', event => {
        if (!map.current) return;

        // Get features at clicked pixel
        const featuresAtPixel = map.current.getFeaturesAtPixel(event.pixel);

        let clickData: {
          coordinate: Coordinate;
          tool?: string;
          feature?: {
            properties: Record<string, unknown>;
            layerType?: string;
            layerId?: string;
          };
        } = {
          coordinate: event.coordinate,
          tool: toolRef.current ?? undefined,
        };

        // Check if we clicked on a feature
        if (featuresAtPixel.length > 0) {
          const feature = featuresAtPixel[0];
          const properties = feature.getProperties();

          // Get the layer information by checking which layer contains this feature
          const layers = map.current.getLayers().getArray();
          let layerInfo = null;

          for (const layer of layers) {
            if (layer instanceof VectorLayer) {
              const source = layer.getSource();
              if (source) {
                const features = source.getFeatures();
                if (features.includes(feature)) {
                  layerInfo = {
                    layerType: layer.get('type') ?? 'vector',
                    layerId: layer.get('id') ?? layer.get('label') ?? 'unknown',
                  };
                  break;
                }
              }
            }
          }

          clickData.feature = {
            properties,
            ...layerInfo,
          };
        }

        onMapClick?.(clickData);
      });

      map.current.getViewport().addEventListener('mouseout', onMouseOut);
    }

    return () => {
      if (map.current) {
        map.current.getViewport().removeEventListener('mouseout', onMouseOut);

        // Clean up custom layers
        customLayers.current.forEach(layer => {
          map.current?.removeLayer(layer);
        });
        customLayers.current = [];

        map.current.setTarget();
        map.current = null;
        mounted.current = false;
      }
    };
  }, []);

  useEffect(() => {
    function createMeasureTooltip() {
      if (measureTooltipElement.current) {
        measureTooltipElement.current.remove();
      }

      measureTooltipElement.current = document.createElement('div');

      measureTooltipElement.current.className =
        'ol-tooltip bg-primary/40 text-xs p-2 rounded mt-8';

      measureTooltip.current = new Overlay({
        element: measureTooltipElement.current,
        offset: [0, -10],
        positioning: 'bottom-center',
        stopEvent: false,
        insertFirst: false,
      });

      map.current?.addOverlay(measureTooltip.current);

      measureTooltipElements.current.push(measureTooltipElement.current);
      measureTooltips.current.push(measureTooltip.current);
    }

    if (tool === 'clear' && map.current) {
      drawSourceRef.current.clear();
      measureSourceRef.current.clear();
      searchSourceRef.current.clear();

      tooltips.current.forEach(overlay => {
        map.current?.removeOverlay(overlay);
      });

      tooltipElements.current.forEach(el => {
        el.remove();
      });

      measureTooltips.current.forEach(overlay => {
        map.current?.removeOverlay(overlay);
      });

      measureTooltipElements.current.forEach(el => {
        el.remove();
      });

      tooltips.current = [];
      tooltipElements.current = [];
      measureTooltips.current = [];
      measureTooltipElements.current = [];

      searchResultID.current = null;

      return;
    }

    const style = new Style({
      fill: new Fill({
        color: 'rgba(106, 191, 75, 0.4)',
      }),
      stroke: new Stroke({
        color: tool === 'draw' ? undefined : 'rgba(0,0,0,0.7)',
        lineDash: tool === 'draw' ? undefined : [10, 10],
        width: 2,
      }),
      image: new CircleStyle({
        radius: 7,
        stroke: new Stroke({
          color: tool === 'draw' ? undefined : 'rgba(0, 0, 0, 0.7)',
        }),
        fill: new Fill({
          color: '#6abf4b',
        }),
      }),
    });

    const draw = new Draw({
      source:
        tool === 'draw' ? drawSourceRef.current : measureSourceRef.current,
      type:
        tool && ['measure-area', 'draw'].includes(tool)
          ? 'Polygon'
          : 'LineString',
      style,
    });

    let listener: EventsKey | undefined;

    if (tooltipElement.current) {
      tooltipElement.current.remove();
    }

    tooltipElement.current = document.createElement('div');
    tooltipElement.current.className =
      'ol-tooltip bg-primary/40 text-xs p-2 rounded hidden mt-8';

    tooltip.current = new Overlay({
      element: tooltipElement.current,
      offset: [15, 0],
      positioning: 'center-left',
    });

    tooltipElements.current.push(tooltipElement.current);
    tooltips.current.push(tooltip.current);

    createMeasureTooltip();

    draw.on('drawstart', event => {
      sketch.current = event.feature;

      let tooltipCoordinates: Coordinate;

      listener = sketch.current.getGeometry()?.on('change', event => {
        const geom = event.target;

        let output = '';

        if (geom instanceof Polygon && tool !== 'draw') {
          const areaInfo = formatArea(geom);

          if (!areaInfo?.value) {
            return;
          }

          output = `${areaInfo?.value}<sup>${areaInfo?.sup}</sup>`;

          tooltipCoordinates = geom.getInteriorPoint().getCoordinates();
        } else if (geom instanceof LineString) {
          output = formatLength(geom) ?? '';

          tooltipCoordinates = geom.getLastCoordinate();
        }
        if (measureTooltipElement.current) {
          measureTooltipElement.current.innerHTML = output;
          measureTooltip.current?.setPosition(tooltipCoordinates);
        }
      });
    });

    draw.on('drawend', event => {
      sketch.current = null;
      measureTooltipElement.current = null;

      if (tool === 'draw') {
        const feature = event.feature;
        const geometry = feature.getGeometry();

        if (geometry instanceof Polygon) {
          const coordinates = geometry.getCoordinates()[0];

          const wgs84Coordinates = coordinates.map((coord: number[]) => {
            return toLonLat(coord, 'EPSG:32613');
          });

          const polygonGeometry = {
            type: 'Polygon' as const,
            coordinates: [wgs84Coordinates],
          };

          setSearchParams(searchParams => {
            searchParams.set(
              'polygon',
              encodePolygonToBase64(wgs84Coordinates)
            );

            searchParams.delete('point');

            return searchParams;
          });

          drawSourceRef.current.clear();
          onDrawEnd?.(polygonGeometry);
        } else {
          drawSourceRef.current.clear();
          onDrawEnd?.();
        }
      }

      if (listener) {
        unByKey(listener);
      }

      createMeasureTooltip();
    });

    if (map.current) {
      if (tool !== 'select' && tool !== 'info') {
        map.current.addInteraction(draw);
      }

      map.current.addOverlay(tooltip.current);

      const pointerMoveEventKey = map.current.on('pointermove', event => {
        if (event.dragging) {
          return;
        }

        let helpMessage = tMap(`controls.tools.tabs.tools.tooltips.${tool}`);

        if (sketch.current) {
          helpMessage = tMap(
            `controls.tools.tabs.tools.tooltips.${tool}-drawing`
          );
        }

        if (tooltipElement.current) {
          tooltipElement.current.innerHTML = helpMessage;
          tooltip.current?.setPosition(event.coordinate);
          tooltipElement.current.classList.remove('hidden');
        }
      });

      return () => {
        unByKey(pointerMoveEventKey);

        map.current?.removeInteraction(draw);

        tooltip.current && map.current?.removeOverlay(tooltip.current);

        measureTooltip.current &&
          map.current?.removeOverlay(measureTooltip.current);
      };
    }
  }, [tool]);

  const propertyData = property ? use(property) : null;
  const searchResultData = searchResult ? use(searchResult) : null;

  useEffect(() => {
    if (tiles.current) {
      tiles.current.forEach(tile => {
        const id = tile.getProperties().id;

        const newVisibility = layersFromProps.find(layer => layer.id === id);

        tile.setVisible(newVisibility?.visible ?? true);
      });
    }
  }, [layersFromProps]);

  useEffect(() => {
    if (map.current) {
      // Remove existing custom layers from map
      customLayers.current.forEach(layer => {
        map.current?.removeLayer(layer);
      });

      // Clear the reference
      customLayers.current = [];

      // Add new custom layers to map
      console.warn('OpenLayerMap - Adding custom vector layers:', {
        total: customVectorLayers.length,
        layers: customVectorLayers.map(layer => ({
          id: layer.get('id'),
          label: layer.get('label'),
          coordinateSystem: layer.get('coordinateSystem'),
          featureCount: layer.getSource()?.getFeatures()?.length ?? 0,
          extent: layer.getSource()?.getExtent(),
        })),
      });

      customVectorLayers.forEach(layer => {
        map.current?.addLayer(layer);
        customLayers.current.push(layer);
      });

      // Log map extent after adding layers
      if (map.current && customVectorLayers.length > 0) {
        const mapView = map.current.getView();
        console.warn('OpenLayerMap - Current map view:', {
          center: mapView.getCenter(),
          zoom: mapView.getZoom(),
          projection: mapView.getProjection().getCode(),
        });
      }
    }
  }, [customVectorLayers]);

  useEffect(() => {
    if (
      map.current &&
      propertyData &&
      propertyID.current !== String(propertyData.id)
    ) {
      propertyID.current = String(propertyData.id);

      const geoJSON = new GeoJSON().readFeatures(propertyData, {
        featureProjection: 'EPSG:32613',
      });

      drawSourceRef.current.clear();
      drawSourceRef.current.addFeatures(geoJSON);

      const geometry = geoJSON[0]?.getGeometry();

      if (geometry) {
        map.current.getView().fit(geometry.getExtent(), {
          padding: [200, 200, 200, 800],
          duration: 300,
          easing: t => t * (2 - t),
        });
      }
    }
  }, [propertyData]);

  useEffect(() => {
    if (
      map.current &&
      searchResultData &&
      searchResultID.current !== searchResultData.place_id
    ) {
      searchResultID.current = searchResultData.place_id;

      searchSourceRef.current.clear();

      const { lat, lng } = searchResultData.geometry.location;

      const coordinates = transform([lng, lat], 'EPSG:4326', 'EPSG:32613');

      const pointFeature = new Feature({
        geometry: new Point(coordinates),
      });

      searchSourceRef.current.addFeature(pointFeature);

      map.current.getView().fit(pointFeature.getGeometry()!.getExtent(), {
        padding: [50, 50, 50, 50],
        maxZoom: 18,
        duration: 500,
      });
    }
  }, [searchResultData]);

  return (
    <div className="w-full h-full relative overflow-hidden" ref={mapContainer}>
      {children}
    </div>
  );
}

export function OpenLayerMapLayersControls({
  children,
  open,
  onToggle,
}: PropsWithChildren & { open: boolean; onToggle: () => void }) {
  return (
    <div
      className={clsx(
        'absolute right-0 top-1/2 z-10 h-1/2 bg-white -translate-y-1/2 w-72 transition',
        {
          'translate-x-full': !open,
        }
      )}
    >
      <button
        className="bg-primary h-full cursor-pointer absolute left-0 -translate-x-full rounded-l-lg"
        type="button"
        onClick={onToggle}
      >
        <ChevronRight
          className={clsx('text-white', {
            'rotate-180': !open,
          })}
        />
      </button>

      <div className="overflow-hidden h-full">{children}</div>
    </div>
  );
}
