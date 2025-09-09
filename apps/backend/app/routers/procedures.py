# Standard library imports
import ast
import base64
import json
import logging
import os
import shutil
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path as PathLib
from typing import Any, Dict, List, Optional
from urllib.parse import unquote

# Third-party imports
from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, Path, Query, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.inspection import inspect
from jinja2 import Environment, FileSystemLoader
import weasyprint
import qrcode
from io import BytesIO
from app.models.requirements_query import RequirementsQuery
from app.models.answer import Answer

# Initialize Jinja2 environment at module level for better performance
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'licenses')
JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Local imports
from app.models.answer import Answer
from app.models.business_license import BusinessLicense
from app.models.business_type_config import BusinessTypeConfig
from app.models.business_types import BusinessType
from app.models.municipality import Municipality
from app.models.municipality_signature import MunicipalitySignature
from app.models.procedure_registrations import ProcedureRegistration
from app.models.procedures import HistoricalProcedure, Procedure
from app.models.requirements_query import RequirementsQuery
from app.models.user import UserModel
from app.schemas.procedures import ProcedureCreate, ProcedureRead
from app.services.dependency_assignment_service import DependencyAssignmentService
from app.services.procedure_notifications import send_license_download_notification, send_procedure_status_notification_sync
from app.utils.role_validation import validate_admin_or_director_role, has_procedure_approval_permissions
from config.security import get_current_user
from config.settings import get_db, settings

logger = logging.getLogger(__name__)

procedures = APIRouter()

ALLOWED_FILE_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024
UPLOAD_DIR = "uploads/payment_orders"
PROCEDURE_UPLOAD_DIR = "uploads/procedures"

def validate_base64_folio(encoded_folio: str) -> str:
    try:
        # First, URL decode in case it's URL encoded
        url_decoded = unquote(encoded_folio)
        
        # Then base64 decode
        decoded_bytes = base64.b64decode(url_decoded, validate=True)
        folio = decoded_bytes.decode("utf-8")
        if not folio or len(folio) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid folio format"
            )
        return folio
    except (base64.binascii.Error, UnicodeDecodeError, ValueError) as e:
        logger.warning(f"Invalid base64 folio received: {encoded_folio}, error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid folio encoding"
        )

def validate_file_upload(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    file_ext = PathLib(file.filename).suffix.lower()
    if file_ext not in ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_FILE_EXTENSIONS)}"
        )
    if hasattr(file, 'size') and file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024)}MB"
        )

async def get_procedure_by_folio(folio: str, db: AsyncSession, 
                               procedure_type: Optional[str] = None, current_user=None) -> Procedure:
    query = select(Procedure).where(Procedure.folio == folio)
    if procedure_type:
        query = query.where(Procedure.procedure_type == procedure_type)
    result = await db.execute(query)
    procedure = result.scalars().first()
    if not procedure:
        error_msg = "Procedure not found"
        if procedure_type:
            error_msg = f"{procedure_type.title()} procedure not found"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_msg
        )
    
    # Apply role-based access control for users with role_id = 1 (Citizen role)
    if current_user and hasattr(current_user, 'role_id') and current_user.role_id == 1:
        # Users with role_id = 1 can only access their own procedures
        if procedure.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only access your own procedures"
            )
    
    return procedure

async def determine_procedure_type(requirements_query_id: Optional[int], db: AsyncSession, folio: Optional[str] = None) -> Optional[str]:
    """
    Determine the procedure type based on the associated RequirementsQuery data and folio prefix.
    
    Args:
        requirements_query_id: ID of the RequirementsQuery record
        db: Database session
        folio: The folio string (used to check for construction prefixes)
    
    Returns:
        - "permits_building_license" for construction procedures
        - "business_license" for commercial procedures  
        - "business_license" as default for business-related activities
        - None if no requirements_query_id is provided
    """
    if not requirements_query_id:
        return None
    
    try:
        # First check if folio indicates construction procedure
        if folio:
            folio_upper = folio.upper()
            # Check for construction-related folio prefixes
            construction_prefixes = ["CONS-", "CONSTRUCCION-", "LICCONS-", "LIC-CONST-", "OBRA-"]
            if any(folio_upper.startswith(prefix) for prefix in construction_prefixes):
                return "permits_building_license"
        
        # Get the requirements query
        stmt = select(RequirementsQuery).filter(RequirementsQuery.id == requirements_query_id)
        result = await db.execute(stmt)
        query = result.scalar_one_or_none()
        
        if not query:
            logger.warning(f"RequirementsQuery with ID {requirements_query_id} not found")
            return None
        
        # Determine type based on SCIAN code and description
        scian_name_lower = (query.scian_name or "").lower()
        scian_code = query.scian_code or ""
        
        # Construction-related SCIAN codes typically start with 23 (Construction sector)
        if scian_code.startswith("23") or any(keyword in scian_name_lower for keyword in [
            "construccion", "construction", "edificacion", "obra", "infraestructura"
        ]):
            return "permits_building_license"
        
        # Most other cases are commercial/business activities
        # This includes retail, services, manufacturing, etc.
        return "business_license"
        
    except Exception as e:
        logger.error(f"Error determining procedure type for requirements_query_id {requirements_query_id}: {e}")
        return "business_license"  # Default to commercial

async def list_procedures_base(folio: Optional[str], db: AsyncSession, current_user=None) -> List[Procedure]:
    # Use eager loading to include municipality relationship
    query = select(Procedure).options(
        selectinload(Procedure.municipality),
        selectinload(Procedure.project_municipality)
    )
    
    # Apply role-based filtering for users with role_id = 1 (Citizen role)
    if current_user and hasattr(current_user, 'role_id') and current_user.role_id == 1:
        # Users with role_id = 1 can only see their own procedures
        query = query.where(Procedure.user_id == current_user.id)
    
    if folio:
        folio = folio.strip()
        if len(folio) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Folio filter too long"
            )
        query = query.where(Procedure.folio.ilike(f"%{folio}%"))
    
    result = await db.execute(query)
    procedures = result.scalars().all()
    
    return procedures

def convert_procedures_to_read(procedures: List[Procedure]) -> List[ProcedureRead]:
    """Convert Procedure objects to ProcedureRead with municipality_name populated"""
    result = []
    for procedure in procedures:
        procedure_dict = procedure.__dict__.copy()
        # Add municipality_name from the relationship
        if procedure.municipality:
            procedure_dict['municipality_name'] = procedure.municipality.name
        else:
            procedure_dict['municipality_name'] = None
        result.append(ProcedureRead(**procedure_dict))
    return result

