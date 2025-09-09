import type { LoaderFunctionArgs, ActionFunctionArgs } from 'react-router';
import {
  useLoaderData,
  useActionData,
  useFetcher,
  useNavigation,
} from 'react-router';
import { useTranslation } from 'react-i18next';
import { useReducer, useCallback, useEffect } from 'react';
import { requireUser } from '../../utils/auth/utils';
import { checkDirectorPermissions } from '@root/app/utils/auth/director';
import { getAccessToken } from '@root/app/utils/auth/auth.server';
import {
  getZoningImpactLevels,
  createZoningImpactLevel,
  updateZoningImpactLevel,
  deleteZoningImpactLevel,
  type ZoningImpactLevel,
  type Polygon,
} from '@root/app/utils/api/zoning_impact_levels';
import { getMapLayers } from '@root/app/utils/api/map_layers';
import { fetchGeoServer } from '@root/app/utils/map/map';
import { createZoningLevelLayers } from '@root/app/utils/map/zoning-levels';
import { OpenLayerMap } from '@root/app/components/OpenLayerMap/OpenLayerMap';
import { ImpactMapFormSchema } from '@root/app/schemas/impact-map-form';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '../../components/Dialog/Dialog';
import { Button } from '../../components/Button/Button';
import { RadioGroup } from '../../components/RadioGroup/RadioGroup';
import {
  Map,
  Plus,
  Trash2,
  Info,
  RefreshCw,
  Layers,
  Save,
  X,
} from 'lucide-react';
import clsx from 'clsx';

export const handle = {
  title: 'director:navigation.impactMap',
  breadcrumb: 'director:navigation.impactMap',
};

export async function loader({ request }: LoaderFunctionArgs) {
  const auth = await requireUser(request);
  const accessToken = await getAccessToken(request);

  const userForPermissions = {
    id: auth.user?.id || 0,
    email: auth.user?.email || '',
    name: auth.user?.name || '',
    role_name: auth.user?.role_name,
    role_id: auth.user?.role_id,
  };

  if (!checkDirectorPermissions(userForPermissions)) {
    throw new Response('Acceso no autorizado', { status: 403 });
  }

  if (!accessToken) {
    throw new Response('Token de acceso requerido', { status: 401 });
  }

  // Get municipality ID from user
  const municipalityId = auth.user?.municipality_id;
  if (!municipalityId) {
    throw new Response('ID de municipio requerido', { status: 400 });
  }

  try {
    const [zoningLevels, mapLayers, states] = await Promise.all([
      getZoningImpactLevels(municipalityId, accessToken),
      getMapLayers({ municipality: municipalityId }),
      fetchGeoServer({
        geoServerURL: process.env.GEOSERVER_URL,
        service: 'WFS',
        request: 'GetFeature',
        version: '2.0.0',
        typename: `${process.env.MAP_ESTADO_LAYER}`,
        count: 1,
        outputFormat: 'application/json',
        cql_filter: `${process.env.MAP_ESTADO_CQL_FILTER}`,
      }),
    ]);

    return {
      auth,
      zoningLevels,
      mapLayers,
      states,
      municipalityId,
      ENV: {
        GEOSERVER_URL: process.env.GEOSERVER_URL,
        MAP_CENTER_LAT: process.env.MAP_CENTER_LAT,
        MAP_CENTER_LON: process.env.MAP_CENTER_LON,
        MAP_MUNICIPIO_LAYER: process.env.MAP_MUNICIPIO_LAYER,
        MAP_TILE_CENTER_X: process.env.MAP_TILE_CENTER_X,
        MAP_TILE_CENTER_Y: process.env.MAP_TILE_CENTER_Y,
        MAP_ESTADO_LAYER: process.env.MAP_ESTADO_LAYER,
        MAP_ESTADO_CQL_FILTER: process.env.MAP_ESTADO_CQL_FILTER,
      },
    };
  } catch (error) {
    console.error('Error loading impact map data:', error);
    throw new Response('Error al cargar datos del mapa de impacto', {
      status: 500,
    });
  }
}

