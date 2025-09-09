# Standard library imports
import base64
import logging
from datetime import datetime
from typing import Optional
from urllib.parse import unquote

# Third-party imports
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Local imports
from app.models.answer import Answer
from app.models.procedures import Procedure
from app.models.requirements_query import RequirementsQuery
from app.services.dependency_assignment_service import DependencyAssignmentService
from config.security import get_current_user
from config.settings import get_db

logger = logging.getLogger(__name__)

router = APIRouter()

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

@router.post("/by_folio/{folio}/submit_for_review")
async def submit_procedure_for_review(
    folio: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Submit a procedure for review after validating all required fields are completed.
    Changes the status from draft (0), pending review (1), or prevention (3) to pending_review (1).
    Allows updates to procedures already in review process.
    """
    try:
        # Decode folio if it's base64 encoded
        try:
            decoded_folio = validate_base64_folio(folio)
        except HTTPException:
            # If base64 validation fails, try to use folio as-is
            decoded_folio = folio
        
        # Get the procedure
        procedure = await get_procedure_by_folio(decoded_folio, db, current_user=current_user)
        
        if not procedure:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Procedure not found"
            )
        
        # Check if user owns the procedure (for citizens)
        if hasattr(current_user, 'role_id') and current_user.role_id == 1:
            if procedure.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only submit your own procedures for review"
                )
        
        # Check if procedure is in draft status (0), in review (1), or prevention status (3)
        if procedure.status not in [0, 1, 3]:
            status_names = {0: "draft", 1: "pending_review", 2: "rejected", 3: "prevention", 7: "license_issued"}
            current_status = status_names.get(procedure.status, f"status_{procedure.status}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Procedure is not in draft, pending review, or prevention status. Current status: {current_status}"
            )
        
        # Get all required fields for this procedure type and municipality
        # If no requirements_query_id, skip field validation (allow submission)
        if not procedure.requirements_query_id:
            logger.warning(f"Procedure {procedure.folio} has no requirements_query_id, skipping field validation")
            # Skip to status update without field validation
        else:
            # Get requirements query to determine municipality and procedure type
            requirements_query_stmt = select(RequirementsQuery).where(
                RequirementsQuery.id == procedure.requirements_query_id
            )
            requirements_query_result = await db.execute(requirements_query_stmt)
            requirements_query = requirements_query_result.scalar_one_or_none()
            
            if not requirements_query:
                logger.warning(f"Requirements query not found for procedure {procedure.folio}, skipping field validation")
            else:
                # Import Field and Requirement models
                from app.models.field import Field
                from app.models.requirements import Requirement
                
                # Get current procedure type (exact match, no hardcoding)
                current_procedure_type = procedure.procedure_type or "business_license"
                
                # Get required fields - filter by municipality, exact procedure type, and required status
                required_fields_stmt = (
                    select(Field)
                    .join(Requirement)
                    .where(
                        Requirement.municipality_id == requirements_query.municipality_id,
                        Requirement.field_id == Field.id,
                        Field.required == 1,
                        Field.procedure_type == current_procedure_type  # Exact match only
                    )
                )
                
                required_fields_result = await db.execute(required_fields_stmt)
                required_fields = required_fields_result.scalars().all()
                
                # Get all answers for this procedure
                answers_stmt = select(Answer).where(Answer.procedure_id == procedure.id)
                answers_result = await db.execute(answers_stmt)
                answers = answers_result.scalars().all()
                answer_dict = {answer.name: answer.value for answer in answers}
                
                # Validate that all required fields have values
                missing_fields = []
                for field in required_fields:
                    if not field.name:
                        continue
                        
                    # Check if the field has a value in answers
                    field_value = answer_dict.get(field.name)
                    
                    # Also check procedure model fields for basic info
                    if not field_value:
                        # Map some common field names to procedure attributes
                        procedure_field_mapping = {
                            'nombre_solicitante': procedure.official_applicant_name,
                            'calle': procedure.street,
                            'numero_exterior': procedure.exterior_number,
                            'colonia': procedure.neighborhood,
                            'nombre_establecimiento': procedure.establishment_name,
                            'direccion_establecimiento': procedure.establishment_address,
                            'superficie_establecimiento': procedure.establishment_area,
                        }
                        
                        field_value = procedure_field_mapping.get(field.name)
                    
                    if not field_value or field_value.strip() == "":
                        missing_fields.append({
                            "name": field.name,
                            "description": field.description or field.name
                        })
                
                if missing_fields:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "message": "Required fields are missing",
                            "missing_fields": missing_fields
                        }
                    )
        
        # Update procedure status to pending_review (1)
        procedure.status = 1
        procedure.sent_to_reviewers = 1
        procedure.sent_to_reviewers_date = datetime.now()
        procedure.updated_at = datetime.now()
        
        await db.commit()
        
        # Assign to dependency reviewers (existing logic)
        try:
            dependency_service = DependencyAssignmentService()
            assignment_result = await dependency_service.assign_procedure_to_dependencies(
                procedure.id, db
            )
            logger.info(f"Dependency assignment result for procedure {procedure.id}: {assignment_result}")
        except Exception as e:
            logger.error(f"Error assigning procedure {procedure.id} to dependencies: {e}")
            # Don't fail the submission if dependency assignment fails
        
        await db.refresh(procedure)
        
        return {
            "success": True,
            "message": "Procedure submitted for review successfully",
            "procedure": {
                "id": procedure.id,
                "folio": procedure.folio,
                "status": procedure.status,
                "sent_to_reviewers": procedure.sent_to_reviewers,
                "sent_to_reviewers_date": procedure.sent_to_reviewers_date.isoformat() if procedure.sent_to_reviewers_date else None,
                "updated_at": procedure.updated_at.isoformat() if procedure.updated_at else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting procedure for review: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