async def is_procedure_complete_auto(procedure, db):
    """
    Checks if all required static and dynamic fields for a procedure are filled.
    If complete, automatically sets sent_to_reviewers to True.
    Returns True if complete, False otherwise.
    """
    # 1. Check static required fields (not nullable, not auto fields)
    insp = inspect(procedure.__class__)
    static_required = [
        c.name for c in insp.columns
        if not c.nullable and c.default is None and c.server_default is None
    ]
    # Exclude fields that are always filled by the system or not user-editable
    exclude_fields = {
        'id', 'created_at', 'updated_at', 'folio', 'user_id', 'municipality_id',
        'requirements_query_id', 'status', 'director_approval', 'sent_to_reviewers',
        'step_one', 'step_two', 'step_three', 'step_four', 'window_license_generated',
        'documents_submission_date', 'procedure_start_date', 'window_seen_date',
        'license_delivered_date', 'no_signature_date', 'sent_to_reviewers_date',
        'current_step', 'renewed_folio', 'entry_role', 'license_status', 'window_user_id',
        'business_type_id', 'project_municipality_id', 'payment_order', 'scian_name',
        'scian_code', 'business_line', 'last_resolution', 'resolution_sense',
    }
    static_required = [f for f in static_required if f not in exclude_fields]
    for field in static_required:
        value = getattr(procedure, field, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            return False

    # 2. Check dynamic required fields from RequirementsQuery
    rq_id = getattr(procedure, 'requirements_query_id', None)
    if rq_id:
        rq = await db.execute(
            select(RequirementsQuery).where(RequirementsQuery.id == rq_id)
        )
        rq_obj = rq.scalar_one_or_none()
        if rq_obj and hasattr(rq_obj, 'requirements'):
            # requirements is expected to be a list of dicts with 'name' and 'required' keys
            requirements = rq_obj.requirements
            if isinstance(requirements, str):
                import json
                try:
                    requirements = json.loads(requirements)
                except Exception:
                    requirements = []
            required_fields = [r['name'] for r in requirements if r.get('required')]
            if required_fields:
                # Get all answers for this procedure
                answers_q = await db.execute(
                    select(Answer).where(Answer.procedure_id == procedure.id)
                )
                answers = {a.name: a.value for a in answers_q.scalars().all()}
                for field in required_fields:
                    val = answers.get(field)
                    if val is None or (isinstance(val, str) and not val.strip()):
                        return False
    
    # If we reach here, the procedure is complete
    # Automatically set sent_to_reviewers to 1 if not already set
    if not procedure.sent_to_reviewers:
        try:
            procedure.sent_to_reviewers = 1  # Set to 1 instead of True for integer field
            # Set the date when sent to reviewers
            
            procedure.sent_to_reviewers_date = datetime.now(timezone.utc)
            
            # Commit the changes to the database
            await db.commit()
            await db.refresh(procedure)
            
            logger.info(f"Procedure {procedure.folio} automatically sent to reviewers - all requirements complete")
        except Exception as e:
            logger.error(f"Error updating sent_to_reviewers for procedure {procedure.folio}: {str(e)}")
            await db.rollback()
    
    return True

@procedures.get("/list", response_model=List[ProcedureRead])
async def list_procedures(folio: Optional[str] = Query(None), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    procedures = await list_procedures_base(folio, db, current_user)
    return convert_procedures_to_read(procedures)

@procedures.get("/director-review", response_model=List[ProcedureRead])
async def list_procedures_director_review(folio: Optional[str] = Query(None), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    procedures = await list_procedures_base(folio, db, current_user)
    return convert_procedures_to_read(procedures)

@procedures.get("/procedure-approvals", response_model=List[ProcedureRead])
async def list_procedure_approvals(
    folio: Optional[str] = Query(None), 
    page: Optional[int] = Query(1, ge=1, description="Page number"),
    per_page: Optional[int] = Query(20, ge=1, le=100, description="Items per page"),
    tab_filter: Optional[str] = Query(None, description="Filter by tab: business_licenses, permits_building_license, en_revisiones, prevenciones, desechados, en_ventanilla"),
    procedure_type: Optional[str] = Query(None, description="Filter by procedure type"),
    db: AsyncSession = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    """
    Get procedures requiring approval - restricted to users with role_id > 1
    Based on legacy analysis: supports tabs like 'En revisiones', 'Prevenciones', 'En ventanilla'
    """
    # Validate user has administrative privileges (role_id > 1)
    user_role_id = getattr(current_user, 'role_id', 1) or 1
    if user_role_id <= 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Administrative privileges required (role_id > 1)"
        )
    
    # Validate user has proper permissions for procedure approvals
    if not has_procedure_approval_permissions(current_user):
        user_role_id = getattr(current_user, 'role_id', 1) or 1
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: Insufficient privileges for procedure approvals (role_id: {user_role_id})"
        )
    
    # Build base query for procedures requiring approval with municipality join
    stmt = select(Procedure).options(joinedload(Procedure.municipality))
    
    # Apply municipality filter for non-admin users
    user_municipality_id = getattr(current_user, 'municipality_id', None)
    if user_municipality_id:
        stmt = stmt.where(Procedure.municipality_id == user_municipality_id)
    
    # Apply folio filter if provided
    if folio:
        stmt = stmt.where(Procedure.folio.ilike(f"%{folio}%"))
    
    # Apply procedure type filter if provided
    if procedure_type:
        stmt = stmt.where(Procedure.procedure_type == procedure_type)
    
    # Apply tab-based filtering
    if tab_filter:
        if tab_filter == "business_licenses":
            # Trámites comerciales (business licenses)
            stmt = stmt.where(
                Procedure.procedure_type.in_(['business_license', 'giro comercial'])
            )
        elif tab_filter == "permits_building_license":
            # Trámites de construcción (building permits)
            stmt = stmt.where(
                Procedure.procedure_type.in_(['permits_building_license', 'licencia construccion'])
            )
        elif tab_filter == "en_revisiones":
            # En revisiones - Procedures sent to reviewers but not yet reviewed
            stmt = stmt.where(
                Procedure.sent_to_reviewers == 1,
                Procedure.step_one.is_(None),
                Procedure.director_approval.is_(None)
            )
        elif tab_filter == "prevenciones":
            # Prevenciones - Procedures with prevention status (status = 3)
            stmt = stmt.where(
                Procedure.status == 3
            )
        elif tab_filter == "desechados":
            # Desechados - Rejected procedures (status = 2)
            stmt = stmt.where(
                Procedure.status == 2
            )
        elif tab_filter == "en_ventanilla":
            # En ventanilla - Ready for window processing
            stmt = stmt.where(
                Procedure.step_one == 1,
                Procedure.step_two == 1,
                Procedure.director_approval.is_(None)
            )
    else:
        # Default: show all procedures that have been sent to reviewers or are in process
        stmt = stmt.where(
            Procedure.sent_to_reviewers == 1
        )
    
    # Order by priority: newer submissions first, then by folio
    stmt = stmt.order_by(Procedure.sent_to_reviewers_date.desc(), Procedure.folio.asc())
    
    # Apply pagination
    offset = (page - 1) * per_page
    stmt = stmt.offset(offset).limit(per_page)
    
    # Execute query
    result = await db.execute(stmt)
    procedures_list = result.scalars().all()
    
    # Convert to ProcedureRead
    response = []
    for procedure in procedures_list:
        procedure_dict = procedure.__dict__.copy()
        
        # Add municipality name if available
        if hasattr(procedure, 'municipality') and procedure.municipality:
            procedure_dict['municipality_name'] = procedure.municipality.name
        else:
            procedure_dict['municipality_name'] = None
            
        # Add business line (use scian_name if available, otherwise procedure_type)
        procedure_dict['business_line'] = procedure.scian_name or procedure.procedure_type
        
        response.append(ProcedureRead(**procedure_dict))
    
    return response

@procedures.get("/window-list", response_model=List[ProcedureRead])
async def list_procedures_window(folio: Optional[str] = Query(None), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    procedures = await list_procedures_base(folio, db, current_user)
    return convert_procedures_to_read(procedures)

@procedures.get("/solvency", response_model=List[ProcedureRead])
async def list_procedures_solvency(folio: Optional[str] = Query(None), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    procedures = await list_procedures_base(folio, db, current_user)
    return convert_procedures_to_read(procedures)

@procedures.get("/licenses", response_model=List[ProcedureRead])
async def list_procedures_licenses(folio: Optional[str] = Query(None), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    procedures = await list_procedures_base(folio, db, current_user)
    return convert_procedures_to_read(procedures)

@procedures.post("/no-electronic-signature/{encoded_folio}", response_model=ProcedureRead)
async def no_electronic_signature(encoded_folio: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    folio = validate_base64_folio(encoded_folio)
    return await get_procedure_by_folio(folio, db, current_user=current_user)

@procedures.post("/continue/{encoded_folio}", response_model=ProcedureRead)
async def continue_procedure(encoded_folio: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    folio = validate_base64_folio(encoded_folio)
    return await get_procedure_by_folio(folio, db, current_user=current_user)

@procedures.post("/entry", response_model=ProcedureRead, status_code=status.HTTP_201_CREATED)
async def procedure_entry(
    payload: ProcedureCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        data = payload.model_dump()
        
        # Check for duplicate folio BEFORE creating the procedure
        if data.get('folio'):
            existing_procedures = await db.execute(
                select(Procedure).where(Procedure.folio == data['folio'])
            )
            existing_list = existing_procedures.scalars().all()
            if existing_list:
                logger.warning(f"Attempt to create duplicate procedure with folio {data['folio']} by user {current_user.id}")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"A procedure with folio '{data['folio']}' already exists..."
                )
        
        datetime_fields = [
            'documents_submission_date', 'procedure_start_date', 
            'window_seen_date', 'license_delivered_date', 
            'no_signature_date', 'sent_to_reviewers_date'
        ]
        for field in datetime_fields:
            value = data.get(field)
            if isinstance(value, datetime) and value.tzinfo is not None:
                data[field] = value.replace(tzinfo=None)
        id_fields = ['requirements_query_id', 'user_id', 'window_user_id']
        for field in id_fields:
            if data.get(field) == 0:
                data[field] = None
        
        # Ensure the procedure is always associated with the authenticated user
        # This is critical for the user to see their own procedures in "Mis Trámites"
        user_role = getattr(current_user, 'role_id', 1) or 1
        if user_role == 1:  # Citizen role
            data['user_id'] = current_user.id
            data['window_user_id'] = None
        else:  # Municipal user roles
            data['window_user_id'] = current_user.id
            # Keep the original user_id if provided, otherwise set to None
            if not data.get('user_id'):
                data['user_id'] = None
        
        # Automatically determine procedure_type if not provided
        if not data.get('procedure_type') and data.get('requirements_query_id'):
            determined_type = await determine_procedure_type(data['requirements_query_id'], db, data.get('folio'))
            if determined_type:
                data['procedure_type'] = determined_type
        
        # Process business type selection if provided
        if data.get('business_type_id'):
            business_type_id = data['business_type_id']
            
            # Get business type information to enhance procedure data
            try:
                
                stmt = select(BusinessType).join(
                    BusinessTypeConfig,
                    BusinessType.id == BusinessTypeConfig.business_type_id
                ).where(
                    BusinessTypeConfig.id == business_type_id
                )
                result = await db.execute(stmt)
                business_type = result.scalars().first()
                
                if business_type:
                    # Update procedure type based on business type if not already set
                    
                                            
                    # Update RequirementsQuery with business type information if available
                    if data.get('requirements_query_id'):
                        try:
                            req_stmt = select(RequirementsQuery).filter(RequirementsQuery.id == data['requirements_query_id'])
                            req_result = await db.execute(req_stmt)
                            req_query = req_result.scalar_one_or_none()
                            
                            if req_query:
                                # Update SCIAN information if business type has a code
                                if business_type.code and not req_query.scian_code:
                                    req_query.scian_code = business_type.code
                                    req_query.scian_name = business_type.name
                                
                                await db.flush()  # Flush changes to RequirementsQuery
                        except Exception as e:
                            logger.warning(f"Could not update RequirementsQuery with business type info: {e}")
                            
                else:
                    logger.warning(f"Business type with config ID {business_type_id} not found")
                    
            except Exception as e:
                logger.error(f"Error processing business type {business_type_id}: {e}")
                # Continue procedure creation even if business type processing fails
            
        # Remove business_type_id from data as it's not a direct Procedure field
        # Always remove it, whether or not it was found in the if block above
        data.pop('business_type_id', None)
        
        # Save requirements_query_id before removing it
        requirements_query_id = data.get('requirements_query_id')
        
        # Also remove any other fields that are not valid Procedure model fields
        # These might be coming from construction requirements or other sources
        # NOTE: Do NOT remove requirements_query_id as it's a valid field in the Procedure model
        invalid_fields = ['license_type', 'interested_party', 'scian', 'entry_date', 
                         'last_resolution', 'resolution_sense', 'municipality']
        for field in invalid_fields:
            data.pop(field, None)
        
        # Copy data from RequirementsQuery if requirements_query_id is provided
        if requirements_query_id:
            try:
                req_stmt = select(RequirementsQuery).filter(RequirementsQuery.id == requirements_query_id)
                req_result = await db.execute(req_stmt)
                req_query = req_result.scalar_one_or_none()
                
                if req_query:
                    # Copy applicant and address information
                    if req_query.applicant_name and not data.get('official_applicant_name'):
                        data['official_applicant_name'] = req_query.applicant_name
                    if req_query.street and not data.get('street'):
                        data['street'] = req_query.street
                    if req_query.neighborhood and not data.get('neighborhood'):
                        data['neighborhood'] = req_query.neighborhood
                    if req_query.municipality_id and not data.get('municipality_id'):
                        data['municipality_id'] = req_query.municipality_id
                    
                    # Copy business establishment information for commercial procedures
                    if data.get('procedure_type') == 'business_license' or data.get('procedure_type') == 'giro comercial':
                        # Use applicant_name as establishment_name if not already set
                        if req_query.applicant_name and not data.get('establishment_name'):
                            data['establishment_name'] = req_query.applicant_name
                        
                        # Set establishment area from activity_area
                        if req_query.activity_area and not data.get('establishment_area'):
                            data['establishment_area'] = str(req_query.activity_area)
                        
                        # Create full establishment address
                        if not data.get('establishment_address'):
                            address_parts = []
                            if req_query.street:
                                address_parts.append(req_query.street)
                            if req_query.neighborhood:
                                address_parts.append(req_query.neighborhood)
                            if req_query.municipality_name:
                                address_parts.append(req_query.municipality_name)
                            if address_parts:
                                data['establishment_address'] = ', '.join(address_parts)
                        
                        # Copy SCIAN information for business classification
                        if req_query.scian_code and not data.get('scian_code'):
                            data['scian_code'] = req_query.scian_code
                        if req_query.scian_name and not data.get('scian_name'):
                            data['scian_name'] = req_query.scian_name
                else:
                    logger.warning(f"RequirementsQuery with id {requirements_query_id} not found")
            except Exception as e:
                logger.warning(f"Could not copy data from requirements_query: {e}")
        
        # Ensure municipality_id is set - fallback to user's municipality_id if not set
        if not data.get('municipality_id') and hasattr(current_user, 'municipality_id') and current_user.municipality_id:
            data['municipality_id'] = current_user.municipality_id
        
        # Explicitly set initial workflow state for new procedures to ensure correct defaults
        if 'status' not in data:
            data['status'] = 0  # New procedures should start at status 0
        if 'director_approval' not in data:
            data['director_approval'] = 0
        if 'sent_to_reviewers' not in data:
            data['sent_to_reviewers'] = 0
        if 'step_one' not in data:
            data['step_one'] = 0
        if 'step_two' not in data:
            data['step_two'] = 0
        if 'step_three' not in data:
            data['step_three'] = 0
        if 'step_four' not in data:
            data['step_four'] = 0
        if 'window_license_generated' not in data:
            data['window_license_generated'] = 0
        
        logger.info(f"Creating procedure with explicit defaults: "
                   f"director_approval={data.get('director_approval')}, "
                   f"sent_to_reviewers={data.get('sent_to_reviewers')}, "
                   f"step_one={data.get('step_one')}, status={data.get('status')}")
        
        procedure = Procedure(**data)
        db.add(procedure)
        await db.commit()
        await db.refresh(procedure)
        

        
        # Copy answers from requirements_query to procedure BEFORE dependency assignment
        if requirements_query_id:
            try:
                logger.info(f"Copying answers from requirements_query_id {requirements_query_id} to procedure {procedure.id}")
                # Find answers associated with the requirements_query
                answers_stmt = select(Answer).where(
                    Answer.requirements_query_id == requirements_query_id,
                    Answer.procedure_id.is_(None)  # Only copy answers that haven't been copied yet
                )
                answers_result = await db.execute(answers_stmt)
                existing_answers = answers_result.scalars().all()
                
                if existing_answers:
                    logger.info(f"Found {len(existing_answers)} answers to copy for procedure {procedure.folio}")
                    # Update each answer to associate it with the new procedure
                    for answer in existing_answers:
                        answer.procedure_id = procedure.id
                        answer.user_id = current_user.id  # Associate with the authenticated user
                        answer.updated_at = datetime.now()
                        logger.debug(f"Copying answer: {answer.name} = {answer.value}")
                    
                    await db.commit()
                    logger.info(f"Successfully copied {len(existing_answers)} answers to procedure {procedure.folio}")
                else:
                    logger.info(f"No answers found for requirements_query_id {requirements_query_id}")
                    
            except Exception as e:
                logger.error(f"Error copying answers from requirements_query to procedure: {e}")
                # Don't fail the procedure creation if answer copying fails
                await db.rollback()
                # Re-commit the procedure
                await db.commit()
        
        # Automatically assign dependency reviewers if procedure requires review
        try:
            logger.info(f"Starting dependency assignment process for procedure {procedure.folio} (type: {procedure.procedure_type})")
            
            # Check if this procedure type should trigger dependency reviews
            should_assign_dependencies = True  # Most procedures need dependency review
            
            # Skip dependency assignment for simple procedures
            skip_types = ['consulta_requisitos', 'requirements_query', 'information_only']
            if procedure.procedure_type and any(skip in procedure.procedure_type.lower() for skip in skip_types):
                should_assign_dependencies = False
                logger.info(f"Skipping dependency assignment for procedure type: {procedure.procedure_type}")
            
            if should_assign_dependencies:
                logger.info(f"Assigning dependencies to procedure {procedure.folio} (municipality_id: {procedure.municipality_id})")
                

                
                assigned_reviews = await DependencyAssignmentService.assign_dependencies_to_procedure(
                    db, procedure
                )
                
                logger.info(f"Dependency assignment returned {len(assigned_reviews)} reviews for procedure {procedure.folio}")
                
                # Log details of each assigned review
                for review in assigned_reviews:
                    logger.info(f"Created dependency review - ID: {review.id}, Department: {review.department_id}, Role: {review.role}, Folio: {review.folio}")
                
                # Also assign director review if needed
                logger.info(f"Checking if director review is needed for procedure {procedure.folio}")
                director_review = await DependencyAssignmentService.assign_director_review(
                    db, procedure
                )
                
                if director_review:
                    logger.info(f"Created director review - ID: {director_review.id}, Folio: {director_review.folio}")
                else:
                    logger.info(f"No director review needed for procedure {procedure.folio}")
                
                total_assigned = len(assigned_reviews)
                if director_review:
                    total_assigned += 1
                    
                logger.info(f"Successfully assigned {total_assigned} dependency reviews to procedure {procedure.folio}")
                
                # Verify notifications were sent by checking for users in the assigned departments
                for review in assigned_reviews:
                    if review.department_id:
                        logger.info(f"Verifying users assigned to department {review.department_id} for notifications")
            else:
                logger.info(f"Skipping dependency assignment for procedure type: {procedure.procedure_type}")
                
        except Exception as e:
            # Log the error but don't fail the procedure creation
            logger.error(f"Failed to assign dependencies to procedure: {str(e)}")
            logger.error(f"Exception details: {type(e).__name__}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Rollback any dependency-related changes but keep the procedure
            await db.rollback()
            # Re-commit the procedure creation if it was rolled back
            try:
                await db.commit()
            except Exception as commit_error:
                logger.error(f"Error re-committing procedure after dependency error: {commit_error}")
            # The procedure is still created successfully even if dependency assignment fails
        
        # Refresh the procedure object and detach it from session to avoid serialization issues
        try:
            await db.refresh(procedure)
            # Detach the object from the session to prevent SQLAlchemy session issues during serialization
            db.expunge(procedure)
        except Exception as refresh_error:
            logger.warning(f"Could not refresh procedure before return: {refresh_error}")
            # If refresh fails, try to get a fresh copy
            try:
                fresh_procedure = await db.execute(
                    select(Procedure).where(Procedure.id == procedure.id)
                )
                procedure = fresh_procedure.scalars().first()
                if procedure:
                    db.expunge(procedure)
            except Exception as fresh_error:
                logger.error(f"Could not get fresh procedure copy: {fresh_error}")
        
        return procedure
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating procedure: {e}")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Exception args: {e.args}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create procedure"
        )

@procedures.post("/renewal-entry", response_model=ProcedureRead, status_code=status.HTTP_201_CREATED)
async def procedure_renewal_entry(payload: ProcedureCreate, db: AsyncSession = Depends(get_db)):
    try:
        data = payload.model_dump()
        data['procedure_type'] = 'refrendo'
        datetime_fields = [
            'documents_submission_date', 'procedure_start_date', 
            'window_seen_date', 'license_delivered_date', 
            'no_signature_date', 'sent_to_reviewers_date'
        ]
        for field in datetime_fields:
            value = data.get(field)
            if isinstance(value, datetime) and value.tzinfo is not None:
                data[field] = value.replace(tzinfo=None)
        id_fields = ['requirements_query_id', 'user_id', 'window_user_id']
        for field in id_fields:
            if data.get(field) == 0:
                data[field] = None
        procedure = Procedure(**data)
        db.add(procedure)
        await db.commit()
        await db.refresh(procedure)
        return procedure
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating renewal procedure: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create renewal procedure"
        )

@procedures.post("/upload-payment-order/{id}", response_model=ProcedureRead)
async def upload_payment_order(
    id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    if id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid procedure ID"
        )
    result = await db.execute(select(Procedure).where(Procedure.id == id))
    procedure = result.scalars().first()
    if not procedure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Procedure not found"
        )
    validate_file_upload(file)
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_ext = PathLib(file.filename).suffix.lower()
        filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        total_size = 0
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(8192):
                total_size += len(chunk)
                if total_size > MAX_FILE_SIZE:
                    buffer.close()
                    os.unlink(file_path)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024)}MB"
                    )
                buffer.write(chunk)
        procedure.payment_order = file_path
        await db.commit()
        await db.refresh(procedure)
        logger.info(f"Uploaded payment order for procedure {id}: {filename}")
        return procedure
    except HTTPException:
        raise
    except Exception as e:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.unlink(file_path)
        await db.rollback()
        logger.error(f"Error uploading payment order for procedure {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload payment order"
        )

@procedures.get("/history", response_model=List[ProcedureRead])
async def get_procedure_history(folio: Optional[str] = Query(None), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    query = select(Procedure).where(Procedure.renewed_folio.isnot(None))
    
    # Apply role-based filtering for users with role_id = 1 (Citizen role)
    if current_user and hasattr(current_user, 'role_id') and current_user.role_id == 1:
        # Users with role_id = 1 can only see their own procedures
        query = query.where(Procedure.user_id == current_user.id)
    
    if folio:
        folio = folio.strip()
        if len(folio) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Folio filter too long"
            )
        query = query.where(Procedure.folio.ilike(f"%{folio}%"))
    result = await db.execute(query)
    return result.scalars().all()

@procedures.get("/applicant-name/{folio}")
async def get_applicant_name(folio: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not folio or len(folio) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid folio"
        )
    procedure = await get_procedure_by_folio(folio, db, current_user=current_user)
    return {"applicant_name": procedure.official_applicant_name}

@procedures.get("/applicant-name-renewal/{folio}")
async def get_applicant_name_renewal(folio: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not folio or len(folio) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid folio"
        )
    procedure = await get_procedure_by_folio(folio, db, procedure_type="refrendo", current_user=current_user)
    return {"applicant_name": procedure.official_applicant_name}

@procedures.get("/owner-name/{folio}")
async def get_owner_name(folio: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not folio or len(folio) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid folio"
        )
    procedure = await get_procedure_by_folio(folio, db, current_user=current_user)
    return {"owner_name": procedure.official_applicant_name}

@procedures.get("/owner-data/{folio}")
async def get_owner_data(folio: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not folio or len(folio) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid folio"
        )
    procedure = await get_procedure_by_folio(folio, db, current_user=current_user)
    return {
        "owner_name": procedure.official_applicant_name,
        "user_id": procedure.user_id,
        "window_user_id": procedure.window_user_id,
        "entry_role": procedure.entry_role,
        "license_status": procedure.license_status,
        "procedure_type": procedure.procedure_type,
    }

@procedures.get("/owner-data-renewal/{folio}")
async def get_owner_data_renewal(folio: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not folio or len(folio) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid folio"
        )
    procedure = await get_procedure_by_folio(folio, db, procedure_type="refrendo", current_user=current_user)
    return {
        "owner_name": procedure.official_applicant_name,
        "user_id": procedure.user_id,
        "window_user_id": procedure.window_user_id,
        "entry_role": procedure.entry_role,
        "license_status": procedure.license_status,
        "procedure_type": procedure.procedure_type,
        "renewed_folio": procedure.renewed_folio,
    }

@procedures.get("/answer/{procedure_id}/{question_name}")
async def get_procedure_answer(procedure_id: int, question_name: str, db: AsyncSession = Depends(get_db)):
    if procedure_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid procedure ID"
        )
    if not question_name or len(question_name) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid question name"
        )
    query = select(Answer).where(
        Answer.procedure_id == procedure_id,
        Answer.name == question_name  
    )
    result = await db.execute(query)
    answer = result.scalars().first()
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found for this question and procedure"
        )
    return {"value": answer.value}