export async function action({ request }: ActionFunctionArgs) {
  const auth = await requireUser(request);
  const accessToken = await getAccessToken(request);

  if (!accessToken) {
    throw new Response('Token de acceso requerido', { status: 401 });
  }

  const formData = await request.formData();
  const formDataObject = Object.fromEntries(formData.entries());

  try {
    const validatedData = ImpactMapFormSchema.parse(formDataObject);

    switch (validatedData._intent) {
      case 'create': {
        const result = await createZoningImpactLevel(
          {
            impact_level: validatedData.impact_level,
            municipality_id: validatedData.municipality_id,
            geom: validatedData.geom,
          },
          accessToken
        );

        return { success: true, data: result };
      }

      case 'update': {
        const updateData: { impact_level?: number; geom?: Polygon } = {};

        if (validatedData.impact_level !== undefined) {
          updateData.impact_level = validatedData.impact_level;
        }

        if (validatedData.geom !== undefined) {
          updateData.geom = validatedData.geom;
        }

        const result = await updateZoningImpactLevel(
          validatedData.id,
          updateData,
          accessToken
        );
        return { success: true, data: result };
      }

      case 'delete': {
        await deleteZoningImpactLevel(validatedData.id, accessToken);
        return { success: true };
      }

      default:
        throw new Response('Acción no válida', { status: 400 });
    }
  } catch (error) {
    console.error('Error in impact map action:', error);

    if (error instanceof Error && 'issues' in error) {
      return {
        success: false,
        error: 'Datos inválidos',
        validationErrors: error.issues,
      };
    }

    return { success: false, error: 'Error en la operación' };
  }
}

type Tool = 'select' | 'draw' | 'info' | null;

type State = {
  activeTool: Tool;
  showToolsPanel: boolean;
  showLevelDialog: boolean;
  showConfirmDialog: boolean;
  showImpactInfoDialog: boolean;
  selectedLevel: ZoningImpactLevel | null;
  pendingGeometry: Polygon | null;
  selectedImpactLevel: number;
  isLoading: boolean;
  error: string | null;
};

type Action =
  | { type: 'SET_TOOL'; payload: Tool }
  | { type: 'TOGGLE_TOOLS_PANEL' }
  | { type: 'SHOW_LEVEL_DIALOG'; payload: { geometry?: Polygon } }
  | { type: 'HIDE_LEVEL_DIALOG' }
  | { type: 'SHOW_CONFIRM_DIALOG'; payload: ZoningImpactLevel }
  | { type: 'HIDE_CONFIRM_DIALOG' }
  | { type: 'SHOW_IMPACT_INFO_DIALOG'; payload: ZoningImpactLevel }
  | { type: 'HIDE_IMPACT_INFO_DIALOG' }
  | { type: 'SELECT_LEVEL'; payload: ZoningImpactLevel | null }
  | { type: 'SET_IMPACT_LEVEL'; payload: number }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'SET_TOOL':
      return { ...state, activeTool: action.payload };
    case 'TOGGLE_TOOLS_PANEL':
      return { ...state, showToolsPanel: !state.showToolsPanel };
    case 'SHOW_LEVEL_DIALOG':
      return {
        ...state,
        showLevelDialog: true,
        pendingGeometry: action.payload.geometry || null,
      };
    case 'HIDE_LEVEL_DIALOG':
      return {
        ...state,
        showLevelDialog: false,
        pendingGeometry: null,
        selectedImpactLevel: 1,
      };
    case 'SHOW_CONFIRM_DIALOG':
      return {
        ...state,
        showConfirmDialog: true,
        selectedLevel: action.payload,
      };
    case 'HIDE_CONFIRM_DIALOG':
      return { ...state, showConfirmDialog: false, selectedLevel: null };
    case 'SHOW_IMPACT_INFO_DIALOG':
      return {
        ...state,
        showImpactInfoDialog: true,
        selectedLevel: action.payload,
      };
    case 'HIDE_IMPACT_INFO_DIALOG':
      return { ...state, showImpactInfoDialog: false, selectedLevel: null };
    case 'SELECT_LEVEL':
      return { ...state, selectedLevel: action.payload };
    case 'SET_IMPACT_LEVEL':
      return { ...state, selectedImpactLevel: action.payload };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
}

