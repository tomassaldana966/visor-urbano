#!/usr/bin/env python3
"""
Map Layers Seeder Script

This script seeds map layers data from layers.json into the FastAPI database.
Run with: python scripts/seed_map_layers.py
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path so we can import from app
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models.map_layers import MapLayer, maplayer_municipality
from app.models.municipality import Municipality
from config.settings import DATABASE_URL

# Hardcoded layers data from layers.json
LAYERS_DATA = [
    {
        "id": 23,
        "value": "chihuhuaOrto2020",
        "label": "Ortofoto 2020",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "chihuhuaOrto2020",
        "visible": True,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 0,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 6,
        "value": "chih_zonif_primaria2023_corregida",
        "label": "Zonificación primaria (2023)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "chih_zonif_primaria2023_corregida",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 1,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 2,
        "value": "zon_secundaria_dissolve_utmz13n",
        "label": "Zonificación secundaria (2023)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "zon_secundaria_dissolve_utmz13n",
        "visible": True,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:4326",
        "version": "1.3.0",
        "format": "image/png",
        "order": 2,
        "editable": False,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 16,
        "value": "chih_estructura_vial2023_corregida",
        "label": "Estructura vial (2023)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "chih_estructura_vial2023_corregida",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 3,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 20,
        "value": "chih_calles_implan",
        "label": "Calles",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "chih_calles_implan",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:4326",
        "version": "1.3.0",
        "format": "image/png",
        "order": 4,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 21,
        "value": "chih_denue_nov2024",
        "label": "DENUE (nov 2024)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "chih_denue_nov2024",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 5,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 14,
        "value": "nodos_estrategicos_2023",
        "label": "Nodos estratégicos",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "nodos_estrategicos_2023",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 6,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 18,
        "value": "asentamiento_humano",
        "label": "Asentamiento humano",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "asentamiento_humano",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:4326",
        "version": "1.3.0",
        "format": "image/png",
        "order": 7,
        "editable": False,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 8,
        "value": "sector_urbano",
        "label": "Sector urbano",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "sector_urbano",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 8,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 7,
        "value": "subcentros_ainfluencia_5000m_2023",
        "label": "Subcentros: área de influencia (5000m)(2023)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "subcentros_ainfluencia_5000m_2023",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 9,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 13,
        "value": "planeacion_especifica_2023",
        "label": "Planeación específica",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "planeacion_especifica_2023",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 10,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 11,
        "value": "potencial_suelo_industrial_2023",
        "label": "Potencial de suelo industrial",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "potencial_suelo_industrial_2023",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 11,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 10,
        "value": "psuelo_industrial_ainfluencia_2023",
        "label": "Potencial de  suelo industrial (área de influencia)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "psuelo_industrial_ainfluencia_2023",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 12,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 3,
        "value": "zona_industrial",
        "label": "Zona industrial (2023)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "zona_industrial",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:4326",
        "version": "1.3.0",
        "format": "image/png",
        "order": 13,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 9,
        "value": "reservas_industriales_2023",
        "label": "Reservas industriales (2023)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "reservas_industriales_2023",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 14,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 1,
        "value": "zprioritaria_equrbano_2023",
        "label": "Zona prioritaria para equipamiento urbano (2023)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "zprioritaria_equrbano_2023",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 15,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 15,
        "value": "gestion_de_riesgos_2023",
        "label": "Gestión de riesgos",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "gestion_de_riesgos_2023",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 16,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 4,
        "value": "zona_homogenea",
        "label": "Zona homogénea",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "zona_homogenea",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 17,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 22,
        "value": "chih_cpv2020_manzanas",
        "label": "Censo de Población y Vivivenda 2020",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "chih_cpv2020_manzanas",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 18,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 17,
        "value": "condicionantes_para_usos_2023",
        "label": "Condicionantes para usos (2023)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "condicionantes_para_usos_2023",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 19,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 5,
        "value": "usos_modificados_2024",
        "label": "Usos modificados (2024)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "usos_modificados_2024",
        "visible": True,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:4326",
        "version": "1.3.0",
        "format": "image/png",
        "order": 20,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 12,
        "value": "poligonos_de_adecuacion_2024",
        "label": "Polígonos de adecuación (2024)",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "poligonos_de_adecuacion_2024",
        "visible": True,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:4326",
        "version": "1.3.0",
        "format": "image/png",
        "order": 21,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 24,
        "value": "predio_urbano",
        "label": "Predios urbanos",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "predio_urbano",
        "visible": True,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:32613",
        "version": "1.3.0",
        "format": "image/png",
        "order": 22,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    },
    {
        "id": 19,
        "value": "chih_construcciones",
        "label": "Construcciones",
        "type": "wms",
        "url": "https://datahub.mpiochih.gob.mx/ows",
        "layers": "chih_construcciones",
        "visible": False,
        "active": True,
        "attribution": None,
        "opacity": 1,
        "server_type": None,
        "projection": "EPSG:4326",
        "version": "1.3.0",
        "format": "image/png",
        "order": 23,
        "editable": True,
        "type_geom": None,
        "cql_filter": None,
        "municipality": [2]
    }
]

def load_layers_data():
    """Return hardcoded layers data"""
    return LAYERS_DATA

async def seed_map_layers():
    """Seed map layers from layers.json into the database"""
    # Create async engine and session
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with AsyncSessionLocal() as session:
        try:
            # Load layers data
            layers_data = load_layers_data()
            print(f"Loaded {len(layers_data)} map layers from hardcoded data")
            
            # Check if layers already exist
            existing_layers = await session.execute(select(MapLayer))
            existing_count = len(existing_layers.scalars().all())
            
            if existing_count > 0:
                print(f"Found {existing_count} existing map layers. Clearing before seeding...")
                # Delete existing associations first to avoid foreign key constraint
                await session.execute(maplayer_municipality.delete())
                # Then delete the layers
                await session.execute(MapLayer.__table__.delete())
                await session.commit()
            
            # Get municipality_id=2 to associate layers with
            municipality_result = await session.execute(
                select(Municipality).where(Municipality.id == 2)
            )
            municipality = municipality_result.scalar_one_or_none()
            
            if not municipality:
                print("ERROR: Municipality with ID 2 not found. Please seed municipalities first.")
                return
            
            print(f"Associating layers with municipality: {municipality.name}")
            
            # Seed each layer
            for layer_data in layers_data:
                # Map JSON structure to model attributes
                map_layer = MapLayer(
                    value=layer_data["value"],
                    label=layer_data["label"],
                    type=layer_data["type"].upper(),  # Convert to uppercase (WMS, WFS)
                    url=layer_data["url"],
                    layers=layer_data["layers"],
                    visible=layer_data["visible"],
                    active=layer_data["active"],
                    attribution=layer_data["attribution"],
                    opacity=float(layer_data["opacity"]),
                    server_type=layer_data["server_type"],
                    projection=layer_data["projection"],
                    version=layer_data["version"],
                    format=layer_data["format"],
                    order=layer_data["order"],
                    editable=layer_data["editable"],
                    type_geom=layer_data["type_geom"],
                    cql_filter=layer_data["cql_filter"]
                )
                
                # Associate with municipality (layers.json has "municipality" array)
                if layer_data.get("municipality") and municipality:
                    map_layer.municipalities = [municipality]
                
                session.add(map_layer)
                print(f"Added layer: {layer_data['label']} (order: {layer_data['order']})")
            
            # Commit all changes
            await session.commit()
            print(f"\n✅ Successfully seeded {len(layers_data)} map layers!")
            print("All layers are associated with municipality_id=2 (Chihuahua)")
            
        except Exception as e:
            print(f"❌ Error seeding map layers: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()
            await engine.dispose()

async def main():
    """Main function to run the seeder"""
    print("🗺️  Starting Map Layers Seeder...")
    print("Using hardcoded layers data")
    
    await seed_map_layers()
    print("Map layers seeding completed!")

if __name__ == "__main__":
    asyncio.run(main())
