from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import logging

from config.settings import get_sync_db as get_db
from app.models.procedures import Procedure
from app.models.municipality import Municipality
from app.models.user import UserModel
from app.schemas.procedures import (
    ConstructionProcedureRead,
    ConstructionProcedureList
)
from config.security import get_current_user
from app.utils.role_validation import RolePermissions

router = APIRouter()
logger = logging.getLogger(__name__)

def _apply_user_access_filters(query, current_user: UserModel, municipality_id: int, user_id: Optional[int] = None):
    """
    Apply user-based access control filters to the query.
    
    Access rules:
    - Super admins and directors: Can see all procedures across all municipalities
    - Municipal admins/supervisors: Can see all procedures in their municipalities  
    - Regular users: Can only see their own procedures
    """
    # Check user's role name from role_name attribute or derive from role_id
    user_role_name = getattr(current_user, 'role_name', None)
    is_superuser = getattr(current_user, 'is_superuser', False)
    
    # Directors and super admins can see everything
    if is_superuser or (user_role_name and user_role_name.lower() in [role.lower() for role in RolePermissions.ADMIN_ROLES]):
        # Apply user filter if specifically requested
        if user_id:
            query = query.filter(Procedure.user_id == user_id)
        return query
    
    # Municipal admins/supervisors can see all procedures in their municipality
    elif user_role_name and user_role_name.lower() in [role.lower() for role in RolePermissions.SUPERVISOR_ROLES]:
        # Verify user has access to the requested municipality
        user_municipality_id = getattr(current_user, 'municipality_id', None)
        if user_municipality_id and user_municipality_id != municipality_id:
            raise HTTPException(
                status_code=403, 
                detail="Access denied: You don't have permission to view procedures for this municipality"
            )
        
        # Apply user filter if specifically requested  
        if user_id:
            query = query.filter(Procedure.user_id == user_id)
        return query
    
    else:
        # Regular users can only see their own procedures
        if user_id and user_id != current_user.id:
            raise HTTPException(
                status_code=403, 
                detail="Access denied: You can only view your own procedures"
            )
        query = query.filter(Procedure.user_id == current_user.id)
        return query

