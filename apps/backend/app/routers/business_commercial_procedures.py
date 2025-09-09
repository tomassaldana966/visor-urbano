from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func, or_
from typing import List, Optional
import logging

from config.settings import get_sync_db as get_db
from app.models.procedures import Procedure
from app.models.business_license import BusinessLicense
from app.models.municipality import Municipality
from app.models.business_sectors import BusinessSector
from app.models.requirements_query import RequirementsQuery
from app.models.user import UserModel
from app.schemas.procedures import (
    BusinessCommercialProcedureRead,
    BusinessCommercialProcedureList
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
    user_role_id = getattr(current_user, 'role_id', None)
    is_superuser = getattr(current_user, 'is_superuser', False)
    
    logger.info(f"_apply_user_access_filters - user_id: {current_user.id}, role_name: {user_role_name}, role_id: {user_role_id}, is_superuser: {is_superuser}, municipality_id: {municipality_id}, filter_user_id: {user_id}")
    
    # If no role_name, try to get it from role_id
    if not user_role_name and user_role_id:
        from app.utils.role_validation import _get_role_name_by_id
        user_role_name = _get_role_name_by_id(user_role_id)
        logger.info(f"Derived role_name from role_id: {user_role_name}")
    
    # Directors and super admins can see everything
    if is_superuser or (user_role_name and user_role_name.lower() in [role.lower() for role in RolePermissions.ADMIN_ROLES]):
        logger.info(f"User has admin/superuser privileges - no restrictions")
        # Apply user filter if specifically requested
        if user_id:
            query = query.filter(Procedure.user_id == user_id)
        return query
    
    # Municipal admins/supervisors can see all procedures in their municipality
    elif user_role_name and user_role_name.lower() in [role.lower() for role in RolePermissions.SUPERVISOR_ROLES]:
        logger.info(f"User has supervisor privileges")
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
        # Regular users (including citizens, users, etc.) can only see their own procedures
        logger.info(f"User has regular privileges - filtering to own procedures only (user_id: {current_user.id})")
        if user_id and user_id != current_user.id:
            raise HTTPException(
                status_code=403, 
                detail="Access denied: You can only view your own procedures"
            )
        query = query.filter(Procedure.user_id == current_user.id)
        return query

@router.get("/", response_model=BusinessCommercialProcedureList)
def list_business_commercial_procedures(
    municipality_id: int = Query(..., description="Municipality ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    status: int = Query(1, description="Procedure status (1=active, 0=inactive)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    List business commercial procedures with address, municipality, and SCIAN information.
    
    Access control:
    - Super admins and directors: Can view all procedures across all municipalities
    - Municipal admins/supervisors: Can view all procedures in their assigned municipalities
    - Regular users: Can only view their own procedures
    
    This endpoint combines data from:
    - procedures (procedure information)
    - requirements_querys (business details, SCIAN codes, applicant info)
    - municipalities (municipality name)
    - business_sectors (SCIAN industry classification code)
    """
    try:
        logger.info(f"list_business_commercial_procedures called with: municipality_id={municipality_id}, user_id={user_id}, status={status}, skip={skip}, limit={limit}")
        logger.info(f"Current user: id={current_user.id}, role_id={getattr(current_user, 'role_id', None)}, role_name={getattr(current_user, 'role_name', None)}")
        
        base_query = db.query(
            Procedure,
            RequirementsQuery,
            Municipality,
            BusinessSector
        ).join(
            RequirementsQuery, 
            Procedure.requirements_query_id == RequirementsQuery.id,
            isouter=True
        ).join(
            Municipality,
            Procedure.municipality_id == Municipality.id,
            isouter=True
        ).join(
            BusinessSector,
            # Try to match by scian_code from RequirementsQuery to SCIAN
            func.lower(RequirementsQuery.scian_code) == func.lower(BusinessSector.industry_classification_code),
            isouter=True
        ).filter(
            and_(
                or_(
                    Procedure.procedure_type == 'business_license',
                    Procedure.procedure_type == 'giro comercial',
                    Procedure.procedure_type.like('%business_license%')
                ),
                Procedure.status == status,
                or_(
                    Procedure.municipality_id == municipality_id,
                    Procedure.project_municipality_id == municipality_id,
                    # Include procedures with NULL municipality_id for user's own procedures
                    and_(
                        Procedure.municipality_id.is_(None),
                        Procedure.project_municipality_id.is_(None)
                    )
                )
            )
        )
        
        # Apply user-based access control
        base_query = _apply_user_access_filters(base_query, current_user, municipality_id, user_id)
        
        # Log the SQL query for debugging
        logger.info(f"Final query before execution: {str(base_query)}")
        
        # Get total count
        total_count = base_query.count()
        logger.info(f"Total count found: {total_count}")
        
        # Get paginated results
        results = base_query.offset(skip).limit(limit).all()
        logger.info(f"Results retrieved: {len(results)} records")
        
        # Transform results to response schema
        procedures = []
        for procedure, requirements_query, municipality, business_sector in results:
            # Build full address from procedure
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
                
                # Address information from procedure
                "street": procedure.street,
                "exterior_number": procedure.exterior_number,
                "interior_number": procedure.interior_number,
                "neighborhood": procedure.neighborhood,
                "full_address": full_address,
                
                # Municipality information (fallback to procedure municipality_id if JOIN failed)
                "municipality_id": municipality.id if municipality else procedure.municipality_id,
                "municipality_name": municipality.name if municipality else (requirements_query.municipality_name if requirements_query else None),
                
                # Business sector information (SCIAN) - prioritize procedure data, fallback to RequirementsQuery
                "industry_classification_code": procedure.scian_code if procedure.scian_code else (requirements_query.scian_code if requirements_query else None),
                "business_line": procedure.scian_name if procedure.scian_name else (requirements_query.scian_name if requirements_query else None),
                "business_line_code": requirements_query.scian if requirements_query else None,
                
                # Business details - prioritize procedure data, fallback to RequirementsQuery
                "business_name": procedure.establishment_name if procedure.establishment_name else (requirements_query.applicant_name if requirements_query else None),
                "detailed_description": requirements_query.scian_name if requirements_query else None,
            }
            
            procedures.append(BusinessCommercialProcedureRead(**procedure_data))
        
        return BusinessCommercialProcedureList(
            procedures=procedures,
            total_count=total_count,
            skip=skip,
            limit=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving business commercial procedures: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while retrieving business commercial procedures."
        )

@router.get("/{procedure_id}", response_model=BusinessCommercialProcedureRead)
def get_business_commercial_procedure(
    procedure_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Get a specific business commercial procedure with all related information.
    
    Access control:
    - Super admins and directors: Can view any procedure
    - Municipal admins/supervisors: Can view procedures in their assigned municipalities
    - Regular users: Can only view their own procedures
    """
    try:
        result = db.query(
            Procedure,
            BusinessLicense,
            Municipality,
            BusinessSector
        ).join(
            BusinessLicense, 
            Procedure.folio == BusinessLicense.license_folio,
            isouter=True
        ).join(
            Municipality,
            Procedure.municipality_id == Municipality.id,
            isouter=True
        ).join(
            BusinessSector,
            func.lower(BusinessLicense.industry_classification_code) == func.lower(BusinessSector.industry_classification_code),
            isouter=True
        ).filter(
            Procedure.id == procedure_id
        ).first()
        
        if not result:
            raise HTTPException(status_code=404, detail="Business commercial procedure not found")
        
        procedure, business_license, municipality, business_sector = result
        
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
        
        # Build full address from procedure
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
            "full_address": full_address,
            
            # Municipality information
            "municipality_id": municipality.id if municipality else None,
            "municipality_name": municipality.name if municipality else None,
            
            # Business sector information (SCIAN)
            "industry_classification_code": business_sector.industry_classification_code if business_sector else None,
            "business_line": business_license.commercial_activity if business_license else None,
            "business_line_code": business_license.industry_classification_code if business_license else None,
            
            # Business details
            "business_name": business_license.owner if business_license else None,
            "detailed_description": business_license.commercial_activity if business_license else None,
        }
        
        return BusinessCommercialProcedureRead(**procedure_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving business commercial procedure {procedure_id}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while retrieving the business commercial procedure."
        )
