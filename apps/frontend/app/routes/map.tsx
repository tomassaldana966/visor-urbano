import {
  OpenLayerMap,
  OpenLayerMapLayersControls,
} from '@/components/OpenLayerMap/OpenLayerMap';
import Skeleton from 'react-loading-skeleton';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/Tabs/Tabs';
import {
  CirclePlus,
  CircleUserRound,
  DraftingCompass,
  Layers,
  MapPin,
  Megaphone,
  Pencil,
  Ruler,
  RulerDimensionLine,
  CloudUpload,
  Info,
  Search,
  CircleX,
  ArrowLeft,
  Upload,
} from 'lucide-react';
import {
  type ComponentProps,
  Suspense,
  useReducer,
  useEffect,
  useState,
} from 'react';
import { useTranslation } from 'react-i18next';
import {
  Await,
  Form,
  Link,
  useLoaderData,
  useNavigation,
  useSearchParams,
  type ActionFunctionArgs,
  type LoaderFunctionArgs,
} from 'react-router';
import { cn } from '@/lib/utils';
import { Input } from '@/components/Input/Input';
import { BloombergLogo } from '@/components/Logos/Bloomberg';
import { CityLogo } from '@/components/Logos/City';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/Dialog/Dialog';
import {
  getBusinessTypes,
  getDynamicFields,
  getMapLayers,
  getMunicipalities,
  getTechnicalSheetURL,
  postRequirementsQueries,
  searchByAddress,
} from '@/utils/api/api.server';
import {
  fetchGeoServer,
  getPropertyData,
  getPolygonCenter,
  decodePolygonFromBase64,
} from '../utils/map/map';
import { PropertyInfo } from '../components/PropertyInfo/PropertyInfo';

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '../components/Accordion/Accordion';
import { Checkbox } from '../components/Checkbox/Checkbox';
import { Button } from '../components/Button/Button';
import { getObjectFromZodIssues } from '../utils/zod/zod';
import {
  commercialRequirementsSchema,
  constructionRequirementsSchema,
} from '../schemas/requirements';
import { Option, Select } from '../components/Select/Select';
import { toLonLat, fromLonLat } from 'ol/proj';
import { processUploadedFile } from '../utils/fileProcessing/fileProcessing';

export function meta() {
  return [{ title: 'Visor Urbano | Mapa' }];
}

export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);

  const searchParams = new URLSearchParams(url.search);

  const point = searchParams.get('point');
  const polygon = searchParams.get('polygon');
  const address = searchParams.get('address');
  const municipality = searchParams.get('municipality');

  let searchResult;

  if (address && municipality) {
    searchResult = searchByAddress({
      address,
      municipality,
    });
  }

  let property = null;
  let polygonFromUrl: number[][] | null = null;

  let queryPoint: string | null = null;

  if (polygon && polygon !== 'null') {
    try {
      polygonFromUrl = decodePolygonFromBase64(polygon);

      if (polygonFromUrl) {
        const center = getPolygonCenter(polygonFromUrl);
        if (center) {
          const [lon, lat] = center;
          const transformed = fromLonLat([lon, lat], 'EPSG:32613');
          queryPoint = `${transformed[0]} ${transformed[1]}`;
        }
      }
    } catch (error) {
      console.error('Error parsing polygon:', error);
    }
  } else if (point && point !== 'null') {
    // Point coordinates are in EPSG:4326 (WGS84) format from map click
    // Transform them to local SRS for GeoServer query, same as polygon processing
    const [lon, lat] = point.split(' ').map(Number);
    const transformed = fromLonLat([lon, lat], 'EPSG:32613');
    queryPoint = `${transformed[0]} ${transformed[1]}`;
  }

  if (queryPoint) {
    property = fetchGeoServer({
      geoServerURL: process.env.GEOSERVER_URL,
      service: 'WFS',
      request: 'GetFeature',
      version: '2.0.0',
      typename: `${process.env.MAP_PREDIOS_LAYER}`,
      count: 1,
      outputFormat: 'application/json',
      cql_filter: `CONTAINS(geom, POINT (${queryPoint}))`,
    })
      .then(async response => {
        const data = await getPropertyData(response, polygonFromUrl);

        const dynamicFields = await getDynamicFields(
          data.municipalityId ?? 2, // Default to municipality 1 if undefined
          'all'
        );

        return {
          ...data,
          businessTypes: data.municipalityId
            ? await getBusinessTypes({
                municipality_id: data.municipalityId,
              })
            : [],
          dynamicFields: dynamicFields,
        };
      })
      .catch(_error => {
        return null;
      });
  }

  const states = await fetchGeoServer({
    geoServerURL: process.env.GEOSERVER_URL,
    service: 'WFS',
    request: 'GetFeature',
    version: '2.0.0',
    typename: `${process.env.MAP_ESTADO_LAYER}`,
    count: 1,
    outputFormat: 'application/json',
    cql_filter: `${process.env.MAP_ESTADO_CQL_FILTER}`,
  });

  let layers;

  try {
    layers = await getMapLayers({ municipality: 2 });
  } catch (error) {
    console.error('Error fetching map layers:', error);
  }

  return {
    layers,
    states,
    property,
    municipalities: getMunicipalities(),
    searchResult,
    ENV: {
      GEOSERVER_URL: process.env.GEOSERVER_URL,
      MAP_CENTER_LAT: process.env.MAP_CENTER_LAT,
      MAP_CENTER_LON: process.env.MAP_CENTER_LON,
      MAP_MUNICIPIO_LAYER: process.env.MAP_MUNICIPIO_LAYER,
      MAP_TILE_CENTER_X: process.env.MAP_TILE_CENTER_X,
      MAP_TILE_CENTER_Y: process.env.MAP_TILE_CENTER_Y,
    },
  };
}

