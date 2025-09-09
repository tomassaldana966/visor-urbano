# 🗺️ Guía de Migración: De GeoServer a ArcGIS

## Tabla de Contenidos

- [Introducción](#introducción)
- [Arquitectura Actual de GeoServer](#arquitectura-actual-de-geoserver)
- [Arquitectura Objetivo de ArcGIS](#arquitectura-objetivo-de-arcgis)
- [Estrategia de Migración](#estrategia-de-migración)
- [Fase 1: Configuración y Preparación](#fase-1-configuración-y-preparación)
- [Fase 2: Migración de Datos](#fase-2-migración-de-datos)
- [Fase 3: Migración de Servicios](#fase-3-migración-de-servicios)
- [Fase 4: Actualizaciones de la Aplicación](#fase-4-actualizaciones-de-la-aplicación)
- [Fase 5: Pruebas y Validación](#fase-5-pruebas-y-validación)
- [Fase 6: Despliegue y Monitoreo](#fase-6-despliegue-y-monitoreo)
- [Análisis de Costos](#análisis-de-costos)
- [Beneficios y Desafíos](#beneficios-y-desafíos)
- [Mejores Prácticas](#mejores-prácticas)
- [Solución de Problemas](#solución-de-problemas)

## Introducción

Esta guía proporciona una hoja de ruta integral para migrar la plataforma Visor Urbano de GeoServer a ArcGIS Online/ArcGIS Enterprise. La migración aprovechará los potentes servicios geoespaciales basados en la nube de Esri, manteniendo la funcionalidad existente y mejorando el rendimiento del sistema.

### Requisitos Previos

- Licencia de ArcGIS Online o ArcGIS Enterprise
- Acceso a la instancia actual de GeoServer
- Acceso administrativo al código base de Visor Urbano
- Acceso a la base de datos PostGIS
- Conocimientos básicos de servicios REST de ArcGIS

### Beneficios Clave de la Migración

- **Rendimiento Mejorado**: ArcGIS proporciona servicios de mapas optimizados con mejor caché
- **Análisis Avanzado**: Herramientas de análisis espacial y servicios de geoprocesamiento integrados
- **Escalabilidad**: Arquitectura nativa en la nube con escalado automático
- **Integración Empresarial**: Mejor integración con sistemas empresariales
- **Soporte Móvil**: Aplicaciones móviles nativas y mapas web responsivos
- **Seguridad**: Seguridad y autenticación de nivel empresarial

## Arquitectura Actual de GeoServer

### Componentes de GeoServer en Visor Urbano

El sistema actual utiliza GeoServer para:

1. **Servicios WMS** - Generación de tiles de mapas y estilizado
2. **Servicios WFS** - Consultas de datos vectoriales y acceso a características
3. **Gestión de Capas** - Organización de capas de datos geográficos
4. **Consultas Espaciales** - Filtros CQL para filtrado de datos

### Flujo de Datos Actual

```
Base de Datos PostGIS → GeoServer → Frontend OpenLayers
```

### Endpoints Clave de GeoServer Utilizados

- **WMS GetMap**: `{GEOSERVER_URL}/ows?service=WMS&request=GetMap`
- **WFS GetFeature**: `{GEOSERVER_URL}/ows?service=WFS&request=GetFeature`
- **WMS GetFeatureInfo**: Para consultas de información de características

### Capas de Mapas Actualmente Gestionadas

- Límites municipales
- Capas de zonificación (primaria y secundaria)
- Redes viales
- Huellas de edificios
- Capas de infraestructura
- Datos censales
- Zonas de gestión de riesgos

## Arquitectura Objetivo de ArcGIS

### Componentes de ArcGIS

1. **ArcGIS Online/Enterprise**
   - Alojamiento de servicios de mapas
   - Servicios de características
   - Mapas web y aplicaciones

2. **Servicios REST de ArcGIS**
   - Servicio de Mapas: Para visualización de mapas
   - Servicio de Características: Para consultas y edición de datos
   - Servicio de Geoprocesamiento: Para análisis espacial

3. **API de ArcGIS para JavaScript**
   - API de mapeo web moderno
   - Alternativa a OpenLayers (opcional)

### Flujo de Datos Objetivo

```
Base de Datos PostGIS → ArcGIS Enterprise → Servicios REST de ArcGIS → Frontend
```

### Estructura de URLs de Servicios

- **Servicio de Mapas**: `https://services.arcgis.com/{orgId}/arcgis/rest/services/{serviceName}/MapServer`
- **Servicio de Características**: `https://services.arcgis.com/{orgId}/arcgis/rest/services/{serviceName}/FeatureServer`

## Estrategia de Migración

### Enfoque de Migración: Implementación por Fases

1. **Configuración del Sistema Paralelo** (Semanas 1-2)
2. **Migración de Datos** (Semanas 3-4)
3. **Migración de Servicios** (Semanas 5-6)
4. **Actualizaciones de la Aplicación** (Semanas 7-8)
5. **Pruebas y Validación** (Semanas 9-10)
6. **Despliegue y Monitoreo** (Semanas 11-12)

### Mitigación de Riesgos

- Mantener GeoServer como respaldo durante la transición
- Implementar banderas de características para cambio de servicios
- Migración gradual capa por capa
- Pruebas exhaustivas en cada fase

## Fase 1: Configuración y Preparación

### Paso 1.1: Configuración del Entorno ArcGIS

1. **Obtener Licencia de ArcGIS**

   ```
   Opciones:
   - ArcGIS Online (SaaS)
   - ArcGIS Enterprise (Local/Nube)
   ```

2. **Crear Organización ArcGIS**
   - Configurar cuenta organizacional
   - Configurar roles y permisos de usuario
   - Establecer convenciones de nomenclatura

3. **Instalar ArcGIS Pro** (si se usa Enterprise)
   - Descargar desde el Portal del Cliente de Esri
   - Configurar conexiones de base de datos
   - Configurar permisos de publicación

### Paso 1.2: Evaluación de la Base de Datos

1. **Analizar Datos PostGIS Actuales**

   ```sql
   -- Verificar sistemas de referencia espacial
   SELECT DISTINCT ST_SRID(geom) as srid,
          COUNT(*) as layer_count
   FROM information_schema.columns c
   JOIN pg_tables t ON c.table_name = t.tablename
   WHERE c.data_type = 'USER-DEFINED'
   AND c.udt_name = 'geometry'
   GROUP BY ST_SRID(geom);

   -- Evaluar calidad de datos
   SELECT schemaname, tablename,
          ST_GeometryType(geom) as geom_type,
          COUNT(*) as feature_count
   FROM pg_tables pt
   JOIN information_schema.columns c ON pt.tablename = c.table_name
   WHERE c.udt_name = 'geometry'
   GROUP BY schemaname, tablename, ST_GeometryType(geom);
   ```

2. **Evaluación de Calidad de Datos**
   - Verificar validez de geometrías
   - Validar sistemas de referencia espacial
   - Identificar relaciones de datos

### Paso 1.3: Configuración del Entorno

1. **Actualizar Variables de Entorno**

   ```env
   # Adiciones al .env del backend
   ARCGIS_SERVER_URL=https://tu-org.maps.arcgis.com
   ARCGIS_USERNAME=tu_usuario
   ARCGIS_PASSWORD=tu_contraseña
   ARCGIS_TOKEN_URL=https://tu-org.maps.arcgis.com/sharing/rest/generateToken
   ARCGIS_CLIENT_ID=tu_client_id
   ARCGIS_CLIENT_SECRET=tu_client_secret

   # Bandera de característica para cambio de servicios
   USE_ARCGIS_SERVICES=false
   ```

2. **Configuración del Frontend**
   ```env
   # Adiciones al .env del frontend
   VITE_ARCGIS_API_KEY=tu_api_key
   VITE_ARCGIS_SERVICES_URL=https://services.arcgis.com/tu-org-id/arcgis/rest/services
   VITE_USE_ARCGIS=false
   ```

## Fase 2: Migración de Datos

### Paso 2.1: Exportar Datos desde PostGIS

1. **Crear Scripts de Exportación de Datos**

   ```python
   # apps/backend/scripts/export_gis_data.py
   import geopandas as gpd
   from sqlalchemy import create_engine
   import os

   def export_layer_to_shapefile(table_name, output_dir):
       """Exportar tabla PostGIS a Shapefile"""
       engine = create_engine(os.getenv('DATABASE_URL'))

       # Leer datos espaciales
       gdf = gpd.read_postgis(
           f"SELECT * FROM {table_name}",
           engine,
           geom_col='geom'
       )

       # Exportar a shapefile
       output_path = f"{output_dir}/{table_name}.shp"
       gdf.to_file(output_path)
       print(f"Exportado {table_name} a {output_path}")

   # Exportar todas las capas de mapas
   LAYERS_TO_EXPORT = [
       'chih_zonif_primaria2023_corregida',
       'zon_secundaria_dissolve_utmz13n',
       'chih_estructura_vial2023_corregida',
       'predio_urbano',
       'chih_limite_municipal',
       # Agregar todas las capas actuales
   ]

   for layer in LAYERS_TO_EXPORT:
       export_layer_to_shapefile(layer, './exports')
   ```

2. **Exportar a Múltiples Formatos**
   ```python
   # Soporte para varios formatos
   def export_layer_multiple_formats(table_name, output_dir):
       gdf = gpd.read_postgis(f"SELECT * FROM {table_name}", engine, geom_col='geom')

       # Shapefile
       gdf.to_file(f"{output_dir}/{table_name}.shp")

       # GeoJSON
       gdf.to_file(f"{output_dir}/{table_name}.geojson", driver='GeoJSON')

       # File Geodatabase
       gdf.to_file(f"{output_dir}/{table_name}.gdb", driver='FileGDB')
   ```

### Paso 2.2: Preparar Datos para ArcGIS

1. **Validación y Limpieza de Datos**

   ```python
   def validate_and_clean_geometries(gdf):
       """Validar y limpiar geometrías para compatibilidad con ArcGIS"""
       # Verificar geometrías válidas
       invalid_geoms = ~gdf.geometry.is_valid
       if invalid_geoms.any():
           print(f"Se encontraron {invalid_geoms.sum()} geometrías inválidas")
           # Arreglar geometrías inválidas
           gdf.loc[invalid_geoms, 'geometry'] = gdf.loc[invalid_geoms, 'geometry'].buffer(0)

       # Asegurar CRS correcto
       if gdf.crs != 'EPSG:4326':
           gdf = gdf.to_crs('EPSG:4326')

       return gdf
   ```

2. **Preparación de Metadatos**
   ```python
   def create_metadata_file(layer_name, gdf):
       """Crear archivo de metadatos para importación a ArcGIS"""
       metadata = {
           'name': layer_name,
           'feature_count': len(gdf),
           'geometry_type': gdf.geometry.type.iloc[0],
           'crs': str(gdf.crs),
           'extent': gdf.total_bounds.tolist(),
           'fields': list(gdf.columns)
       }

       with open(f'./exports/{layer_name}_metadata.json', 'w') as f:
           json.dump(metadata, f, indent=2)
   ```

### Paso 2.3: Subir Datos a ArcGIS

1. **Usando API de ArcGIS para Python**

   ```python
   # Instalar: pip install arcgis
   from arcgis.gis import GIS
   from arcgis.features import FeatureLayerCollection

   def upload_to_arcgis_online(shapefile_path, layer_name):
       """Subir shapefile a ArcGIS Online"""
       # Conectar a ArcGIS Online
       gis = GIS("https://arcgis.com", username, password)

       # Subir shapefile
       shp_item = gis.content.add({
           'title': layer_name,
           'tags': 'visor-urbano, municipal, gis',
           'type': 'Shapefile'
       }, data=shapefile_path)

       # Publicar como servicio de características
       feature_service = shp_item.publish()

       print(f"Publicado {layer_name} como servicio de características: {feature_service.url}")
       return feature_service
   ```

2. **Script de Subida por Lotes**
   ```python
   def batch_upload_layers():
       """Subir todas las capas exportadas a ArcGIS"""
       gis = GIS("https://arcgis.com", username, password)

       uploaded_services = {}

       for layer in LAYERS_TO_EXPORT:
           try:
               service = upload_to_arcgis_online(
                   f'./exports/{layer}.shp',
                   f'VisorUrbano_{layer}'
               )
               uploaded_services[layer] = service.url
           except Exception as e:
               print(f"Falló la subida de {layer}: {e}")

       # Guardar URLs de servicios para configuración de aplicación
       with open('./exports/arcgis_service_urls.json', 'w') as f:
           json.dump(uploaded_services, f, indent=2)
   ```

## Fase 3: Migración de Servicios

### Paso 3.1: Crear Wrapper de Servicios ArcGIS

1. **Cliente de Servicios ArcGIS**

   ```python
   # apps/backend/app/services/arcgis_service.py
   import requests
   import json
   from typing import Dict, List, Optional
   from config.settings import get_settings

   class ArcGISService:
       def __init__(self):
           self.settings = get_settings()
           self.base_url = self.settings.ARCGIS_SERVER_URL
           self.token = self._get_token()

       def _get_token(self) -> str:
           """Generar token de acceso de ArcGIS"""
           token_url = f"{self.base_url}/sharing/rest/generateToken"

           params = {
               'username': self.settings.ARCGIS_USERNAME,
               'password': self.settings.ARCGIS_PASSWORD,
               'referer': self.settings.APP_URL,
               'f': 'json'
           }

           response = requests.post(token_url, data=params)
           result = response.json()

           if 'token' in result:
               return result['token']
           else:
               raise Exception(f"Falló la obtención del token: {result}")

       def query_features(self, service_url: str, where: str = "1=1",
                         geometry: Optional[str] = None,
                         spatial_rel: str = "esriSpatialRelIntersects") -> Dict:
           """Consultar características del Servicio de Características de ArcGIS"""
           query_url = f"{service_url}/query"

           params = {
               'where': where,
               'outFields': '*',
               'f': 'json',
               'token': self.token,
               'returnGeometry': 'true'
           }

           if geometry:
               params['geometry'] = geometry
               params['spatialRel'] = spatial_rel

           response = requests.get(query_url, params=params)
           return response.json()

       def get_map_image(self, service_url: str, bbox: str, size: str = "400,400") -> bytes:
           """Obtener imagen de mapa del Servicio de Mapas de ArcGIS"""
           export_url = f"{service_url}/export"

           params = {
               'bbox': bbox,
               'bboxSR': '4326',
               'imageSR': '4326',
               'size': size,
               'format': 'png',
               'f': 'image',
               'token': self.token
           }

           response = requests.get(export_url, params=params)
           return response.content
   ```

2. **Descubrimiento y Configuración de Servicios**
   ```python
   def discover_arcgis_services():
       """Descubrir servicios ArcGIS disponibles y crear configuración"""
       arcgis = ArcGISService()

       # Obtener todos los servicios
       services_url = f"{arcgis.base_url}/rest/services"
       response = requests.get(f"{services_url}?f=json&token={arcgis.token}")
       services_info = response.json()

       service_config = {}

       for service in services_info.get('services', []):
           service_name = service['name']
           service_type = service['type']

           if 'VisorUrbano' in service_name:
               service_config[service_name] = {
                   'url': f"{services_url}/{service_name}/{service_type}",
                   'type': service_type,
                   'capabilities': service.get('capabilities', [])
               }

       return service_config
   ```

### Paso 3.2: Actualizar Servicios del Backend

1. **Crear Capa de Abstracción de Servicios**

   ```python
   # apps/backend/app/services/map_service.py
   from abc import ABC, abstractmethod
   from .geoserver_service import GeoServerService
   from .arcgis_service import ArcGISService

   class MapServiceInterface(ABC):
       @abstractmethod
       def query_features(self, layer: str, filters: Dict) -> Dict:
           pass

       @abstractmethod
       def get_map_image(self, layers: List[str], bbox: str) -> bytes:
           pass

   class MapServiceFactory:
       @staticmethod
       def create_service() -> MapServiceInterface:
           if get_settings().USE_ARCGIS_SERVICES:
               return ArcGISMapService()
           else:
               return GeoServerMapService()
   ```

2. **Actualizar Router de Capas de Mapas**

   ```python
   # apps/backend/app/routers/map_layers.py - adiciones

   @router.get("/services/config")
   async def get_service_configuration():
       """Obtener configuración actual del servicio de mapas"""
       if get_settings().USE_ARCGIS_SERVICES:
           arcgis_service = ArcGISService()
           return {
               'provider': 'arcgis',
               'services': discover_arcgis_services(),
               'base_url': arcgis_service.base_url
           }
       else:
           return {
               'provider': 'geoserver',
               'base_url': get_settings().GEOSERVER_URL
           }

   @router.post("/migrate/layer/{layer_id}")
   async def migrate_layer_to_arcgis(layer_id: int, db: AsyncSession = Depends(get_db)):
       """Migrar capa específica de GeoServer a ArcGIS"""
       # Implementación para migración de capa individual
       pass
   ```

### Paso 3.3: Actualizar Esquema de Base de Datos

1. **Agregar Campos de ArcGIS al Modelo MapLayer**

   ```python
   # apps/backend/app/models/map_layers.py - adiciones

   class MapLayer(Base):
       # ... campos existentes ...

       # Campos específicos de ArcGIS
       arcgis_service_url = Column(String(500), nullable=True)
       arcgis_layer_id = Column(Integer, nullable=True)
       arcgis_service_type = Column(String(50), nullable=True)  # MapServer, FeatureServer
       service_provider = Column(String(20), default='geoserver')  # geoserver, arcgis
   ```

2. **Crear Script de Migración**

   ```python
   # apps/backend/migrations/versions/add_arcgis_fields.py
   """Agregar campos de ArcGIS a map_layers

   Revision ID: add_arcgis_fields
   Revises: previous_revision
   Create Date: 2024-xx-xx
   """

   def upgrade():
       op.add_column('map_layers', sa.Column('arcgis_service_url', sa.String(500), nullable=True))
       op.add_column('map_layers', sa.Column('arcgis_layer_id', sa.Integer, nullable=True))
       op.add_column('map_layers', sa.Column('arcgis_service_type', sa.String(50), nullable=True))
       op.add_column('map_layers', sa.Column('service_provider', sa.String(20), default='geoserver'))
   ```

## Fase 4: Actualizaciones de la Aplicación

### Paso 4.1: Actualizaciones de la Capa de Servicios del Frontend

1. **Crear Cliente de API de ArcGIS**

   ```typescript
   // apps/frontend/app/utils/arcgis/arcgis-client.ts

   export interface ArcGISFeatureQuery {
     where?: string;
     geometry?: string;
     spatialRel?: string;
     outFields?: string;
     returnGeometry?: boolean;
   }

   export class ArcGISClient {
     private baseUrl: string;
     private token?: string;

     constructor(baseUrl: string, token?: string) {
       this.baseUrl = baseUrl;
       this.token = token;
     }

     async queryFeatures(serviceUrl: string, query: ArcGISFeatureQuery = {}) {
       const params = new URLSearchParams({
         where: query.where || '1=1',
         outFields: query.outFields || '*',
         returnGeometry: String(query.returnGeometry ?? true),
         f: 'json',
         ...(this.token && { token: this.token }),
       });

       if (query.geometry) {
         params.append('geometry', query.geometry);
         params.append(
           'spatialRel',
           query.spatialRel || 'esriSpatialRelIntersects'
         );
       }

       const response = await fetch(`${serviceUrl}/query?${params}`);

       if (!response.ok) {
         throw new Error(`Falló la consulta de ArcGIS: ${response.statusText}`);
       }

       return response.json();
     }

     async exportMap(serviceUrl: string, bbox: string, size = '400,400') {
       const params = new URLSearchParams({
         bbox,
         bboxSR: '4326',
         imageSR: '4326',
         size,
         format: 'png',
         f: 'image',
         ...(this.token && { token: this.token }),
       });

       const response = await fetch(`${serviceUrl}/export?${params}`);

       if (!response.ok) {
         throw new Error(
           `Falló la exportación de mapa de ArcGIS: ${response.statusText}`
         );
       }

       return response.blob();
     }
   }
   ```

2. **Actualizar Utilidades de Mapas**

   ```typescript
   // apps/frontend/app/utils/map/arcgis-service.ts
   import { ArcGISClient } from '../arcgis/arcgis-client';

   export async function fetchArcGISFeatures(params: {
     serviceUrl: string;
     where?: string;
     geometry?: string;
     spatialRel?: string;
   }) {
     const client = new ArcGISClient(
       import.meta.env.VITE_ARCGIS_SERVICES_URL,
       import.meta.env.VITE_ARCGIS_API_KEY
     );

     return client.queryFeatures(params.serviceUrl, {
       where: params.where,
       geometry: params.geometry,
       spatialRel: params.spatialRel,
     });
   }

   // Convertir respuesta de ArcGIS a GeoJSON
   export function arcgisToGeoJSON(arcgisResponse: any) {
     if (!arcgisResponse.features) {
       return { type: 'FeatureCollection', features: [] };
     }

     const features = arcgisResponse.features.map((feature: any) => ({
       type: 'Feature',
       geometry: feature.geometry,
       properties: feature.attributes,
     }));

     return {
       type: 'FeatureCollection',
       features,
     };
   }
   ```

### Paso 4.2: Actualizar Integración con OpenLayers

1. **Crear Fuente de Capa ArcGIS**

   ```typescript
   // apps/frontend/app/components/OpenLayerMap/sources/ArcGISSource.ts
   import TileLayer from 'ol/layer/Tile';
   import XYZ from 'ol/source/XYZ';
   import VectorLayer from 'ol/layer/Vector';
   import VectorSource from 'ol/source/Vector';
   import GeoJSON from 'ol/format/GeoJSON';
   import {
     fetchArcGISFeatures,
     arcgisToGeoJSON,
   } from '@root/app/utils/map/arcgis-service';

   export function createArcGISTileLayer(serviceUrl: string, layerId?: number) {
     const tileUrl = layerId
       ? `${serviceUrl}/tile/{z}/{y}/{x}`
       : `${serviceUrl}/MapServer/tile/{z}/{y}/{x}`;

     return new TileLayer({
       source: new XYZ({
         url: tileUrl,
         attributions: 'Esri, ArcGIS',
       }),
     });
   }

   export async function createArcGISVectorLayer(
     serviceUrl: string,
     query?: { where?: string; geometry?: string }
   ) {
     try {
       const response = await fetchArcGISFeatures({
         serviceUrl,
         ...query,
       });

       const geoJSON = arcgisToGeoJSON(response);

       const vectorSource = new VectorSource({
         features: new GeoJSON().readFeatures(geoJSON, {
           featureProjection: 'EPSG:3857',
           dataProjection: 'EPSG:4326',
         }),
       });

       return new VectorLayer({
         source: vectorSource,
       });
     } catch (error) {
       console.error('Falló la creación de capa vectorial de ArcGIS:', error);
       return null;
     }
   }
   ```

2. **Actualizar Componente OpenLayerMap**

   ```typescript
   // apps/frontend/app/components/OpenLayerMap/OpenLayerMap.tsx - adiciones

   import {
     createArcGISTileLayer,
     createArcGISVectorLayer,
   } from './sources/ArcGISSource';

   // Agregar al componente existente
   const createLayerFromConfig = async (layer: MapLayer) => {
     if (layer.service_provider === 'arcgis') {
       if (layer.type === 'TILE' || layer.type === 'WMS') {
         return createArcGISTileLayer(
           layer.arcgis_service_url!,
           layer.arcgis_layer_id
         );
       } else if (layer.type === 'WFS' || layer.type === 'FEATURE') {
         return await createArcGISVectorLayer(layer.arcgis_service_url!);
       }
     } else {
       // Lógica existente de GeoServer
       return new TileLayer({
         source: new TileWMS({
           url: layer.url,
           params: {
             LAYERS: layer.layers,
             // ... parámetros existentes
           },
         }),
       });
     }
   };
   ```

### Paso 4.3: Actualizar Gestión de Capas de Mapas

1. **Actualizar Esquema de Capa de Mapas**

   ```typescript
   // apps/frontend/app/schemas/map-layers.ts - adiciones

   export const MapLayerSchema = z.object({
     // ... campos existentes ...
     arcgis_service_url: z.string().nullable(),
     arcgis_layer_id: z.number().nullable(),
     arcgis_service_type: z.enum(['MapServer', 'FeatureServer']).nullable(),
     service_provider: z.enum(['geoserver', 'arcgis']).default('geoserver'),
   });
   ```

2. **Actualizar UI de Gestión de Capas**

   ```typescript
   // apps/frontend/app/routes/director/municipal-layers.tsx - adiciones

   const ServiceProviderSelector = () => (
     <Select name="service_provider" label="Proveedor de Servicios">
       <Option value="geoserver">GeoServer</Option>
       <Option value="arcgis">ArcGIS</Option>
     </Select>
   );

   const ArcGISServiceFields = ({ isVisible }: { isVisible: boolean }) => (
     <div className={clsx('grid gap-4', { hidden: !isVisible })}>
       <Input
         name="arcgis_service_url"
         label="URL del Servicio ArcGIS"
         placeholder="https://services.arcgis.com/..."
       />
       <Input
         name="arcgis_layer_id"
         type="number"
         label="ID de Capa"
         placeholder="0"
       />
       <Select name="arcgis_service_type" label="Tipo de Servicio">
         <Option value="MapServer">Servidor de Mapas</Option>
         <Option value="FeatureServer">Servidor de Características</Option>
       </Select>
     </div>
   );
   ```

## Fase 5: Pruebas y Validación

### Paso 5.1: Pruebas Unitarias

1. **Pruebas de Servicios del Backend**

   ```python
   # apps/backend/tests/test_arcgis_service.py
   import pytest
   from unittest.mock import patch, Mock
   from app.services.arcgis_service import ArcGISService

   class TestArcGISService:
       @pytest.fixture
       def arcgis_service(self):
           with patch('app.services.arcgis_service.get_settings') as mock_settings:
               mock_settings.return_value.ARCGIS_SERVER_URL = 'https://test.arcgis.com'
               mock_settings.return_value.ARCGIS_USERNAME = 'test_user'
               mock_settings.return_value.ARCGIS_PASSWORD = 'test_pass'

               service = ArcGISService()
               service.token = 'test_token'
               return service

       @patch('requests.get')
       def test_query_features(self, mock_get, arcgis_service):
           # Mock respuesta exitosa
           mock_response = Mock()
           mock_response.json.return_value = {
               'features': [
                   {
                       'geometry': {'x': -100, 'y': 40},
                       'attributes': {'name': 'Característica de Prueba'}
                   }
               ]
           }
           mock_get.return_value = mock_response

           result = arcgis_service.query_features(
               'https://test.arcgis.com/rest/services/TestService/FeatureServer/0'
           )

           assert 'features' in result
           assert len(result['features']) == 1
   ```

2. **Pruebas de Servicios del Frontend**

   ```typescript
   // apps/frontend/app/utils/arcgis/arcgis-client.test.ts
   import { describe, it, expect, vi } from 'vitest';
   import { ArcGISClient } from './arcgis-client';

   // Mock fetch
   global.fetch = vi.fn();

   describe('ArcGISClient', () => {
     it('debería consultar características exitosamente', async () => {
       const mockResponse = {
         features: [
           {
             geometry: { x: -100, y: 40 },
             attributes: { name: 'Característica de Prueba' },
           },
         ],
       };

       (fetch as any).mockResolvedValueOnce({
         ok: true,
         json: async () => mockResponse,
       });

       const client = new ArcGISClient('https://test.arcgis.com', 'test_token');
       const result = await client.queryFeatures(
         'https://test.arcgis.com/FeatureServer/0'
       );

       expect(result).toEqual(mockResponse);
     });

     it('debería manejar errores de consulta', async () => {
       (fetch as any).mockResolvedValueOnce({
         ok: false,
         statusText: 'No Encontrado',
       });

       const client = new ArcGISClient('https://test.arcgis.com');

       await expect(
         client.queryFeatures('https://test.arcgis.com/FeatureServer/0')
       ).rejects.toThrow('Falló la consulta de ArcGIS: No Encontrado');
     });
   });
   ```

### Paso 5.2: Pruebas de Integración

1. **Pruebas de Migración de Capas End-to-End**

   ```python
   # apps/backend/tests/test_layer_migration.py

   @pytest.mark.integration
   class TestLayerMigration:
       async def test_full_layer_migration_workflow(self):
           """Probar flujo completo de migración de capas de GeoServer a ArcGIS"""
           # 1. Exportar desde PostGIS
           # 2. Subir a ArcGIS
           # 3. Actualizar configuración de base de datos
           # 4. Verificar funcionalidad de capa
           pass

       async def test_service_switching(self):
           """Probar cambio entre servicios GeoServer y ArcGIS"""
           # Probar funcionalidad de bandera de característica
           pass
   ```

2. **Pruebas de Integración del Frontend**

   ```typescript
   // apps/e2e/tests/arcgis-migration.spec.ts
   import { test, expect } from '@playwright/test';

   test.describe('Migración ArcGIS', () => {
     test('debería mostrar mapa con capas ArcGIS', async ({ page }) => {
       // Habilitar servicios ArcGIS
       await page.goto('/director/settings');
       await page.check('#use-arcgis-services');
       await page.click('button[type="submit"]');

       // Navegar al mapa
       await page.goto('/map');

       // Verificar que el mapa se carga
       await expect(page.locator('.ol-viewport')).toBeVisible();

       // Verificar que las capas están cargadas
       await expect(page.locator('[data-testid="layer-list"]')).toContainText(
         'ArcGIS'
       );
     });

     test('debería consultar características del servicio ArcGIS', async ({
       page,
     }) => {
       await page.goto('/map');

       // Hacer clic en el mapa para activar consulta de características
       await page.locator('.ol-viewport').click();

       // Verificar que se muestra información de características
       await expect(page.locator('[data-testid="feature-info"]')).toBeVisible();
     });
   });
   ```

### Paso 5.3: Pruebas de Rendimiento

1. **Script de Pruebas de Carga**

   ```python
   # scripts/performance_test.py
   import asyncio
   import aiohttp
   import time
   from statistics import mean, median

   async def test_service_performance():
       """Comparar rendimiento GeoServer vs ArcGIS"""

       # Configuraciones de prueba
       geoserver_url = "https://datahub.mpiochih.gob.mx/ows"
       arcgis_url = "https://services.arcgis.com/tu-org/arcgis/rest/services"

       test_queries = [
           {"service": "WFS", "typename": "predio_urbano", "count": 100},
           {"service": "WMS", "layers": "chih_zonif_primaria2023_corregida"},
       ]

       results = {}

       async with aiohttp.ClientSession() as session:
           # Probar GeoServer
           geoserver_times = []
           for _ in range(10):
               start_time = time.time()
               # Hacer solicitud a GeoServer
               end_time = time.time()
               geoserver_times.append(end_time - start_time)

           # Probar ArcGIS
           arcgis_times = []
           for _ in range(10):
               start_time = time.time()
               # Hacer solicitud a ArcGIS
               end_time = time.time()
               arcgis_times.append(end_time - start_time)

       results['geoserver'] = {
           'promedio': mean(geoserver_times),
           'mediana': median(geoserver_times),
           'min': min(geoserver_times),
           'max': max(geoserver_times)
       }

       results['arcgis'] = {
           'promedio': mean(arcgis_times),
           'mediana': median(arcgis_times),
           'min': min(arcgis_times),
           'max': max(arcgis_times)
       }

       return results
   ```

## Fase 6: Despliegue y Monitoreo

### Paso 6.1: Estrategia de Despliegue

1. **Implementación de Banderas de Características**

   ```python
   # apps/backend/app/core/feature_flags.py
   from enum import Enum
   from config.settings import get_settings

   class FeatureFlag(Enum):
       USE_ARCGIS_SERVICES = "use_arcgis_services"
       ARCGIS_LAYER_MIGRATION = "arcgis_layer_migration"
       PARALLEL_SERVICE_TESTING = "parallel_service_testing"

   def is_feature_enabled(flag: FeatureFlag) -> bool:
       settings = get_settings()
       return getattr(settings, flag.value.upper(), False)

   def get_map_service():
       if is_feature_enabled(FeatureFlag.USE_ARCGIS_SERVICES):
           return ArcGISService()
       return GeoServerService()
   ```

2. **Plan de Despliegue Gradual**
   ```yaml
   # deployment/rollout-plan.yml
   phases:
     - name: 'Pruebas Internas'
       duration: '1 semana'
       percentage: 0
       features:
         - parallel_service_testing

     - name: 'Usuarios Limitados'
       duration: '1 semana'
       percentage: 10
       features:
         - use_arcgis_services
         - arcgis_layer_migration

     - name: 'Pruebas Expandidas'
       duration: '2 semanas'
       percentage: 50
       features:
         - use_arcgis_services

     - name: 'Despliegue Completo'
       duration: 'continuo'
       percentage: 100
       features:
         - use_arcgis_services
   ```

### Paso 6.2: Monitoreo y Logging

1. **Monitoreo de Salud de Servicios**

   ```python
   # apps/backend/app/monitoring/service_health.py
   import asyncio
   import logging
   from typing import Dict, Any
   from app.services.arcgis_service import ArcGISService
   from app.services.geoserver_service import GeoServerService

   logger = logging.getLogger(__name__)

   class ServiceHealthMonitor:
       def __init__(self):
           self.arcgis_service = ArcGISService()
           self.geoserver_service = GeoServerService()

       async def check_service_health(self) -> Dict[str, Any]:
           """Verificar salud de servicios GeoServer y ArcGIS"""
           results = {
               'timestamp': datetime.utcnow().isoformat(),
               'services': {}
           }

           # Verificar ArcGIS
           try:
               start_time = time.time()
               token = self.arcgis_service._get_token()
               response_time = time.time() - start_time

               results['services']['arcgis'] = {
                   'status': 'saludable',
                   'response_time': response_time,
                   'token_valid': bool(token)
               }
           except Exception as e:
               results['services']['arcgis'] = {
                   'status': 'no_saludable',
                   'error': str(e)
               }
               logger.error(f"Falló verificación de salud del servicio ArcGIS: {e}")

           # Verificar GeoServer
           try:
               start_time = time.time()
               # Hacer solicitud simple WMS GetCapabilities
               response_time = time.time() - start_time

               results['services']['geoserver'] = {
                   'status': 'saludable',
                   'response_time': response_time
               }
           except Exception as e:
               results['services']['geoserver'] = {
                   'status': 'no_saludable',
                   'error': str(e)
               }
               logger.error(f"Falló verificación de salud del servicio GeoServer: {e}")

           return results

   # Endpoint de verificación de salud
   @router.get("/health/services")
   async def get_services_health():
       monitor = ServiceHealthMonitor()
       return await monitor.check_service_health()
   ```

2. **Recolección de Métricas de Rendimiento**

   ```python
   # apps/backend/app/monitoring/metrics.py
   import time
   from functools import wraps
   from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

   # Métricas
   SERVICE_REQUESTS = Counter(
       'map_service_requests_total',
       'Total de solicitudes de servicio de mapas',
       ['service_type', 'operation', 'status']
   )

   SERVICE_DURATION = Histogram(
       'map_service_duration_seconds',
       'Duración de solicitud de servicio de mapas',
       ['service_type', 'operation']
   )

   def track_service_metrics(service_type: str, operation: str):
       def decorator(func):
           @wraps(func)
           async def wrapper(*args, **kwargs):
               start_time = time.time()
               status = 'success'

               try:
                   result = await func(*args, **kwargs)
                   return result
               except Exception as e:
                   status = 'error'
                   raise
               finally:
                   duration = time.time() - start_time
                   SERVICE_REQUESTS.labels(
                       service_type=service_type,
                       operation=operation,
                       status=status
                   ).inc()
                   SERVICE_DURATION.labels(
                       service_type=service_type,
                       operation=operation
                   ).observe(duration)

           return wrapper
       return decorator

   @router.get("/metrics")
   async def get_metrics():
       return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
   ```

### Paso 6.3: Estrategia de Rollback

1. **Activadores de Rollback Automático**

   ```python
   # apps/backend/app/monitoring/rollback.py
   class AutoRollbackMonitor:
       def __init__(self):
           self.error_threshold = 0.1  # 10% tasa de error
           self.response_time_threshold = 5.0  # 5 segundos

       async def check_rollback_conditions(self, metrics: Dict) -> bool:
           """Verificar si se debe activar rollback automático"""
           arcgis_metrics = metrics.get('services', {}).get('arcgis', {})

           # Verificar tasa de error
           if arcgis_metrics.get('error_rate', 0) > self.error_threshold:
               logger.warning("Tasa de error de ArcGIS excedió el umbral, activando rollback")
               return True

           # Verificar tiempo de respuesta
           if arcgis_metrics.get('avg_response_time', 0) > self.response_time_threshold:
               logger.warning("Tiempo de respuesta de ArcGIS excedió el umbral, activando rollback")
               return True

           return False

       async def execute_rollback(self):
           """Ejecutar rollback automático a GeoServer"""
           # Deshabilitar servicios ArcGIS
           os.environ['USE_ARCGIS_SERVICES'] = 'false'

           # Limpiar caché de aplicación
           # Notificar administradores

           logger.info("Rollback automático a GeoServer completado")
   ```

2. **Procedimiento de Rollback Manual**

   ```bash
   #!/bin/bash
   # scripts/rollback_to_geoserver.sh

   echo "Iniciando rollback a GeoServer..."

   # 1. Actualizar variables de entorno
   export USE_ARCGIS_SERVICES=false

   # 2. Actualizar banderas de características en base de datos
   psql $DATABASE_URL -c "UPDATE system_settings SET value = 'false' WHERE key = 'use_arcgis_services';"

   # 3. Reiniciar servicios de aplicación
   docker-compose restart backend
   docker-compose restart frontend

   # 4. Verificar servicios
   curl -f http://localhost:8000/health || exit 1
   curl -f http://localhost:5173 || exit 1

   echo "Rollback completado exitosamente"
   ```

## Análisis de Costos

### Costos de Licenciamiento

1. **ArcGIS Online**
   - **Licencia Creator**: $7,000/año por usuario
   - **Licencia Professional**: $8,000/año por usuario
   - **Créditos de Servicio**: Variable basado en uso
   - **Almacenamiento Adicional**: $1,000/año por 1TB

2. **ArcGIS Enterprise**
   - **Licencia Base**: $10,000+/año
   - **Extensiones**: $2,000-$5,000/año cada una
   - **Infraestructura**: Costos de alojamiento en la nube

3. **Desarrollo y Migración**
   - **Tiempo de Desarrollo**: 8-12 semanas
   - **Entrenamiento**: $5,000-$10,000
   - **Pruebas y QA**: 2-4 semanas

### Cálculo de ROI

**Beneficios:**

- Reducción en mantenimiento de infraestructura
- Mejor rendimiento y escalabilidad
- Capacidades de análisis avanzado
- Mejor soporte móvil
- Seguridad de nivel empresarial

**Punto de equilibrio**: Típicamente 18-24 meses para organizaciones con 10+ usuarios

## Beneficios y Desafíos

### Beneficios

1. **Mejoras de Rendimiento**
   - Servicio de tiles optimizado con CDN
   - Mejores mecanismos de caché
   - Reducción de carga del servidor

2. **Capacidades Avanzadas**
   - Herramientas de análisis espacial integradas
   - Transmisión de datos en tiempo real
   - Servicios optimizados para móviles
   - Soporte para visualización 3D

3. **Características Empresariales**
   - Integración de inicio de sesión único
   - Controles de seguridad avanzados
   - Certificaciones de cumplimiento
   - Soporte 24/7

4. **Escalabilidad**
   - Escalado automático
   - Disponibilidad global
   - Balanceado de carga

### Desafíos

1. **Dependencia del Proveedor**
   - Dependencia del ecosistema Esri
   - Complejidad de migración para cambios futuros

2. **Costos de Licenciamiento**
   - Tarifas de suscripción continuas
   - Consumo de créditos de servicio

3. **Curva de Aprendizaje**
   - Nuevas APIs y flujos de trabajo
   - Requisitos de entrenamiento del personal

4. **Control de Datos**
   - Almacenamiento de datos basado en la nube
   - Opciones de personalización limitadas

## Mejores Prácticas

### Gestión de Datos

1. **Preparación de Datos**
   - Validar geometrías antes de subir
   - Estandarizar esquemas de atributos
   - Optimizar tamaños de archivo
   - Documentar metadatos

2. **Configuración de Servicios**
   - Usar tipos de servicio apropiados (Map vs Feature)
   - Configurar ajustes de caché
   - Establecer seguridad adecuada
   - Monitorear patrones de uso

3. **Optimización de Rendimiento**
   - Usar servicios de tiles para mapas base
   - Implementar filtros de servicio de características
   - Cachear datos accedidos frecuentemente
   - Optimizar geometrías de consulta

### Seguridad

1. **Autenticación**

   ```python
   # Implementar OAuth 2.0 para servicios ArcGIS
   class ArcGISOAuthClient:
       def __init__(self, client_id: str, client_secret: str):
           self.client_id = client_id
           self.client_secret = client_secret

       async def get_access_token(self) -> str:
           # Implementar flujo OAuth
           pass
   ```

2. **Control de Acceso**
   - Implementar acceso basado en roles
   - Usar permisos a nivel de servicio
   - Monitorear logs de acceso
   - Auditorías de seguridad regulares

### Monitoreo

1. **Monitoreo de Servicios**
   - Seguimiento de tiempo de respuesta
   - Monitoreo de tasa de error
   - Análisis de uso
   - Dashboards de rendimiento

2. **Monitoreo de Costos**
   - Uso de créditos de servicio
   - Consumo de almacenamiento
   - Seguimiento de volumen de solicitudes
   - Reportes de costos mensuales

## Solución de Problemas

### Problemas Comunes

1. **Fallas de Autenticación**

   ```python
   # Depurar generación de token
   def debug_token_generation():
       try:
           token = arcgis_service._get_token()
           print(f"Token generado exitosamente: {token[:10]}...")
       except Exception as e:
           print(f"Falló la generación de token: {e}")
           # Verificar credenciales, conectividad de red
   ```

2. **Problemas de Descubrimiento de Servicios**

   ```python
   # Verificar disponibilidad de servicio
   async def verify_service_availability(service_url: str):
       try:
           response = await fetch(f"{service_url}?f=json")
           if response.status == 200:
               print("Servicio está disponible")
           else:
               print(f"Servicio devolvió estado: {response.status}")
       except Exception as e:
           print(f"Falló verificación de servicio: {e}")
   ```

3. **Problemas de Proyección de Datos**
   ```python
   # Manejar transformaciones de sistema de coordenadas
   def transform_coordinates(geom, source_crs, target_crs):
       import pyproj
       transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)
       # Transformar coordenadas de geometría
   ```

### Problemas de Rendimiento

1. **Respuesta Lenta de Consultas**
   - Verificar balance de créditos de servicio
   - Verificar índices espaciales
   - Optimizar filtros de consulta
   - Considerar caché de datos

2. **Alto Uso de Memoria**
   - Implementar paginación para conjuntos de datos grandes
   - Usar streaming para exportación de datos
   - Optimizar simplificación de geometría

### Recursos de Soporte

1. **Documentación de Esri**
   - Referencia de API REST de ArcGIS
   - Guías de mejores prácticas
   - Guías de optimización de rendimiento

2. **Recursos de Comunidad**
   - Foros de la Comunidad Esri
   - Stack Overflow
   - Repositorios de GitHub

3. **Recursos de Entrenamiento**
   - Cursos de entrenamiento Esri
   - Tutoriales en línea
   - Programas de certificación

---

## Conclusión

Esta guía de migración proporciona una hoja de ruta integral para la transición de GeoServer a ArcGIS manteniendo la funcionalidad del sistema y mejorando el rendimiento. El enfoque por fases minimiza los riesgos y asegura una transición suave.

### Factores Clave de Éxito

1. **Planificación Exhaustiva**: Entender la arquitectura actual del sistema y los requisitos
2. **Migración Gradual**: Implementar cambios incrementalmente con pruebas apropiadas
3. **Monitoreo**: Monitorear continuamente el rendimiento y la experiencia del usuario
4. **Entrenamiento**: Asegurar que el equipo esté apropiadamente entrenado en las nuevas tecnologías
5. **Documentación**: Mantener documentación integral durante todo el proceso
