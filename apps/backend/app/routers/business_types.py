from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, and_
from sqlalchemy.orm import selectinload, joinedload
from typing import List

from app.models.business_type_config import BusinessTypeConfig
from app.models.business_types import BusinessType
from app.models.business_sectors import BusinessSector
from app.models.business_sector_configurations import BusinessSectorConfiguration
from app.schemas.business_type_config import (
    BusinessTypeDisableRequest,
    BusinessTypeCertificateStatusRequest,
    BusinessTypeConfigResponse,
    BusinessTypeImpactRequest
)
from app.schemas.business_types import (
    BusinessTypeCreate,
    BusinessTypeResponse
)
from app.schemas.business_sectors import (
    BusinessSectorEnabledResponse,
    BusinessSectorConfigurationResponse
)
from config.settings import get_db
from config.security import get_current_user
from app.utils.role_validation import require_admin_or_director_role

router = APIRouter()

@router.post("/", response_model=BusinessTypeResponse)
async def create_business_type(
    data: BusinessTypeCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin_or_director_role)
):
    """
    Create a new business type.
    
    This endpoint allows admins and directors to create new business types
    with their name, description, SCIAN code, and related words.
    
    Requires admin or director privileges.
    """
    # Check if business type with same name already exists
    stmt = select(BusinessType).where(BusinessType.name == data.name)
    result = await db.execute(stmt)
    existing_business_type = result.scalar_one_or_none()
    
    if existing_business_type:
        raise HTTPException(
            status_code=400,
            detail=f"Business type with name '{data.name}' already exists"
        )
    
    # Check if SCIAN code already exists (if provided)
    if data.code:
        stmt = select(BusinessType).where(BusinessType.code == data.code)
        result = await db.execute(stmt)
        existing_code = result.scalar_one_or_none()
        
        if existing_code:
            raise HTTPException(
                status_code=400,
                detail=f"Business type with SCIAN code '{data.code}' already exists"
            )
    
    # Create new business type
    business_type = BusinessType(
        name=data.name,
        description=data.description,
        is_active=data.is_active,
        code=data.code,
        related_words=data.related_words
    )
    
    db.add(business_type)
    await db.commit()
    await db.refresh(business_type)
    
    return business_type