const ortofotoLayer = {
  id: 'ortofoto-2020',
  label: 'Ortofoto 2020',
  url: 'http://localhost:8080/geoserver/visorurbano/wms',
  layers: 'visorurbano:ortofoto_ok',
  format: 'image/jpeg',
  projection: 'EPSG:32613',
  visible: true,
  server_type: 'geoserver',
};

function validateFormFields(
  fields: Record<string, string | null>,
  requiredFields: string[]
): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  for (const field of requiredFields) {
    if (!fields[field] || fields[field]?.trim() === '') {
      errors.push(`${field} is required`);
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

function parseNumericField(
  value: string | null,
  fieldName: string,
  allowNull = false
): { value: number | null; error?: string } {
  if (!value || value.trim() === '') {
    if (allowNull) {
      return { value: null };
    }
    return { value: null, error: `${fieldName} is required` };
  }

  const parsed = Number(value);
  if (isNaN(parsed)) {
    return { value: null, error: `${fieldName} must be a valid number` };
  }

  return { value: parsed };
}

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();

  const intent = formData.get('_intent');

  switch (intent) {
    case 'getRequirements': {
      const licenseType = formData.get('license_type') as string;

      if (licenseType === 'commercial') {
        if (!formData.has('person_type')) {
          let person_type = 'Moral';

          ['carta_poder_rad', 'propietario_rad', 'arrendatario_rad'].forEach(
            key => {
              const value = formData.get(key) as string;
              if (
                ['persona_fisica', 'propietario_i', 'arrendatario_i'].includes(
                  value
                )
              ) {
                person_type = 'Física';
              }
            }
          );

          formData.set('person_type', person_type);
        }

        const businessType = formData.get('businessType') as string;

        if (businessType?.includes('|')) {
          const [scian_code, scian_name] = businessType.split('|');

          if (!formData.has('scian_code')) {
            formData.set('scian_code', scian_code || '');
          }
          if (!formData.has('scian_name')) {
            formData.set('scian_name', scian_name || '');
          }
          if (!formData.has('activity_description')) {
            formData.set('activity_description', scian_name || '');
          }
        } else if (businessType) {
          if (!formData.has('scian_code')) {
            formData.set('scian_code', '');
          }
          if (!formData.has('scian_name')) {
            formData.set('scian_name', businessType);
          }
          if (!formData.has('activity_description')) {
            formData.set('activity_description', businessType);
          }
        }

        const alcoholSales = formData.get('alcohol_sales') as string;

        if (alcoholSales?.includes('|')) {
          const [alcoholValue] = alcoholSales.split('|');
          formData.set('alcohol_sales', alcoholValue);
        }
      }

      const data: Record<string, string | Record<string, string>> = {};

      for (const [key, value] of formData.entries()) {
        if (typeof value === 'string') {
          data[key] = value;
        }
      }

      const dynamicFields: Record<string, string> = {};

      Object.entries(data).forEach(([key, value]) => {
        if (key.startsWith('dynamicFields.')) {
          const fieldKey = key.replace('dynamicFields.', '');

          if (typeof value === 'string') {
            dynamicFields[fieldKey] = value;

            delete data[key];
          }
        }
      });

      data.dynamic_fields = dynamicFields;

      data.applicant_character = data.dynamic_fields.quien_tramita;

      const schema =
        licenseType === 'commercial'
          ? commercialRequirementsSchema
          : constructionRequirementsSchema;

      const result = schema.safeParse(data);

      const errors = getObjectFromZodIssues(result.error?.issues);

      const formDataObject: Record<string, string> = {};
      for (const [key, value] of formData.entries()) {
        if (typeof value === 'string') {
          formDataObject[key] = value;
        }
      }

      if (errors || !result.data) {
        console.error('Validation errors:', JSON.stringify(errors, null, 2));
        return {
          formData: formDataObject,
          error: 'Error sending requirements',
          licenseType,
        };
      }

      const requirements = await postRequirementsQueries(result.data);

      if (!requirements) {
        return {
          formData: formDataObject,
          error: 'Error sending requirements',
          licenseType,
        };
      }

      return {
        success: true,
        requirements: {
          folio: requirements.folio,
          url: requirements.url,
          issue_license: requirements.issue_license,
          message: requirements.message,
          data: requirements.data,
        },
      };
    }
    case 'downloadTechnicalSheet': {
      try {
        const fields = {
          address: formData.get('address') as string,
          square_meters: formData.get('square_meters') as string,
          coordinates: formData.get('coordinates') as string,
          image: formData.get('image') as string,
          municipality_id: formData.get('municipality_id') as string,
          technical_sheet_download_id: formData.get(
            'technical_sheet_download_id'
          ) as string,
        };

        const validation = validateFormFields(fields, [
          'address',
          'coordinates',
          'municipality_id',
        ]);

        if (!validation.isValid) {
          console.error('Validation errors:', validation.errors);
          return {
            error: `Missing required fields: ${validation.errors.join(', ')}`,
          };
        }

        const municipalityResult = parseNumericField(
          fields.municipality_id,
          'municipality_id'
        );
        if (municipalityResult.error) {
          console.error('Municipality ID error:', municipalityResult.error);
          return { error: municipalityResult.error };
        }

        const technicalSheetResult = parseNumericField(
          fields.technical_sheet_download_id,
          'technical_sheet_download_id',
          true
        );
        if (technicalSheetResult.error) {
          console.error(
            'Technical sheet ID error:',
            technicalSheetResult.error
          );
          return { error: technicalSheetResult.error };
        }

        const technicalSheetURL = await getTechnicalSheetURL({
          address: fields.address,
          square_meters: fields.square_meters,
          coordinates: fields.coordinates,
          image: fields.image,
          municipality_id: municipalityResult.value!,
          technical_sheet_download_id: technicalSheetResult.value,
        });

        return {
          technicalSheetURL,
        };
      } catch (error) {
        console.error('Error in downloadTechnicalSheet:', error);
        return {
          error: 'Invalid form data for technical sheet download',
        };
      }
    }
    default:
      break;
  }

  return {};
}

const asideOptions = [
  {
    icon: (
      <CircleUserRound
        size={24}
        className="text-black/20 group-hover:text-white"
      />
    ),
    id: 'user',
    to: '/login',
  },
  {
    icon: (
      <CirclePlus size={24} className="text-black/20 group-hover:text-white" />
    ),
    label: 'aside.new',
    onClick: () => {
      const addressElement = document.getElementById('address');
      if (addressElement && addressElement instanceof HTMLInputElement) {
        addressElement.focus();
      }
    },
    id: 'new',
  },
  {
    icon: <Layers size={24} className="text-black/20 group-hover:text-white" />,
    label: 'aside.layers',
    id: 'layers',
  },
  {
    icon: (
      <Megaphone size={24} className="text-black/20 group-hover:text-white" />
    ),
    label: 'aside.commercial',
    id: 'commercial',
    hidden: true,
  },
  {
    icon: (
      <RulerDimensionLine
        size={24}
        className="text-black/20 group-hover:text-white"
      />
    ),
    label: 'aside.measure',
    id: 'measure',
  },
  {
    icon: (
      <CloudUpload size={24} className="text-black/20 group-hover:text-white" />
    ),
    label: 'aside.upload',
    id: 'upload',
  },
  {
    icon: <Info size={24} className="text-black/20 group-hover:text-white" />,
    label: 'aside.info',
    id: 'info',
  },
] as const;

const tools = [
  {
    id: 'select',
    icon: <MapPin size={16} />,
    label: 'controls.tools.tabs.tools.list.select',
  },
  {
    id: 'draw',
    icon: <Pencil size={16} />,
    label: 'controls.tools.tabs.tools.list.draw',
  },
  {
    id: 'measure-lineal',
    icon: <Ruler size={16} />,
    label: 'controls.tools.tabs.tools.list.measure-lineal',
  },
  {
    id: 'measure-area',
    icon: <DraftingCompass size={16} />,
    label: 'controls.tools.tabs.tools.list.measure-area',
  },
  {
    id: 'info',
    icon: <Info size={16} />,
    label: 'controls.tools.tabs.tools.list.info',
  },
] as const;

type State = {
  layers: Awaited<ReturnType<typeof loader>>['layers'];
  mode: (typeof asideOptions)[number]['id'] | null;
  selectedTool: ComponentProps<typeof OpenLayerMap>['tool'];
  showInfo: boolean;
  showMapControls: boolean;
  pendingPoint?: string;
  layerInfoData: { layerName: string; data: unknown }[] | null;
  showLayerInfoDialog: boolean;
  showUploadDialog: boolean;
  uploadStep: 'disclaimer' | 'file-selection';
  uploadProcessing: boolean;
  uploadError: string | null;
};

type Actions =
  | {
      type: 'SET_TOOL';
      payload: State['selectedTool'];
    }
  | {
      type: 'SET_MODE';
      payload: State['mode'];
    }
  | {
      type: 'MAP_CLICK';
      payload: {
        coordinates: number[];
      };
    }
  | {
      type: 'SET_SHOW_INFO';
      payload: boolean;
    }
  | {
      type: 'TOGGLE_LAYER';
      payload: {
        id: number;
      };
    }
  | {
      type: 'TOGGLE_SHOW_MAP_CONTROLS';
    }
  | {
      type: 'SET_LAYER_INFO_DATA';
      payload: { layerName: string; data: unknown }[];
    }
  | {
      type: 'SET_SHOW_LAYER_INFO_DIALOG';
      payload: boolean;
    }
  | {
      type: 'SET_SHOW_UPLOAD_DIALOG';
      payload: boolean;
    }
  | {
      type: 'SET_UPLOAD_STEP';
      payload: State['uploadStep'];
    }
  | {
      type: 'SET_UPLOAD_PROCESSING';
      payload: boolean;
    }
  | {
      type: 'SET_UPLOAD_ERROR';
      payload: string | null;
    };

export default function MapRoute() {
  const { t: tMap } = useTranslation('map');

  const navigation = useNavigation();

  
  const loaderData = useLoaderData<typeof loader>();

  const [searchParams, setSearchParams] = useSearchParams();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const [state, dispatch] = useReducer(
    (state: State, action: Actions) => {
      switch (action.type) {
        case 'SET_TOOL': {
          return {
            ...state,
            selectedTool: action.payload,
          };
        }
        case 'SET_MODE': {
          return {
            ...state,
            mode: action.payload,
            showMapControls: true,
            selectedTool:
              action.payload === 'info' ? 'info' : state.selectedTool,
          };
        }
        case 'MAP_CLICK': {
          if (state.selectedTool === 'select') {
            // Transform coordinates from map projection (EPSG:32613) to WGS84 (EPSG:4326)
            // to match how polygon coordinates are stored
            const wgs84Coordinates = toLonLat(
              action.payload.coordinates,
              'EPSG:32613'
            );
            return {
              ...state,
              showInfo: true,
              pendingPoint: wgs84Coordinates.join(' '),
            };
          } else if (state.mode === 'info') {
            const visibleLayers =
              state.layers?.filter(layer => layer.visible) || [];
            const coordinates = action.payload.coordinates;

            const [lon, lat] = toLonLat(coordinates, 'EPSG:32613');

            const tolerance = 0.0001;
            const bbox = `${lat - tolerance},${lon - tolerance},${lat + tolerance},${lon + tolerance}`;

            const fetchPromises = visibleLayers.map(async layer => {
              try {
                const data = await fetchGeoServer({
                  geoServerURL: loaderData.ENV.GEOSERVER_URL,
                  SERVICE: 'WMS',
                  VERSION: '1.3.0',
                  REQUEST: 'GetFeatureInfo',
                  FORMAT: 'image/png',
                  TRANSPARENT: 'true',
                  QUERY_LAYERS: layer.layers,
                  LAYERS: layer.layers,
                  SRS: layer.projection,
                  CRS: 'EPSG:4326',
                  TILED: 'true',
                  TILESORIGIN: '-180,-90',
                  INFO_FORMAT: 'application/json',
                  FEATURE_COUNT: 10,
                  I: parseInt(loaderData.ENV.MAP_TILE_CENTER_X ?? '128'),
                  J: parseInt(loaderData.ENV.MAP_TILE_CENTER_Y ?? '128'),
                  WIDTH: 256,
                  HEIGHT: 256,
                  STYLES: '',
                  BBOX: bbox,
                });

                let properties = {};

                if (
                  data &&
                  Array.isArray(data.features) &&
                  data.features[0]?.properties
                ) {
                  properties = data.features[0].properties;
                }

                return { layerName: layer.label, data: properties };
              } catch (error) {
                console.error(
                  `Error fetching data from layer ${layer.label}:`,
                  error
                );
                return {
                  layerName: layer.label,
                  data: {
                    error:
                      error instanceof Error ? error.message : 'Unknown error',
                  },
                };
              }
            });

            Promise.all(fetchPromises).then(results => {
              if (
                results.some(
                  r => !(r.data && (r.data as { error?: unknown }).error)
                )
              ) {
                dispatch({
                  type: 'SET_LAYER_INFO_DATA',
                  payload: results,
                });
                dispatch({
                  type: 'SET_SHOW_LAYER_INFO_DIALOG',
                  payload: true,
                });
              }
            });

            return {
              ...state,
            };
          } else {
            return {
              ...state,
            };
          }
        }
        case 'TOGGLE_LAYER': {
          const newState = structuredClone(state);

          const updatedLayers = state.layers?.map(layer => {
            if (layer.id === action.payload.id) {
              return {
                ...layer,
                visible: !layer.visible,
              };
            }
            return layer;
          });

          return {
            ...newState,
            layers: updatedLayers,
          };
        }
        case 'SET_SHOW_INFO': {
          return {
            ...state,
            showInfo: action.payload,
          };
        }
        case 'TOGGLE_SHOW_MAP_CONTROLS': {
          return {
            ...structuredClone(state),
            showMapControls: !state.showMapControls,
          };
        }
        case 'SET_LAYER_INFO_DATA': {
          return {
            ...state,
            layerInfoData: action.payload,
          };
        }
        case 'SET_SHOW_LAYER_INFO_DIALOG': {
          return {
            ...state,
            showLayerInfoDialog: action.payload,
          };
        }
        case 'SET_SHOW_UPLOAD_DIALOG': {
          return {
            ...state,
            showUploadDialog: action.payload,
            uploadStep: action.payload ? 'disclaimer' : state.uploadStep,
            uploadError: action.payload ? null : state.uploadError,
          };
        }
        case 'SET_UPLOAD_STEP': {
          return {
            ...state,
            uploadStep: action.payload,
            uploadError: null,
          };
        }
        case 'SET_UPLOAD_PROCESSING': {
          return {
            ...state,
            uploadProcessing: action.payload,
          };
        }
        case 'SET_UPLOAD_ERROR': {
          return {
            ...state,
            uploadError: action.payload,
            uploadProcessing: false,
          };
        }
        default: {
          return state;
        }
      }
    },
    {
      layers: loaderData?.layers,
      mode: 'layers',
      selectedTool: 'select',
      showInfo: !!loaderData.property,
      showMapControls: false,
      layerInfoData: null,
      showLayerInfoDialog: false,
      showUploadDialog: false,
      uploadStep: 'disclaimer',
      uploadProcessing: false,
      uploadError: null,
    }
  );

  const layersWithOrtofoto = state.layers
  ? [ortofotoLayer, ...state.layers]
  : [ortofotoLayer];
  
  const handleFileUpload = async (file: File) => {
    dispatch({ type: 'SET_UPLOAD_PROCESSING', payload: true });
    dispatch({ type: 'SET_UPLOAD_ERROR', payload: null });

    const result = await processUploadedFile(file);

    if ('message' in result) {
      // Error case
      dispatch({
        type: 'SET_UPLOAD_ERROR',
        payload: result.message + (result.details ? ': ' + result.details : ''),
      });
    } else {
      // Success case
      setSearchParams(searchParams => {
        searchParams.set('polygon', result.polygonBase64);
        searchParams.delete('point');
        return searchParams;
      });

      dispatch({ type: 'SET_SHOW_UPLOAD_DIALOG', payload: false });
      setSelectedFile(null);
    }

    dispatch({ type: 'SET_UPLOAD_PROCESSING', payload: false });
  };

  useEffect(() => {
    if (state.pendingPoint) {
      setSearchParams(prev => {
        const newParams = new URLSearchParams(prev);

        newParams.set('point', state.pendingPoint!);
        newParams.delete('polygon');

        return newParams;
      });
    }
  }, [state.pendingPoint, setSearchParams]);

  return (
    <main className="w-screen h-screen relative">
      <header className="flex justify-between gap-4 pl-20 py-4 px-8 items-center shadow-2xl bg-white absolute top-0 left-0 right-0 z-20">
        <Link to="/">
          <img
            src="/logos/visor-urbano.svg"
            alt="Visor Urbano"
            className="h-12"
          />
        </Link>
        <div className="flex gap-4 items-center">
          <CityLogo />

          <BloombergLogo />
        </div>
      </header>

      <aside className="fixed top-0 left-0 bottom-0 h-full bg-primary z-20 w-18 rounded-e-2xl shadow-2xl text-white text-center flex flex-col justify-center">
        <ul className="flex flex-col gap-2 text-xs items-center">
          {asideOptions
            .filter(option => ('hidden' in option ? !option.hidden : true))
            .map(option => {
              const className =
                'hover:bg-black/20 w-full flex flex-col gap-1 items-center justify-center p-2 text-white/70 hover:text-white cursor-pointer group';

              return (
                <li className="flex flex-col w-full" key={option.id}>
                  {'to' in option ? (
                    <Link className={className} to={option.to}>
                      {option.icon}
                    </Link>
                  ) : (
                    <button
                      className={className}
                      onClick={() => {
                        if (
                          'onClick' in option &&
                          typeof option.onClick === 'function'
                        ) {
                          option.onClick();
                        } else if (option.id === 'upload') {
                          dispatch({
                            type: 'SET_SHOW_UPLOAD_DIALOG',
                            payload: true,
                          });
                        } else {
                          dispatch({
                            type: 'SET_MODE',
                            payload: option.id,
                          });
                        }
                      }}
                    >
                      {option.icon}
                      {'label' in option ? tMap(option.label) : null}
                    </button>
                  )}
                </li>
              );
            })}
        </ul>
      </aside>

      <Form
        method="GET"
        className="fixed top-26 left-22 z-10 gap-2 flex flex-col w-xs"
      >
        <Suspense
          fallback={
            <Select disabled placeholder={tMap('search.municipality')} />
          }
        >
          <Await resolve={loaderData.municipalities}>
            {municipalities => (
              <Select
                required
                name="municipality"
                placeholder={tMap('search.municipality')}
                defaultValue={searchParams.get('municipality') ?? ''}
              >
                {municipalities.map(municipality => (
                  <Option key={municipality.id} value={`${municipality.name}`}>
                    {municipality.name}
                  </Option>
                ))}
              </Select>
            )}
          </Await>
        </Suspense>

        <Input
          required
          type="text"
          placeholder="Search"
          defaultValue={searchParams.get('address') ?? ''}
          name="address"
          id="address"
          post={
            <Button>
              <Search size={18} />
            </Button>
          }
        />

        <Button
          onClick={() => {
            dispatch({
              type: 'SET_TOOL',
              payload: 'clear',
            });
          }}
          type="button"
        >
          {tMap('search.clearMap')}
        </Button>
      </Form>

      <section
        className={cn(
          'fixed left-0 top-0 z-10 bg-white pl-24 pt-36 bottom-0 pr-4 max-w-md w-full overflow-y-auto transition-transform',
          {
            '-translate-x-full': !state.showInfo,
          }
        )}
      >
        <button
          className="absolute right-4 top-24 cursor-pointer"
          onClick={() => dispatch({ type: 'SET_SHOW_INFO', payload: false })}
        >
          <CircleX />
        </button>
        <Suspense>
          <Await resolve={loaderData.property}>
            {property =>
              navigation.state === 'loading' ? (
                <Skeleton className="h-16 my-4" count={6} />
              ) : (
                <PropertyInfo
                  onDrawClick={() =>
                    dispatch({
                      type: 'SET_TOOL',
                      payload: 'draw',
                    })
                  }
                  property={property}
                />
              )
            }
          </Await>
        </Suspense>
      </section>

      <OpenLayerMap
        municipioLayer={loaderData.ENV.MAP_MUNICIPIO_LAYER ?? ''}
        geoServerURL={loaderData.ENV.GEOSERVER_URL ?? ''}
        states={loaderData.states}
        searchResult={loaderData.searchResult}
        layers={layersWithOrtofoto}
        property={loaderData.property}
        center={{
          lat: parseFloat(loaderData.ENV.MAP_CENTER_LAT ?? '0'),
          lon: parseFloat(loaderData.ENV.MAP_CENTER_LON ?? '0'),
        }}
        tool={state.selectedTool}
        onMapClick={({ coordinate }) => {
          dispatch({
            type: 'MAP_CLICK',
            payload: {
              coordinates: coordinate,
            },
          });
        }}
        onDrawEnd={() => {
          dispatch({
            type: 'SET_SHOW_INFO',
            payload: true,
          });
        }}
      >
        <OpenLayerMapLayersControls
          open={state.showMapControls}
          onToggle={() =>
            dispatch({
              type: 'TOGGLE_SHOW_MAP_CONTROLS',
            })
          }
        >
          <Tabs
            key={state.mode}
            defaultValue={
              state.mode && ['measure', 'upload', 'info'].includes(state.mode)
                ? 'tools'
                : 'layers'
            }
            className="p-4 h-full"
          >
            <TabsList>
              {state.mode &&
              ['measure', 'upload', 'info'].includes(state.mode) ? (
                <TabsTrigger value="tools">
                  {tMap('controls.tools.tabs.tools.title')}
                </TabsTrigger>
              ) : null}

              {state.mode === 'layers' ? (
                <>
                  <TabsTrigger value="layers">
                    {tMap('controls.layers.tabs.layers')}
                  </TabsTrigger>

                  <TabsTrigger value="conventions">
                    {tMap('controls.layers.tabs.conventions')}
                  </TabsTrigger>
                </>
              ) : null}
            </TabsList>

            {state.mode === 'layers' ? (
              <div className="overflow-y-auto">
                <TabsContent value="layers">
                  <ul>
                    {state.layers?.map(layer => (
                      <li key={layer.id}>
                        <Checkbox
                          label={layer.label}
                          id={`layer-${layer.id}`}
                          checked={layer.visible}
                          onCheckedChange={_checked => {
                            dispatch({
                              type: 'TOGGLE_LAYER',
                              payload: { id: layer.id },
                            });
                          }}
                        />
                      </li>
                    ))}
                  </ul>
                </TabsContent>

                <TabsContent value="conventions">
                  <Accordion type="single" collapsible>
                    {state.layers?.map(layer => (
                      <AccordionItem key={layer.id} value={`${layer.id}`}>
                        <AccordionTrigger>{layer.label}</AccordionTrigger>

                        <AccordionContent>
                          <img
                            alt={`Leyenda WMS ${layer.label}`}
                            style={{ maxWidth: 'initial' }}
                            src={
                              layer.url.endsWith('?')
                                ? `${layer.url}service=wms&request=GetLegendGraphic&VERSION=${layer.version}&FORMAT=image/png&LAYER=${layer.layers}`
                                : `${layer.url}?service=wms&request=GetLegendGraphic&VERSION=${layer.version}&FORMAT=image/png&LAYER=${layer.layers}`
                            }
                          />
                        </AccordionContent>
                      </AccordionItem>
                    ))}
                  </Accordion>
                </TabsContent>
              </div>
            ) : null}

            {state.mode &&
            ['measure', 'upload', 'info'].includes(state.mode) ? (
              <TabsContent value="tools">
                <ul className="flex flex-col">
                  {tools.map(tool => (
                    <li key={tool.id}>
                      <button
                        className={cn(
                          'flex gap-2 items-center p-2 border-slate-100 border w-full hover:border-primary',
                          {
                            'border-primary bg-primary/20':
                              state.selectedTool === tool.id,
                          }
                        )}
                        type="button"
                        onClick={() =>
                          dispatch({
                            type: 'SET_TOOL',
                            payload: tool.id,
                          })
                        }
                      >
                        {tool.icon}

                        {tMap(tool.label)}
                      </button>
                    </li>
                  ))}
                </ul>
              </TabsContent>
            ) : null}
          </Tabs>
        </OpenLayerMapLayersControls>
      </OpenLayerMap>

      {/* Layer Info Dialog */}
      <Dialog
        open={state.showLayerInfoDialog}
        onOpenChange={open =>
          dispatch({
            type: 'SET_SHOW_LAYER_INFO_DIALOG',
            payload: open,
          })
        }
      >
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-hidden">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Info size={20} />
              {tMap('info.dialog.title')}
            </DialogTitle>
          </DialogHeader>

          <div className="flex-1 overflow-auto">
            {state.layerInfoData && state.layerInfoData.length > 0 ? (
              <Accordion type="multiple" className="w-full">
                {state.layerInfoData.map((layerData, index) => (
                  <AccordionItem
                    key={layerData.layerName}
                    value={layerData.layerName}
                  >
                    <AccordionTrigger className="text-left">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold">
                          {layerData.layerName}
                        </span>
                        <span className="text-xs text-gray-500">
                          {(layerData.data as { features?: unknown[] })
                            ?.features?.length
                            ? `${(layerData.data as { features: unknown[] }).features.length} features`
                            : 'Data available'}
                        </span>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent>
                      <div className="space-y-4">
                        <div className="bg-gray-50 rounded-lg p-4">
                          <pre className="text-sm overflow-auto max-h-96 whitespace-pre-wrap">
                            {JSON.stringify(layerData.data, null, 2)}
                          </pre>
                        </div>
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Info size={48} className="mx-auto mb-4 text-gray-300" />
                <p>{tMap('info.dialog.noData')}</p>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>

      {/* Upload Dialog */}
      <Dialog
        open={state.showUploadDialog}
        onOpenChange={open =>
          dispatch({
            type: 'SET_SHOW_UPLOAD_DIALOG',
            payload: open,
          })
        }
      >
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              {state.uploadStep === 'disclaimer' && (
                <>
                  <CloudUpload size={20} />
                  {tMap('upload.dialog.title')}
                </>
              )}
              {state.uploadStep === 'file-selection' && (
                <>
                  <Upload size={20} />
                  {tMap('upload.dialog.selectFile')}
                </>
              )}
            </DialogTitle>
          </DialogHeader>

          {state.uploadStep === 'disclaimer' && (
            <>
              <div className="py-6">
                <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                  {tMap('upload.dialog.disclaimer')}
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-200">
                <Button
                  onClick={() =>
                    dispatch({
                      type: 'SET_SHOW_UPLOAD_DIALOG',
                      payload: false,
                    })
                  }
                  variant="destructive"
                  className="flex-1"
                >
                  {tMap('upload.dialog.cancel')}
                </Button>
                <Button
                  onClick={() => {
                    dispatch({
                      type: 'SET_UPLOAD_STEP',
                      payload: 'file-selection',
                    });
                  }}
                  variant="primary"
                  className="flex-1"
                >
                  {tMap('upload.dialog.continue')}
                </Button>
              </div>
            </>
          )}

          {state.uploadStep === 'file-selection' && (
            <>
              <div className="py-6 space-y-6">
                {state.uploadError && (
                  <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                    <div className="flex items-center gap-2">
                      <CircleX size={16} className="text-red-600" />
                      <p className="text-sm font-medium text-red-800">
                        {tMap('upload.dialog.error')}
                      </p>
                    </div>
                    <p className="text-sm text-red-700 mt-1">
                      {state.uploadError}
                    </p>
                  </div>
                )}

                <div
                  className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer"
                  onClick={() => {
                    console.warn(
                      'Drop zone clicked, processing:',
                      state.uploadProcessing
                    );
                    if (!state.uploadProcessing) {
                      const fileInput = document.getElementById(
                        'file-upload'
                      ) as HTMLInputElement;
                      console.warn('File input element:', fileInput);
                      fileInput?.click();
                    }
                  }}
                >
                  <input
                    type="file"
                    id="file-upload"
                    className="hidden"
                    accept=".kml,.kmz,.geojson,.json,.shp,.zip"
                    onChange={e => {
                      const file = e.target.files?.[0];
                      console.warn('File selected:', file?.name);
                      if (file) {
                        setSelectedFile(file);
                        dispatch({ type: 'SET_UPLOAD_ERROR', payload: null });
                      }
                    }}
                    disabled={state.uploadProcessing}
                  />
                  <div
                    className={cn(
                      'flex flex-col items-center gap-4',
                      state.uploadProcessing && 'opacity-50'
                    )}
                  >
                    <CloudUpload size={48} className="text-gray-400" />
                    <div>
                      <p className="text-lg font-medium text-gray-700">
                        {state.uploadProcessing
                          ? tMap('upload.dialog.processing')
                          : tMap('upload.dialog.dropZone.title')}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        {tMap('upload.dialog.dropZone.subtitle')}
                      </p>
                    </div>
                    <div
                      className={cn(
                        'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2',
                        state.uploadProcessing &&
                          'opacity-50 cursor-not-allowed'
                      )}
                    >
                      {tMap('upload.dialog.selectFile')}
                    </div>
                  </div>
                </div>

                {selectedFile && (
                  <div className="flex items-center gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <svg
                        className="w-4 h-4 text-green-600"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">
                        {selectedFile.name}
                      </p>
                      <p className="text-sm text-gray-500">
                        {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => setSelectedFile(null)}
                    >
                      <CircleX size={16} />
                    </Button>
                  </div>
                )}

                <div className="text-sm text-gray-600">
                  <p className="font-medium mb-2">
                    {tMap('upload.dialog.supportedFormats')}:
                  </p>
                  <ul className="list-disc list-inside space-y-1 text-gray-500">
                    <li>KML/KMZ files</li>
                    <li>GeoJSON files</li>
                    <li>Shapefile (ZIP)</li>
                  </ul>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-200">
                <Button
                  onClick={() =>
                    dispatch({
                      type: 'SET_UPLOAD_STEP',
                      payload: 'disclaimer',
                    })
                  }
                  variant="outline"
                  className="flex-1"
                >
                  <ArrowLeft size={16} className="mr-2" />
                  {tMap('upload.dialog.back')}
                </Button>
                <Button
                  onClick={async () => {
                    if (selectedFile) {
                      await handleFileUpload(selectedFile);
                    }
                  }}
                  variant="primary"
                  className="flex-1"
                  disabled={!selectedFile || state.uploadProcessing}
                >
                  {state.uploadProcessing
                    ? tMap('upload.dialog.processing')
                    : tMap('upload.dialog.upload')}
                </Button>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </main>
  );
}