@procedures.post("/copy/{encoded_folio}/{user_id}", response_model=ProcedureRead, status_code=status.HTTP_201_CREATED)
async def copy_procedure(encoded_folio: str, user_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    # Decode the folio
    decoded_folio = validate_base64_folio(encoded_folio)
    
    try:
        # Get the original procedure (this will check access for role_id = 1 users)
        original = await get_procedure_by_folio(decoded_folio, db, current_user=current_user)
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Original procedure not found"
            )
        raise
    
    try:
        # Copy the data
        data = {}
        # Only copy actual column attributes from table metadata
        col_keys = [column.name for column in Procedure.__table__.columns]
        for key in col_keys:
            if key not in {"id", "created_at", "updated_at"}:
                data[key] = getattr(original, key)
        
        # Generate new folio and assign to user
        new_folio = f"COPY-{str(uuid.uuid4())[:8].upper()}"
        data["folio"] = new_folio
        data["user_id"] = user_id
        
        # Reset procedure state for new copy
        data["current_step"] = 1
        data["status"] = 1
        data["step_one"] = 0
        data["step_two"] = 0
        data["step_three"] = 0
        data["step_four"] = 0
        data["director_approval"] = 0
        data["window_license_generated"] = 0
        
        # Clear workflow dates
        data["documents_submission_date"] = None
        data["procedure_start_date"] = None
        data["window_seen_date"] = None
        data["license_delivered_date"] = None
        data["no_signature_date"] = None
        data["sent_to_reviewers_date"] = None
        
        new_procedure = Procedure(**data)
        db.add(new_procedure)
        await db.commit()
        await db.refresh(new_procedure)
        logger.info(f"Copied procedure {original.folio} to new procedure {new_procedure.folio}")
        return new_procedure
    except Exception as e:
        await db.rollback()
        logger.error(f"Error copying procedure {decoded_folio}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to copy procedure: {e}"
        )

