from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.settings import get_db
from app.models.zoning_control_regulations import ZoningControlRegulation
from app.schemas.zoning_control_regulations import ZoningControlRegulationResponse
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[ZoningControlRegulationResponse])
async def get_zoning_control_regulations(
    municipality_id: Optional[int] = Query(None),
    district: Optional[str] = Query(None),
    regulation_key: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(ZoningControlRegulation)

    if municipality_id is not None:
        query = query.where(ZoningControlRegulation.municipality_id == municipality_id)
    if district is not None:
        query = query.where(ZoningControlRegulation.district == district)
    if regulation_key is not None:
        query = query.where(ZoningControlRegulation.regulation_key == regulation_key)

    result = await db.execute(query)
    return result.scalars().all()
