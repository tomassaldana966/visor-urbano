from fastapi import APIRouter, Depends, HTTPException, Query, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from config.settings import get_db
from config.security import get_current_user
from typing import List
import base64
from datetime import datetime, timedelta, timezone
import logging


def get_utc_naive_now():
    """Get current UTC datetime as naive (for consistency with database storage)"""
    return datetime.now(timezone.utc).replace(tzinfo=None)

from app.models.requirements import Requirement
from app.models.requirements_query import RequirementsQuery
from app.models.procedures import Procedure
from app.models.municipality import Municipality
from app.schemas.requirements import (
    RequirementResponse,
    RequirementCreate,
    RequirementUpdate,
    RequirementValidationUpdate,
    FolioValidationResponse,
)

logger = logging.getLogger(__name__)
requirements = APIRouter()

@requirements.get("/", response_model=List[RequirementResponse])
async def list_requirements(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieves the list of requirements for the municipality assigned to the authenticated user.
    Supports pagination via the skip and limit parameters.
    """
    if not hasattr(current_user, 'municipality_id') or current_user.municipality_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no municipality assigned"
        )
    query = select(Requirement).where(
        Requirement.municipality_id == current_user.municipality_id
    ).offset(skip).limit(limit)
    result = await db.execute(query)
    requirements_list = result.scalars().all()
    return requirements_list

@requirements.get("/{requirement_id}", response_model=RequirementResponse)
async def get_requirement(
    requirement_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves information for a specific requirement by its ID.
    """
    result = await db.execute(select(Requirement).where(Requirement.id == requirement_id))
    requirement = result.scalars().first()
    if requirement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    return requirement

@requirements.post("/activate", response_model=dict, status_code=status.HTTP_202_ACCEPTED)
async def activate_requirement(
    requirement_data: RequirementCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Activates (creates) a new requirement for the municipality assigned to the authenticated user.
    """
    if not hasattr(current_user, 'municipality_id') or current_user.municipality_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no municipality assigned"
        )
    requirement_data.municipality_id = current_user.municipality_id
    new_requirement = Requirement(**requirement_data.model_dump())
    db.add(new_requirement)
    await db.commit()
    await db.refresh(new_requirement)
    return {"message": "Requirement activated successfully"}

@requirements.delete("/{requirement_id}/deactivate", status_code=status.HTTP_202_ACCEPTED)
async def deactivate_requirement(
    requirement_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Deactivates (deletes) a specific requirement by its ID.
    """
    result = await db.execute(select(Requirement).where(Requirement.id == requirement_id))
    requirement = result.scalars().first()
    if requirement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    await db.delete(requirement)
    await db.commit()
    return {"message": "Requirement deactivated successfully"}

@requirements.get("/validate/folio/{encoded_folio}", response_model=List[FolioValidationResponse])
async def validate_folio_requirements(
    encoded_folio: str = Path(..., description="Base64 encoded folio"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Validates the requirements associated with a base64-encoded folio.
    Checks the existence and validity of the folio and that the municipality allows online procedures.
    """
    try:
        decoded_folio = base64.b64decode(encoded_folio).decode('utf-8')
    except Exception as e:
        logger.warning(f"Invalid base64 folio received: {encoded_folio}, error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid folio encoding"
        )
    thirty_days_ago = get_utc_naive_now() - timedelta(days=30)
    query = select(RequirementsQuery).where(
        and_(
            RequirementsQuery.folio == decoded_folio,
            RequirementsQuery.created_at > thirty_days_ago
        )
    )
    result = await db.execute(query)
    requirements_queries = result.scalars().all()
    if not requirements_queries:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The procedure folio does not exist or is no longer valid. Enter a correct one or check the requirements again here"
        )
    first_query = requirements_queries[0]
    municipality_result = await db.execute(
        select(Municipality).where(Municipality.id == first_query.municipality_id)
    )
    municipality = municipality_result.scalars().first()
    if not municipality or not municipality.issue_license:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This municipality is not available for online procedures, so it is recommended to go to it to carry out the procedure and validate the validity of the requirements."
        )
    logger.info(f"User {current_user.id} started a new procedure for folio: {decoded_folio}")
    return [
        FolioValidationResponse(
            id=req.id,
            folio=req.folio,
            municipality_id=req.municipality_id,
            municipality_name=req.municipality_name,
            street=req.street,
            neighborhood=req.neighborhood,
            scian_code=req.scian_code,
            scian_name=req.scian_name,
            property_area=float(req.property_area),
            activity_area=float(req.activity_area),
            applicant_name=req.applicant_name,
            applicant_character=req.applicant_character,
            person_type=req.person_type,
            status=req.status,
            user_id=req.user_id,
            alcohol_sales=req.alcohol_sales,
            created_at=req.created_at
        ) for req in requirements_queries
    ]

@requirements.put("/validate/folio/{requirements_query_id}", response_model=dict)
async def update_folio_requirements(
    requirements_query_id: int,
    validation_data: RequirementValidationUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Updates the validation of the requirements for a folio and creates the procedure if it does not exist.
    Controls access according to the user's role.
    """
    user_role = getattr(current_user, 'role_id', 1) or 1
    query_result = await db.execute(
        select(RequirementsQuery).where(RequirementsQuery.id == requirements_query_id)
    )
    requirements_query = query_result.scalars().first()
    if not requirements_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirements query not found"
        )
    
    # Store original user_id for access check
    original_user_id = requirements_query.user_id
    
    procedure_result = await db.execute(
        select(Procedure).where(Procedure.folio == requirements_query.folio)
    )
    existing_procedures = procedure_result.scalars().all()  # Get ALL procedures with this folio
    
    if not existing_procedures:
        # No existing procedure, safe to create new one
        # Check if the folio is already in use by another user in requirements
        if original_user_id != 0 and original_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This folio is already in use by another user"
            )
        
        # Only update user_id when creating new procedure
        requirements_query.user_id = current_user.id
        await db.commit()
        
        new_procedure = Procedure(
            folio=requirements_query.folio,
            current_step=0,
            user_signature="",
            user_id=current_user.id if user_role == 1 else None,
            window_user_id=current_user.id if user_role > 1 else None,
            entry_role=user_role,
            procedure_start_date=get_utc_naive_now(),
            window_seen_date=get_utc_naive_now() if user_role > 1 else None,
            license_pdf="",
            status=1,
            requirements_query_id=requirements_query_id,
            # Copy information from requirements_query
            official_applicant_name=requirements_query.applicant_name,
            street=requirements_query.street,
            neighborhood=requirements_query.neighborhood,
            project_municipality_id=requirements_query.municipality_id
        )
        db.add(new_procedure)
        await db.commit()
        await db.refresh(new_procedure)
        logger.info(f"Created new procedure ID {new_procedure.id} for user {current_user.id} with folio {new_procedure.folio}")
        return {
            "message": "Procedure created successfully",
            "procedure_id": new_procedure.id,
            "folio": new_procedure.folio
        }
    elif len(existing_procedures) > 1:
        # Multiple procedures with same folio detected - this is a data integrity issue
        logger.error(f"Multiple procedures found with folio {requirements_query.folio}: {[p.id for p in existing_procedures]}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Data integrity issue: Multiple procedures exist with this folio. Please contact support."
        )
    else:
        # Exactly one existing procedure
        existing_procedure = existing_procedures[0]
        # Check if procedure belongs to current user or if user has admin privileges
        procedure_user_id = existing_procedure.user_id
        procedure_window_user_id = existing_procedure.window_user_id
        
        # Allow access if:
        # 1. Current user is the owner (user_id matches)
        # 2. Current user is a municipal user (role > 1) who created it (window_user_id matches)
        # 3. Current user has admin privileges (role > 1)
        has_access = False
        
        if user_role == 1:  # Citizen
            has_access = (procedure_user_id == current_user.id)
        else:  # Municipal user
            has_access = True  # Municipal users can access procedures in their municipality
        
        if has_access:
            logger.info(f"Granted access to existing procedure ID {existing_procedure.id} for user {current_user.id}")
            return {
                "message": "Procedure access granted",
                "procedure_id": existing_procedure.id,
                "folio": existing_procedure.folio
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this procedure - folio belongs to another user"
            )
