from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from datetime import datetime, timezone
from config.settings import get_db
from config.security import get_current_user
from app.models import DependencyResolution
from app.schemas.dependency_resolutions import (
    DependencyResolutionResponse,
    DependencyResolutionCreate,
    DependencyResolutionUpdate,
)
from app.utils.role_validation import validate_admin_or_director_role

router = APIRouter(prefix="/dependency_resolutions")


@router.get("/by_folio/{folio}", response_model=List[DependencyResolutionResponse])
async def get_resolutions_by_folio(
    folio: str = Path(..., description="Procedure folio to search for"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_admin_or_director_role(current_user)
    try:
        result = await db.execute(
            select(DependencyResolution)
            .options(selectinload(DependencyResolution.procedure))
            .join(DependencyResolution.procedure)
            .where(DependencyResolution.procedure.has(folio=folio))
        )
        resolutions = result.scalars().all()
        if not resolutions:
            raise HTTPException(
                status_code=404, 
                detail=f"No dependency resolutions found for folio: {folio}"
            )
        return resolutions
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving dependency resolutions: {str(e)}"
        )


@router.post("/", response_model=DependencyResolutionResponse)
async def create_resolution(
    data: DependencyResolutionCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_admin_or_director_role(current_user)
    try:
        if not data.procedure_id:
            raise HTTPException(
                status_code=400,
                detail="procedure_id is required"
            )
        from app.models.procedures import Procedure
        result = await db.execute(
            select(Procedure).where(Procedure.id == data.procedure_id)
        )
        procedure = result.scalar_one_or_none()
        if not procedure:
            raise HTTPException(
                status_code=404,
                detail=f"Procedure with id {data.procedure_id} not found"
            )
        resolution_data = data.model_dump()
        resolution_data['user_id'] = getattr(current_user, 'id', None)
        resolution = DependencyResolution(**resolution_data)
        db.add(resolution)
        await db.commit()
        await db.refresh(resolution)
        return resolution
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating dependency resolution: {str(e)}"
        )


@router.patch("/{resolution_id}", response_model=DependencyResolutionResponse)
async def update_resolution(
    resolution_id: int = Path(..., description="ID of the resolution to update"),
    data: DependencyResolutionUpdate = ...,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_admin_or_director_role(current_user)
    try:
        if resolution_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid resolution_id. Must be a positive integer."
            )
        result = await db.execute(
            select(DependencyResolution).where(DependencyResolution.id == resolution_id)
        )
        resolution = result.scalar_one_or_none()
        if not resolution:
            raise HTTPException(
                status_code=404, 
                detail=f"Dependency resolution with id {resolution_id} not found"
            )
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No update data provided"
            )
        for key, value in update_data.items():
            setattr(resolution, key, value)
        resolution.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(resolution)
        return resolution
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error updating dependency resolution: {str(e)}"
        )