@router.post("/disable", response_model=BusinessTypeConfigResponse)
async def disable_business_type(
    data: BusinessTypeDisableRequest, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    stmt = select(BusinessTypeConfig).where(
        BusinessTypeConfig.business_type_id == data.business_type_id,
        BusinessTypeConfig.municipality_id == current_user.municipality_id
    ).options(selectinload(BusinessTypeConfig.business_type))
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()

    if record:
        record.is_disabled = True
    else:
        record = BusinessTypeConfig(
            business_type_id=data.business_type_id,
            municipality_id=current_user.municipality_id,
            is_disabled=True
        )
        db.add(record)

    await db.commit()
    await db.refresh(record)
    
    if record.business_type:
        record.name = record.business_type.name
        record.description = record.business_type.description
        record.code = record.business_type.code
        record.related_words = record.business_type.related_words
    
    return record

@router.post("/disable/status/{status}", response_model=BusinessTypeConfigResponse)
async def update_disabled_status(
    status: int,
    data: BusinessTypeDisableRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    is_disabled = bool(status)

    stmt = select(BusinessTypeConfig).where(
        BusinessTypeConfig.business_type_id == data.business_type_id,
        BusinessTypeConfig.municipality_id == current_user.municipality_id
    ).options(selectinload(BusinessTypeConfig.business_type))
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()

    if record:
        record.is_disabled = is_disabled
    else:
        record = BusinessTypeConfig(
            business_type_id=data.business_type_id,
            municipality_id=current_user.municipality_id,
            is_disabled=is_disabled
        )
        db.add(record)

    await db.commit()
    await db.refresh(record)
    
    if not record.business_type:
        stmt = select(BusinessTypeConfig).where(
            BusinessTypeConfig.id == record.id
        ).options(selectinload(BusinessTypeConfig.business_type))
        result = await db.execute(stmt)
        record = result.scalar_one()
    
    if record.business_type:
        record.name = record.business_type.name
        record.description = record.business_type.description
        record.code = record.business_type.code
        record.related_words = record.business_type.related_words
    
    return record

@router.post("/disable/certificate/{status}", response_model=BusinessTypeConfigResponse)
async def update_certificate_status(
    status: int,
    data: BusinessTypeCertificateStatusRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    toggled = bool(status)  # Update logic to directly use the status value

    stmt = select(BusinessTypeConfig).where(
        BusinessTypeConfig.business_type_id == data.business_type_id,
        BusinessTypeConfig.municipality_id == current_user.municipality_id
    ).options(selectinload(BusinessTypeConfig.business_type))
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()

    if record:
        record.has_certificate = toggled
    else:
        record = BusinessTypeConfig(
            business_type_id=data.business_type_id,
            municipality_id=current_user.municipality_id,
            has_certificate=toggled
        )
        db.add(record)

    await db.commit()
    await db.refresh(record)

    if record.business_type:
        record.name = record.business_type.name
        record.description = record.business_type.description
        record.code = record.business_type.code
        record.related_words = record.business_type.related_words

    return record

@router.delete("/disable/{id}", status_code=204)
async def delete_disabled_record(id: int, db: AsyncSession = Depends(get_db)):
    stmt = delete(BusinessTypeConfig).where(BusinessTypeConfig.id == id)
    await db.execute(stmt)
    await db.commit()

@router.get("/enabled", response_model=List[BusinessTypeConfigResponse])
async def get_enabled_business_types(
    municipality_id: int = Query(..., description="Municipality ID to filter enabled business types"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all enabled business types for a specific municipality.
    
    This endpoint returns business types that are NOT disabled (is_disabled = False)
    along with their full details including name, description, SCIAN code (code),
    and related words (related_words).
    """
    stmt = (
        select(BusinessTypeConfig)
        .join(BusinessType)
        .options(selectinload(BusinessTypeConfig.business_type))
        .where(
            BusinessTypeConfig.municipality_id == municipality_id,
            BusinessTypeConfig.is_disabled == False
        )
    )
    result = await db.execute(stmt)
    configs = result.scalars().all()
        
    for config in configs:
        if config.business_type:
            config.name = config.business_type.name
            config.description = config.business_type.description
            config.code = config.business_type.code
            config.related_words = config.business_type.related_words
            
    return configs

@router.get("/disabled", response_model=List[BusinessTypeConfigResponse])
async def get_disabled_business_types(
    municipality_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all disabled business types for a specific municipality.
    
    This endpoint returns business types that are disabled (is_disabled = True)
    along with their full details including name, description, SCIAN code (code),
    and related words (related_words).
    """
    stmt = (
        select(BusinessTypeConfig)
        .join(BusinessType)
        .options(selectinload(BusinessTypeConfig.business_type))
        .where(
            BusinessTypeConfig.municipality_id == municipality_id,
            BusinessTypeConfig.is_disabled == True
        )
    )
    result = await db.execute(stmt)
    configs = result.scalars().all()
    
    # Transfer business type attributes for proper serialization
    for config in configs:
        if config.business_type:
            config.name = config.business_type.name
            config.description = config.business_type.description
            config.code = config.business_type.code
            config.related_words = config.business_type.related_words
            
    return configs

@router.get("/all", response_model=List[BusinessTypeConfigResponse])
async def get_all_business_type_configurations(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all business type configurations for a specific municipality.
    
    This endpoint returns all business types with their configuration flags and business type details.
    """
    municipality_id = current_user.municipality_id
    stmt = (
        select(BusinessTypeConfig)
        .join(BusinessType)
        .options(selectinload(BusinessTypeConfig.business_type))
        .where(BusinessTypeConfig.municipality_id == municipality_id)
    )
    result = await db.execute(stmt)
    configs = result.scalars().all()
    
    # Transfer business type attributes for proper serialization
    for config in configs:
        if config.business_type:
            config.name = config.business_type.name
            config.description = config.business_type.description
            config.code = config.business_type.code
            config.related_words = config.business_type.related_words
            
    return configs

@router.patch("/impact", response_model=BusinessTypeConfigResponse)
async def update_business_type_impact(
    data: BusinessTypeImpactRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin_or_director_role)
):
    """
    Update the impact level of a business type for the current municipality.

    This endpoint allows admins and directors to update the impact level
    of a specific business type configuration for their municipality.

    Requires admin or director privileges.
    """
    # First check if the business type exists
    stmt = select(BusinessType).where(BusinessType.id == data.business_type_id)
    result = await db.execute(stmt)
    business_type = result.scalar_one_or_none()

    if not business_type:
        raise HTTPException(
            status_code=404,
            detail=f"Business type with ID '{data.business_type_id}' not found"
        )

    # Check if configuration exists for this municipality
    stmt = select(BusinessTypeConfig).where(
        BusinessTypeConfig.business_type_id == data.business_type_id,
        BusinessTypeConfig.municipality_id == current_user.municipality_id
    ).options(selectinload(BusinessTypeConfig.business_type))
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()

    if config:
        config.impact_level = data.impact_level
    else:
        config = BusinessTypeConfig(
            business_type_id=data.business_type_id,
            municipality_id=current_user.municipality_id,
            impact_level=data.impact_level
        )
        db.add(config)

    await db.commit()
    await db.refresh(config)

    # Transfer business type attributes for proper serialization
    if not config.business_type:
        stmt = select(BusinessTypeConfig).where(
            BusinessTypeConfig.id == config.id
        ).options(selectinload(BusinessTypeConfig.business_type))
        result = await db.execute(stmt)
        config = result.scalar_one()
    
    if config.business_type:
        config.name = config.business_type.name
        config.description = config.business_type.description
        config.code = config.business_type.code
        config.related_words = config.business_type.related_words

    return config