@procedures.post("/copy-historical/{historical_id}", response_model=ProcedureRead, status_code=status.HTTP_201_CREATED)
async def copy_historical_procedure(historical_id: int, db: AsyncSession = Depends(get_db)):
    if historical_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid historical procedure ID"
        )
    
    # Get the historical procedure
    result = await db.execute(select(HistoricalProcedure).where(HistoricalProcedure.id == historical_id))
    historical = result.scalars().first()
    if not historical:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Historical procedure not found"
        )
    
    try:
        # Copy the data
        data = {}
        for key, value in historical.__dict__.items():
            if key not in {"id", "_sa_instance_state", "created_at", "updated_at"}:
                data[key] = value
        
        # Generate new folio 
        new_folio = f"HIST-{str(uuid.uuid4())[:8].upper()}"
        data["folio"] = new_folio
        
        # Reset procedure state for new copy
        data["current_step"] = 1
        data["status"] = 1
        data["step_one"] = 0
        data["step_two"] = 0
        data["step_three"] = 0
        data["step_four"] = 0
        data["director_approval"] = 0
        data["window_license_generated"] = 0
        
        # Clear workflow dates 
        data["documents_submission_date"] = None
        data["procedure_start_date"] = None
        data["window_seen_date"] = None
        data["license_delivered_date"] = None
        data["no_signature_date"] = None
        data["sent_to_reviewers_date"] = None
        
        new_procedure = Procedure(**data)
        db.add(new_procedure)
        await db.commit()
        await db.refresh(new_procedure)
        logger.info(f"Copied historical procedure {historical_id} to new procedure {new_procedure.folio}")
        return new_procedure
    except Exception as e:
        await db.rollback()
        logger.error(f"Error copying historical procedure {historical_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to copy historical procedure"
        )

@procedures.get("/historical-list", response_model=List[ProcedureRead], status_code=status.HTTP_200_OK)
async def list_historical_procedures(db: AsyncSession = Depends(get_db)):
    """
    List all archived historical procedures.
    """
    result = await db.execute(select(HistoricalProcedure))
    return result.scalars().all()

@procedures.patch("/{id}", response_model=ProcedureRead)
async def update_procedure(
    id: int, 
    data: dict, 
    db: AsyncSession = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    """
    Update procedure data by ID.
    Allows updating specific fields of a procedure.
    """
    if id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid procedure ID"
        )
    
    try:
        # Get the existing procedure
        result = await db.execute(select(Procedure).where(Procedure.id == id))
        procedure = result.scalar_one_or_none()
        
        if not procedure:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Procedure not found"
            )
        
        # Apply role-based access control for users with role_id = 1 (Citizen role)
        if current_user and hasattr(current_user, 'role_id') and current_user.role_id == 1:
            # Users with role_id = 1 can only update their own procedures
            if procedure.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: You can only update your own procedures"
                )
        
        # Process the updates
        updated_fields = []
        dynamic_fields_updates = []
        
        for field_name, field_value in data.items():
            # Skip invalid or protected fields
            if field_name in ['id', 'created_at', 'updated_at']:
                continue
            
            # Handle dynamic fields (they start with "dynamic_")
            if field_name.startswith('dynamic_'):
                # Remove the "dynamic_" prefix to get the actual field name
                actual_field_name = field_name.replace('dynamic_', '')
                dynamic_fields_updates.append({
                    'name': actual_field_name,
                    'value': field_value
                })
                logger.info(f"Dynamic field update: {actual_field_name} = {field_value}")
                continue
                
            # Check if the field exists in the model
            if hasattr(Procedure, field_name):
                # Handle datetime fields
                if field_name in [
                    'documents_submission_date', 'procedure_start_date', 
                    'window_seen_date', 'license_delivered_date', 
                    'no_signature_date', 'sent_to_reviewers_date'
                ]:
                    if isinstance(field_value, str):
                        try:
                            field_value = datetime.fromisoformat(field_value.replace('Z', '+00:00'))
                            if field_value.tzinfo is not None:
                                field_value = field_value.replace(tzinfo=None)
                        except ValueError:
                            logger.warning(f"Invalid datetime format for {field_name}: {field_value}")
                            continue
                
                # Update the field
                setattr(procedure, field_name, field_value)
                updated_fields.append(field_name)
        
        # Handle dynamic fields updates in the Answer table
        if dynamic_fields_updates:
            for field_update in dynamic_fields_updates:
                field_name = field_update['name']
                field_value = field_update['value']
                
                # Check if an answer already exists for this procedure and field
                existing_answer = await db.execute(
                    select(Answer).where(
                        Answer.procedure_id == procedure.id,
                        Answer.name == field_name
                    )
                )
                answer = existing_answer.scalar_one_or_none()
                
                if answer:
                    # Update existing answer
                    answer.value = field_value
                    logger.info(f"Updated existing answer: {field_name} = {field_value}")
                else:
                    # Create new answer
                    new_answer = Answer(
                        procedure_id=procedure.id,
                        name=field_name,
                        value=field_value,
                        user_id=current_user.id,
                        status=1
                    )
                    db.add(new_answer)
                    logger.info(f"Created new answer: {field_name} = {field_value}")
        
        if updated_fields or dynamic_fields_updates:
            await db.commit()
            await db.refresh(procedure)
            logger.info(f"Updated procedure {id} - regular fields: {updated_fields}, dynamic fields: {len(dynamic_fields_updates)} by user {current_user.id}")
        else:
            logger.info(f"No valid fields to update for procedure {id}")
        
        # Get municipality name if municipality_id exists
        municipality_name = None
        if procedure.municipality_id:
            municipality_result = await db.execute(
                select(Municipality.name).where(Municipality.id == procedure.municipality_id)
            )
            municipality_name = municipality_result.scalar_one_or_none()
        
        # Create response dict with municipality name as string
        response_data = {
            **{c.name: getattr(procedure, c.name) for c in procedure.__table__.columns},
            'municipality': municipality_name
        }
                
        if await is_procedure_complete_auto(procedure, db):
            if procedure.status != 1:
                procedure.status = 1
                await db.commit()
                await db.refresh(procedure)
        
        return response_data
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating procedure {id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update procedure"
        )


