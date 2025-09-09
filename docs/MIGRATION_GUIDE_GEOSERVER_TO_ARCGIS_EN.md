# 🗺️ Migration Guide: From GeoServer to ArcGIS

## Table of Contents

- [Introduction](#introduction)
- [Current GeoServer Architecture](#current-geoserver-architecture)
- [ArcGIS Target Architecture](#arcgis-target-architecture)
- [Migration Strategy](#migration-strategy)
- [Phase 1: Setup and Preparation](#phase-1-setup-and-preparation)
- [Phase 2: Data Migration](#phase-2-data-migration)
- [Phase 3: Service Migration](#phase-3-service-migration)
- [Phase 4: Application Updates](#phase-4-application-updates)
- [Phase 5: Testing and Validation](#phase-5-testing-and-validation)
- [Phase 6: Deployment and Monitoring](#phase-6-deployment-and-monitoring)
- [Cost Analysis](#cost-analysis)
- [Benefits and Challenges](#benefits-and-challenges)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Introduction

This guide provides a comprehensive roadmap for migrating the Visor Urbano platform from GeoServer to ArcGIS Online/ArcGIS Enterprise. The migration will leverage Esri's powerful cloud-based geospatial services while maintaining the existing functionality and improving system performance.

### Prerequisites

- ArcGIS Online or ArcGIS Enterprise license
- Access to existing GeoServer instance
- Administrative access to Visor Urbano codebase
- PostGIS database access
- Basic knowledge of ArcGIS REST Services

### Key Benefits of Migration

- **Enhanced Performance**: ArcGIS provides optimized map services with better caching
- **Advanced Analytics**: Built-in spatial analysis tools and geoprocessing services
- **Scalability**: Cloud-native architecture with automatic scaling
- **Enterprise Integration**: Better integration with enterprise systems
- **Mobile Support**: Native mobile applications and responsive web maps
- **Security**: Enterprise-grade security and authentication

## Current GeoServer Architecture

### GeoServer Components in Visor Urbano

The current system uses GeoServer for:

1. **WMS Services** - Map tile generation and styling
2. **WFS Services** - Vector data queries and feature access
3. **Layer Management** - Geographic data layer organization
4. **Spatial Queries** - CQL filters for data filtering

### Current Data Flow

```
PostGIS Database → GeoServer → OpenLayers Frontend
```

### Key GeoServer Endpoints Used

- **WMS GetMap**: `{GEOSERVER_URL}/ows?service=WMS&request=GetMap`
- **WFS GetFeature**: `{GEOSERVER_URL}/ows?service=WFS&request=GetFeature`
- **WMS GetFeatureInfo**: For feature information queries

### Map Layers Currently Managed

- Municipal boundaries
- Zoning layers (primary and secondary)
- Street networks
- Building footprints
- Infrastructure layers
- Census data
- Risk management zones

## ArcGIS Target Architecture

### ArcGIS Components

1. **ArcGIS Online/Enterprise**
   - Map services hosting
   - Feature services
   - Web maps and applications

2. **ArcGIS REST Services**
   - Map Service: For map visualization
   - Feature Service: For data queries and editing
   - Geoprocessing Service: For spatial analysis

3. **ArcGIS API for JavaScript**
   - Modern web mapping API
   - Alternative to OpenLayers (optional)

### Target Data Flow

```
PostGIS Database → ArcGIS Enterprise → ArcGIS REST Services → Frontend
```

### Service URLs Structure

- **Map Service**: `https://services.arcgis.com/{orgId}/arcgis/rest/services/{serviceName}/MapServer`
- **Feature Service**: `https://services.arcgis.com/{orgId}/arcgis/rest/services/{serviceName}/FeatureServer`

## Migration Strategy

### Migration Approach: Phased Implementation

1. **Parallel System Setup** (Weeks 1-2)
2. **Data Migration** (Weeks 3-4)
3. **Service Migration** (Weeks 5-6)
4. **Application Updates** (Weeks 7-8)
5. **Testing & Validation** (Weeks 9-10)
6. **Deployment & Monitoring** (Weeks 11-12)

### Risk Mitigation

- Maintain GeoServer as fallback during transition
- Implement feature flags for service switching
- Gradual layer-by-layer migration
- Comprehensive testing at each phase

## Phase 1: Setup and Preparation

### Step 1.1: ArcGIS Environment Setup

1. **Obtain ArcGIS License**

   ```
   Options:
   - ArcGIS Online (SaaS)
   - ArcGIS Enterprise (On-premises/Cloud)
   ```

2. **Create ArcGIS Organization**
   - Set up organizational account
   - Configure user roles and permissions
   - Establish naming conventions

3. **Install ArcGIS Pro** (if using Enterprise)
   - Download from Esri Customer Portal
   - Configure database connections
   - Set up publishing permissions

### Step 1.2: Database Assessment

1. **Analyze Current PostGIS Data**

   ```sql
   -- Check spatial reference systems
   SELECT DISTINCT ST_SRID(geom) as srid,
          COUNT(*) as layer_count
   FROM information_schema.columns c
   JOIN pg_tables t ON c.table_name = t.tablename
   WHERE c.data_type = 'USER-DEFINED'
   AND c.udt_name = 'geometry'
   GROUP BY ST_SRID(geom);

   -- Assess data quality
   SELECT schemaname, tablename,
          ST_GeometryType(geom) as geom_type,
          COUNT(*) as feature_count
   FROM pg_tables pt
   JOIN information_schema.columns c ON pt.tablename = c.table_name
   WHERE c.udt_name = 'geometry'
   GROUP BY schemaname, tablename, ST_GeometryType(geom);
   ```

2. **Data Quality Assessment**
   - Check for geometry validity
   - Validate spatial reference systems
   - Identify data relationships

### Step 1.3: Environment Configuration

1. **Update Environment Variables**

   ```env
   # Backend .env additions
   ARCGIS_SERVER_URL=https://your-org.maps.arcgis.com
   ARCGIS_USERNAME=your_username
   ARCGIS_PASSWORD=your_password
   ARCGIS_TOKEN_URL=https://your-org.maps.arcgis.com/sharing/rest/generateToken
   ARCGIS_CLIENT_ID=your_client_id
   ARCGIS_CLIENT_SECRET=your_client_secret

   # Feature flag for service switching
   USE_ARCGIS_SERVICES=false
   ```

2. **Frontend Configuration**
   ```env
   # Frontend .env additions
   VITE_ARCGIS_API_KEY=your_api_key
   VITE_ARCGIS_SERVICES_URL=https://services.arcgis.com/your-org-id/arcgis/rest/services
   VITE_USE_ARCGIS=false
   ```

## Phase 2: Data Migration

### Step 2.1: Export Data from PostGIS

1. **Create Data Export Scripts**

   ```python
   # apps/backend/scripts/export_gis_data.py
   import geopandas as gpd
   from sqlalchemy import create_engine
   import os

   def export_layer_to_shapefile(table_name, output_dir):
       """Export PostGIS table to Shapefile"""
       engine = create_engine(os.getenv('DATABASE_URL'))

       # Read spatial data
       gdf = gpd.read_postgis(
           f"SELECT * FROM {table_name}",
           engine,
           geom_col='geom'
       )

       # Export to shapefile
       output_path = f"{output_dir}/{table_name}.shp"
       gdf.to_file(output_path)
       print(f"Exported {table_name} to {output_path}")

   # Export all map layers
   LAYERS_TO_EXPORT = [
       'chih_zonif_primaria2023_corregida',
       'zon_secundaria_dissolve_utmz13n',
       'chih_estructura_vial2023_corregida',
       'predio_urbano',
       'chih_limite_municipal',
       # Add all current layers
   ]

   for layer in LAYERS_TO_EXPORT:
       export_layer_to_shapefile(layer, './exports')
   ```

2. **Export to Multiple Formats**
   ```python
   # Support for various formats
   def export_layer_multiple_formats(table_name, output_dir):
       gdf = gpd.read_postgis(f"SELECT * FROM {table_name}", engine, geom_col='geom')

       # Shapefile
       gdf.to_file(f"{output_dir}/{table_name}.shp")

       # GeoJSON
       gdf.to_file(f"{output_dir}/{table_name}.geojson", driver='GeoJSON')

       # File Geodatabase
       gdf.to_file(f"{output_dir}/{table_name}.gdb", driver='FileGDB')
   ```

### Step 2.2: Prepare Data for ArcGIS

1. **Data Validation and Cleaning**

   ```python
   def validate_and_clean_geometries(gdf):
       """Validate and clean geometries for ArcGIS compatibility"""
       # Check for valid geometries
       invalid_geoms = ~gdf.geometry.is_valid
       if invalid_geoms.any():
           print(f"Found {invalid_geoms.sum()} invalid geometries")
           # Fix invalid geometries
           gdf.loc[invalid_geoms, 'geometry'] = gdf.loc[invalid_geoms, 'geometry'].buffer(0)

       # Ensure correct CRS
       if gdf.crs != 'EPSG:4326':
           gdf = gdf.to_crs('EPSG:4326')

       return gdf
   ```

2. **Metadata Preparation**
   ```python
   def create_metadata_file(layer_name, gdf):
       """Create metadata file for ArcGIS import"""
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

### Step 2.3: Upload Data to ArcGIS

1. **Using ArcGIS API for Python**

   ```python
   # Install: pip install arcgis
   from arcgis.gis import GIS
   from arcgis.features import FeatureLayerCollection

   def upload_to_arcgis_online(shapefile_path, layer_name):
       """Upload shapefile to ArcGIS Online"""
       # Connect to ArcGIS Online
       gis = GIS("https://arcgis.com", username, password)

       # Upload shapefile
       shp_item = gis.content.add({
           'title': layer_name,
           'tags': 'visor-urbano, municipal, gis',
           'type': 'Shapefile'
       }, data=shapefile_path)

       # Publish as feature service
       feature_service = shp_item.publish()

       print(f"Published {layer_name} as feature service: {feature_service.url}")
       return feature_service
   ```

2. **Batch Upload Script**
   ```python
   def batch_upload_layers():
       """Upload all exported layers to ArcGIS"""
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
               print(f"Failed to upload {layer}: {e}")

       # Save service URLs for application configuration
       with open('./exports/arcgis_service_urls.json', 'w') as f:
           json.dump(uploaded_services, f, indent=2)
   ```

## Phase 3: Service Migration

### Step 3.1: Create ArcGIS Service Wrapper

1. **ArcGIS Service Client**

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
           """Generate ArcGIS access token"""
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
               raise Exception(f"Failed to get token: {result}")

       def query_features(self, service_url: str, where: str = "1=1",
                         geometry: Optional[str] = None,
                         spatial_rel: str = "esriSpatialRelIntersects") -> Dict:
           """Query features from ArcGIS Feature Service"""
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
           """Get map image from ArcGIS Map Service"""
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

2. **Service Discovery and Configuration**
   ```python
   def discover_arcgis_services():
       """Discover available ArcGIS services and create configuration"""
       arcgis = ArcGISService()

       # Get all services
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

### Step 3.2: Update Backend Services

1. **Create Service Abstraction Layer**

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

2. **Update Map Layer Router**

   ```python
   # apps/backend/app/routers/map_layers.py - additions

   @router.get("/services/config")
   async def get_service_configuration():
       """Get current map service configuration"""
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
       """Migrate specific layer from GeoServer to ArcGIS"""
       # Implementation for individual layer migration
       pass
   ```

### Step 3.3: Update Database Schema

1. **Add ArcGIS Fields to MapLayer Model**

   ```python
   # apps/backend/app/models/map_layers.py - additions

   class MapLayer(Base):
       # ... existing fields ...

       # ArcGIS specific fields
       arcgis_service_url = Column(String(500), nullable=True)
       arcgis_layer_id = Column(Integer, nullable=True)
       arcgis_service_type = Column(String(50), nullable=True)  # MapServer, FeatureServer
       service_provider = Column(String(20), default='geoserver')  # geoserver, arcgis
   ```

2. **Create Migration Script**

   ```python
   # apps/backend/migrations/versions/add_arcgis_fields.py
   """Add ArcGIS fields to map_layers

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

## Phase 4: Application Updates

### Step 4.1: Frontend Service Layer Updates

1. **Create ArcGIS API Client**

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
         throw new Error(`ArcGIS query failed: ${response.statusText}`);
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
         throw new Error(`ArcGIS map export failed: ${response.statusText}`);
       }

       return response.blob();
     }
   }
   ```

2. **Update Map Utilities**

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

   // Convert ArcGIS response to GeoJSON
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

### Step 4.2: Update OpenLayers Integration

1. **Create ArcGIS Layer Source**

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
       console.error('Failed to create ArcGIS vector layer:', error);
       return null;
     }
   }
   ```

2. **Update OpenLayerMap Component**

   ```typescript
   // apps/frontend/app/components/OpenLayerMap/OpenLayerMap.tsx - additions

   import {
     createArcGISTileLayer,
     createArcGISVectorLayer,
   } from './sources/ArcGISSource';

   // Add to existing component
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
       // Existing GeoServer logic
       return new TileLayer({
         source: new TileWMS({
           url: layer.url,
           params: {
             LAYERS: layer.layers,
             // ... existing params
           },
         }),
       });
     }
   };
   ```

### Step 4.3: Update Map Layer Management

1. **Update Map Layer Schema**

   ```typescript
   // apps/frontend/app/schemas/map-layers.ts - additions

   export const MapLayerSchema = z.object({
     // ... existing fields ...
     arcgis_service_url: z.string().nullable(),
     arcgis_layer_id: z.number().nullable(),
     arcgis_service_type: z.enum(['MapServer', 'FeatureServer']).nullable(),
     service_provider: z.enum(['geoserver', 'arcgis']).default('geoserver'),
   });
   ```

2. **Update Layer Management UI**

   ```typescript
   // apps/frontend/app/routes/director/municipal-layers.tsx - additions

   const ServiceProviderSelector = () => (
     <Select name="service_provider" label="Service Provider">
       <Option value="geoserver">GeoServer</Option>
       <Option value="arcgis">ArcGIS</Option>
     </Select>
   );

   const ArcGISServiceFields = ({ isVisible }: { isVisible: boolean }) => (
     <div className={clsx('grid gap-4', { hidden: !isVisible })}>
       <Input
         name="arcgis_service_url"
         label="ArcGIS Service URL"
         placeholder="https://services.arcgis.com/..."
       />
       <Input
         name="arcgis_layer_id"
         type="number"
         label="Layer ID"
         placeholder="0"
       />
       <Select name="arcgis_service_type" label="Service Type">
         <Option value="MapServer">Map Server</Option>
         <Option value="FeatureServer">Feature Server</Option>
       </Select>
     </div>
   );
   ```

## Phase 5: Testing and Validation

### Step 5.1: Unit Testing

1. **Backend Service Tests**

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
           # Mock successful response
           mock_response = Mock()
           mock_response.json.return_value = {
               'features': [
                   {
                       'geometry': {'x': -100, 'y': 40},
                       'attributes': {'name': 'Test Feature'}
                   }
               ]
           }
           mock_get.return_value = mock_response

           result = arcgis_service.query_features(
               'https://test.arcgis.com/rest/services/TestService/FeatureServer/0'
           )

           assert 'features' in result
           assert len(result['features']) == 1

       @patch('requests.get')
       def test_get_map_image(self, mock_get, arcgis_service):
           mock_get.return_value.content = b'fake_image_data'

           result = arcgis_service.get_map_image(
               'https://test.arcgis.com/rest/services/TestService/MapServer',
               '-180,-90,180,90'
           )

           assert result == b'fake_image_data'
   ```

2. **Frontend Service Tests**

   ```typescript
   // apps/frontend/app/utils/arcgis/arcgis-client.test.ts
   import { describe, it, expect, vi } from 'vitest';
   import { ArcGISClient } from './arcgis-client';

   // Mock fetch
   global.fetch = vi.fn();

   describe('ArcGISClient', () => {
     it('should query features successfully', async () => {
       const mockResponse = {
         features: [
           {
             geometry: { x: -100, y: 40 },
             attributes: { name: 'Test Feature' },
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

     it('should handle query errors', async () => {
       (fetch as any).mockResolvedValueOnce({
         ok: false,
         statusText: 'Not Found',
       });

       const client = new ArcGISClient('https://test.arcgis.com');

       await expect(
         client.queryFeatures('https://test.arcgis.com/FeatureServer/0')
       ).rejects.toThrow('ArcGIS query failed: Not Found');
     });
   });
   ```

### Step 5.2: Integration Testing

1. **End-to-End Layer Testing**

   ```python
   # apps/backend/tests/test_layer_migration.py

   @pytest.mark.integration
   class TestLayerMigration:
       async def test_full_layer_migration_workflow(self):
           """Test complete layer migration from GeoServer to ArcGIS"""
           # 1. Export from PostGIS
           # 2. Upload to ArcGIS
           # 3. Update database configuration
           # 4. Verify layer functionality
           pass

       async def test_service_switching(self):
           """Test switching between GeoServer and ArcGIS services"""
           # Test feature flag functionality
           pass
   ```

2. **Frontend Integration Tests**

   ```typescript
   // apps/e2e/tests/arcgis-migration.spec.ts
   import { test, expect } from '@playwright/test';

   test.describe('ArcGIS Migration', () => {
     test('should display map with ArcGIS layers', async ({ page }) => {
       // Enable ArcGIS services
       await page.goto('/director/settings');
       await page.check('#use-arcgis-services');
       await page.click('button[type="submit"]');

       // Navigate to map
       await page.goto('/map');

       // Verify map loads
       await expect(page.locator('.ol-viewport')).toBeVisible();

       // Verify layers are loaded
       await expect(page.locator('[data-testid="layer-list"]')).toContainText(
         'ArcGIS'
       );
     });

     test('should query features from ArcGIS service', async ({ page }) => {
       await page.goto('/map');

       // Click on map to trigger feature query
       await page.locator('.ol-viewport').click();

       // Verify feature info displayed
       await expect(page.locator('[data-testid="feature-info"]')).toBeVisible();
     });
   });
   ```

### Step 5.3: Performance Testing

1. **Load Testing Script**

   ```python
   # scripts/performance_test.py
   import asyncio
   import aiohttp
   import time
   from statistics import mean, median

   async def test_service_performance():
       """Compare GeoServer vs ArcGIS performance"""

       # Test configurations
       geoserver_url = "https://datahub.mpiochih.gob.mx/ows"
       arcgis_url = "https://services.arcgis.com/your-org/arcgis/rest/services"

       test_queries = [
           {"service": "WFS", "typename": "predio_urbano", "count": 100},
           {"service": "WMS", "layers": "chih_zonif_primaria2023_corregida"},
       ]

       results = {}

       async with aiohttp.ClientSession() as session:
           # Test GeoServer
           geoserver_times = []
           for _ in range(10):
               start_time = time.time()
               # Make GeoServer request
               end_time = time.time()
               geoserver_times.append(end_time - start_time)

           # Test ArcGIS
           arcgis_times = []
           for _ in range(10):
               start_time = time.time()
               # Make ArcGIS request
               end_time = time.time()
               arcgis_times.append(end_time - start_time)

       results['geoserver'] = {
           'mean': mean(geoserver_times),
           'median': median(geoserver_times),
           'min': min(geoserver_times),
           'max': max(geoserver_times)
       }

       results['arcgis'] = {
           'mean': mean(arcgis_times),
           'median': median(arcgis_times),
           'min': min(arcgis_times),
           'max': max(arcgis_times)
       }

       return results
   ```

## Phase 6: Deployment and Monitoring

### Step 6.1: Deployment Strategy

1. **Feature Flag Implementation**

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

2. **Gradual Rollout Plan**
   ```yaml
   # deployment/rollout-plan.yml
   phases:
     - name: 'Internal Testing'
       duration: '1 week'
       percentage: 0
       features:
         - parallel_service_testing

     - name: 'Limited Users'
       duration: '1 week'
       percentage: 10
       features:
         - use_arcgis_services
         - arcgis_layer_migration

     - name: 'Expanded Testing'
       duration: '2 weeks'
       percentage: 50
       features:
         - use_arcgis_services

     - name: 'Full Deployment'
       duration: 'ongoing'
       percentage: 100
       features:
         - use_arcgis_services
   ```

### Step 6.2: Monitoring and Logging

1. **Service Health Monitoring**

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
           """Check health of both GeoServer and ArcGIS services"""
           results = {
               'timestamp': datetime.utcnow().isoformat(),
               'services': {}
           }

           # Check ArcGIS
           try:
               start_time = time.time()
               token = self.arcgis_service._get_token()
               response_time = time.time() - start_time

               results['services']['arcgis'] = {
                   'status': 'healthy',
                   'response_time': response_time,
                   'token_valid': bool(token)
               }
           except Exception as e:
               results['services']['arcgis'] = {
                   'status': 'unhealthy',
                   'error': str(e)
               }
               logger.error(f"ArcGIS service health check failed: {e}")

           # Check GeoServer
           try:
               start_time = time.time()
               # Make simple WMS GetCapabilities request
               response_time = time.time() - start_time

               results['services']['geoserver'] = {
                   'status': 'healthy',
                   'response_time': response_time
               }
           except Exception as e:
               results['services']['geoserver'] = {
                   'status': 'unhealthy',
                   'error': str(e)
               }
               logger.error(f"GeoServer service health check failed: {e}")

           return results

   # Health check endpoint
   @router.get("/health/services")
   async def get_services_health():
       monitor = ServiceHealthMonitor()
       return await monitor.check_service_health()
   ```

2. **Performance Metrics Collection**

   ```python
   # apps/backend/app/monitoring/metrics.py
   import time
   from functools import wraps
   from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

   # Metrics
   SERVICE_REQUESTS = Counter(
       'map_service_requests_total',
       'Total map service requests',
       ['service_type', 'operation', 'status']
   )

   SERVICE_DURATION = Histogram(
       'map_service_duration_seconds',
       'Map service request duration',
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

### Step 6.3: Rollback Strategy

1. **Automatic Rollback Triggers**

   ```python
   # apps/backend/app/monitoring/rollback.py
   class AutoRollbackMonitor:
       def __init__(self):
           self.error_threshold = 0.1  # 10% error rate
           self.response_time_threshold = 5.0  # 5 seconds

       async def check_rollback_conditions(self, metrics: Dict) -> bool:
           """Check if automatic rollback should be triggered"""
           arcgis_metrics = metrics.get('services', {}).get('arcgis', {})

           # Check error rate
           if arcgis_metrics.get('error_rate', 0) > self.error_threshold:
               logger.warning("ArcGIS error rate exceeded threshold, triggering rollback")
               return True

           # Check response time
           if arcgis_metrics.get('avg_response_time', 0) > self.response_time_threshold:
               logger.warning("ArcGIS response time exceeded threshold, triggering rollback")
               return True

           return False

       async def execute_rollback(self):
           """Execute automatic rollback to GeoServer"""
           # Disable ArcGIS services
           os.environ['USE_ARCGIS_SERVICES'] = 'false'

           # Clear application cache
           # Notify administrators

           logger.info("Automatic rollback to GeoServer completed")
   ```

2. **Manual Rollback Procedure**

   ```bash
   #!/bin/bash
   # scripts/rollback_to_geoserver.sh

   echo "Starting rollback to GeoServer..."

   # 1. Update environment variables
   export USE_ARCGIS_SERVICES=false

   # 2. Update database feature flags
   psql $DATABASE_URL -c "UPDATE system_settings SET value = 'false' WHERE key = 'use_arcgis_services';"

   # 3. Restart application services
   docker-compose restart backend
   docker-compose restart frontend

   # 4. Verify services
   curl -f http://localhost:8000/health || exit 1
   curl -f http://localhost:5173 || exit 1

   echo "Rollback completed successfully"
   ```

## Cost Analysis

### Licensing Costs

1. **ArcGIS Online**
   - **Creator License**: $7,000/year per user
   - **Professional License**: $8,000/year per user
   - **Service Credits**: Variable based on usage
   - **Additional Storage**: $1,000/year per 1TB

2. **ArcGIS Enterprise**
   - **Base License**: $10,000+/year
   - **Extensions**: $2,000-$5,000/year each
   - **Infrastructure**: Cloud hosting costs

3. **Development and Migration**
   - **Development Time**: 8-12 weeks
   - **Training**: $5,000-$10,000
   - **Testing and QA**: 2-4 weeks

### ROI Calculation

**Benefits:**

- Reduced infrastructure maintenance
- Improved performance and scalability
- Advanced analytics capabilities
- Better mobile support
- Enterprise-grade security

**Break-even**: Typically 18-24 months for organizations with 10+ users

## Benefits and Challenges

### Benefits

1. **Performance Improvements**
   - Optimized tile serving with CDN
   - Better caching mechanisms
   - Reduced server load

2. **Advanced Capabilities**
   - Built-in spatial analysis tools
   - Real-time data streaming
   - Mobile-optimized services
   - 3D visualization support

3. **Enterprise Features**
   - Single sign-on integration
   - Advanced security controls
   - Compliance certifications
   - 24/7 support

4. **Scalability**
   - Automatic scaling
   - Global availability
   - Load balancing

### Challenges

1. **Vendor Lock-in**
   - Dependence on Esri ecosystem
   - Migration complexity for future changes

2. **Licensing Costs**
   - Ongoing subscription fees
   - Service credit consumption

3. **Learning Curve**
   - New APIs and workflows
   - Staff training requirements

4. **Data Control**
   - Cloud-based data storage
   - Limited customization options

## Best Practices

### Data Management

1. **Data Preparation**
   - Validate geometries before upload
   - Standardize attribute schemas
   - Optimize file sizes
   - Document metadata

2. **Service Configuration**
   - Use appropriate service types (Map vs Feature)
   - Configure caching settings
   - Set up proper security
   - Monitor usage patterns

3. **Performance Optimization**
   - Use tiled services for base maps
   - Implement feature service filters
   - Cache frequently accessed data
   - Optimize query geometries

### Security

1. **Authentication**

   ```python
   # Implement OAuth 2.0 for ArcGIS services
   class ArcGISOAuthClient:
       def __init__(self, client_id: str, client_secret: str):
           self.client_id = client_id
           self.client_secret = client_secret

       async def get_access_token(self) -> str:
           # Implement OAuth flow
           pass
   ```

2. **Access Control**
   - Implement role-based access
   - Use service-level permissions
   - Monitor access logs
   - Regular security audits

### Monitoring

1. **Service Monitoring**
   - Response time tracking
   - Error rate monitoring
   - Usage analytics
   - Performance dashboards

2. **Cost Monitoring**
   - Service credit usage
   - Storage consumption
   - Request volume tracking
   - Monthly cost reports

## Troubleshooting

### Common Issues

1. **Authentication Failures**

   ```python
   # Debug token generation
   def debug_token_generation():
       try:
           token = arcgis_service._get_token()
           print(f"Token generated successfully: {token[:10]}...")
       except Exception as e:
           print(f"Token generation failed: {e}")
           # Check credentials, network connectivity
   ```

2. **Service Discovery Issues**

   ```python
   # Verify service availability
   async def verify_service_availability(service_url: str):
       try:
           response = await fetch(f"{service_url}?f=json")
           if response.status == 200:
               print("Service is available")
           else:
               print(f"Service returned status: {response.status}")
       except Exception as e:
           print(f"Service check failed: {e}")
   ```

3. **Data Projection Issues**
   ```python
   # Handle coordinate system transformations
   def transform_coordinates(geom, source_crs, target_crs):
       import pyproj
       transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)
       # Transform geometry coordinates
   ```

### Performance Issues

1. **Slow Query Response**
   - Check service credit balance
   - Verify spatial indexes
   - Optimize query filters
   - Consider data caching

2. **High Memory Usage**
   - Implement pagination for large datasets
   - Use streaming for data export
   - Optimize geometry simplification

### Support Resources

1. **Esri Documentation**
   - ArcGIS REST API reference
   - Best practices guides
   - Performance tuning guides

2. **Community Resources**
   - Esri Community forums
   - Stack Overflow
   - GitHub repositories

3. **Training Resources**
   - Esri training courses
   - Online tutorials
   - Certification programs

---

## Conclusion

This migration guide provides a comprehensive roadmap for transitioning from GeoServer to ArcGIS while maintaining system functionality and improving performance. The phased approach minimizes risks and ensures a smooth transition.
