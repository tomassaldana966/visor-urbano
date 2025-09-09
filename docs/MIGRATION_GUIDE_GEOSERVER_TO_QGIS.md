# Guía de Migración: GeoServer a QGIS para Visor Urbano

## Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Análisis de Arquitectura Actual](#análisis-de-arquitectura-actual)
3. [Arquitectura Objetivo con QGIS](#arquitectura-objetivo-con-qgis)
4. [Estrategia de Migración](#estrategia-de-migración)
5. [Implementación Técnica](#implementación-técnica)
6. [Ejemplos de Código](#ejemplos-de-código)
7. [Pruebas y Validación](#pruebas-y-validación)
8. [Estrategia de Despliegue](#estrategia-de-despliegue)
9. [Análisis de Costos](#análisis-de-costos)
10. [Mejores Prácticas](#mejores-prácticas)
11. [Solución de Problemas](#solución-de-problemas)
12. [Recursos](#recursos)

## Resumen Ejecutivo

Este documento proporciona una ruta de migración integral de GeoServer a QGIS para la plataforma SIG municipal Visor Urbano. QGIS ofrece una alternativa de código abierto con poderosas capacidades de escritorio y funcionalidad de servidor a través de QGIS Server, convirtiéndolo en una excelente opción para aplicaciones municipales.

### Beneficios Clave de la Migración

- **Costo-efectivo**: Solución de código abierto sin tarifas de licencia
- **Integración de Escritorio**: Potente QGIS Desktop para gestión y análisis de datos
- **Cumplimiento de Estándares**: Cumplimiento completo de OGC (WMS, WFS, WCS, WMTS)
- **Flexibilidad**: Amplio ecosistema de plugins y opciones de personalización
- **Soporte Comunitario**: Comunidad de código abierto grande y activa
- **Integración PostGIS**: Excelente soporte nativo para PostGIS

### Cronograma de Migración

- **Fase 1**: Configuración de Entorno y Pruebas (2-3 semanas)
- **Fase 2**: Migración de Datos y Configuración de Servicios (3-4 semanas)
- **Fase 3**: Integración Frontend (2-3 semanas)
- **Fase 4**: Pruebas y Optimización (2 semanas)
- **Fase 5**: Despliegue en Producción (1 semana)

## Análisis de Arquitectura Actual

### Implementación Actual de GeoServer

Basado en el análisis del código de Visor Urbano:

```yaml
# Stack Actual
Servidor Web: GeoServer
Base de Datos: PostGIS/PostgreSQL
Frontend: React + OpenLayers
Backend: FastAPI (Python)
Despliegue: Contenedores Docker
```

### Servicios Actuales

- **WMS**: Servicio de Mapas Web para visualización de raster
- **WFS**: Servicio de Características Web para acceso a datos vectoriales
- **Estilos**: Archivos SLD (Styled Layer Descriptor)
- **Seguridad**: Autenticación básica y acceso basado en roles
- **Fuentes de Datos**: Conexiones a base de datos PostGIS

### Configuración Actual de Capas

```python
# De seed_map_layers.py
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

## Arquitectura Objetivo con QGIS

### Arquitectura de QGIS Server

```yaml
# Stack QGIS Objetivo
Servidor de Mapas: QGIS Server
Herramienta de Escritorio: QGIS Desktop
Base de Datos: PostGIS/PostgreSQL (sin cambios)
Frontend: React + OpenLayers (cambios mínimos)
Backend: FastAPI (cambios mínimos)
Despliegue: Contenedores Docker
```

### Componentes de QGIS Server

1. **QGIS Server**: Aplicación FastCGI para servicios web
2. **Apache/Nginx**: Proxy de servidor web
3. **QGIS Desktop**: Creación y gestión de proyectos
4. **PostgreSQL/PostGIS**: Base de datos espacial (sin cambios)

### Endpoints de Servicios

```
WMS: /qgis/nombre_proyecto?SERVICE=WMS&REQUEST=GetCapabilities
WFS: /qgis/nombre_proyecto?SERVICE=WFS&REQUEST=GetCapabilities
WCS: /qgis/nombre_proyecto?SERVICE=WCS&REQUEST=GetCapabilities
WMTS: /qgis/nombre_proyecto?SERVICE=WMTS&REQUEST=GetCapabilities
```

## Estrategia de Migración

### Fase 1: Configuración del Entorno (2-3 semanas)

#### 1.1 Instalación de QGIS Server

```dockerfile
# Dockerfile para QGIS Server
FROM qgis/qgis-server:3.34

# Instalar dependencias adicionales
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-fcgid \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Configurar Apache
COPY apache-qgis.conf /etc/apache2/sites-available/
RUN a2ensite apache-qgis && a2enmod fcgid

# Copiar proyectos QGIS
COPY projects/ /data/projects/

EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]
```

#### 1.2 Configuración de Apache

```apache
# apache-qgis.conf
<VirtualHost *:80>
    ServerName qgis-server
    DocumentRoot /var/www/html

    # QGIS Server vía FastCGI
    ScriptAlias /qgis/ /usr/lib/cgi-bin/qgis_mapserv.fcgi/

    <Location /qgis/>
        SetHandler fcgid-script
        Options +ExecCGI
        Allow from all
        Require all granted

        # Variables de entorno de QGIS Server
        SetEnv QGIS_SERVER_LOG_LEVEL 0
        SetEnv QGIS_SERVER_LOG_FILE /var/log/qgis/qgis-server.log
        SetEnv QGIS_PROJECT_FILE /data/projects/visor-urbano.qgs
        SetEnv QGIS_SERVER_IGNORE_BAD_LAYERS 1
    </Location>

    # Habilitar CORS
    Header always set Access-Control-Allow-Origin "*"
    Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS"
    Header always set Access-Control-Allow-Headers "Content-Type"
</VirtualHost>
```

### Fase 2: Migración de Datos y Configuración de Servicios (3-4 semanas)

#### 2.1 Creación de Proyectos QGIS

Usando QGIS Desktop, crear archivos de proyecto (.qgs) que reemplacen los workspaces de GeoServer:

```xml
<!-- Extracto de visor-urbano.qgs -->
<?xml version="1.0" encoding="UTF-8"?>
<qgis version="3.34.0" projectname="Visor Urbano">
  <properties>
    <WMSServiceTitle type="QString">Visor Urbano WMS</WMSServiceTitle>
    <WMSServiceAbstract type="QString">Servicios SIG Municipales</WMSServiceAbstract>
    <WMSKeywordList type="QStringList">
      <value>municipal</value>
      <value>planificacion</value>
      <value>urbano</value>
    </WMSKeywordList>
    <WMSContactOrganization type="QString">Municipalidad</WMSContactOrganization>
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

#### 2.2 Configuración de Conexión a Base de Datos

```python
# qgis_config.py - Helper para conexión a base de datos
import os
from typing import Dict, Any

def get_postgis_connection_string() -> str:
    """Generar cadena de conexión PostGIS para QGIS"""
    return (
        f"host={os.getenv('POSTGRES_HOST', 'localhost')} "
        f"port={os.getenv('POSTGRES_PORT', '5432')} "
        f"user={os.getenv('POSTGRES_USER', 'gis_user')} "
        f"password={os.getenv('POSTGRES_PASSWORD', 'password')} "
        f"dbname={os.getenv('POSTGRES_DB', 'visor_urbano')}"
    )

def create_layer_config(table_name: str, geometry_column: str = 'geom') -> Dict[str, Any]:
    """Crear configuración de capa QGIS"""
    return {
        'datasource': f"{get_postgis_connection_string()} table={table_name} ({geometry_column})",
        'provider': 'postgres',
        'layer_name': table_name.replace('_', ' ').title()
    }
```

#### 2.3 Migración de Estilos

Convertir estilos SLD al formato QML de QGIS:

```python
# style_converter.py
import xml.etree.ElementTree as ET
from pathlib import Path

def convert_sld_to_qml(sld_file: Path, qml_file: Path):
    """Convertir estilos SLD al formato QML de QGIS"""

    # Parsear SLD
    sld_tree = ET.parse(sld_file)
    sld_root = sld_tree.getroot()

    # Crear estructura QML
    qml_root = ET.Element('qgis')
    qml_root.set('version', '3.34.0')

    # Extraer información de simbolizadores
    symbolizers = sld_root.findall('.//sld:PolygonSymbolizer',
                                  namespaces={'sld': 'http://www.opengis.net/sld'})

    # Convertir a renderer de QGIS
    renderer = ET.SubElement(qml_root, 'renderer-v2')
    renderer.set('type', 'singleSymbol')

    symbols = ET.SubElement(renderer, 'symbols')
    symbol = ET.SubElement(symbols, 'symbol')
    symbol.set('name', '0')
    symbol.set('type', 'fill')

    # Agregar capa de relleno
    layer = ET.SubElement(symbol, 'layer')
    layer.set('class', 'SimpleFill')

    # Escribir archivo QML
    qml_tree = ET.ElementTree(qml_root)
    qml_tree.write(qml_file, encoding='utf-8', xml_declaration=True)
```

### Fase 3: Integración Frontend (2-3 semanas)

#### 3.1 Actualizaciones de Configuración de OpenLayers

```typescript
// OpenLayerMap.tsx actualizado para QGIS Server
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

// Uso en el componente OpenLayerMap
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

#### 3.2 Actualizaciones del Servicio Backend

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
        """Obtener capacidades del servicio desde QGIS Server"""
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
        """Obtener información de características de capa WMS"""
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
        """Obtener bounding box de capa"""
        capabilities = await self.get_capabilities('WMS')
        layers = capabilities.get('layers', [])

        for layer_info in layers:
            if layer_info.get('name') == layer:
                return layer_info.get('bbox')
        return None

    def _parse_capabilities(self, xml_content: str, service: str) -> Dict[str, Any]:
        """Parsear XML de capacidades WMS/WFS"""
        root = ET.fromstring(xml_content)

        if service == 'WMS':
            return self._parse_wms_capabilities(root)
        elif service == 'WFS':
            return self._parse_wfs_capabilities(root)

        return {}

    def _parse_wms_capabilities(self, root: ET.Element) -> Dict[str, Any]:
        """Parsear capacidades WMS"""
        layers = []

        # Encontrar todos los elementos Layer
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

#### 3.3 Configuración del Entorno

```bash
# Actualizaciones .env para QGIS Server
QGIS_SERVER_URL=http://qgis-server:80
QGIS_PROJECT_NAME=visor-urbano
QGIS_SERVER_LOG_LEVEL=0
QGIS_DATA_PATH=/data/projects
```

### Fase 4: Configuración de Docker Compose

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

## Pruebas y Validación

### Pruebas Unitarias para Integración QGIS

```python
# tests/test_qgis_service.py
import pytest
from httpx import AsyncClient
from app.services.qgis_service import QGISServerService

@pytest.mark.asyncio
async def test_qgis_capabilities():
    """Probar endpoint de capacidades de QGIS Server"""
    service = QGISServerService()
    capabilities = await service.get_capabilities('WMS')

    assert capabilities['service'] == 'WMS'
    assert 'layers' in capabilities
    assert len(capabilities['layers']) > 0

@pytest.mark.asyncio
async def test_qgis_feature_info():
    """Probar solicitud GetFeatureInfo"""
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
    """Probar recuperación de extensión de capa"""
    service = QGISServerService()
    extent = await service.get_layer_extent('limites_municipales')

    assert extent is not None
    assert len(extent) == 4
    assert all(isinstance(coord, (int, float)) for coord in extent)
```

### Pruebas de Integración

```python
# tests/test_qgis_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_qgis_layer_endpoint():
    """Probar endpoint de listado de capas"""
    response = client.get("/api/v1/layers")
    assert response.status_code == 200

    layers = response.json()
    assert isinstance(layers, list)
    assert len(layers) > 0

def test_qgis_map_endpoint():
    """Probar endpoint de renderizado de mapas"""
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

## Análisis de Costos

### Beneficios de Código Abierto

- **Licenciamiento**: $0 (vs GeoServer: $0, vs ArcGIS: $1,500-$7,000/año)
- **Hardware**: Requisitos estándar de servidor
- **Capacitación**: Curva de aprendizaje moderada para QGIS Desktop
- **Soporte**: Soporte comunitario + soporte comercial opcional

### Costos de Implementación

- **Tiempo de Desarrollo**: 8-10 semanas
- **Capacitación**: 1-2 semanas para el equipo
- **Pruebas**: 2 semanas
- **Costo Total Estimado**: $15,000-$25,000

### Ahorros a Largo Plazo

- **Licenciamiento Anual**: $0
- **Mantenimiento**: Reducido (código abierto)
- **Escalabilidad**: Capacidad de escalado horizontal
- **Flexibilidad**: Opciones extensas de personalización

## Mejores Prácticas

### 1. Gestión de Proyectos QGIS

```python
# Utilidades de gestión de proyectos
import shutil
from pathlib import Path

def backup_qgis_project(project_path: Path, backup_dir: Path):
    """Crear respaldo de proyecto QGIS"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f"backup_{timestamp}"
    shutil.copytree(project_path, backup_path)
    return backup_path

def validate_qgis_project(project_file: Path) -> bool:
    """Validar archivo de proyecto QGIS"""
    try:
        tree = ET.parse(project_file)
        root = tree.getroot()
        return root.tag == 'qgis'
    except ET.ParseError:
        return False
```

### 2. Optimización de Rendimiento

- Usar índices espaciales en tablas PostGIS
- Configurar caché de QGIS Server
- Implementar caché de teselas para capas accedidas frecuentemente
- Usar pool de conexiones para acceso a base de datos

### 3. Configuración de Seguridad

```apache
# Headers de seguridad
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options SAMEORIGIN
Header always set X-XSS-Protection "1; mode=block"

# Limitación de velocidad
<Location /qgis/>
    # Configurar mod_evasive o similar
    DOSHashTableSize 4096
    DOSPageCount 3
    DOSSiteCount 50
    DOSPageInterval 1
    DOSSiteInterval 1
    DOSBlockingPeriod 600
</Location>
```

### 4. Monitoreo y Registro

```python
# qgis_monitor.py
import logging
from pathlib import Path

def setup_qgis_logging():
    """Configurar registro de QGIS Server"""
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

## Solución de Problemas

### Problemas Comunes y Soluciones

#### 1. QGIS Server No Inicia

**Síntomas**: Errores 500, servidor no responde
**Soluciones**:

- Verificar configuración de Apache
- Verificar permisos del archivo de proyecto QGIS
- Revisar archivos de log: `/var/log/qgis/qgis-server.log`

#### 2. Problemas de Conexión a Base de Datos

**Síntomas**: Capas no cargan, errores de conexión
**Soluciones**:

```python
# Probar conexión a base de datos
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
        print(f"Versión PostGIS: {version[0]}")
        return True
    except Exception as e:
        print(f"Conexión falló: {e}")
        return False
```

#### 3. Problemas de Estilos

**Síntomas**: Capas aparecen con estilos por defecto
**Soluciones**:

- Verificar que archivos QML estén en ubicación correcta
- Revisar referencias en archivo de proyecto QGIS
- Usar QGIS Desktop para probar estilos

#### 4. Problemas de Rendimiento

**Síntomas**: Renderizado lento de mapas, timeouts
**Soluciones**:

- Habilitar índices espaciales
- Configurar caché del lado del servidor
- Optimizar consultas de base de datos
- Usar geometrías simplificadas para niveles de vista general

## Recursos

### Documentación

- [Documentación QGIS Server](https://docs.qgis.org/3.34/es/docs/server_manual/)
- [Guía de Usuario QGIS Desktop](https://docs.qgis.org/3.34/es/docs/user_manual/)
- [Documentación PostGIS](https://postgis.net/documentation/)

### Materiales de Capacitación

- Fundamentos de QGIS Desktop para creación de proyectos
- Administración de QGIS Server
- Gestión de base de datos espacial PostGIS
- Patrones de integración con OpenLayers

### Recursos Comunitarios

- [Comunidad QGIS](https://qgis.org/es/site/getinvolved/)
- [QGIS Stack Exchange](https://gis.stackexchange.com/questions/tagged/qgis)
- [Lista de Correo de Usuarios PostGIS](https://lists.osgeo.org/mailman/listinfo/postgis-users)

### Soporte Comercial

- [North River Geographic](https://north-road.com/) - Desarrollo y soporte QGIS
- [Kartoza](https://kartoza.com/) - Consultoría QGIS y PostGIS
- [OPENGIS.ch](https://www.opengis.ch/) - Desarrollo y capacitación QGIS

---

Esta guía de migración proporciona una ruta integral de GeoServer a QGIS, manteniendo la robustez y funcionalidad de la plataforma Visor Urbano mientras aprovecha los beneficios del ecosistema QGIS. El enfoque por fases asegura mínima disrupción de las operaciones mientras proporciona una ruta clara de actualización.