const impactLevelColors = {
  1: '#4ade80', // green-400 - Mínimo
  2: '#facc15', // yellow-400 - Bajo
  3: '#fb923c', // orange-400 - Medio
  4: '#f87171', // red-400 - Alto
  5: '#dc2626', // red-600 - Máximo
};

const impactLevelLabels = {
  1: 'Mínimo',
  2: 'Bajo',
  3: 'Medio',
  4: 'Alto',
  5: 'Máximo',
};

export default function ImpactMapRoute() {
  const { t: tDirector } = useTranslation('director');
  const { t: tCommon } = useTranslation('common');
  const { zoningLevels, mapLayers, states, municipalityId, ENV } =
    useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();
  const navigation = useNavigation();
  const fetcher = useFetcher<typeof action>();

  const [state, dispatch] = useReducer(reducer, {
    activeTool: null,
    showToolsPanel: false,
    showLevelDialog: false,
    showConfirmDialog: false,
    showImpactInfoDialog: false,
    selectedLevel: null,
    pendingGeometry: null,
    selectedImpactLevel: 1,
    isLoading: false,
    error: null,
  });

  const handleMapClick = useCallback(
    (data: {
      coordinate: number[];
      tool?: string;
      feature?: {
        properties: Record<string, unknown>;
        layerType?: string;
        layerId?: string;
      };
    }) => {
      if (data.tool === 'info' && data.feature) {
        // Check if this is a zoning impact level feature
        if (data.feature.layerType === 'zoning-impact-level') {
          const impactLevel = data.feature.properties.impact_level as number;
          const levelId = data.feature.properties.id as number;
          const municipalityId = data.feature.properties
            .municipality_id as number;

          // Find the full zoning level data
          const zoningLevel = zoningLevels.find(level => level.id === levelId);

          if (zoningLevel) {
            dispatch({
              type: 'SHOW_IMPACT_INFO_DIALOG',
              payload: zoningLevel,
            });
          }
        }
      }
    },
    [zoningLevels]
  );

  const handleDrawEnd = useCallback(
    (geometry?: Polygon) => {
      if (state.activeTool === 'draw' && geometry) {
        dispatch({
          type: 'SHOW_LEVEL_DIALOG',
          payload: { geometry },
        });
        dispatch({ type: 'SET_TOOL', payload: null });
      }
    },
    [state.activeTool]
  );

  const handleSaveLevel = useCallback(() => {
    if (!state.pendingGeometry) return;

    const formData = new FormData();
    formData.append('_intent', 'create');
    formData.append('impact_level', state.selectedImpactLevel.toString());
    formData.append('municipality_id', municipalityId.toString());
    formData.append('geom', JSON.stringify(state.pendingGeometry));

    fetcher.submit(formData, { method: 'POST' });

    dispatch({ type: 'HIDE_LEVEL_DIALOG' });
  }, [
    state.pendingGeometry,
    state.selectedImpactLevel,
    municipalityId,
    fetcher,
  ]);

  const handleDeleteLevel = useCallback((level: ZoningImpactLevel) => {
    dispatch({ type: 'SHOW_CONFIRM_DIALOG', payload: level });
  }, []);

  const confirmDelete = useCallback(() => {
    if (!state.selectedLevel) return;

    const formData = new FormData();
    formData.append('_intent', 'delete');
    formData.append('id', state.selectedLevel.id.toString());

    fetcher.submit(formData, { method: 'POST' });

    dispatch({ type: 'HIDE_CONFIRM_DIALOG' });
  }, [state.selectedLevel, fetcher]);

  const isSubmitting =
    navigation.state === 'submitting' || fetcher.state === 'submitting';

  // Create custom vector layers from zoning levels
  const zoningLevelLayers = createZoningLevelLayers(zoningLevels);

  // Debug: Log the created layers
  useEffect(() => {
    console.warn('Impact Map - Created zoning level layers:', {
      total: zoningLevelLayers.length,
      layers: zoningLevelLayers.map(layer => ({
        id: layer.get('id'),
        label: layer.get('label'),
        coordinateSystem: layer.get('coordinateSystem'),
        featureCount: layer.getSource()?.getFeatures()?.length ?? 0,
      })),
    });
  }, [zoningLevelLayers]);

  // Handle fetcher errors only
  useEffect(() => {
    if (fetcher.data && !fetcher.data.success) {
      dispatch({
        type: 'SET_ERROR',
        payload: fetcher.data.error ?? 'Error en la operación',
      });
    }
  }, [fetcher.data]);

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Map className="h-6 w-6 text-blue-600" />
            <div>
              <h1 className="text-xl font-semibold text-gray-900">
                {tDirector('impactMap.title')}
              </h1>
              <p className="text-sm text-gray-600">
                {tDirector('impactMap.subtitle')}
              </p>
            </div>
          </div>

          <Button
            onClick={() => dispatch({ type: 'TOGGLE_TOOLS_PANEL' })}
            variant="outline"
            className="flex items-center space-x-2"
          >
            <Layers className="h-4 w-4" />
            <span>{tDirector('impactMap.tools')}</span>
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 relative">
        {/* Map */}
        <OpenLayerMap
          center={{
            lat: parseFloat(ENV.MAP_CENTER_LAT ?? '0'),
            lon: parseFloat(ENV.MAP_CENTER_LON ?? '0'),
          }}
          geoServerURL={ENV.GEOSERVER_URL}
          municipioLayer={ENV.MAP_MUNICIPIO_LAYER}
          states={states}
          layers={mapLayers}
          customVectorLayers={zoningLevelLayers}
          tool={state.activeTool ?? undefined}
          onMapClick={handleMapClick}
          onDrawEnd={handleDrawEnd}
        />

        {/* Tools Panel */}
        <div
          className={clsx(
            'absolute right-0 top-0 h-full w-80 bg-white shadow-lg transform duration-300 z-10 transition',
            {
              'translate-x-full opacity-0 pointer-events-none':
                !state.showToolsPanel,
              'translate-x-0 opacity-100': state.showToolsPanel,
            }
          )}
        >
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">
                {tDirector('impactMap.toolsPanel.title')}
              </h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => dispatch({ type: 'TOGGLE_TOOLS_PANEL' })}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>

          <div className="p-4 space-y-4">
            {/* Drawing Tools */}
            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-2">
                {tDirector('impactMap.toolsPanel.drawingTools')}
              </h4>
              <div className="grid grid-cols-2 gap-2">
                <Button
                  variant={state.activeTool === 'draw' ? 'primary' : 'outline'}
                  size="sm"
                  onClick={() =>
                    dispatch({ type: 'SET_TOOL', payload: 'draw' })
                  }
                  className="flex items-center space-x-2"
                >
                  <Plus className="h-4 w-4" />
                  <span>{tDirector('impactMap.actions.add')}</span>
                </Button>

                <Button
                  variant={state.activeTool === 'info' ? 'primary' : 'outline'}
                  size="sm"
                  onClick={() =>
                    dispatch({ type: 'SET_TOOL', payload: 'info' })
                  }
                  className="flex items-center space-x-2"
                >
                  <Info className="h-4 w-4" />
                  <span>{tDirector('impactMap.actions.info')}</span>
                </Button>
              </div>
            </div>

            {/* Impact Levels List */}
            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-2">
                {tDirector('impactMap.toolsPanel.impactLevels')}
              </h4>

              {/* Legend */}
              <div className="mb-3 p-3 bg-gray-50 rounded-lg">
                <h5 className="text-xs font-medium text-gray-700 mb-2">
                  {tDirector('impactMap.toolsPanel.legend')}
                </h5>
                <div className="space-y-1">
                  {Object.entries(impactLevelLabels).map(([level, label]) => (
                    <div key={level} className="flex items-center space-x-2">
                      <div
                        className="w-3 h-3 rounded border border-gray-300"
                        style={{
                          backgroundColor:
                            impactLevelColors[
                              Number(level) as keyof typeof impactLevelColors
                            ],
                        }}
                      />
                      <span className="text-xs text-gray-600">
                        {label} (Nivel {level})
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-2 max-h-60 overflow-y-auto">
                {zoningLevels.map(level => {
                  // Find the corresponding layer to get coordinate system info
                  const correspondingLayer = zoningLevelLayers.find(
                    layer => layer.get('dbId') === level.id
                  );
                  const coordinateSystem =
                    correspondingLayer?.get('coordinateSystem') ?? 'unknown';

                  return (
                    <div
                      key={level.id}
                      className="flex items-center p-2 border border-gray-200 rounded-lg"
                    >
                      <div className="flex items-center space-x-3">
                        <div
                          className="w-4 h-4 rounded"
                          style={{
                            backgroundColor:
                              impactLevelColors[
                                level.impact_level as keyof typeof impactLevelColors
                              ],
                          }}
                        />
                        <div className="flex flex-col">
                          <span className="text-sm font-medium">
                            {
                              impactLevelLabels[
                                level.impact_level as keyof typeof impactLevelLabels
                              ]
                            }
                          </span>
                          <span className="text-xs text-gray-500">
                            ID: {level.id} | Coords: {coordinateSystem}
                          </span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {state.error && (
        <div className="fixed top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded z-50">
          <div className="flex items-center justify-between">
            <span>{state.error}</span>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => dispatch({ type: 'SET_ERROR', payload: null })}
              className="ml-2 text-red-700 hover:text-red-800"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}

      {/* Impact Level Selection Dialog */}
      <Dialog
        open={state.showLevelDialog}
        onOpenChange={() => dispatch({ type: 'HIDE_LEVEL_DIALOG' })}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {tDirector('impactMap.dialogs.selectLevel.title')}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <p className="text-sm text-gray-600">
              {tDirector('impactMap.dialogs.selectLevel.description')}
            </p>

            <div className="space-y-3">
              <RadioGroup
                label={tDirector('impactMap.dialogs.selectLevel.impactLevel')}
                name="impact_level"
                value={state.selectedImpactLevel.toString()}
                onChange={value =>
                  dispatch({ type: 'SET_IMPACT_LEVEL', payload: Number(value) })
                }
                options={Object.entries(impactLevelLabels).map(
                  ([value, label]) => ({
                    value,
                    label,
                    description: (
                      <div className="flex items-center space-x-2">
                        <div
                          className="w-3 h-3 rounded-sm"
                          style={{
                            backgroundColor:
                              impactLevelColors[
                                Number(value) as keyof typeof impactLevelColors
                              ],
                          }}
                        />
                      </div>
                    ),
                  })
                )}
              />
            </div>

            <div className="flex justify-end space-x-2">
              <Button
                variant="outline"
                onClick={() => dispatch({ type: 'HIDE_LEVEL_DIALOG' })}
              >
                {tCommon('cancel')}
              </Button>
              <Button
                onClick={handleSaveLevel}
                disabled={isSubmitting || !state.pendingGeometry}
                className="flex items-center space-x-2"
              >
                <Save className="h-4 w-4" />
                <span>{tCommon('save')}</span>
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={state.showConfirmDialog}
        onOpenChange={() => dispatch({ type: 'HIDE_CONFIRM_DIALOG' })}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {tDirector('impactMap.dialogs.confirmDelete.title')}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <p className="text-sm text-gray-600">
              {tDirector('impactMap.dialogs.confirmDelete.description')}
            </p>
            {state.selectedLevel && (
              <div className="flex items-center space-x-2 p-2 bg-gray-50 rounded">
                <div
                  className="w-4 h-4 rounded"
                  style={{
                    backgroundColor:
                      impactLevelColors[
                        state.selectedLevel
                          .impact_level as keyof typeof impactLevelColors
                      ],
                  }}
                />
                <span className="text-sm font-medium">
                  {
                    impactLevelLabels[
                      state.selectedLevel
                        .impact_level as keyof typeof impactLevelLabels
                    ]
                  }
                </span>
              </div>
            )}

            <div className="flex justify-end space-x-2">
              <Button
                variant="outline"
                onClick={() => dispatch({ type: 'HIDE_CONFIRM_DIALOG' })}
              >
                {tCommon('cancel')}
              </Button>
              <Button
                variant="destructive"
                onClick={confirmDelete}
                disabled={isSubmitting}
                className="flex items-center space-x-2"
              >
                <Trash2 className="h-4 w-4" />
                <span>{tCommon('delete')}</span>
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Impact Info Dialog */}
      <Dialog
        open={state.showImpactInfoDialog}
        onOpenChange={() => dispatch({ type: 'HIDE_IMPACT_INFO_DIALOG' })}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {tDirector('impactMap.dialogs.impactInfo.title')}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            {state.selectedLevel ? (
              <>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">
                      {tDirector('impactMap.dialogs.impactInfo.fields.id')}
                    </label>
                    <p className="text-sm text-gray-900">
                      {state.selectedLevel.id}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">
                      {tDirector(
                        'impactMap.dialogs.impactInfo.fields.municipalityId'
                      )}
                    </label>
                    <p className="text-sm text-gray-900">
                      {state.selectedLevel.municipality_id}
                    </p>
                  </div>
                </div>

                <div>
                  <label className="text-sm font-medium text-gray-700">
                    {tDirector(
                      'impactMap.dialogs.impactInfo.fields.impactLevel'
                    )}
                  </label>
                  <div className="flex items-center space-x-2 mt-1">
                    <div
                      className="w-4 h-4 rounded"
                      style={{
                        backgroundColor:
                          impactLevelColors[
                            state.selectedLevel
                              .impact_level as keyof typeof impactLevelColors
                          ],
                      }}
                    />
                    <span className="text-sm font-medium">
                      {
                        impactLevelLabels[
                          state.selectedLevel
                            .impact_level as keyof typeof impactLevelLabels
                        ]
                      }
                    </span>
                    <span className="text-sm text-gray-500">
                      (Nivel {state.selectedLevel.impact_level})
                    </span>
                  </div>
                </div>

                {state.selectedLevel.geom && (
                  <div>
                    <label className="text-sm font-medium text-gray-700">
                      {tDirector(
                        'impactMap.dialogs.impactInfo.fields.geometry'
                      )}
                    </label>
                    <p className="text-xs text-gray-600 mt-1">
                      {tDirector(
                        'impactMap.dialogs.impactInfo.fields.geometryType'
                      )}
                      : {state.selectedLevel.geom.type}
                    </p>
                    <p className="text-xs text-gray-600">
                      {tDirector(
                        'impactMap.dialogs.impactInfo.fields.coordinates'
                      )}
                      : {state.selectedLevel.geom.coordinates.length}{' '}
                      {tDirector('impactMap.dialogs.impactInfo.fields.rings')}
                    </p>
                  </div>
                )}

                <div className="flex justify-between items-center pt-4 border-t">
                  <Button
                    variant="outline"
                    onClick={() => handleDeleteLevel(state.selectedLevel!)}
                    className="flex items-center space-x-2 text-red-600 hover:text-red-700"
                  >
                    <Trash2 className="h-4 w-4" />
                    <span>{tCommon('delete')}</span>
                  </Button>
                  <Button
                    onClick={() =>
                      dispatch({ type: 'HIDE_IMPACT_INFO_DIALOG' })
                    }
                  >
                    {tCommon('close')}
                  </Button>
                </div>
              </>
            ) : (
              <p className="text-sm text-gray-600">
                {tDirector('impactMap.dialogs.impactInfo.noData')}
              </p>
            )}
          </div>
        </DialogContent>
      </Dialog>

      {/* Loading Dialog */}
      <Dialog open={isSubmitting} onOpenChange={() => {}}>
        <DialogContent className="sm:max-w-md">
          <div className="flex items-center justify-center p-6">
            <div className="flex items-center space-x-3">
              <RefreshCw className="h-5 w-5 animate-spin text-blue-600" />
              <span className="text-sm font-medium">{tCommon('loading')}</span>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
