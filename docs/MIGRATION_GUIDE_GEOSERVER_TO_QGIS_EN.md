# Migration Guide: GeoServer to QGIS for Visor Urbano

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Architecture Analysis](#current-architecture-analysis)
3. [QGIS Target Architecture](#qgis-target-architecture)
4. [Migration Strategy](#migration-strategy)
5. [Technical Implementation](#technical-implementation)
6. [Code Examples](#code-examples)
7. [Testing and Validation](#testing-and-validation)
8. [Deployment Strategy](#deployment-strategy)
9. [Cost Analysis](#cost-analysis)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)
12. [Resources](#resources)

## Executive Summary

This document provides a comprehensive migration path from GeoServer to QGIS for the Visor Urbano municipal GIS platform. QGIS offers an open-source alternative with powerful desktop capabilities and server functionality through QGIS Server, making it an excellent choice for municipal applications.

### Key Benefits of Migration

- **Cost-effective**: Open-source solution with no licensing fees
- **Desktop Integration**: Powerful QGIS Desktop for data management and analysis
- **Standards Compliance**: Full OGC compliance (WMS, WFS, WCS, WMTS)
- **Flexibility**: Extensive plugin ecosystem and customization options
- **Community Support**: Large, active open-source community
- **PostGIS Integration**: Excellent native PostGIS support

### Migration Timeline

- **Phase 1**: Environment Setup and Testing (2-3 weeks)
- **Phase 2**: Data Migration and Service Configuration (3-4 weeks)
- **Phase 3**: Frontend Integration (2-3 weeks)
- **Phase 4**: Testing and Optimization (2 weeks)
- **Phase 5**: Production Deployment (1 week)

## Current Architecture Analysis

### Existing GeoServer Implementation

Based on the Visor Urbano codebase analysis:

```yaml
# Current Stack
Web Server: GeoServer
Database: PostGIS/PostgreSQL
Frontend: React + OpenLayers
Backend: FastAPI (Python)
Deployment: Docker containers
```

### Current Services

- **WMS**: Web Map Service for raster visualization
- **WFS**: Web Feature Service for vector data access
- **Styling**: SLD (Styled Layer Descriptor) files
- **Security**: Basic authentication and role-based access
- **Data Sources**: PostGIS database connections

### Current Layer Configuration

```python
# From seed_map_layers.py
layers = [
    {
        "name": "Límites Municipales",
        "type": "WMS",
        "url": "http://geoserver:8080/geoserver/visor/wms",
        "layer_name": "visor:limites_municipales"
    },
    {
        "name": "Zonificación",
        "type": "WFS",
        "url": "http://geoserver:8080/geoserver/visor/wfs",
        "layer_name": "visor:zonificacion"
    }
]
```

## QGIS Target Architecture

### QGIS Server Architecture

```yaml
# Target QGIS Stack
Map Server: QGIS Server
Desktop Tool: QGIS Desktop
Database: PostGIS/PostgreSQL (unchanged)
Frontend: React + OpenLayers (minimal changes)
Backend: FastAPI (minimal changes)
Deployment: Docker containers
```

### QGIS Server Components

1. **QGIS Server**: FastCGI application for web services
2. **Apache/Nginx**: Web server proxy
3. **QGIS Desktop**: Project creation and management
4. **PostgreSQL/PostGIS**: Spatial database (unchanged)

### Service Endpoints

```
WMS: /qgis/project_name?SERVICE=WMS&REQUEST=GetCapabilities
WFS: /qgis/project_name?SERVICE=WFS&REQUEST=GetCapabilities
WCS: /qgis/project_name?SERVICE=WCS&REQUEST=GetCapabilities
WMTS: /qgis/project_name?SERVICE=WMTS&REQUEST=GetCapabilities
```

## Migration Strategy

### Phase 1: Environment Setup (2-3 weeks)

#### 1.1 QGIS Server Installation

```dockerfile
# Dockerfile for QGIS Server
FROM qgis/qgis-server:3.34

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-fcgid \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Configure Apache
COPY apache-qgis.conf /etc/apache2/sites-available/
RUN a2ensite apache-qgis && a2enmod fcgid

# Copy QGIS projects
COPY projects/ /data/projects/

EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]
```

#### 1.2 Apache Configuration

```apache
# apache-qgis.conf
<VirtualHost *:80>
    ServerName qgis-server
    DocumentRoot /var/www/html

    # QGIS Server via FastCGI
    ScriptAlias /qgis/ /usr/lib/cgi-bin/qgis_mapserv.fcgi/

    <Location /qgis/>
        SetHandler fcgid-script
        Options +ExecCGI
        Allow from all
        Require all granted

        # QGIS Server environment variables
        SetEnv QGIS_SERVER_LOG_LEVEL 0
        SetEnv QGIS_SERVER_LOG_FILE /var/log/qgis/qgis-server.log
        SetEnv QGIS_PROJECT_FILE /data/projects/visor-urbano.qgs
        SetEnv QGIS_SERVER_IGNORE_BAD_LAYERS 1
    </Location>

    # Enable CORS
    Header always set Access-Control-Allow-Origin "*"
    Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS"
    Header always set Access-Control-Allow-Headers "Content-Type"
</VirtualHost>
```

### Phase 2: Data Migration and Service Configuration (3-4 weeks)

#### 2.1 QGIS Project Creation

Using QGIS Desktop, create project files (.qgs) that replace GeoServer workspaces:

```xml
<!-- visor-urbano.qgs excerpt -->
<?xml version="1.0" encoding="UTF-8"?>
<qgis version="3.34.0" projectname="Visor Urbano">
  <properties>
    <WMSServiceTitle type="QString">Visor Urbano WMS</WMSServiceTitle>
    <WMSServiceAbstract type="QString">Municipal GIS Services</WMSServiceAbstract>
    <WMSKeywordList type="QStringList">
      <value>municipal</value>
      <value>planning</value>
      <value>urbano</value>
    </WMSKeywordList>
    <WMSContactOrganization type="QString">Municipality</WMSContactOrganization>
    <WMSOnlineResource type="QString">http://localhost/qgis/</WMSOnlineResource>
  </properties>

  <projectlayers>
    <maplayer>
      <id>limites_municipales_layer</id>
      <datasource>
        host=postgres port=5432 user=gis_user password=password
        dbname=visor_urbano table=limites_municipales (geom)
      </datasource>
      <layername>Límites Municipales</layername>
      <provider>postgres</provider>
    </maplayer>
  </projectlayers>
</qgis>
```

#### 2.2 Database Connection Configuration

```python
# qgis_config.py - Database connection helper
import os
from typing import Dict, Any

def get_postgis_connection_string() -> str:
    """Generate PostGIS connection string for QGIS"""
    return (
        f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
        f"port={os.getenv('POSTGRES_PORT', '5432')} "
        f"user={os.getenv('POSTGRES_USER', 'gis_user')} "
        f"password={os.getenv('POSTGRES_PASSWORD', 'password')} "
        f"dbname={os.getenv('POSTGRES_DB', 'visor_urbano')}"
    )

def create_layer_config(table_name: str, geometry_column: str = 'geom') -> Dict[str, Any]:
    """Create QGIS layer configuration"""
    return {
        'datasource': f"{get_postgis_connection_string()} table={table_name} ({geometry_column})",
        'provider': 'postgres',
        'layer_name': table_name.replace('_', ' ').title()
    }
```

#### 2.3 Styling Migration

Convert SLD styles to QGIS QML format:

```python
# style_converter.py
import xml.etree.ElementTree as ET
from pathlib import Path

def convert_sld_to_qml(sld_file: Path, qml_file: Path):
    """Convert SLD styling to QGIS QML format"""

    # Parse SLD
    sld_tree = ET.parse(sld_file)
    sld_root = sld_tree.getroot()

    # Create QML structure
    qml_root = ET.Element('qgis')
    qml_root.set('version', '3.34.0')

    # Extract symbolizer information
    symbolizers = sld_root.findall('.//sld:PolygonSymbolizer',
                                  namespaces={'sld': 'http://www.opengis.net/sld'})

    # Convert to QGIS renderer
    renderer = ET.SubElement(qml_root, 'renderer-v2')
    renderer.set('type', 'singleSymbol')

    symbols = ET.SubElement(renderer, 'symbols')
    symbol = ET.SubElement(symbols, 'symbol')
    symbol.set('name', '0')
    symbol.set('type', 'fill')

    # Add fill layer
    layer = ET.SubElement(symbol, 'layer')
    layer.set('class', 'SimpleFill')

    # Write QML file
    qml_tree = ET.ElementTree(qml_root)
    qml_tree.write(qml_file, encoding='utf-8', xml_declaration=True)
```

### Phase 3: Frontend Integration (2-3 weeks)

#### 3.1 OpenLayers Configuration Updates

```typescript
// Updated OpenLayerMap.tsx for QGIS Server
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import ImageLayer from 'ol/layer/Image';
import ImageWMS from 'ol/source/ImageWMS';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { GeoJSON } from 'ol/format';

interface QGISLayerConfig {
  name: string;
  type: 'WMS' | 'WFS';
  project: string;
  layers: string;
  url: string;
  visible?: boolean;
}

class QGISLayerManager {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  createWMSLayer(config: QGISLayerConfig): ImageLayer<ImageWMS> {
    return new ImageLayer({
      source: new ImageWMS({
        url: `${this.baseUrl}/qgis/${config.project}`,
        params: {
          LAYERS: config.layers,
          VERSION: '1.3.0',
          FORMAT: 'image/png',
          TRANSPARENT: true,
          CRS: 'EPSG:4326',
        },
        serverType: 'qgis',
      }),
      visible: config.visible ?? true,
    });
  }

  createWFSLayer(config: QGISLayerConfig): VectorLayer<VectorSource> {
    const vectorSource = new VectorSource({
      format: new GeoJSON(),
      url: extent => {
        return (
          `${this.baseUrl}/qgis/${config.project}?` +
          `SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&` +
          `TYPENAME=${config.layers}&` +
          `OUTPUTFORMAT=application/json&` +
          `SRSNAME=EPSG:4326&` +
          `BBOX=${extent.join(',')},EPSG:4326`
        );
      },
      strategy: extent => [extent],
    });

    return new VectorLayer({
      source: vectorSource,
      visible: config.visible ?? true,
    });
  }
}

// Usage in OpenLayerMap component
const qgisManager = new QGISLayerManager(
  process.env.REACT_APP_QGIS_SERVER_URL || 'http://localhost'
);

const municipalBoundariesLayer = qgisManager.createWMSLayer({
  name: 'Límites Municipales',
  type: 'WMS',
  project: 'visor-urbano',
  layers: 'limites_municipales',
  url: qgisManager.baseUrl,
});

const zoningLayer = qgisManager.createWFSLayer({
  name: 'Zonificación',
  type: 'WFS',
  project: 'visor-urbano',
  layers: 'zonificacion',
  url: qgisManager.baseUrl,
});
```

#### 3.2 Backend Service Updates

```python
# app/services/qgis_service.py
import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from app.core.config import settings

class QGISServerService:
    def __init__(self):
        self.base_url = settings.QGIS_SERVER_URL
        self.project_name = settings.QGIS_PROJECT_NAME

    async def get_capabilities(self, service: str = 'WMS') -> Dict[str, Any]:
        """Get service capabilities from QGIS Server"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/qgis/{self.project_name}",
                params={
                    'SERVICE': service,
                    'REQUEST': 'GetCapabilities',
                    'VERSION': '1.3.0' if service == 'WMS' else '2.0.0'
                }
            )
            response.raise_for_status()
            return self._parse_capabilities(response.text, service)

    async def get_feature_info(self,
                             layer: str,
                             x: int,
                             y: int,
                             width: int,
                             height: int,
                             bbox: List[float]) -> Dict[str, Any]:
        """Get feature information from WMS layer"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/qgis/{self.project_name}",
                params={
                    'SERVICE': 'WMS',
                    'REQUEST': 'GetFeatureInfo',
                    'VERSION': '1.3.0',
                    'LAYERS': layer,
                    'QUERY_LAYERS': layer,
                    'FORMAT': 'image/png',
                    'INFO_FORMAT': 'application/json',
                    'X': x,
                    'Y': y,
                    'WIDTH': width,
                    'HEIGHT': height,
                    'BBOX': ','.join(map(str, bbox)),
                    'CRS': 'EPSG:4326'
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_layer_extent(self, layer: str) -> Optional[List[float]]:
        """Get layer bounding box"""
        capabilities = await self.get_capabilities('WMS')
        layers = capabilities.get('layers', [])

        for layer_info in layers:
            if layer_info.get('name') == layer:
                return layer_info.get('bbox')
        return None

    def _parse_capabilities(self, xml_content: str, service: str) -> Dict[str, Any]:
        """Parse WMS/WFS capabilities XML"""
        root = ET.fromstring(xml_content)

        if service == 'WMS':
            return self._parse_wms_capabilities(root)
        elif service == 'WFS':
            return self._parse_wfs_capabilities(root)

        return {}

    def _parse_wms_capabilities(self, root: ET.Element) -> Dict[str, Any]:
        """Parse WMS capabilities"""
        layers = []

        # Find all Layer elements
        for layer_elem in root.findall('.//Layer'):
            name_elem = layer_elem.find('Name')
            title_elem = layer_elem.find('Title')
            bbox_elem = layer_elem.find('.//BoundingBox[@CRS="EPSG:4326"]')

            if name_elem is not None and name_elem.text:
                layer_info = {
                    'name': name_elem.text,
                    'title': title_elem.text if title_elem is not None else name_elem.text,
                    'queryable': layer_elem.get('queryable', '0') == '1'
                }

                if bbox_elem is not None:
                    layer_info['bbox'] = [
                        float(bbox_elem.get('minx', 0)),
                        float(bbox_elem.get('miny', 0)),
                        float(bbox_elem.get('maxx', 0)),
                        float(bbox_elem.get('maxy', 0))
                    ]

                layers.append(layer_info)

        return {
            'service': 'WMS',
            'version': root.get('version'),
            'layers': layers
        }
```

#### 3.3 Environment Configuration

```bash
# .env updates for QGIS Server
QGIS_SERVER_URL=http://qgis-server:80
QGIS_PROJECT_NAME=visor-urbano
QGIS_SERVER_LOG_LEVEL=0
QGIS_DATA_PATH=/data/projects
```

### Phase 4: Docker Compose Configuration

```yaml
# docker-compose.qgis.yml
version: '3.8'

services:
  qgis-server:
    build:
      context: ./docker/qgis
      dockerfile: Dockerfile
    ports:
      - '8080:80'
    environment:
      - QGIS_SERVER_LOG_LEVEL=0
      - QGIS_SERVER_LOG_FILE=/var/log/qgis/qgis-server.log
      - QGIS_PROJECT_FILE=/data/projects/visor-urbano.qgs
      - QGIS_SERVER_IGNORE_BAD_LAYERS=1
    volumes:
      - ./qgis/projects:/data/projects:ro
      - qgis_logs:/var/log/qgis
    depends_on:
      - postgres
    networks:
      - visor-network

  postgres:
    image: postgis/postgis:15-3.3
    environment:
      - POSTGRES_DB=visor_urbano
      - POSTGRES_USER=gis_user
      - POSTGRES_PASSWORD=gis_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init:/docker-entrypoint-initdb.d
    ports:
      - '5432:5432'
    networks:
      - visor-network

  frontend:
    build:
      context: ./apps/frontend
      dockerfile: Dockerfile
    ports:
      - '3000:3000'
    environment:
      - REACT_APP_QGIS_SERVER_URL=http://localhost:8080
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - qgis-server
      - backend
    networks:
      - visor-network

  backend:
    build:
      context: ./apps/backend
      dockerfile: Dockerfile
    ports:
      - '8000:8000'
    environment:
      - QGIS_SERVER_URL=http://qgis-server:80
      - POSTGRES_HOST=postgres
      - POSTGRES_DB=visor_urbano
      - POSTGRES_USER=gis_user
      - POSTGRES_PASSWORD=gis_password
    depends_on:
      - postgres
      - qgis-server
    networks:
      - visor-network

volumes:
  postgres_data:
  qgis_logs:

networks:
  visor-network:
    driver: bridge
```

## Testing and Validation

### Unit Tests for QGIS Integration

```python
# tests/test_qgis_service.py
import pytest
from httpx import AsyncClient
from app.services.qgis_service import QGISServerService

@pytest.mark.asyncio
async def test_qgis_capabilities():
    """Test QGIS Server capabilities endpoint"""
    service = QGISServerService()
    capabilities = await service.get_capabilities('WMS')

    assert capabilities['service'] == 'WMS'
    assert 'layers' in capabilities
    assert len(capabilities['layers']) > 0

@pytest.mark.asyncio
async def test_qgis_feature_info():
    """Test GetFeatureInfo request"""
    service = QGISServerService()

    feature_info = await service.get_feature_info(
        layer='limites_municipales',
        x=100, y=100,
        width=200, height=200,
        bbox=[-74.1, 4.5, -74.0, 4.6]
    )

    assert 'features' in feature_info

@pytest.mark.asyncio
async def test_layer_extent():
    """Test layer extent retrieval"""
    service = QGISServerService()
    extent = await service.get_layer_extent('limites_municipales')

    assert extent is not None
    assert len(extent) == 4
    assert all(isinstance(coord, (int, float)) for coord in extent)
```

### Integration Tests

```python
# tests/test_qgis_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_qgis_layer_endpoint():
    """Test layer listing endpoint"""
    response = client.get("/api/v1/layers")
    assert response.status_code == 200

    layers = response.json()
    assert isinstance(layers, list)
    assert len(layers) > 0

def test_qgis_map_endpoint():
    """Test map rendering endpoint"""
    response = client.get("/api/v1/map/wms", params={
        'LAYERS': 'limites_municipales',
        'BBOX': '-74.1,4.5,-74.0,4.6',
        'WIDTH': '256',
        'HEIGHT': '256',
        'FORMAT': 'image/png'
    })
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/png'
```

## Cost Analysis

### Open Source Benefits

- **Licensing**: $0 (vs GeoServer: $0, vs ArcGIS: $1,500-$7,000/year)
- **Hardware**: Standard server requirements
- **Training**: Moderate learning curve for QGIS Desktop
- **Support**: Community support + optional commercial support

### Implementation Costs

- **Development Time**: 8-10 weeks
- **Training**: 1-2 weeks for team
- **Testing**: 2 weeks
- **Total Estimated Cost**: $15,000-$25,000

### Long-term Savings

- **Annual Licensing**: $0
- **Maintenance**: Reduced (open source)
- **Scalability**: Horizontal scaling capability
- **Flexibility**: Extensive customization options

## Best Practices

### 1. QGIS Project Management

```python
# Project management utilities
import shutil
from pathlib import Path

def backup_qgis_project(project_path: Path, backup_dir: Path):
    """Create backup of QGIS project"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f"backup_{timestamp}"
    shutil.copytree(project_path, backup_path)
    return backup_path

def validate_qgis_project(project_file: Path) -> bool:
    """Validate QGIS project file"""
    try:
        tree = ET.parse(project_file)
        root = tree.getroot()
        return root.tag == 'qgis'
    except ET.ParseError:
        return False
```

### 2. Performance Optimization

- Use spatial indexes on PostGIS tables
- Configure QGIS Server caching
- Implement tile caching for frequently accessed layers
- Use connection pooling for database access

### 3. Security Configuration

```apache
# Security headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options SAMEORIGIN
Header always set X-XSS-Protection "1; mode=block"

# Rate limiting
<Location /qgis/>
    # Configure mod_evasive or similar
    DOSHashTableSize 4096
    DOSPageCount 3
    DOSSiteCount 50
    DOSPageInterval 1
    DOSSiteInterval 1
    DOSBlockingPeriod 600
</Location>
```

### 4. Monitoring and Logging

```python
# qgis_monitor.py
import logging
from pathlib import Path

def setup_qgis_logging():
    """Configure QGIS Server logging"""
    log_dir = Path('/var/log/qgis')
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'qgis-server.log'),
            logging.StreamHandler()
        ]
    )
```

## Troubleshooting

### Common Issues and Solutions

#### 1. QGIS Server Not Starting

**Symptoms**: 500 errors, server not responding
**Solutions**:

- Check Apache configuration
- Verify QGIS project file permissions
- Check log files: `/var/log/qgis/qgis-server.log`

#### 2. Database Connection Issues

**Symptoms**: Layers not loading, connection errors
**Solutions**:

```python
# Test database connection
import psycopg2

def test_postgis_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        cursor = conn.cursor()
        cursor.execute('SELECT PostGIS_version();')
        version = cursor.fetchone()
        print(f"PostGIS version: {version[0]}")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
```

#### 3. Styling Issues

**Symptoms**: Layers appear with default styling
**Solutions**:

- Verify QML files are in correct location
- Check QGIS project file references
- Use QGIS Desktop to test styling

#### 4. Performance Issues

**Symptoms**: Slow map rendering, timeouts
**Solutions**:

- Enable spatial indexes
- Configure server-side caching
- Optimize database queries
- Use simplified geometries for overview levels

## Resources

### Documentation

- [QGIS Server Documentation](https://docs.qgis.org/3.34/en/docs/server_manual/)
- [QGIS Desktop User Guide](https://docs.qgis.org/3.34/en/docs/user_manual/)
- [PostGIS Documentation](https://postgis.net/documentation/)

### Training Materials

- QGIS Desktop basics for project creation
- QGIS Server administration
- PostGIS spatial database management
- OpenLayers integration patterns

### Community Resources

- [QGIS Community](https://qgis.org/en/site/getinvolved/)
- [QGIS Stack Exchange](https://gis.stackexchange.com/questions/tagged/qgis)
- [PostGIS Users Mailing List](https://lists.osgeo.org/mailman/listinfo/postgis-users)

### Commercial Support

- [North River Geographic](https://north-road.com/) - QGIS development and support
- [Kartoza](https://kartoza.com/) - QGIS and PostGIS consulting
- [OPENGIS.ch](https://www.opengis.ch/) - QGIS development and training

---

This migration guide provides a comprehensive path from GeoServer to QGIS, maintaining the robustness and functionality of the Visor Urbano platform while leveraging the benefits of the QGIS ecosystem. The phased approach ensures minimal disruption to operations while providing a clear upgrade path.