@router.get("/", response_model=ConstructionProcedureList)
def list_construction_procedures(
    municipality_id: int = Query(..., description="Municipality ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    status: int = Query(1, description="Procedure status (1=active, 0=inactive)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    List construction procedures with address and municipality information.
    
    Access control:
    - Super admins and directors: Can view all procedures across all municipalities
    - Municipal admins/supervisors: Can view all procedures in their assigned municipalities
    - Regular users: Can only view their own procedures
    
    This endpoint combines data from:
    - procedures (procedure information and address data)
    - municipalities (municipality name)
    """
    try:
        # Base query joining procedures with municipalities
        # Using the new municipality_id field for better consistency
        # Adding DISTINCT to avoid duplicates
        base_query = db.query(
            Procedure,
            Municipality
        ).join(
            Municipality,
            Procedure.municipality_id == Municipality.id,
            isouter=True
        ).filter(
            and_(
                Procedure.procedure_type.like('%permits_building_license%'),
                Procedure.status == status,
                # More inclusive filter to include procedures with NULL municipality_id
                # for citizen users who may have procedures without assigned municipality
                (Procedure.municipality_id == municipality_id) | 
                ((Procedure.municipality_id.is_(None)) & (Procedure.project_municipality_id.is_(None)))
            )
        ).distinct(Procedure.id)
         # Apply user-based access control
        base_query = _apply_user_access_filters(base_query, current_user, municipality_id, user_id)
        
        # Get total count
        total_count = base_query.count()
        
        # Get paginated results
        results = base_query.offset(skip).limit(limit).all()
        
        # Transform results to response schema
        procedures = []
        for procedure, municipality in results:
            # Build full address from procedure fields
            address_parts = []
            if procedure.street:
                address_parts.append(procedure.street)
            if procedure.exterior_number:
                address_parts.append(procedure.exterior_number)
            if procedure.interior_number:
                address_parts.append(f"Int. {procedure.interior_number}")
            full_address = " ".join(address_parts) if address_parts else None
            
            procedure_data = {
                # Procedure fields
                "id": procedure.id,
                "folio": procedure.folio,
                "current_step": procedure.current_step,
                "procedure_type": procedure.procedure_type,
                "license_status": procedure.license_status,
                "status": procedure.status,
                "procedure_start_date": procedure.procedure_start_date,
                "created_at": procedure.created_at,
                "updated_at": procedure.updated_at,
                "official_applicant_name": procedure.official_applicant_name,
                
                # Address information from procedures table
                "street": procedure.street,
                "exterior_number": procedure.exterior_number,
                "interior_number": procedure.interior_number,
                "neighborhood": procedure.neighborhood,
                "reference": procedure.reference,
                "full_address": full_address,
                
                # Municipality information
                "municipality_id": municipality.id if municipality else None,
                "municipality_name": municipality.name if municipality else None,
            }
            
            procedures.append(ConstructionProcedureRead(**procedure_data))
        
        return ConstructionProcedureList(
            procedures=procedures,
            total_count=total_count,
            skip=skip,
            limit=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving construction procedures: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while retrieving construction procedures."
        )

@router.get("/{procedure_id}", response_model=ConstructionProcedureRead)
def get_construction_procedure(
    procedure_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Get a specific construction procedure with all related information.
    
    Access control:
    - Super admins and directors: Can view any procedure
    - Municipal admins/supervisors: Can view procedures in their assigned municipalities
    - Regular users: Can only view their own procedures
    """
    try:
        result = db.query(
            Procedure,
            Municipality
        ).join(
            Municipality,
            Procedure.municipality_id == Municipality.id,
            isouter=True
        ).filter(
            and_(
                Procedure.id == procedure_id,
                Procedure.procedure_type.like('%construccion%')
            )
        ).first()
        
        if not result:
            raise HTTPException(status_code=404, detail="Construction procedure not found")
        
        procedure, municipality = result
        
        # Apply access control for the specific procedure
        user_role_name = getattr(current_user, 'role_name', None)
        is_superuser = getattr(current_user, 'is_superuser', False)
        
        # Directors and super admins can see everything
        if not (is_superuser or (user_role_name and user_role_name.lower() in [role.lower() for role in RolePermissions.ADMIN_ROLES])):
            # Municipal admins/supervisors can see procedures in their municipality
            if user_role_name and user_role_name.lower() in [role.lower() for role in RolePermissions.SUPERVISOR_ROLES]:
                user_municipality_id = getattr(current_user, 'municipality_id', None)
                if user_municipality_id and user_municipality_id != procedure.municipality_id:
                    raise HTTPException(
                        status_code=403, 
                        detail="Access denied: You don't have permission to view procedures for this municipality"
                    )
            else:
                # Regular users can only see their own procedures
                if procedure.user_id != current_user.id:
                    raise HTTPException(
                        status_code=403, 
                        detail="Access denied: You can only view your own procedures"
                    )
        
        # Build full address from procedure fields
        address_parts = []
        if procedure.street:
            address_parts.append(procedure.street)
        if procedure.exterior_number:
            address_parts.append(procedure.exterior_number)
        if procedure.interior_number:
            address_parts.append(f"Int. {procedure.interior_number}")
        full_address = " ".join(address_parts) if address_parts else None
        
        procedure_data = {
            # Procedure fields
            "id": procedure.id,
            "folio": procedure.folio,
            "current_step": procedure.current_step,
            "procedure_type": procedure.procedure_type,
            "license_status": procedure.license_status,
            "status": procedure.status,
            "procedure_start_date": procedure.procedure_start_date,
            "created_at": procedure.created_at,
            "updated_at": procedure.updated_at,
            "official_applicant_name": procedure.official_applicant_name,
            
            # Address information
            "street": procedure.street,
            "exterior_number": procedure.exterior_number,
            "interior_number": procedure.interior_number,
            "neighborhood": procedure.neighborhood,
            "reference": procedure.reference,
            "full_address": full_address,
            
            # Municipality information
            "municipality_id": municipality.id if municipality else None,
            "municipality_name": municipality.name if municipality else None,
        }
        
        return ConstructionProcedureRead(**procedure_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving construction procedure {procedure_id}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while retrieving the construction procedure."
        )