@procedures.patch("/by_folio/{encoded_folio}", response_model=ProcedureRead)
async def update_procedure_by_folio(
    encoded_folio: str, 
    data: dict, 
    db: AsyncSession = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    """
    Update procedure data by folio.
    Convenient endpoint for updating procedures when you only have the folio.
    """
    # Decode base64 folio like other endpoints
    folio = validate_base64_folio(encoded_folio)
    logger.info(f"Update procedure by folio - Encoded: {encoded_folio}, Decoded: {folio}")
    logger.info(f"Update data received: {data}")
    
    if not folio or len(folio) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid folio"
        )
    
    try:
        # Get the procedure by folio (this already includes access control)
        procedure = await get_procedure_by_folio(folio, db, current_user=current_user)
        logger.info(f"Found procedure {procedure.id} for folio {folio}")
        
        # Process the updates
        updated_fields = []
        dynamic_fields_updates = []
        
        for field_name, field_value in data.items():
            # Skip invalid or protected fields
            if field_name in ['id', 'created_at', 'updated_at']:
                continue
            
            # Handle dynamic fields (they start with "dynamic_")
            if field_name.startswith('dynamic_'):
                # Remove the "dynamic_" prefix to get the actual field name
                actual_field_name = field_name.replace('dynamic_', '')
                dynamic_fields_updates.append({
                    'name': actual_field_name,
                    'value': field_value
                })
                logger.info(f"Dynamic field update: {actual_field_name} = {field_value}")
                continue
                
            # Check if the field exists in the model
            if hasattr(Procedure, field_name):
                # Handle datetime fields
                if field_name in [
                    'documents_submission_date', 'procedure_start_date', 
                    'window_seen_date', 'license_delivered_date', 
                    'no_signature_date', 'sent_to_reviewers_date'
                ]:
                    if isinstance(field_value, str):
                        try:
                            field_value = datetime.fromisoformat(field_value.replace('Z', '+00:00'))
                            if field_value.tzinfo is not None:
                                field_value = field_value.replace(tzinfo=None)
                        except ValueError:
                            logger.warning(f"Invalid datetime format for {field_name}: {field_value}")
                            continue
                
                # Update the field
                setattr(procedure, field_name, field_value)
                updated_fields.append(field_name)
        
        # Handle dynamic fields updates in the Answer table
        if dynamic_fields_updates:
            for field_update in dynamic_fields_updates:
                field_name = field_update['name']
                field_value = field_update['value']
                
                # Check if an answer already exists for this procedure and field
                existing_answer = await db.execute(
                    select(Answer).where(
                        Answer.procedure_id == procedure.id,
                        Answer.name == field_name
                    )
                )
                answer = existing_answer.scalar_one_or_none()
                
                if answer:
                    # Update existing answer
                    answer.value = field_value
                    logger.info(f"Updated existing answer: {field_name} = {field_value}")
                else:
                    # Create new answer
                    new_answer = Answer(
                        procedure_id=procedure.id,
                        name=field_name,
                        value=field_value,
                        user_id=current_user.id,
                        status=1
                    )
                    db.add(new_answer)
                    logger.info(f"Created new answer: {field_name} = {field_value}")
        
        if updated_fields or dynamic_fields_updates:
            await db.commit()
            await db.refresh(procedure)
            logger.info(f"Updated procedure {folio} - regular fields: {updated_fields}, dynamic fields: {len(dynamic_fields_updates)} by user {current_user.id}")
        else:
            logger.info(f"No valid fields to update for procedure {folio}")
        
        # Get municipality name if municipality_id exists
        municipality_name = None
        if procedure.municipality_id:
            municipality_result = await db.execute(
                select(Municipality.name).where(Municipality.id == procedure.municipality_id)
            )
            municipality_name = municipality_result.scalar_one_or_none()
        
        # Create response dict with municipality name as string
        response_data = {
            **{c.name: getattr(procedure, c.name) for c in procedure.__table__.columns},
            'municipality': municipality_name
        }
        
        
        if await is_procedure_complete_auto(procedure, db):
            if procedure.status != 1:
                procedure.status = 1
                await db.commit()
                await db.refresh(procedure)
        
        return response_data
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating procedure {folio}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update procedure"
        )

@procedures.post("/update_answers/{encoded_folio}")
async def update_procedure_answers(
    encoded_folio: str = Path(..., description="Base64 encoded folio"),
    answers_data: Dict[str, Any] = Body(..., description="Field answers to update"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Update or create answers for a procedure by folio.
    This endpoint handles dynamic field data that should be stored in the Answer table.
    """
    try:
        # Decode the folio
        try:
            folio = base64.b64decode(encoded_folio).decode("utf-8")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid base64 encoded folio"
            )
        
        # Get the procedure
        procedure = await get_procedure_by_folio(folio, db, current_user=current_user)
        if not procedure:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Procedure not found"
            )
        
        logger.info(f"Updating answers for procedure {procedure.id} (folio: {folio})")
        logger.info(f"Answers data: {answers_data}")
        
        # Update or create each answer
        updated_count = 0
        created_count = 0
        
        for field_name, field_value in answers_data.items():
            if field_value is not None and field_value != '':
                # Check if answer already exists
                stmt = select(Answer).where(
                    Answer.procedure_id == procedure.id,
                    Answer.name == field_name
                )
                result = await db.execute(stmt)
                all_answers = result.scalars().all()  # Get all matching answers first
                
                if len(all_answers) > 1:
                    logger.warning(f"Found {len(all_answers)} duplicate answers for field '{field_name}' in procedure {procedure.id}")
                    # Keep the first one and delete the rest
                    for duplicate in all_answers[1:]:
                        await db.delete(duplicate)
                        logger.info(f"Deleted duplicate answer with id {duplicate.id}")
                
                existing_answer = all_answers[0] if all_answers else None  # Take the first one
                
                if existing_answer:
                    # Update existing answer
                    # For file objects, store as JSON string
                    if isinstance(field_value, dict) and 'name' in field_value and 'size' in field_value:
                        # This is a file metadata object, store as JSON
                        existing_answer.value = json.dumps(field_value)
                        logger.info(f"Updated file answer: {field_name} = {field_value.get('name', 'unknown')}")
                    else:
                        # Regular field, store as string
                        existing_answer.value = str(field_value)
                        logger.info(f"Updated answer: {field_name} = {field_value}")
                    
                    existing_answer.user_id = current_user.id
                    updated_count += 1
                else:
                    # Create new answer
                    # For file objects, store as JSON string
                    if isinstance(field_value, dict) and 'name' in field_value and 'size' in field_value:
                        # This is a file metadata object, store as JSON
                        value_to_store = json.dumps(field_value)
                        logger.info(f"Created file answer: {field_name} = {field_value.get('name', 'unknown')}")
                    else:
                        # Regular field, store as string
                        value_to_store = str(field_value)
                        logger.info(f"Created answer: {field_name} = {field_value}")
                    
                    new_answer = Answer(
                        procedure_id=procedure.id,
                        name=field_name,
                        value=value_to_store,
                        user_id=current_user.id
                    )
                    db.add(new_answer)
                    created_count += 1
        
        # Commit the changes
        await db.commit()
        
        logger.info(f"Successfully updated {updated_count} and created {created_count} answers for procedure {procedure.id}")
        
        return {
            "success": True,
            "message": f"Updated {updated_count} and created {created_count} answers",
            "procedure_id": procedure.id,
            "folio": folio
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating answers for folio {encoded_folio}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update procedure answers"
        )

@procedures.post("/upload_documents/{encoded_folio}")
async def upload_procedure_documents(
    encoded_folio: str = Path(..., description="Base64 encoded folio"),
    files: List[UploadFile] = File(..., description="Documents to upload"),
    field_names: str = Form(..., description="Comma-separated field names corresponding to files"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Upload documents for a procedure and store file paths in the Answer table.
    This endpoint handles file uploads for dynamic document fields.
    """
    try:
        # Decode the folio
        try:
            folio = base64.b64decode(encoded_folio).decode("utf-8")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid base64 encoded folio"
            )
        
        # Get the procedure
        procedure = await get_procedure_by_folio(folio, db, current_user=current_user)
        if not procedure:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Procedure not found"
            )
        
        logger.info(f"Uploading documents for procedure {procedure.id} (folio: {folio})")
        
        # Parse field names
        field_name_list = [name.strip() for name in field_names.split(',')]
        
        if len(files) != len(field_name_list):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Number of files must match number of field names"
            )
        
        logger.info(f"Files to upload: {field_name_list}")
        
        uploaded_files = {}
        upload_count = 0
        
        # Create upload directory for this procedure
        procedure_upload_dir = os.path.join(PROCEDURE_UPLOAD_DIR, f"procedure_{procedure.id}")
        os.makedirs(procedure_upload_dir, exist_ok=True)
        
        for i, (field_name, file) in enumerate(zip(field_name_list, files)):
            if file and file.filename:
                # Validate the file
                validate_file_upload(file)
                
                try:
                    # Generate unique filename
                    file_ext = PathLib(file.filename).suffix.lower()
                    unique_filename = f"{field_name}_{uuid.uuid4().hex}{file_ext}"
                    file_path = os.path.join(procedure_upload_dir, unique_filename)
                    
                    # Save the file
                    total_size = 0
                    with open(file_path, "wb") as buffer:
                        while chunk := await file.read(8192):
                            total_size += len(chunk)
                            if total_size > MAX_FILE_SIZE:
                                buffer.close()
                                os.unlink(file_path)
                                raise HTTPException(
                                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                                    detail=f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024)}MB"
                                )
                            buffer.write(chunk)
                    
                    # Store file metadata in Answer table
                    file_metadata = {
                        "filename": file.filename,
                        "original_name": file.filename,
                        "file_path": file_path,
                        "size": total_size,
                        "content_type": file.content_type
                    }
                    
                    # Check if answer already exists
                    stmt = select(Answer).where(
                        Answer.procedure_id == procedure.id,
                        Answer.name == field_name
                    )
                    result = await db.execute(stmt)
                    existing_answer = result.scalars().first()
                    
                    if existing_answer:
                        # Update existing answer
                        existing_answer.value = json.dumps(file_metadata)
                        existing_answer.user_id = current_user.id
                        logger.info(f"Updated document answer: {field_name}")
                    else:
                        # Create new answer
                        new_answer = Answer(
                            procedure_id=procedure.id,
                            name=field_name,
                            value=json.dumps(file_metadata),
                            user_id=current_user.id
                        )
                        db.add(new_answer)
                        logger.info(f"Created document answer: {field_name}")
                    
                    uploaded_files[field_name] = {
                        "filename": file.filename,
                        "size": total_size,
                        "file_path": file_path
                    }
                    upload_count += 1
                    
                except Exception as file_error:
                    # Clean up file if upload failed
                    if 'file_path' in locals() and os.path.exists(file_path):
                        os.unlink(file_path)
                    logger.error(f"Error uploading file {field_name}: {file_error}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Failed to upload file {field_name}: {str(file_error)}"
                    )
        
        # Commit all changes
        await db.commit()
        
        logger.info(f"Successfully uploaded {upload_count} documents for procedure {procedure.id}")
        
        return {
            "success": True,
            "message": f"Uploaded {upload_count} documents",
            "procedure_id": procedure.id,
            "folio": folio,
            "uploaded_files": uploaded_files
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading documents for folio {encoded_folio}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload procedure documents"
        )


