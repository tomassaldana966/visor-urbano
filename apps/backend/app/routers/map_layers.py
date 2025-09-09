from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from config.settings import get_db
from app.models.map_layers import MapLayer
from app.models.municipality import Municipality
from app.schemas.map_layers import MapLayerCreate, MapLayerUpdate, MapLayerResponse
from typing import List, Optional

router = APIRouter()

# Helper function to construct response data consistent with MapLayerResponse
def _build_map_layer_response_data(layer: MapLayer) -> dict:
    municipalities = getattr(layer, "municipalities", [])
    return {
        "id": layer.id,
        "value": layer.value,
        "label": layer.label,
        "type": layer.type,
        "url": layer.url,
        "layers": layer.layers,
        "visible": layer.visible,
        "active": layer.active,
        "attribution": layer.attribution,
        "opacity": layer.opacity,
        "server_type": layer.server_type,
        "projection": layer.projection,
        "version": layer.version,
        "format": layer.format,
        "order": layer.order,
        "editable": layer.editable,
        "type_geom": layer.type_geom,
        "cql_filter": layer.cql_filter,
        "municipality_ids": [m.id for m in municipalities]
    }

@router.get("/", response_model=List[MapLayerResponse])
async def list_map_layers(
    municipality: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    if municipality:
        stmt = (
            select(MapLayer)
            .options(selectinload(MapLayer.municipalities))
            .join(MapLayer.municipalities)
            .where(Municipality.id == municipality)
            .order_by(MapLayer.order)
        )
    else:
        stmt = (
            select(MapLayer)
            .options(selectinload(MapLayer.municipalities))
            .order_by(MapLayer.order)
        )

    result = await db.execute(stmt)
    layers = result.scalars().all()
    
    return [_build_map_layer_response_data(layer) for layer in layers]


@router.get("/{id}", response_model=MapLayerResponse)
async def get_map_layer(db: AsyncSession = Depends(get_db), id: int = Path(..., gt=0, description="The ID of the map layer, must be greater than 0")):
    result = await db.execute(
        select(MapLayer)
        .options(selectinload(MapLayer.municipalities)) # Eager load municipalities
        .where(MapLayer.id == id)
    )
    layer = result.scalar_one_or_none()
    if not layer:
        raise HTTPException(status_code=404, detail="Map layer not found")
    return _build_map_layer_response_data(layer)


@router.post("/", response_model=MapLayerResponse, status_code=201)
async def create_map_layer(data: MapLayerCreate, db: AsyncSession = Depends(get_db)):
    layer = MapLayer(**data.model_dump(exclude={"municipality_ids"})) # Use model_dump
    if data.municipality_ids:
        municipality_qs = await db.execute(
            select(Municipality).where(Municipality.id.in_(data.municipality_ids))
        )
        layer.municipalities = municipality_qs.scalars().all()
    db.add(layer)
    await db.commit()
    await db.refresh(layer)
    
    # Re-query the layer with municipalities eagerly loaded to avoid lazy loading issues
    result = await db.execute(
        select(MapLayer)
        .options(selectinload(MapLayer.municipalities))
        .where(MapLayer.id == layer.id)
    )
    layer_with_municipalities = result.scalar_one()
    
    return _build_map_layer_response_data(layer_with_municipalities)


@router.patch("/{id}", response_model=MapLayerResponse)
async def update_map_layer(data: MapLayerUpdate, db: AsyncSession = Depends(get_db), id: int = Path(..., gt=0, description="The ID of the map layer, must be greater than 0")):
    result = await db.execute(
        select(MapLayer)
        .options(selectinload(MapLayer.municipalities)) # Eager load municipalities
        .where(MapLayer.id == id)
    )
    layer = result.scalar_one_or_none()
    if not layer:
        raise HTTPException(status_code=404, detail="Map layer not found")

    for key, value in data.model_dump(exclude_unset=True, exclude={"municipality_ids"}).items(): # Use model_dump
        setattr(layer, key, value)

    if data.municipality_ids is not None: # Check for None to allow clearing municipalities with []
        if data.municipality_ids: # If not empty list
            municipality_qs = await db.execute(
                select(Municipality).where(Municipality.id.in_(data.municipality_ids))
            )
            layer.municipalities = municipality_qs.scalars().all()
        else: # If empty list, clear the association
            layer.municipalities = []


    await db.commit()
    await db.refresh(layer)
    # Similar to create, ensure layer object is fully up-to-date for the response
    return _build_map_layer_response_data(layer)
