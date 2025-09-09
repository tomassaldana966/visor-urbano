from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.settings import get_db
from app.models.zoning_impact_level import ZoningImpactLevel
from app.schemas.zoning_impact_level import (
    ZoningImpactLevelCreate,
    ZoningImpactLevelUpdate,
    ZoningImpactLevelResponse
)
from typing import List
from geoalchemy2.shape import to_shape, from_shape # type: ignore
from shapely.geometry import mapping, shape # type: ignore
from shapely.ops import transform # type: ignore
import pyproj # type: ignore

router = APIRouter()

def transform_geom_to_utm(geom_dict):
    """Transform geometry from WGS84 (EPSG:4326) to UTM Zone 13N (EPSG:32613)"""
    if not geom_dict:
        return None
    
    # Create shapely geometry from GeoJSON
    shapely_geom = shape(geom_dict)
    
    # Set up coordinate transformation
    transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32613", always_xy=True)
    
    # Transform the geometry
    transformed_geom = transform(transformer.transform, shapely_geom)
    
    # Convert to geoalchemy2 format
    return from_shape(transformed_geom, srid=32613)

def transform_geom_to_wgs84(geom):
    """Transform geometry from UTM Zone 13N (EPSG:32613) to WGS84 (EPSG:4326)"""
    if not geom:
        return None
    
    # Convert from geoalchemy2 to shapely
    shapely_geom = to_shape(geom)
    
    # Set up coordinate transformation
    transformer = pyproj.Transformer.from_crs("EPSG:32613", "EPSG:4326", always_xy=True)
    
    # Transform the geometry
    transformed_geom = transform(transformer.transform, shapely_geom)
    
    # Convert to GeoJSON
    return mapping(transformed_geom)

@router.get("/", response_model=List[ZoningImpactLevelResponse])
async def list_zoning_impact_levels(
    municipality_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(ZoningImpactLevel).where(ZoningImpactLevel.municipality_id == municipality_id)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    
    output = []
    for row in rows:
        data = {
            "id": row.id,
            "impact_level": row.impact_level,
            "municipality_id": row.municipality_id,
            "geom": transform_geom_to_wgs84(row.geom)
        }
        output.append(data)
    return output

@router.get("/{id}", response_model=ZoningImpactLevelResponse)
async def get_zoning_impact_level(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(ZoningImpactLevel).where(ZoningImpactLevel.id == id)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Zoning impact level not found")
    
    data = {
        "id": item.id,
        "impact_level": item.impact_level,
        "municipality_id": item.municipality_id,
        "geom": transform_geom_to_wgs84(item.geom)
    }
    return data

@router.post("/", response_model=ZoningImpactLevelResponse)
async def create_zoning_impact_level(data: ZoningImpactLevelCreate, db: AsyncSession = Depends(get_db)):
    # Convert GeoJSON to UTM coordinates
    geom_value = None
    if data.geom:
        geom_value = transform_geom_to_utm(data.geom.model_dump())
    
    new_zone = ZoningImpactLevel(
        impact_level=data.impact_level,
        municipality_id=data.municipality_id,
        geom=geom_value
    )
    
    db.add(new_zone)
    await db.commit()
    await db.refresh(new_zone)
    
    result = {
        "id": new_zone.id,
        "impact_level": new_zone.impact_level,
        "municipality_id": new_zone.municipality_id,
        "geom": transform_geom_to_wgs84(new_zone.geom)
    }
    return result

@router.patch("/{id}", response_model=ZoningImpactLevelResponse)
async def update_zoning_impact_level(
    id: int,
    data: ZoningImpactLevelUpdate,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(ZoningImpactLevel).where(ZoningImpactLevel.id == id)
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Zoning Impact level not found")

    # Handle geometry conversion
    update_data = data.model_dump(exclude_unset=True)
    if 'geom' in update_data and update_data['geom'] is not None:
        update_data['geom'] = transform_geom_to_utm(update_data['geom'])

    for key, value in update_data.items():
        setattr(record, key, value)

    await db.commit()
    await db.refresh(record)
    
    response_data = {
        "id": record.id,
        "impact_level": record.impact_level,
        "municipality_id": record.municipality_id,
        "geom": transform_geom_to_wgs84(record.geom)
    }
    return response_data

@router.delete("/{id}", status_code=204)
async def delete_zoning_impact_level(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(ZoningImpactLevel).where(ZoningImpactLevel.id == id)
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Zoning Impact level not found")

    await db.delete(record)
    await db.commit()