@procedures.get("/{procedure_id}/download/{field_name}", response_class=FileResponse)
async def download_procedure_file(
    procedure_id: int,
    field_name: str,
    db: AsyncSession = Depends(get_db)
):
    """Download a file uploaded for a specific procedure field"""
    try:
        logger.info(f"Attempting to download file for procedure {procedure_id}, field {field_name}")
        
        # Get the procedure
        stmt = select(Procedure).where(Procedure.id == procedure_id)
        result = await db.execute(stmt)
        procedure = result.scalars().first()
        
        if not procedure:
            logger.warning(f"Procedure {procedure_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Procedure not found"
            )
        
        # Get the file metadata from the Answer table
        stmt = select(Answer).where(
            Answer.procedure_id == procedure_id,
            Answer.name == field_name
        )
        result = await db.execute(stmt)
        answer = result.scalars().first()
        
        if not answer or not answer.value:
            logger.warning(f"Answer not found for procedure {procedure_id}, field {field_name}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        
        logger.info(f"Found answer for {field_name}: {answer.value}")
        
        # Parse the file metadata
        try:
            if isinstance(answer.value, str):
                # Try JSON first
                try:
                    file_metadata = json.loads(answer.value)
                except json.JSONDecodeError:
                    # If JSON fails, try to evaluate as Python dict literal
                    try:
                        file_metadata = ast.literal_eval(answer.value)
                    except (ValueError, SyntaxError):
                        # If both fail, it might be just a filename string
                        file_metadata = {"filename": answer.value}
            else:
                file_metadata = answer.value
            
            file_path = file_metadata.get('file_path')
            original_name = file_metadata.get('original_name') or file_metadata.get('filename')
            content_type = file_metadata.get('content_type', 'application/octet-stream')
            
            logger.info(f"Parsed metadata - file_path: {file_path}, original_name: {original_name}")
        except Exception as e:
            logger.error(f"Failed to parse file metadata: {e}, value: {answer.value}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file metadata"
            )
        
        if not file_path or not os.path.exists(file_path):
            logger.error(f"File not found on disk: {file_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found on disk"
            )
        
        logger.info(f"Serving file: {file_path}")
        
        # Return the file
        return FileResponse(
            path=file_path,
            filename=original_name,
            media_type=content_type
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file for procedure {procedure_id}, field {field_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download file"
        )

@procedures.get("/approvals", response_model=List[ProcedureRead])
async def list_procedure_approvals(folio: Optional[str] = Query(None), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """
    List procedures pending approval.
    Restricted to users with role_id > 1.
    """
    # Check if the user has a role_id greater than 1
    if not current_user or not hasattr(current_user, 'role_id') or current_user.role_id <= 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: This action is restricted to authorized personnel"
        )
    
    query = select(Procedure).where(Procedure.status == 1)  # Status 1 indicates pending approval
    
    if folio:
        folio = folio.strip()
        if len(folio) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Folio filter too long"
            )
        query = query.where(Procedure.folio.ilike(f"%{folio}%"))
    
    result = await db.execute(query)
    procedures = result.scalars().all()
    
    return procedures

@procedures.post("/approve/{encoded_folio}", response_model=ProcedureRead)
async def approve_procedure(encoded_folio: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Approve a procedure.
    Restricted to users with role_id > 1.
    """
    # Check if the user has a role_id greater than 1
    if not current_user or not hasattr(current_user, 'role_id') or current_user.role_id <= 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: This action is restricted to authorized personnel"
        )
    
    folio = validate_base64_folio(encoded_folio)
    
    try:
        # Get the procedure
        procedure = await get_procedure_by_folio(folio, db)
        
        # Store previous status for notification
        previous_status = procedure.status
        
        # Update the procedure status to approved (status code 2)
        procedure.status = 2
        procedure.approved_by = current_user.id
        procedure.approval_date = datetime.now()
        
        await db.commit()
        await db.refresh(procedure)
        
        logger.info(f"Procedure {folio} approved by user {current_user.id}")
        
        # Send notification to user about status change
        try:
            from app.services.procedure_notifications import send_procedure_status_notification
            await send_procedure_status_notification(
                db=db,
                procedure=procedure,
                previous_status=previous_status,
                new_status=2,
                reason="Trámite aprobado por la autoridad competente"
            )
        except Exception as e:
            logger.error(f"Failed to send approval notification for procedure {folio}: {e}")
            # Don't fail the main operation if notification fails
        
        return procedure
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error approving procedure {folio}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve procedure"
        )

@procedures.post("/reject/{encoded_folio}", response_model=ProcedureRead)
async def reject_procedure(encoded_folio: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Reject a procedure.
    Restricted to users with role_id > 1.
    """
    # Check if the user has a role_id greater than 1
    if not current_user or not hasattr(current_user, 'role_id') or current_user.role_id <= 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: This action is restricted to authorized personnel"
        )
    
    folio = validate_base64_folio(encoded_folio)
    
    try:
        # Get the procedure
        procedure = await get_procedure_by_folio(folio, db)
        
        # Store previous status for notification
        previous_status = procedure.status
        
        # Update the procedure status to rejected (status code 3)
        procedure.status = 3
        procedure.rejected_by = current_user.id
        procedure.rejection_date = datetime.now()
        
        await db.commit()
        await db.refresh(procedure)
        
        logger.info(f"Procedure {folio} rejected by user {current_user.id}")
        
        # Send notification to user about status change
        try:
            from app.services.procedure_notifications import send_procedure_status_notification
            await send_procedure_status_notification(
                db=db,
                procedure=procedure,
                               previous_status=previous_status,
                new_status=3,
                reason="Trámite rechazado. Favor de revisar los comentarios del revisor."
            )
        except Exception as e:
            logger.error(f"Failed to send rejection notification for procedure {folio}: {e}")
            # Don't fail the main operation if notification fails
        
        return procedure
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error rejecting procedure {folio}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reject procedure"
        )

