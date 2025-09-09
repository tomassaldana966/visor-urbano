from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.functions import ST_AsGeoJSON  # type: ignore
from app.models.procedure_registrations import ProcedureRegistration
from app.schemas.procedure_registrations import ProcedureRegistrationResponse, ProcedureRegistrationGeoResponse, ProcedureRegistrationCreate, ProcedureRegistrationUpdate
from config.settings import get_db
from typing import List, Optional
import json

router = APIRouter()

@router.get("/", response_model=List[ProcedureRegistrationResponse])
async def list_procedure_registrations(
    municipio_id: Optional[int] = Query(None),
    business_sector: Optional[str] = Query(None),
    reference: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(ProcedureRegistration)

    if municipio_id:
        query = query.where(ProcedureRegistration.municipality_id == municipio_id)
    if business_sector:
        query = query.where(ProcedureRegistration.business_sector.ilike(f"%{business_sector}%"))
    if reference:
        query = query.where(ProcedureRegistration.reference.ilike(f"%{reference}%"))

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/geometry", response_model=List[ProcedureRegistrationGeoResponse])
async def list_procedure_registrations_with_geometry(
    municipio_id: Optional[int] = Query(None),
    business_sector: Optional[str] = Query(None),
    reference: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(
        ProcedureRegistration.id,
        ProcedureRegistration.reference,
        ProcedureRegistration.area,
        ProcedureRegistration.business_sector,
        ProcedureRegistration.procedure_type,
        ProcedureRegistration.procedure_origin,
        ProcedureRegistration.historical_id,
        ProcedureRegistration.bbox,
        ProcedureRegistration.municipality_id,
        ST_AsGeoJSON(ProcedureRegistration.geom).label('geom_json')
    )

    if municipio_id:
        query = query.where(ProcedureRegistration.municipality_id == municipio_id)
    if business_sector:
        query = query.where(ProcedureRegistration.business_sector.ilike(f"%{business_sector}%"))
    if reference:
        query = query.where(ProcedureRegistration.reference.ilike(f"%{reference}%"))

    result = await db.execute(query)
    records = result.fetchall()
    
    response_data = []
    for record in records:
        item = {
            "id": record.id,
            "reference": record.reference,
            "area": record.area,
            "business_sector": record.business_sector,
            "procedure_type": record.procedure_type,
            "procedure_origin": record.procedure_origin,
            "historical_id": record.historical_id,
            "bbox": record.bbox,
            "municipality_id": record.municipality_id,
            "geom": json.loads(record.geom_json) if record.geom_json else None
        }
        response_data.append(item)
    
    return response_data


@router.get("/geometry/{id}", response_model=ProcedureRegistrationGeoResponse)
async def get_procedure_registration_with_geometry(id: int, db: AsyncSession = Depends(get_db)):
    query = select(
        ProcedureRegistration.id,
        ProcedureRegistration.reference,
        ProcedureRegistration.area,
        ProcedureRegistration.business_sector,
        ProcedureRegistration.procedure_type,
        ProcedureRegistration.procedure_origin,
        ProcedureRegistration.historical_id,
        ProcedureRegistration.bbox,
        ProcedureRegistration.municipality_id,
        ST_AsGeoJSON(ProcedureRegistration.geom).label('geom_json')
    ).where(ProcedureRegistration.id == id)
    
    result = await db.execute(query)
    record = result.fetchone()
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return {
        "id": record.id,
        "reference": record.reference,
        "area": record.area,
        "business_sector": record.business_sector,
        "procedure_type": record.procedure_type,
        "procedure_origin": record.procedure_origin,
        "historical_id": record.historical_id,
        "bbox": record.bbox,
        "municipality_id": record.municipality_id,
        "geom": json.loads(record.geom_json) if record.geom_json else None
    }


@router.get("/{id}", response_model=ProcedureRegistrationResponse)
async def get_procedure_registration(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProcedureRegistration).where(ProcedureRegistration.id == id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.post("/", response_model=ProcedureRegistrationResponse)
async def create_procedure_registration(
    data: ProcedureRegistrationCreate, db: AsyncSession = Depends(get_db)
):
    create_data = data.model_dump(exclude_unset=True) if hasattr(data, 'model_dump') else data.dict(exclude_unset=True)
    new_record = ProcedureRegistration(**create_data)
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record


@router.patch("/geometry/{id}", response_model=ProcedureRegistrationGeoResponse)
async def update_procedure_registration_geom(
    id: int, data: dict, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ProcedureRegistration).where(ProcedureRegistration.id == id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    field_mapping = {
        "folio": "reference",
        "giro": "business_sector",
        "area": "area",
        "municipio": "municipality_id"
    }

    props = data.get("properties", {})
    for key in ["folio", "giro", "area", "municipio"]:
        if key in props:
            setattr(record, field_mapping[key], props[key])

    await db.commit()
    await db.refresh(record)
    return record


@router.patch("/{id}", response_model=ProcedureRegistrationResponse)
async def update_procedure_registration(
    id: int, data: ProcedureRegistrationUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ProcedureRegistration).where(ProcedureRegistration.id == id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    update_data = data.model_dump(exclude_unset=True) if hasattr(data, 'model_dump') else data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(record, key, value)

    await db.commit()
    await db.refresh(record)
    return record


@router.delete("/{id}")
async def delete_procedure_registration(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProcedureRegistration).where(ProcedureRegistration.id == id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    await db.delete(record)
    await db.commit()
    return {"detail": "Record deleted successfully"}
