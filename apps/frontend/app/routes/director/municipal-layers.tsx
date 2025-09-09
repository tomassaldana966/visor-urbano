import type { LoaderFunctionArgs, ActionFunctionArgs } from 'react-router';
import { useLoaderData, useFetcher } from 'react-router';
import { useTranslation } from 'react-i18next';
import { useReducer, useEffect } from 'react';
import type { ReactElement } from 'react';
import { requireAuth } from '../../utils/auth/auth.server';
import { checkDirectorPermissions } from '@root/app/utils/auth/director';
import {
  getMapLayers,
  createMapLayer,
  updateMapLayer,
} from '../../utils/api/map_layers';
import {
  MapLayerCreateSchema,
  MapLayerUpdateSchema,
  MapLayerFormSchema,
  type MapLayer,
} from '@root/app/schemas/map-layers';
import { DataTable } from '../../components/Director/Charts/DataTable';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '../../components/Dialog/Dialog';
import { Input } from '../../components/Input/Input';
import { Button } from '../../components/Button/Button';
import { Select, Option } from '../../components/Select/Select';
import { Checkbox } from '../../components/Checkbox/Checkbox';
import { Slider } from '../../components/Slider/Slider';
import { cn } from '@/utils/cn';
import { Plus, Layers, Eye, Edit, ToggleLeft, ToggleRight } from 'lucide-react';

type ModalMode = 'closed' | 'add' | 'edit';

interface LayerState {
  modalMode: ModalMode;
  selectedLayer: MapLayer | null;
  layerType: string;
  opacity: number[];
}

type LayerAction =
  | { type: 'OPEN_ADD_MODAL' }
  | { type: 'OPEN_EDIT_MODAL'; layer: MapLayer }
  | { type: 'CLOSE_MODAL' }
  | { type: 'SET_LAYER_TYPE'; layerType: string }
  | { type: 'SET_OPACITY'; opacity: number[] }
  | { type: 'RESET_FORM' };

const initialState: LayerState = {
  modalMode: 'closed',
  selectedLayer: null,
  layerType: '',
  opacity: [1],
};

function layerReducer(state: LayerState, action: LayerAction): LayerState {
  switch (action.type) {
    case 'OPEN_ADD_MODAL':
      return {
        ...state,
        modalMode: 'add',
        selectedLayer: null,
        layerType: '',
        opacity: [1],
      };
    case 'OPEN_EDIT_MODAL':
      return {
        ...state,
        modalMode: 'edit',
        selectedLayer: action.layer,
        layerType: action.layer.type ?? '',
        opacity: [action.layer.opacity],
      };
    case 'CLOSE_MODAL':
      return {
        ...state,
        modalMode: 'closed',
        selectedLayer: null,
        layerType: '',
        opacity: [1],
      };
    case 'SET_LAYER_TYPE':
      return {
        ...state,
        layerType: action.layerType,
      };
    case 'SET_OPACITY':
      return {
        ...state,
        opacity: action.opacity,
      };
    case 'RESET_FORM':
      return {
        ...state,
        selectedLayer: null,
        layerType: '',
        opacity: [1],
      };
    default:
      return state;
  }
}

export const handle = {
  title: 'director:navigation.municipalLayers',
  breadcrumb: 'director:navigation.municipalLayers',
};

export async function action({ request }: ActionFunctionArgs) {
  const auth = await requireAuth(request);

  const userForPermissions = {
    id: auth.id ?? 0,
    email: auth.email ?? '',
    name: auth.name ?? '',
    role_name: auth.role_name,
  };

  if (!checkDirectorPermissions(userForPermissions)) {
    throw new Response('Unauthorized access', { status: 403 });
  }

  const municipalityId = auth.municipality_id;

  if (!municipalityId) {
    throw new Response('User without assigned municipality', { status: 403 });
  }

  const formData = await request.formData();
  const intent = formData.get('intent');

  if (intent === 'create') {
    try {
      const formObject = Object.fromEntries(formData.entries());

      const formResult = MapLayerFormSchema.safeParse(formObject);

      if (!formResult.success) {
        console.error('Form validation errors:', formResult.error.errors);
        return { error: 'Invalid form data' };
      }

      const createData = {
        ...formResult.data,
        municipality_ids: [municipalityId],
      };

      const validatedData = MapLayerCreateSchema.parse(createData);

      await createMapLayer(validatedData);

      return { success: true };
    } catch (error) {
      console.error('Error creating map layer:', error);
      return { error: 'Error creating layer' };
    }
  }

  if (intent === 'update') {
    try {
      const layerId = formData.get('layerId') as string;
      if (!layerId) {
        return { error: 'Layer ID not provided' };
      }

      const formObject = Object.fromEntries(formData.entries());
      delete formObject.layerId;
      delete formObject.intent;

      const formResult = MapLayerFormSchema.safeParse(formObject);

      if (!formResult.success) {
        console.error('Form validation errors:', formResult.error.errors);
        return { error: 'Invalid form data' };
      }

      const updateData = {
        ...formResult.data,
        municipality_ids: [municipalityId],
      };

      const validatedData = MapLayerUpdateSchema.parse(updateData);

      await updateMapLayer(Number(layerId), validatedData);
      return { success: true };
    } catch (error) {
      console.error('Error updating map layer:', error);
      return { error: 'Error updating layer' };
    }
  }

  return null;
}

