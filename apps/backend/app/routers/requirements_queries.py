from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import base64
import logging
import io

from config.settings import get_db
from config.security import get_current_user
from app.schemas.requirements_queries import (
    RequirementsQueryCreateSchema,
    RequirementsQueryOutSchema,
    ProcedureInfoSchema,
    ProcedureTypeInfoSchema,
    ProcedureRenewalInfoSchema,
    RequirementsQueryCreateWithDynamicFieldsSchema
)
from app.services.requirements_queries import (
    get_procedure_info,
    get_procedure_info_type,
    get_procedure_info_renewal,
    get_requirements_pdf,
    submit_requirements_query,
    RequirementsQueriesService,
    get_folio_requirements_pdf
)

logger = logging.getLogger(__name__)

router = APIRouter()

def decode_and_validate_folio(folio: str) -> str:
    try:
        decoded_folio = base64.b64decode(folio).decode("utf-8")
        if not decoded_folio or not decoded_folio.strip() or any(ord(c) < 32 for c in decoded_folio):
            raise ValueError("Invalid folio content")
        return decoded_folio
    except (base64.binascii.Error, UnicodeDecodeError, ValueError) as e:
        logger.error(f"Error decoding folio {folio}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid folio format"
        )

@router.get("/{folio}/info", response_model=ProcedureInfoSchema)
async def get_procedure_information(
    folio: str,
    db: AsyncSession = Depends(get_db)
) -> ProcedureInfoSchema:
    decoded_folio = decode_and_validate_folio(folio)
    try:
        return await get_procedure_info(decoded_folio, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error for folio {decoded_folio} in get_procedure_information: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error retrieving procedure information"
        )

@router.get("/{folio}/type", response_model=ProcedureTypeInfoSchema)
async def get_procedure_type_information(
    folio: str,
    db: AsyncSession = Depends(get_db)
) -> ProcedureTypeInfoSchema:
    decoded_folio = decode_and_validate_folio(folio)
    try:
        return await get_procedure_info_type(decoded_folio, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error for folio {decoded_folio} in get_procedure_type_information: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error retrieving procedure type information"
        )

@router.get("/{folio}/renewal", response_model=ProcedureRenewalInfoSchema)
async def get_procedure_renewal_information(
    folio: str,
    db: AsyncSession = Depends(get_db)
) -> ProcedureRenewalInfoSchema:
    decoded_folio = decode_and_validate_folio(folio)
    try:
        return await get_procedure_info_renewal(decoded_folio, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error for folio {decoded_folio} in get_procedure_renewal_information: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error retrieving procedure renewal information"
        )

@router.get("/{folio}/requirements/{requirement_id}/pdf")
async def generate_requirements_pdf(
    folio: str,
    requirement_id: int, 
    db: AsyncSession = Depends(get_db)
):
    decoded_folio = decode_and_validate_folio(folio)
    try:
        pdf_result = await get_requirements_pdf(decoded_folio, requirement_id, db)
        pdf_bytes = base64.b64decode(pdf_result.pdf_data)
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                 "Content-Disposition": f'inline; filename="{pdf_result.filename}"'
            }
        )
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Value error for PDF generation: folio={decoded_folio}, requirement_id={requirement_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid requirement ID format" 
        )
    except Exception as e:
        logger.error(f"Unexpected error in PDF generation: folio={decoded_folio}, requirement_id={requirement_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during PDF generation"
        )

@router.post(
    "/",
    response_model=RequirementsQueryOutSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_requirements_query(
    data: RequirementsQueryCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
) -> RequirementsQueryOutSchema:
    try:
        return await submit_requirements_query(data, db)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating requirements query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during query submission"
        )

@router.post(
    "/requirements",
    response_model=dict,
    status_code=status.HTTP_201_CREATED
)
async def create_requirements_query_with_dynamic_fields(
    data: RequirementsQueryCreateWithDynamicFieldsSchema,
    db: AsyncSession = Depends(get_db)
) -> dict:
    try:
        result = await RequirementsQueriesService.submit_requirements_query_with_dynamic_fields(
            data, 
            db,
            current_user=None  # No user authentication required for requirements query creation
        )
        return {
            "data": result.get("data", {}),
            "message": "Requirements query processed successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing requirements query with dynamic fields: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during query processing"
        )

@router.get("/{folio}/requirements/pdf")
async def generate_folio_requirements_pdf(
    folio: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate PDF with all requirements for a given folio.
    This endpoint doesn't require a specific requirement_id and returns all requirements.
    """
    decoded_folio = decode_and_validate_folio(folio)
    try:
        # Get all requirements for this folio
        pdf_result = await get_folio_requirements_pdf(decoded_folio, db)
        pdf_bytes = base64.b64decode(pdf_result.pdf_data)
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                 "Content-Disposition": f'inline; filename="{pdf_result.filename}"'
            }
        )
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Value error for folio PDF generation: folio={decoded_folio}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid folio format" 
        )
    except Exception as e:
        logger.error(f"Error generating PDF for folio {decoded_folio}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error generating PDF"
        )