@procedures.post("/issue-license/{encoded_folio}", status_code=status.HTTP_201_CREATED)
async def issue_license_scanned(
    encoded_folio: str,
    file: UploadFile = File(...),
    opening_time: str = Form(...),
    closing_time: str = Form(...),
    authorized_area: str = Form(...),
    license_cost: Optional[str] = Form(None),
    signatures: Optional[str] = Form(None),
    observations: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Issue a license by uploading a scanned PDF document
    Creates a business_license record based on the procedure
    """
    # Validate user permissions
    try:
        validate_admin_or_director_role(current_user)
    except HTTPException:
        # Check if user has supervisory role for license issuing
        user_role_name = getattr(current_user, 'role_name', None)
        if not (user_role_name and any(role.lower() in user_role_name.lower() 
                                     for role in ['revisor', 'supervisor', 'ventanilla', 'director'])):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Insufficient privileges for license issuing"
            )

    # Validate and decode folio
    folio = validate_base64_folio(encoded_folio)
    
    # Validate file upload
    validate_file_upload(file)
    
    try:
        # Get the procedure
        logger.info(f"Getting procedure for folio: {folio}")
        procedure = await get_procedure_by_folio(folio, db, current_user=current_user)
        logger.info(f"Found procedure with ID: {procedure.id}")
        
        # Check if procedure is approved
        # Status 2 = Aprobado, or director_approval = 1 for older procedures
        if procedure.status != 2 and procedure.director_approval != 1:
            logger.warning(f"Procedure {folio} is not approved. Status: {procedure.status}, Director Approval: {procedure.director_approval}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Procedure must be approved before issuing license"
            )
        
        # Check if license already exists
        logger.info(f"Checking if license already exists for folio: {folio}")
        license_query = select(BusinessLicense).where(BusinessLicense.license_folio == folio)
        license_result = await db.execute(license_query)
        existing_license = license_result.scalars().first()
        logger.info(f"Got existing license result: {existing_license}")
        if existing_license:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="License already exists for this procedure"
            )
        
        # Create uploads directory if it doesn't exist
        license_upload_dir = "uploads/licenses"
        os.makedirs(license_upload_dir, exist_ok=True)
        
        # Generate unique filename (escape folio for filesystem safety)
        safe_folio = folio.replace("/", "-").replace("\\", "-")
        file_extension = PathLib(file.filename).suffix.lower()
        unique_filename = f"{safe_folio}_{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(license_upload_dir, unique_filename)
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse signatures if provided
        signature_data = {}
        if signatures:
            try:
                parsed_signatures = json.loads(signatures)
                # Extract signature IDs if provided
                signature_ids = parsed_signatures.get('signature_ids', [])
                
                # Get signature data from municipality_signatures table
                if signature_ids and procedure.municipality_id:
                    signatures_result = await db.execute(
                        select(MunicipalitySignature)
                        .where(MunicipalitySignature.municipality_id == procedure.municipality_id)
                        .where(MunicipalitySignature.id.in_(signature_ids))
                        .order_by(MunicipalitySignature.orden)
                    )
                    signatures_from_db = signatures_result.scalars().all()
                    
                    # Map signatures to business license fields (up to 4 signatures)
                    for i, sig in enumerate(signatures_from_db[:4], 1):
                        signature_data[f'signer_name_{i}'] = sig.signer_name
                        signature_data[f'department_{i}'] = sig.department
                        signature_data[f'signature_{i}'] = sig.signature
            except json.JSONDecodeError:
                logger.warning(f"Invalid signatures JSON: {signatures}")
        
        # Get RequirementsQuery data for copying establishment information
        requirements_query = None
        if procedure.requirements_query_id:
            try:
                rq_stmt = select(RequirementsQuery).filter(RequirementsQuery.id == procedure.requirements_query_id)
                rq_result = await db.execute(rq_stmt)
                requirements_query = rq_result.scalars().first()
            except Exception as e:
                logger.warning(f"Could not fetch RequirementsQuery {procedure.requirements_query_id}: {e}")
        
        # Extract establishment data from procedure dynamic fields (JSON)
        establishment_name = None
        establishment_address = None  
        establishment_phone = None
        establishment_email = None
        
        # Try to get establishment data from procedure JSON fields
        if hasattr(procedure, 'establishment_name') and procedure.establishment_name:
            establishment_name = procedure.establishment_name
        if hasattr(procedure, 'establishment_address') and procedure.establishment_address:
            establishment_address = procedure.establishment_address
        if hasattr(procedure, 'establishment_phone') and procedure.establishment_phone:
            establishment_phone = procedure.establishment_phone
        if hasattr(procedure, 'establishment_email') and procedure.establishment_email:
            establishment_email = procedure.establishment_email
            
        # Fallback to dynamic fields (answers) if establishment data is missing
        try:
            from app.models.answer import Answer
            answers_stmt = select(Answer).filter(Answer.procedure_id == procedure.id)
            answers_result = await db.execute(answers_stmt)
            answers = answers_result.scalars().all()
            
            for answer in answers:
                if answer.name and answer.value:
                    # Map dynamic field names to establishment data
                    if not establishment_name and answer.name.lower() in ['nombre_establecimiento', 'establishment_name']:
                        establishment_name = answer.value
                    elif not establishment_address and answer.name.lower() in ['direccion_establecimiento', 'establishment_address']:
                        establishment_address = answer.value
                    elif not establishment_phone and answer.name.lower() in ['telefono_establecimiento', 'establishment_phone']:
                        establishment_phone = answer.value
                    elif not establishment_email and answer.name.lower() in ['email_establecimiento', 'establishment_email']:
                        establishment_email = answer.value
        except Exception as e:
            logger.warning(f"Could not fetch dynamic fields for procedure {procedure.id}: {e}")
            
        # Create business license record
        business_license = BusinessLicense(
            owner=procedure.official_applicant_name or "N/A",
            license_folio=folio,
            commercial_activity=procedure.scian_name or procedure.procedure_type or "N/A",
            industry_classification_code=procedure.scian_code or "N/A",
            authorized_area=authorized_area,
            opening_time=opening_time,
            closing_time=closing_time,
            owner_last_name_p="",  # Could be extracted from procedure if available
            owner_last_name_m="",  # Could be extracted from procedure if available
            national_id="",  # Could be extracted from procedure if available
            owner_profile="",
            logo_image=None,
            signature=None,
            minimap_url=None,
            scanned_pdf=file_path,  # Store the uploaded file path
            license_year=datetime.now().year,
            license_category=1,
            generated_by_user_id=current_user.id,
            payment_status=0,  # Not paid as per requirement
            municipality_id=procedure.municipality_id,
            license_type="scanned",
            license_status="issued",
            observations=observations,
            # Add signature information if provided
            signer_name_1=signature_data.get('signer_name_1'),
            department_1=signature_data.get('department_1'),
            signature_1=signature_data.get('signature_1'),
            signer_name_2=signature_data.get('signer_name_2'),
            department_2=signature_data.get('department_2'),
            signature_2=signature_data.get('signature_2'),
            signer_name_3=signature_data.get('signer_name_3'),
            department_3=signature_data.get('department_3'),
            signature_3=signature_data.get('signature_3'),
            signer_name_4=signature_data.get('signer_name_4'),
            department_4=signature_data.get('department_4'),
            signature_4=signature_data.get('signature_4'),
            # Copy establishment data and linkage fields
            procedure_id=procedure.id,
            requirements_query_id=procedure.requirements_query_id,
            establishment_name=establishment_name,
            establishment_address=establishment_address,
            establishment_phone=establishment_phone,
            establishment_email=establishment_email,
        )
        
        db.add(business_license)
        
        # Update procedure to mark license as issued
        procedure.license_pdf = file_path
        procedure.license_status = "issued"
        procedure.status = 7  # Licencia emitida en resumen
        procedure.window_license_generated = 1  # Mark license as generated in window
        procedure.license_delivered_date = datetime.now()  # Set delivery date to now
        procedure.updated_at = datetime.now()
        
        await db.commit()
        await db.refresh(business_license)
        
        logger.info(f"License issued successfully for procedure {folio} by user {current_user.id}")
        
        # Send license download notification
        try:
            license_data = {
                "license_number": str(business_license.id).zfill(5),
                "license_folio": business_license.license_folio
            }
            portal_url = f"https://visorurbano.jalisco.gob.mx/dashboard"
            
            # Send license download notification
            await send_license_download_notification(
                db=db,
                procedure=procedure,
                license_data=license_data,
                portal_url=portal_url
            )
            logger.info(f"License download notification sent for procedure {folio}")
        except Exception as e:
            logger.error(f"Failed to send license download notification for {folio}: {str(e)}")
            # Don't fail the main operation if notification fails
        
        return {
            "message": "License issued successfully",
            "license_id": business_license.id,
            "license_folio": business_license.license_folio,
            "file_path": business_license.scanned_pdf
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        # Clean up uploaded file if there was an error
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        logger.error(f"Error issuing license for procedure {folio}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to issue license"
        )

@procedures.post("/generate-license/{encoded_folio}", status_code=status.HTTP_201_CREATED)
async def generate_license_by_system(
    encoded_folio: str,
    license_data: Optional[dict] = Body(None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Generate a license automatically using the system template
    Creates a business_license record and generates a PDF using the template
    Accepts optional license data including opening/closing times, authorized area, and selected signatures
    """
    # Validate user permissions
    try:
        validate_admin_or_director_role(current_user)
    except HTTPException:
        # Check if user has supervisory role for license issuing
        user_role_name = getattr(current_user, 'role_name', None)
        if not (user_role_name and any(role.lower() in user_role_name.lower() 
                                     for role in ['revisor', 'supervisor', 'ventanilla', 'director'])):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Insufficient privileges for license issuing"
            )

    # Validate and decode folio
    folio = validate_base64_folio(encoded_folio)
    
    try:
        # Get the procedure
        logger.info(f"Getting procedure for folio: {folio}")
        procedure = await get_procedure_by_folio(folio, db, current_user=current_user)
        logger.info(f"Found procedure with ID: {procedure.id}")
        
        # Check if procedure is approved
        # Status 2 = Aprobado, or director_approval = 1 for older procedures
        if procedure.status != 2 and procedure.director_approval != 1:
            logger.warning(f"Procedure {folio} is not approved. Status: {procedure.status}, Director Approval: {procedure.director_approval}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Procedure must be approved before issuing license"
            )
        
        # Check if license already exists
        logger.info(f"Checking if license already exists for folio: {folio}")
        license_query = select(BusinessLicense).where(BusinessLicense.license_folio == folio)
        license_result = await db.execute(license_query)
        existing_license = license_result.scalars().first()
        logger.info(f"Got existing license result: {existing_license}")
        if existing_license:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="License already exists for this procedure"
            )
        
        # Get municipality information
        municipality_result = await db.execute(
            select(Municipality).where(Municipality.id == procedure.municipality_id)
        )
        municipality = municipality_result.scalars().first()
        if not municipality:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Municipality not found"
            )
        
        # Extract license data from request body if provided
        opening_time = "08:00"  # Default opening time
        closing_time = "18:00"  # Default closing time
        authorized_area = "0"  # Default value
        license_cost = "0"  # Default cost
        observations = "License generated automatically by the system"
        selected_signature_ids = []
        
        if license_data:
            opening_time = license_data.get('opening_time', opening_time)
            closing_time = license_data.get('closing_time', closing_time)
            authorized_area = license_data.get('authorized_area', authorized_area)
            license_cost = license_data.get('license_cost', license_cost)
            observations = license_data.get('observations', observations)
            selected_signature_ids = license_data.get('signature_ids', [])
        
        # Get selected signatures from municipality if signature IDs provided
        signatures_for_template = []
        signature_data = {}
        if selected_signature_ids and procedure.municipality_id:
            signatures_result = await db.execute(
                select(MunicipalitySignature)
                .where(MunicipalitySignature.municipality_id == procedure.municipality_id)
                .where(MunicipalitySignature.id.in_(selected_signature_ids))
                .order_by(MunicipalitySignature.orden)
            )
            signatures = signatures_result.scalars().all()
            
            # Prepare signatures for template
            for sig in signatures:
                # Use local file path for PDF generation, URL for web display
                signature_path = None
                if sig.signature:
                    # For PDF generation, use local file path
                    signature_path = sig.signature if os.path.exists(sig.signature) else None
                
                signatures_for_template.append({
                    'signer_name': sig.signer_name,
                    'position_title': sig.department,
                    'signature_image': signature_path
                })
            
            # Map signatures to business license fields (up to 4 signatures)
            for i, sig in enumerate(signatures[:4], 1):
                signature_data[f'signer_name_{i}'] = sig.signer_name
                signature_data[f'department_{i}'] = sig.department
                signature_data[f'signature_{i}'] = sig.signature
        
        # Get RequirementsQuery data for copying establishment information
        requirements_query = None
        if procedure.requirements_query_id:
            try:
                rq_stmt = select(RequirementsQuery).filter(RequirementsQuery.id == procedure.requirements_query_id)
                rq_result = await db.execute(rq_stmt)
                requirements_query = rq_result.scalars().first()
            except Exception as e:
                logger.warning(f"Could not fetch RequirementsQuery {procedure.requirements_query_id}: {e}")
        
        # Extract establishment data from procedure dynamic fields (JSON)
        establishment_name = None
        establishment_address = None  
        establishment_phone = None
        establishment_email = None
        
        # Try to get establishment data from procedure JSON fields
        if hasattr(procedure, 'establishment_name') and procedure.establishment_name:
            establishment_name = procedure.establishment_name
        if hasattr(procedure, 'establishment_address') and procedure.establishment_address:
            establishment_address = procedure.establishment_address
        if hasattr(procedure, 'establishment_phone') and procedure.establishment_phone:
            establishment_phone = procedure.establishment_phone
        if hasattr(procedure, 'establishment_email') and procedure.establishment_email:
            establishment_email = procedure.establishment_email
            
        # Fallback to dynamic fields (answers) if establishment data is missing
        try:
            from app.models.answer import Answer
            answers_stmt = select(Answer).filter(Answer.procedure_id == procedure.id)
            answers_result = await db.execute(answers_stmt)
            answers = answers_result.scalars().all()
            
            for answer in answers:
                if answer.name and answer.value:
                    # Map dynamic field names to establishment data
                    if not establishment_name and answer.name.lower() in ['nombre_establecimiento', 'establishment_name']:
                        establishment_name = answer.value
                    elif not establishment_address and answer.name.lower() in ['direccion_establecimiento', 'establishment_address']:
                        establishment_address = answer.value
                    elif not establishment_phone and answer.name.lower() in ['telefono_establecimiento', 'establishment_phone']:
                        establishment_phone = answer.value
                    elif not establishment_email and answer.name.lower() in ['email_establecimiento', 'establishment_email']:
                        establishment_email = answer.value
        except Exception as e:
            logger.warning(f"Could not fetch dynamic fields for procedure {procedure.id}: {e}")
            
        # Create business license record
        business_license = BusinessLicense(
            owner=procedure.official_applicant_name or "N/A",
            license_folio=folio,
            commercial_activity=procedure.scian_name or procedure.procedure_type or "N/A",
            industry_classification_code=procedure.scian_code or "N/A",
            authorized_area=authorized_area,
            opening_time=opening_time,
            closing_time=closing_time,
            owner_last_name_p="",  # Could be extracted from procedure if available
            owner_last_name_m="",  # Could be extracted from procedure if available
            national_id="",  # Could be extracted from procedure if available
            owner_profile="",
            logo_image=None,
            signature=None,
            minimap_url=None,
            scanned_pdf=file_path,  # Store the uploaded file path
            license_year=datetime.now().year,
            license_category=1,
            generated_by_user_id=current_user.id,
            payment_status=0,  # Not paid as per requirement
            municipality_id=procedure.municipality_id,
            license_type="scanned",
            license_status="issued",
            observations=observations,
            # Add signature information if provided
            signer_name_1=signature_data.get('signer_name_1'),
            department_1=signature_data.get('department_1'),
            signature_1=signature_data.get('signature_1'),
            signer_name_2=signature_data.get('signer_name_2'),
            department_2=signature_data.get('department_2'),
            signature_2=signature_data.get('signature_2'),
            signer_name_3=signature_data.get('signer_name_3'),
            department_3=signature_data.get('department_3'),
            signature_3=signature_data.get('signature_3'),
            signer_name_4=signature_data.get('signer_name_4'),
            department_4=signature_data.get('department_4'),
            signature_4=signature_data.get('signature_4'),
            # Copy establishment data and linkage fields
            procedure_id=procedure.id,
            requirements_query_id=procedure.requirements_query_id,
            establishment_name=establishment_name,
            establishment_address=establishment_address,
            establishment_phone=establishment_phone,
            establishment_email=establishment_email,
        )
        
        db.add(business_license)
        
        # Update procedure to mark license as issued
        procedure.license_pdf = file_path
        procedure.license_status = "issued"
        procedure.status = 7  # Licencia emitida en resumen
        procedure.window_license_generated = 1  # Mark license as generated in window
        procedure.license_delivered_date = datetime.now()  # Set delivery date to now
        procedure.updated_at = datetime.now()
        
        await db.commit()
        await db.refresh(business_license)
        
        logger.info(f"License generated successfully for procedure {folio} by user {current_user.id}")
        
        # Send license download notification
        try:
            license_data = {
                "license_number": str(business_license.id).zfill(5),
                "license_folio": business_license.license_folio
            }
            portal_url = f"https://visorurbano.jalisco.gob.mx/dashboard"
            
            # Send license download notification
            await send_license_download_notification(
                db=db,
                procedure=procedure,
                license_data=license_data,
                portal_url=portal_url
            )
            logger.info(f"License download notification sent for procedure {folio}")
        except Exception as e:
            logger.error(f"Failed to send license download notification for {folio}: {str(e)}")
            # Don't fail the main operation if notification fails
        
        return {
            "message": "License generated successfully",
            "license_id": business_license.id,
            "license_folio": business_license.license_folio,
            "file_path": business_license.scanned_pdf,
            "license_type": "system_generated"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        # Clean up generated file if there was an error
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        logger.error(f"Error generating license for procedure {folio}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate license"
        )

@procedures.get("/licenses-issued", response_model=List[Dict[str, Any]])
async def list_issued_licenses(
    page: Optional[int] = Query(1, ge=1, description="Page number"),
    per_page: Optional[int] = Query(20, ge=1, le=100, description="Items per page"),
    folio: Optional[str] = Query(None, description="Filter by folio"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    List issued licenses - accessible to users with administrative privileges
    """
    # Validate user permissions
    user_role_id = getattr(current_user, 'role_id', 1) or 1
    if user_role_id <= 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Administrative privileges required"
        )
    
    try:
        # Build query for issued licenses
        stmt = select(BusinessLicense).options(joinedload(BusinessLicense.municipality))
        
        # Apply municipality filter for non-admin users
        user_municipality_id = getattr(current_user, 'municipality_id', None)
        if user_municipality_id and user_role_id < 5:  # Not super admin
            stmt = stmt.where(BusinessLicense.municipality_id == user_municipality_id)
        
        # Apply folio filter if provided
        if folio:
            stmt = stmt.where(BusinessLicense.license_folio.ilike(f"%{folio}%"))
        
        # Order by creation date (newest first)
        stmt = stmt.order_by(BusinessLicense.created_at.desc())
        
        # Apply pagination
        offset = (page - 1) * per_page
        stmt = stmt.offset(offset).limit(per_page)
        
        # Execute query
        result = await db.execute(stmt)
        licenses = result.scalars().all()
        
        # Format response
        response = []
        for license in licenses:
            license_dict = {
                "id": license.id,
                "license_folio": license.license_folio,
                "owner": license.owner,
                "commercial_activity": license.commercial_activity,
                "industry_classification_code": license.industry_classification_code,
                "authorized_area": license.authorized_area,
                "opening_time": license.opening_time,
                "closing_time": license.closing_time,
                "license_status": license.license_status,
                "license_type": license.license_type,
                "payment_status": license.payment_status,
                "created_at": license.created_at.isoformat() if license.created_at else None,
                "updated_at": license.updated_at.isoformat() if license.updated_at else None,
                "municipality_name": license.municipality.name if license.municipality else None,
                "scanned_pdf": license.scanned_pdf,
                "observations": license.observations,
            }
            response.append(license_dict)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing issued licenses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list issued licenses"
        )

@procedures.get("/license/{license_id}/download")
async def download_license_pdf(
    license_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Download the scanned license PDF
    """
    # Validate user permissions
    user_role_id = getattr(current_user, 'role_id', 1) or 1
    if user_role_id <= 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Administrative privileges required"
        )
    
    try:
        # Get the license
        stmt = select(BusinessLicense).where(BusinessLicense.id == license_id)
        result = await db.execute(stmt)
        license = result.scalar_first()
        
        if not license:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="License not found"
            )
        
        # Check municipality access for non-admin users
        user_municipality_id = getattr(current_user, 'municipality_id', None)
        if user_municipality_id and user_role_id < 5:  # Not super admin
            if license.municipality_id != user_municipality_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: You can only access licenses from your municipality"
                )
        
        # Check if file exists
        if not license.scanned_pdf or not os.path.exists(license.scanned_pdf):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="License PDF file not found"
            )
        
        logger.info(f"Serving license file for license ID {license_id}: {license.scanned_pdf}")
        
        # Return file
        return FileResponse(
            path=license.scanned_pdf,
            filename=f"license_{license.license_folio}.pdf",
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading license PDF {license_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download license PDF"
        )

@procedures.get("/enhanced", response_model=List[ProcedureRead])
async def list_procedures_enhanced(
    folio: Optional[str] = Query(None), 
    db: AsyncSession = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    """
    Enhanced procedures endpoint that includes complete address and SCIAN information
    by joining with RequirementsQuery and other related tables
    """
    # Build query with joins to get complete information
    query = select(Procedure).options(
        selectinload(Procedure.municipality),
        selectinload(Procedure.project_municipality)
    )
    
    # Apply role-based filtering for users with role_id = 1 (Citizen role)
    if current_user and hasattr(current_user, 'role_id') and current_user.role_id == 1:
        # Users with role_id = 1 can only see their own procedures
        query = query.where(Procedure.user_id == current_user.id)
    
    if folio:
        folio = folio.strip()
        if len(folio) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Folio filter too long"
            )
        query = query.where(Procedure.folio.ilike(f"%{folio}%"))
    
    result = await db.execute(query)
    procedures = result.scalars().all()
    
    # Convert to enhanced format with complete information
    enhanced_procedures = []
    for procedure in procedures:
        procedure_dict = procedure.__dict__.copy()
        
        # Add municipality_name from the relationship
        if procedure.municipality:
            procedure_dict['municipality_name'] = procedure.municipality.name
        elif procedure.project_municipality:
            procedure_dict['municipality_name'] = procedure.project_municipality.name
        else:
            procedure_dict['municipality_name'] = None
            
        # Build complete address if individual fields are available
        if procedure.street or procedure.exterior_number:
            address_parts = []
            if procedure.street:
                address_parts.append(procedure.street)
            if procedure.exterior_number:
                address_parts.append(procedure.exterior_number)
            if procedure.interior_number:
                address_parts.append(f"Int. {procedure.interior_number}")
            procedure_dict['full_address'] = " ".join(address_parts) if address_parts else None
        else:
            procedure_dict['full_address'] = None
            
        # Use SCIAN information from procedure if available
        if procedure.scian_code:
            procedure_dict['business_line'] = procedure.scian_name or procedure.scian_code
        else:
            procedure_dict['business_line'] = None
            
        enhanced_procedures.append(ProcedureRead(**procedure_dict))
    
    return enhanced_procedures

@procedures.get("/license/status/{encoded_folio}")
async def get_license_status_by_folio(
    encoded_folio: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get the license status by folio (for users to check if their license is ready for download)
    """
    # Validate and decode folio
    folio = validate_base64_folio(encoded_folio)
    
    try:
        # Get the procedure first to verify ownership
        procedure = await get_procedure_by_folio(folio, db, current_user=current_user)
        
        # For regular users (role_id = 1), verify they own this procedure
        user_role_id = getattr(current_user, 'role_id', 1) or 1
        if user_role_id == 1 and procedure.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only check your own license status"
            )
        
        # Get the business license by folio
        license_query = select(BusinessLicense).where(BusinessLicense.license_folio == folio)
        license_result = await db.execute(license_query)
        license = license_result.scalars().first()
        
        license_status = {
            "folio": folio,
            "procedure_status": procedure.status,
            "license_exists": license is not None,
            "license_paid": license.payment_status == 1 if license else False,
            "license_file_exists": bool(license and license.scanned_pdf and os.path.exists(license.scanned_pdf)) if license else False,
            "can_download": False
        }
        
        # License can be downloaded if:
        # 1. License exists
        # 2. License is paid (payment_status = 1)
        # 3. PDF file exists
        # 4. Procedure status is 7 (license issued)
        if (license and 
            license.payment_status == 1 and 
            license.scanned_pdf and 
            os.path.exists(license.scanned_pdf) and
            procedure.status == 7):
            license_status["can_download"] = True
        
        return license_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking license status for folio {folio}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check license status"
        )

@procedures.get("/license/download-by-folio/{encoded_folio}")
async def download_license_by_folio(
    encoded_folio: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Download the license PDF by folio (for users to download their own licenses)
    """
    # Validate and decode folio
    folio = validate_base64_folio(encoded_folio)
    
    try:
        # Get the procedure first to verify ownership
        procedure = await get_procedure_by_folio(folio, db, current_user=current_user)
        
        # For regular users (role_id = 1), verify they own this procedure
        user_role_id = getattr(current_user, 'role_id', 1) or 1
        if user_role_id == 1 and procedure.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only download your own licenses"
            )
        
        # Get the business license by folio
        license_query = select(BusinessLicense).where(BusinessLicense.license_folio == folio)
        license_result = await db.execute(license_query)
        license = license_result.scalars().first()
        
        if not license:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="License not found"
            )
        
        # Check if license is paid and ready for download
        if license.payment_status != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="License payment is required before download"
            )
        
        # Check if procedure status is correct (license issued)
        if procedure.status != 7:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="License is not yet issued"
            )
        
        # Check if file exists
        if not license.scanned_pdf or not os.path.exists(license.scanned_pdf):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="License PDF file not found"
            )
        
        logger.info(f"Serving license file for folio {folio}: {license.scanned_pdf}")
        
        # Return file
        return FileResponse(
            path=license.scanned_pdf,
            filename=f"licencia_{folio}.pdf",
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading license for folio {folio}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download license"
        )