export async function loader({ request }: LoaderFunctionArgs) {
  const auth = await requireAuth(request);

  const userForPermissions = {
    id: auth.id ?? 0,
    email: auth.email ?? '',
    name: auth.name ?? '',
    role_name: auth.role_name,
  };

  if (!checkDirectorPermissions(userForPermissions)) {
    throw new Response('Unauthorized access', { status: 403 });
  }

  const municipalityId = auth.municipality_id;
  if (!municipalityId) {
    throw new Response('User without assigned municipality', { status: 403 });
  }

  const layers = await getMapLayers({ municipality: municipalityId });
  if (!layers) {
    throw new Response('Error loading layers', { status: 500 });
  }

  return { auth, layers };
}

export default function MunicipalLayers() {
  const { t } = useTranslation('municipal-layers');
  const { layers } = useLoaderData<typeof loader>();
  const fetcher = useFetcher<typeof action>();

  const [state, dispatch] = useReducer(layerReducer, initialState);

  useEffect(() => {
    if (fetcher.data?.success) {
      dispatch({ type: 'CLOSE_MODAL' });
    }
  }, [fetcher.data]);

  const handleEdit = (layer: MapLayer) => {
    dispatch({ type: 'OPEN_EDIT_MODAL', layer });
  };

  const columns: Array<{
    key: keyof MapLayer;
    label: string;
    sortable?: boolean;
    render?: (value: unknown, row: MapLayer) => ReactElement;
  }> = [
    {
      key: 'label',
      label: t('columns.name'),
      sortable: true,
      render: (value: unknown, row: MapLayer) => (
        <div className="flex items-center space-x-2">
          <Layers className="h-4 w-4 text-gray-400" />
          <div>
            <div className="font-medium text-gray-900">{row.label}</div>
            <div className="text-sm text-gray-500">{row.layers}</div>
          </div>
        </div>
      ),
    },
    {
      key: 'type',
      label: t('columns.type'),
      render: (value: unknown, row: MapLayer) => (
        <span
          className={cn(
            'inline-flex px-2 py-1 text-xs font-medium rounded-full',
            row.type === 'vector' && 'bg-blue-100 text-blue-800',
            row.type === 'raster' && 'bg-green-100 text-green-800',
            row.type === 'wms' && 'bg-purple-100 text-purple-800',
            !['vector', 'raster', 'wms'].includes(row.type) &&
              'bg-orange-100 text-orange-800'
          )}
        >
          {row.type.toUpperCase()}
        </span>
      ),
    },
    {
      key: 'format',
      label: t('columns.format'),
    },
    {
      key: 'server_type',
      label: t('columns.server'),
      render: (value: unknown, row: MapLayer) => (
        <span className="text-sm text-gray-600">
          {row.server_type
            ? row.server_type.toUpperCase()
            : t('status.notAvailable')}
        </span>
      ),
    },
    {
      key: 'visible',
      label: t('columns.visible'),
      sortable: true,
      render: (value: unknown, row: MapLayer) => (
        <span
          className={cn(
            'inline-flex px-2 py-1 text-xs font-medium rounded-full',
            row.visible
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          )}
        >
          {row.visible ? t('status.visible') : t('status.hidden')}
        </span>
      ),
    },
    {
      key: 'active',
      label: t('columns.status'),
      sortable: true,
      render: (value: unknown, row: MapLayer) => (
        <div className="flex items-center space-x-1">
          {row.active ? (
            <ToggleRight className="h-5 w-5 text-green-600" />
          ) : (
            <ToggleLeft className="h-5 w-5 text-gray-400" />
          )}
          <span
            className={cn(
              'text-sm',
              row.active ? 'text-green-600' : 'text-gray-400'
            )}
          >
            {row.active ? t('status.active') : t('status.inactive')}
          </span>
        </div>
      ),
    },
    {
      key: 'editable',
      label: t('columns.editable'),
      render: (value: unknown, row: MapLayer) => (
        <span
          className={cn(
            'inline-flex px-2 py-1 text-xs font-medium rounded-full',
            row.editable
              ? 'bg-blue-100 text-blue-800'
              : 'bg-gray-100 text-gray-800'
          )}
        >
          {row.editable ? t('status.yes') : t('status.no')}
        </span>
      ),
    },
    {
      key: 'opacity',
      label: t('columns.opacity'),
      render: (value: unknown, row: MapLayer) => (
        <span className="text-sm text-gray-600">
          {Math.round(row.opacity * 100)}%
        </span>
      ),
    },
    {
      key: 'order',
      label: t('columns.order'),
      sortable: true,
    },
    {
      key: 'url',
      label: t('columns.url'),
      sortable: true,
      render: (value: unknown, row: MapLayer) => (
        <span className="text-sm text-gray-600 truncate max-w-xs">
          {row.url}
        </span>
      ),
    },
    {
      key: 'attribution',
      label: t('columns.attribution'),
      render: (value: unknown, row: MapLayer) => (
        <span className="text-sm text-gray-600">
          {row.attribution ?? t('status.notAvailable')}
        </span>
      ),
    },
    {
      key: 'projection',
      label: t('columns.projection'),
    },
    {
      key: 'version',
      label: t('columns.version'),
    },
    {
      key: 'value',
      label: t('columns.value'),
      sortable: true,
    },
    {
      key: 'type_geom',
      label: t('columns.geometryType'),
      render: (value: unknown, row: MapLayer) => (
        <span className="text-sm text-gray-600">
          {row.type_geom ?? t('status.notAvailable')}
        </span>
      ),
    },
    {
      key: 'cql_filter',
      label: t('columns.cqlFilter'),
      sortable: true,
      render: (value: unknown, row: MapLayer) => (
        <span className="text-sm text-gray-600 truncate max-w-xs">
          {row.cql_filter ?? t('status.notAvailable')}
        </span>
      ),
    },
    {
      key: 'id',
      label: t('columns.actions'),
      render: (value: unknown, row: MapLayer) => (
        <div className="flex items-center space-x-2">
          <Button variant="tertiary" onClick={() => handleEdit(row)}>
            <Edit className="h-4 w-4" />
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6 px-5 md:px-8 lg:px-10 py-6 md:py-8 lg:py-10">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {t('page.title')}
          </h1>
          <p className="text-gray-600 mt-1">{t('page.description')}</p>
        </div>
        <Button onClick={() => dispatch({ type: 'OPEN_ADD_MODAL' })}>
          <Plus className="h-4 w-4 mr-2" />
          {t('actions.addLayer')}
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Layers className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  {t('statistics.totalLayers')}
                </dt>
                <dd className="text-lg font-medium text-gray-900">
                  {layers.length}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <ToggleRight className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  {t('statistics.activeLayers')}
                </dt>
                <dd className="text-lg font-medium text-gray-900">
                  {layers.filter(l => l.active).length}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Eye className="h-8 w-8 text-purple-600" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">
                  {t('statistics.visibleLayers')}
                </dt>
                <dd className="text-lg font-medium text-gray-900">
                  {layers.filter(l => l.visible).length}
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <DataTable
          data={layers}
          columns={columns}
          title={t('page.title')}
          exportable
          searchable
          initialSort={{ key: 'label', direction: 'asc' }}
        />
      </div>

      <Dialog
        open={state.modalMode === 'add'}
        onOpenChange={open => {
          if (!open) {
            dispatch({ type: 'CLOSE_MODAL' });
          }
        }}
      >
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{t('modal.addTitle')}</DialogTitle>
          </DialogHeader>
          {fetcher.data?.error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {fetcher.data.error}
            </div>
          )}
          <fetcher.Form method="POST" className="space-y-4">
            <input type="hidden" name="intent" value="create" />

            <Input
              id="label"
              name="label"
              type="text"
              label={t('form.layerName')}
              placeholder={t('placeholders.layerName')}
              required
            />

            <Input
              id="value"
              name="value"
              type="text"
              label={t('form.layerValue')}
              placeholder={t('placeholders.layerValue')}
              required
            />

            <Input
              id="layers"
              name="layers"
              type="text"
              label={t('form.layers')}
              placeholder={t('placeholders.layers')}
              required
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Select
                name="type"
                defaultValue="wms"
                label={t('form.layerType')}
                placeholder={t('placeholders.selectType')}
                onValueChange={value =>
                  dispatch({ type: 'SET_LAYER_TYPE', layerType: value })
                }
              >
                <Option value="wms">{t('layerTypes.wms')}</Option>
                <Option value="xyz">{t('layerTypes.xyz')}</Option>
              </Select>

              <Select
                name="server_type"
                label={t('form.serverType')}
                placeholder={t('placeholders.selectServer')}
              >
                <Option value="geoserver">{t('serverTypes.geoserver')}</Option>
                <Option value="mapserver">{t('serverTypes.mapserver')}</Option>
                <Option value="qgis">{t('serverTypes.qgis')}</Option>
                <Option value="carmentaserver">
                  {t('serverTypes.carmentaserver')}
                </Option>
              </Select>
            </div>

            <Input
              id="url"
              name="url"
              type="url"
              label={t('form.serviceUrl')}
              placeholder={t('placeholders.serviceUrl')}
              required
            />

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Input
                id="format"
                name="format"
                type="text"
                label={t('form.format')}
                placeholder={t('placeholders.format')}
                required
              />

              {state.layerType === 'wms' ? (
                <Select
                  name="version"
                  defaultValue="1.3.0"
                  label={t('form.version')}
                  placeholder={t('placeholders.selectVersion')}
                >
                  <Option value="1.1.1">1.1.1</Option>
                  <Option value="1.3.0">1.3.0</Option>
                </Select>
              ) : (
                <>
                  <input name="version" type="hidden" value="1.0" />
                  <Input
                    id="version"
                    type="text"
                    label={t('form.version')}
                    value="1.0"
                    disabled
                  />
                </>
              )}

              <Input
                id="projection"
                name="projection"
                type="text"
                label={t('form.projection')}
                placeholder={t('placeholders.projection')}
                defaultValue="EPSG:4326"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Slider
                id="opacity"
                value={state.opacity}
                onValueChange={(value: number[]) =>
                  dispatch({ type: 'SET_OPACITY', opacity: value })
                }
                min={0}
                max={1}
                step={0.01}
                className="w-full"
                label={`${t('form.opacity')}: ${Math.round(state.opacity[0] * 100)}%`}
              />
              <input type="hidden" name="opacity" value={state.opacity[0]} />

              <Input
                id="order"
                name="order"
                type="number"
                min="0"
                label={t('form.order')}
                defaultValue="0"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                id="attribution"
                name="attribution"
                type="text"
                label={t('form.attribution')}
                placeholder={t('placeholders.attribution')}
              />

              <Input
                id="type_geom"
                name="type_geom"
                type="text"
                label={t('form.geometryType')}
                placeholder={t('placeholders.geometryType')}
              />
            </div>

            <Input
              id="cql_filter"
              name="cql_filter"
              type="text"
              label={t('form.cqlFilter')}
              placeholder={t('placeholders.cqlFilter')}
            />

            <div className="flex items-center space-x-4">
              <Checkbox
                name="active"
                label={t('form.activateLayer')}
                defaultChecked
              />
              <Checkbox
                name="visible"
                label={t('form.visible')}
                defaultChecked
              />
              <Checkbox
                name="editable"
                label={t('form.editable')}
                defaultChecked
              />
            </div>

            <DialogFooter>
              <Button
                type="button"
                variant="secondary"
                onClick={() => dispatch({ type: 'CLOSE_MODAL' })}
                disabled={fetcher.state === 'submitting'}
              >
                {t('actions.cancel')}
              </Button>
              <Button type="submit" disabled={fetcher.state === 'submitting'}>
                {fetcher.state === 'submitting'
                  ? t('actions.adding')
                  : t('actions.add')}
              </Button>
            </DialogFooter>
          </fetcher.Form>
        </DialogContent>
      </Dialog>

      <Dialog
        open={state.modalMode === 'edit'}
        onOpenChange={open => {
          if (!open) {
            dispatch({ type: 'CLOSE_MODAL' });
          }
        }}
      >
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{t('modal.editTitle')}</DialogTitle>
          </DialogHeader>
          {fetcher.data?.error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {fetcher.data.error}
            </div>
          )}
          {state.selectedLayer && (
            <fetcher.Form method="POST" className="space-y-4">
              <input type="hidden" name="intent" value="update" />
              <input
                type="hidden"
                name="layerId"
                value={state.selectedLayer.id}
              />

              <Input
                id="edit-label"
                name="label"
                type="text"
                label={t('form.layerName')}
                defaultValue={state.selectedLayer.label}
                required
              />

              <Input
                id="edit-value"
                name="value"
                type="text"
                label={t('form.layerValue')}
                defaultValue={state.selectedLayer.value}
                required
              />

              <Input
                id="edit-layers"
                name="layers"
                type="text"
                label={t('form.layers')}
                defaultValue={state.selectedLayer.layers}
                required
              />

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Select
                  name="type"
                  defaultValue={state.selectedLayer.type}
                  label={t('form.layerType')}
                  placeholder={t('placeholders.selectType')}
                  onValueChange={value =>
                    dispatch({ type: 'SET_LAYER_TYPE', layerType: value })
                  }
                >
                  <Option value="wms">{t('layerTypes.wms')}</Option>
                  <Option value="xyz">{t('layerTypes.xyz')}</Option>
                </Select>

                <Select
                  name="server_type"
                  defaultValue={state.selectedLayer.server_type ?? ''}
                  label={t('form.serverType')}
                  placeholder={t('placeholders.selectServer')}
                >
                  <Option value="geoserver">
                    {t('serverTypes.geoserver')}
                  </Option>
                  <Option value="mapserver">
                    {t('serverTypes.mapserver')}
                  </Option>
                  <Option value="qgis">{t('serverTypes.qgis')}</Option>
                  <Option value="carmentaserver">
                    {t('serverTypes.carmentaserver')}
                  </Option>
                </Select>
              </div>

              <Input
                id="edit-url"
                name="url"
                type="url"
                label={t('form.serviceUrl')}
                defaultValue={state.selectedLayer.url}
                required
              />

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Input
                  id="edit-format"
                  name="format"
                  type="text"
                  label={t('form.format')}
                  defaultValue={state.selectedLayer.format}
                  required
                />

                {state.layerType === 'wms' ? (
                  <Select
                    name="version"
                    defaultValue={state.selectedLayer.version}
                    label={t('form.version')}
                    placeholder={t('placeholders.selectVersion')}
                  >
                    <Option value="1.1.1">1.1.1</Option>
                    <Option value="1.3.0">1.3.0</Option>
                  </Select>
                ) : (
                  <Input
                    id="edit-version"
                    name="version"
                    type="text"
                    label={t('form.version')}
                    defaultValue={state.selectedLayer.version}
                  />
                )}

                <Input
                  id="edit-projection"
                  name="projection"
                  type="text"
                  label={t('form.projection')}
                  defaultValue={state.selectedLayer.projection}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Slider
                  id="edit-opacity"
                  value={state.opacity}
                  onValueChange={(value: number[]) =>
                    dispatch({ type: 'SET_OPACITY', opacity: value })
                  }
                  min={0}
                  max={1}
                  step={0.01}
                  className="w-full"
                  label={`${t('form.opacity')}: ${Math.round(state.opacity[0] * 100)}%`}
                />
                <input type="hidden" name="opacity" value={state.opacity[0]} />

                <Input
                  id="edit-order"
                  name="order"
                  type="number"
                  min="0"
                  label={t('form.order')}
                  defaultValue={state.selectedLayer.order}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  id="edit-attribution"
                  name="attribution"
                  type="text"
                  label={t('form.attribution')}
                  defaultValue={state.selectedLayer.attribution ?? ''}
                />

                <Input
                  id="edit-type_geom"
                  name="type_geom"
                  type="text"
                  label={t('form.geometryType')}
                  defaultValue={state.selectedLayer.type_geom ?? ''}
                />
              </div>

              <Input
                id="edit-cql_filter"
                name="cql_filter"
                type="text"
                label={t('form.cqlFilter')}
                defaultValue={state.selectedLayer.cql_filter ?? ''}
              />

              <div className="flex items-center space-x-4">
                <Checkbox
                  name="active"
                  label={t('form.activateLayer')}
                  defaultChecked={state.selectedLayer.active}
                />
                <Checkbox
                  name="visible"
                  label={t('form.visible')}
                  defaultChecked={state.selectedLayer.visible}
                />
                <Checkbox
                  name="editable"
                  label={t('form.editable')}
                  defaultChecked={state.selectedLayer.editable}
                />
              </div>

              <DialogFooter>
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => dispatch({ type: 'CLOSE_MODAL' })}
                  disabled={fetcher.state === 'submitting'}
                >
                  {t('actions.cancel')}
                </Button>
                <Button type="submit" disabled={fetcher.state === 'submitting'}>
                  {fetcher.state === 'submitting'
                    ? t('actions.updating')
                    : t('actions.save')}
                </Button>
              </DialogFooter>
            </fetcher.Form>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
