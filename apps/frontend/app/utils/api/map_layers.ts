import { requestAPI } from './base';
import {
  MapLayersSchema,
  type MapLayerCreate,
  type MapLayerUpdate,
} from '@root/app/schemas/map-layers';

export async function getMapLayers({ municipality }: { municipality: number }) {
  return requestAPI({
    endpoint: 'v1/map_layers',
    data: {
      municipality,
    },
  }).then(response => {
    const result = MapLayersSchema.safeParse(response);

    if (result.success) {
      const sortedLayers: typeof result.data = [];

      result.data.forEach((layer, idx) => {
        let inserted = false;

        for (let i = 0; i < sortedLayers.length; i++) {
          if (layer.order < sortedLayers[i].order) {
            sortedLayers.splice(i, 0, layer);
            inserted = true;
            break;
          }
        }

        if (!inserted) {
          sortedLayers.push(layer);
        }
      });

      return sortedLayers;
    } else {
      return undefined;
    }
  });
}

export async function createMapLayer(data: MapLayerCreate) {
  return requestAPI({
    endpoint: 'v1/map_layers/',
    method: 'POST',
    data,
  });
}

export async function updateMapLayer(id: number, data: MapLayerUpdate) {
  return requestAPI({
    endpoint: `v1/map_layers/${id}`,
    method: 'PATCH',
    data,
  });
}
