from fastapi import APIRouter, Depends, Response, HTTPException, Query, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
import io
import os
import uuid
import math
import logging
import base64
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_, or_, func, outerjoin, case
from sqlalchemy.sql.functions import coalesce
from app.services.formats.business_licenses import generate_unsigned_receipt_pdf, generate_signed_receipt_pdf, generate_responsible_letter_pdf, generate_provisional_opening_pdf
from app.services.procedure_notifications import send_procedure_status_notification_sync
from app.models.business_license import BusinessLicense
from app.models.procedures import Procedure
from app.models.requirements_query import RequirementsQuery
from app.models.municipality import Municipality
from app.models.business_license_status_log import BusinessLicenseStatusLog
from app.models.user import UserModel
from app.models.user_roles import UserRoleModel
from app.schemas.business_license import BusinessLicensePublic, BusinessLicenseResponse, BusinessLicenseRead
from config.settings import get_db, get_sync_db
from config.security import get_current_user
from typing import List, Optional
from datetime import datetime
import pandas as pd  # type: ignore
from sqlalchemy.orm import Session
import re

def decode_folio_from_base64(encoded_folio: str) -> str:
    """
    Decode a base64-encoded folio to its original string value.
    
    Args:
        encoded_folio: The base64-encoded folio string
        
    Returns:
        The decoded folio string
        
    Raises:
        HTTPException: 400 status if the folio encoding is invalid
    """
    try:
        decoded_bytes = base64.b64decode(encoded_folio, validate=True)
        folio = decoded_bytes.decode("utf-8")
        return folio
    except Exception as e:
        logging.error(f"Error decoding folio {encoded_folio}: {e}")
        raise HTTPException(status_code=400, detail="Invalid folio encoding")

def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize a string to be safe for use as a filename.
    
    Args:
        filename: The original filename string
        max_length: Maximum length for the filename (default: 255)
        
    Returns:
        A sanitized filename safe for filesystem use
    """
    # Remove or replace invalid characters for filenames
    # Invalid characters: < > : " | ? * \ / and control characters (0-31)
    invalid_chars = r'[<>:"|?*\\/\x00-\x1f\x7f]'
    
    # Replace invalid characters with underscore
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Replace multiple consecutive underscores with single underscore
    sanitized = re.sub(r'_+', '_', sanitized)
    
    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(' .')
    
    # Ensure filename is not empty after sanitization
    if not sanitized:
        sanitized = 'file'
    
    # Truncate if too long, but preserve file extension if present
    if len(sanitized) > max_length:
        if '.' in sanitized:
            name, ext = sanitized.rsplit('.', 1)
            max_name_length = max_length - len(ext) - 1  # -1 for the dot
            sanitized = name[:max_name_length] + '.' + ext
        else:
            sanitized = sanitized[:max_length]
    
    return sanitized

# Calculate total pages
class PaginatedBusinessLicenseResponse(BaseModel):
    items: List[dict]  # Use dict to allow dynamic fields from joins
    total: int
    page: int
    per_page: int
    total_pages: int

class PaymentUpdateRequest(BaseModel):
    payment_status: int  # 1 for paid, 0 for unpaid
    payment_receipt_file: str = None  # Optional file path for receipt

class LicenseStatusUpdateRequest(BaseModel):
    license_status: str  # New license status
    reason: Optional[str] = None  # Reason for status change
    reason_file: Optional[str] = None  # Optional file path for supporting document


router = APIRouter()

@router.get("/public", response_model=BusinessLicenseResponse)
async def list_business_licenses_public(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str = Query("", description="Search in folio, commercial activity, or SCIAN code"),
    municipality_id: int = Query(None, description="Filter by municipality"),
    db: AsyncSession = Depends(get_db)
):
    """
    List business licenses for public consumption (similar to legacy boletin).
    Only returns non-sensitive information suitable for public viewing.
    """
    offset = (page - 1) * per_page
    
    # Build base query using the new establishment fields stored directly in BusinessLicense
    base_query = (
        select(
            BusinessLicense,
            Municipality.name.label("municipality_name"),
            # For legacy licenses without establishment data, fallback to procedure joins
            case(
                (BusinessLicense.establishment_phone.isnot(None), BusinessLicense.establishment_phone),
                else_=Procedure.establishment_phone
            ).label("establishment_phone"),
            case(
                (BusinessLicense.establishment_name.isnot(None), BusinessLicense.establishment_name),
                else_=coalesce(Procedure.establishment_name, RequirementsQuery.applicant_name)
            ).label("establishment_name"),
            case(
                (BusinessLicense.establishment_address.isnot(None), BusinessLicense.establishment_address),
                else_=coalesce(
                    Procedure.establishment_address,
                    func.concat(RequirementsQuery.street, ', ', RequirementsQuery.neighborhood)
                )
            ).label("establishment_address"),
            case(
                (BusinessLicense.establishment_email.isnot(None), BusinessLicense.establishment_email),
                else_=UserModel.email
            ).label("user_email"),
        )
        .outerjoin(Municipality, BusinessLicense.municipality_id == Municipality.id)
        .outerjoin(Procedure, BusinessLicense.procedure_id == Procedure.id)
        .outerjoin(RequirementsQuery, BusinessLicense.requirements_query_id == RequirementsQuery.id)
        .outerjoin(UserModel, Procedure.user_id == UserModel.id)
        .where(
            and_(
                BusinessLicense.deleted_at.is_(None),  # Only active licenses
                BusinessLicense.license_status != 'cancelled'  # Exclude cancelled licenses
            )
        )
    )
    
    # Apply search filter
    if search.strip():
        search_term = f"%{search.strip()}%"
        base_query = base_query.where(
            or_(
                BusinessLicense.license_folio.ilike(search_term),
                BusinessLicense.commercial_activity.ilike(search_term),
                BusinessLicense.industry_classification_code.ilike(search_term)
            )
        )
    
    # Apply municipality filter
    if municipality_id is not None:
        base_query = base_query.where(BusinessLicense.municipality_id == municipality_id)
    
    # Count total matching licenses for pagination
    count_query = select(func.count(BusinessLicense.id)).where(
        and_(
            BusinessLicense.deleted_at.is_(None),  # Only active licenses
            BusinessLicense.license_status != 'cancelled'  # Exclude cancelled licenses
        )
    )
    # Apply search filter
    if search.strip():
        search_term = f"%{search.strip()}%"
        count_query = count_query.where(
            or_(
                BusinessLicense.license_folio.ilike(search_term),
                BusinessLicense.commercial_activity.ilike(search_term),
                BusinessLicense.industry_classification_code.ilike(search_term)
            )
        )
    # Apply municipality filter
    if municipality_id is not None:
        count_query = count_query.where(BusinessLicense.municipality_id == municipality_id)
    
    total_count_result = await db.execute(count_query)
    total_count = total_count_result.scalar() or 0
    
    # Calculate total pages
    total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1
    
    # Add ordering and pagination to the main query
    paginated_query = base_query.order_by(desc(BusinessLicense.created_at)).offset(offset).limit(per_page)
    
    # Execute the main query
    result = await db.execute(paginated_query)
    rows = result.all()
    
    # Create the response objects with all necessary fields
    licenses = []
    for row in rows:
        # Use Pydantic's from_orm to properly serialize the SQLAlchemy model
        license_model = BusinessLicensePublic.model_validate(row[0], from_attributes=True)
        license_data = license_model.model_dump()
        
        # Add additional fields with safe access
        license_data["municipality_name"] = row[1] if len(row) > 1 else None  # Municipality name
        license_data["establishment_phone"] = row[2] if len(row) > 2 else None  # Establishment phone (priority to license field)
        license_data["establishment_name"] = row[3] if len(row) > 3 else None  # Establishment name (priority to license field)
        license_data["establishment_address"] = row[4] if len(row) > 4 else None  # Establishment address (priority to license field)
        license_data["user_email"] = row[5] if len(row) > 5 else None  # User email as fallback for establishment email
        
        licenses.append(license_data)
    
    # Return data with pagination info
    return {
        "items": licenses,
        "page": page,
        "per_page": per_page,
        "total": total_count,
        "total_pages": total_pages
    }

@router.get("/unsigned_receipt/{encoded_folio}")
async def get_unsigned_receipt(encoded_folio: str, db: AsyncSession = Depends(get_db)):    
    
    try:
        # Decode the base64 folio
        folio = decode_folio_from_base64(encoded_folio)
        
        logging.info(f"Generating unsigned receipt for decoded folio: {folio}")
        
        pdf = await generate_unsigned_receipt_pdf(folio, db)
        return Response(content=pdf, media_type="application/pdf")
    except HTTPException:
        # Re-raise HTTPException to preserve status codes (like 400 for invalid encoding)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{encoded_folio}/download_receipt")
async def download_receipt(encoded_folio: str, db: AsyncSession = Depends(get_db)):
    """Download payment receipt for a business license"""
    
    try:
        # Decode the base64 folio
        folio = decode_folio_from_base64(encoded_folio)
        
        logging.info(f"Downloading receipt for decoded folio: {folio}")
        
        # Find the license by folio
        stmt = select(BusinessLicense).where(
            BusinessLicense.license_folio == folio,
            BusinessLicense.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        license_obj = result.scalars().first()
        
        if not license_obj:
            raise HTTPException(status_code=404, detail=f"License with folio {folio} not found")
        
        # Check if payment receipt file exists
        if not license_obj.payment_receipt_file or not os.path.exists(license_obj.payment_receipt_file):
            raise HTTPException(
                status_code=404, 
                detail="Recibo no disponible. No se ha subido un recibo de pago para esta licencia aún. Para descargar el recibo, primero debe marcarse como pagada y subir el comprobante de pago."
            )
        
        # Return the uploaded payment receipt file
        return FileResponse(
            path=license_obj.payment_receipt_file,
            media_type='application/octet-stream',
            filename=f"receipt_{folio}.pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error downloading receipt for folio {folio}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading receipt: {str(e)}")

@router.get("/{encoded_folio}/download_license")
async def download_license(encoded_folio: str, db: AsyncSession = Depends(get_db)):
    """Download the scanned business license document"""    
    
    try:
        # Decode the base64 folio
        folio = decode_folio_from_base64(encoded_folio)
        
        logging.info(f"Downloading license for decoded folio: {folio}")
        
        # Find the license by folio
        stmt = select(BusinessLicense).where(
            BusinessLicense.license_folio == folio,
            BusinessLicense.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        license_obj = result.scalars().first()
        
        if not license_obj:
            logging.error(f"License with folio {folio} not found")
            raise HTTPException(status_code=404, detail=f"License with folio {folio} not found")
        
        logging.info(f"Found license, scanned_pdf path: {license_obj.scanned_pdf}")
        
        # Check if scanned PDF exists
        if not license_obj.scanned_pdf or not os.path.exists(license_obj.scanned_pdf):
            logging.error(f"PDF file not found at path: {license_obj.scanned_pdf}")
            raise HTTPException(
                status_code=404, 
                detail="Licencia no disponible. No se ha escaneado la licencia oficial aún."
            )
        
        logging.info(f"Returning file: {license_obj.scanned_pdf}")
        
        # Return the scanned license file
        safe_folio = sanitize_filename(folio)
        return FileResponse(
            path=license_obj.scanned_pdf,
            media_type='application/pdf',
            filename=f"license_{safe_folio}.pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error downloading license for folio {folio}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading license document: {str(e)}")

@router.get("/signed_receipt/{encoded_folio}", summary="Get signed submission receipt")
async def get_signed_receipt(encoded_folio: str, db: AsyncSession = Depends(get_db)):    
    
    try:
        # Decode the base64 folio
        folio = decode_folio_from_base64(encoded_folio)
        
        logging.info(f"Generating signed receipt for decoded folio: {folio}")
        
        pdf_bytes = await generate_signed_receipt_pdf(folio=folio, db=db)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=signed_receipt_{folio}.pdf"
            }
        )
    except HTTPException:
        # Re-raise HTTPException to preserve status codes (like 400 for invalid encoding)
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error generating PDF: {str(e)}")
    
@router.get(
    "/responsible_letter/{encoded_folio}",
    response_class=Response,
    summary="Generate and return the Letter of Responsibility PDF"
)
async def get_responsible_letter(
    encoded_folio: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Fetches the data for the given folio, renders the Jinja2 template into PDF,
    and returns it inline with Content-Type application/pdf.
    """    
    
    try:
        # Decode the base64 folio
        folio = decode_folio_from_base64(encoded_folio)
        
        logging.info(f"Generating responsible letter for decoded folio: {folio}")
        
        pdf_bytes = await generate_responsible_letter_pdf(db=db, folio=folio)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename=responsible_letter_{folio}.pdf"
            },
        )
    except HTTPException:        
        raise
    except Exception as e:        
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get(
    "/provisional_opening/{encoded_folio}",
    summary="Get provisional opening PDF",
    responses={200: {"content": {"application/pdf": {}}}}
)
async def provisional_opening(
    encoded_folio: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):    
    
    try:
        # Decode the base64 folio
        folio = decode_folio_from_base64(encoded_folio)
        
        logging.info(f"Generating provisional opening for decoded folio: {folio}")
        
        pdf_bytes = await generate_provisional_opening_pdf(db=db, folio=folio)
        return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf")
    except HTTPException:
        # Re-raise HTTPException to preserve status codes (like 400 for invalid encoding)
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/export")
def export_business_licenses(
    municipality_id: int = Query(..., description="Municipality ID"),
    db: Session = Depends(get_sync_db)
):
    """
    Export business licenses to Excel file.
    This is the legacy export functionality migrated from business_license_histories.
    """
    records = db.query(BusinessLicense).filter(
        BusinessLicense.municipality_id == municipality_id,
        BusinessLicense.deleted_at.is_(None)
    ).all()

    export_data = [
        {
            "License Folio": r.license_folio,
            "Commercial Activity": r.commercial_activity,
            "Industry Classification Code": r.industry_classification_code,
            "Owner": f"{r.owner or ''} {r.owner_last_name_p or ''} {r.owner_last_name_m or ''}".strip(),
            "Municipality ID": r.municipality_id,
            "License Type": r.license_type,
            "License Status": r.license_status,
            "Opening Time": r.opening_time,
            "Closing Time": r.closing_time,
            "Authorized Area": r.authorized_area,
            "License Year": r.license_year,
            "Payment Status": r.payment_status,
            "Created At": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else "",
        } for r in records
    ]

    df = pd.DataFrame(export_data)
    stream = io.BytesIO()
    df.to_excel(stream, index=False, engine='openpyxl')
    stream.seek(0)

    filename = f"business_licenses_{datetime.now().date()}.xlsx"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}

    return StreamingResponse(stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

@router.get("/", response_model=PaginatedBusinessLicenseResponse)
def list_business_licenses(
    municipality_id: int = Query(..., description="Municipality ID"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    per_page: int = Query(20, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_sync_db)
):
    """
    List business licenses for directors/administrators by municipality.
    Returns detailed license information for management purposes with pagination.
    """
    try:
        # Calculate skip based on page
        skip = (page - 1) * per_page
        
        # Get total count
        total = db.query(BusinessLicense)\
            .filter(BusinessLicense.municipality_id == municipality_id)\
            .filter(BusinessLicense.deleted_at.is_(None))\
            .count()
        
        # Get paginated results - use new establishment fields from BusinessLicense directly
        results = db.query(
            BusinessLicense,
            case(
                (BusinessLicense.establishment_name.isnot(None), BusinessLicense.establishment_name),
                else_=coalesce(Procedure.establishment_name, RequirementsQuery.applicant_name)
            ).label('procedure_establishment_name'),
            case(
                (BusinessLicense.establishment_address.isnot(None), BusinessLicense.establishment_address),
                else_=coalesce(
                    Procedure.establishment_address,
                    func.concat(RequirementsQuery.street, ', ', RequirementsQuery.neighborhood)
                )
            ).label('procedure_establishment_address'),
            case(
                (BusinessLicense.establishment_phone.isnot(None), BusinessLicense.establishment_phone),
                else_=Procedure.establishment_phone
            ).label('procedure_establishment_phone'),
            case(
                (BusinessLicense.establishment_email.isnot(None), BusinessLicense.establishment_email),
                else_=UserModel.email
            ).label('user_email'),
            RequirementsQuery.scian_name.label('procedure_scian_name'),
        )\
            .outerjoin(Procedure, BusinessLicense.procedure_id == Procedure.id)\
            .outerjoin(RequirementsQuery, BusinessLicense.requirements_query_id == RequirementsQuery.id)\
            .outerjoin(UserModel, Procedure.user_id == UserModel.id)\
            .filter(BusinessLicense.municipality_id == municipality_id)\
            .filter(BusinessLicense.deleted_at.is_(None))\
            .order_by(desc(BusinessLicense.created_at))\
            .offset(skip)\
            .limit(per_page)\
            .all()
        
        # Convert results to include additional information
        enhanced_results = []
        for result in results:
            business_license = result[0]
            procedure_establishment_name = result[1]
            procedure_establishment_address = result[2]
            procedure_establishment_phone = result[3]
            user_email = result[4]
            procedure_scian_name = result[5]
            
            # Create a dict from the business license
            license_dict = {c.name: getattr(business_license, c.name) for c in business_license.__table__.columns}
            
            # Add additional information from the procedure and related data
            if procedure_establishment_name:
                license_dict['procedure_establishment_name'] = procedure_establishment_name
            if procedure_establishment_address:
                license_dict['procedure_establishment_address'] = procedure_establishment_address
            if procedure_establishment_phone:
                license_dict['procedure_establishment_phone'] = procedure_establishment_phone
            if user_email:
                license_dict['user_email'] = user_email
            if procedure_scian_name:
                license_dict['procedure_scian_name'] = procedure_scian_name
                
            enhanced_results.append(license_dict)
        
        
        total_pages = math.ceil(total / per_page) if total > 0 else 1
        
        return PaginatedBusinessLicenseResponse(
            items=enhanced_results,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
    except Exception as e:
        logging.error(f"Error retrieving business licenses: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving business licenses.")

@router.put("/{encoded_license_folio}/payment")
def update_payment_status(
    encoded_license_folio: str,
    payment_data: PaymentUpdateRequest,
    db: Session = Depends(get_sync_db)
):
    """
    Update payment status of a business license.
    """
    
    try:
        # Decode the base64 folio
        license_folio = decode_folio_from_base64(encoded_license_folio)
        
        logging.info(f"Updating payment status for decoded folio: {license_folio}")
        
        # Find the license by folio
        license_obj = db.query(BusinessLicense)\
            .filter(BusinessLicense.license_folio == license_folio)\
            .filter(BusinessLicense.deleted_at.is_(None))\
            .first()
        
        if not license_obj:
            raise HTTPException(status_code=404, detail="License not found")
        
        # Update payment status and date
        license_obj.payment_status = payment_data.payment_status
        if payment_data.payment_status == 1:  # If paid
            license_obj.payment_date = datetime.now()
        
        # Update receipt file if provided
        if payment_data.payment_receipt_file:
            license_obj.payment_receipt_file = payment_data.payment_receipt_file
        
        license_obj.updated_at = datetime.now()
        
        db.commit()
        db.refresh(license_obj)
        
        return {"message": "Payment status updated successfully", "license": license_obj}
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating payment status: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while updating payment status.")

@router.put("/{encoded_license_folio}/status")
def update_license_status(
    encoded_license_folio: str,
    status_data: LicenseStatusUpdateRequest,
    db: Session = Depends(get_sync_db)
):
    """
    Update the status of a business license.
    """
    
    try:
        # Decode the base64 folio
        license_folio = decode_folio_from_base64(encoded_license_folio)
        
        logging.info(f"Updating license status for decoded folio: {license_folio}")
        
        # Find the license by folio
        license_obj = db.query(BusinessLicense)\
            .filter(BusinessLicense.license_folio == license_folio)\
            .filter(BusinessLicense.deleted_at.is_(None))\
            .first()
        
        if not license_obj:
            raise HTTPException(status_code=404, detail="License not found")
        
        # Store previous status for logging
        previous_status = license_obj.license_status
        
        # Create status log entry
        status_log = BusinessLicenseStatusLog(
            license_id=license_obj.id,
            previous_status=previous_status,
            new_status=status_data.license_status,
            reason=status_data.reason,
            reason_file=status_data.reason_file,
            changed_by_user_id=None,  # TODO: Get current user ID
            changed_at=datetime.now()
        )
        db.add(status_log)
        
        # Update license status and related fields
        license_obj.license_status = status_data.license_status
        if status_data.reason:
            license_obj.reason = status_data.reason
        if status_data.reason_file:
            license_obj.reason_file = status_data.reason_file
        license_obj.status_change_date = datetime.now()
        
        db.commit()
        db.refresh(license_obj)
        
        # Send license status change notification
        try:
            # Get the related procedure to send notification to the user
            procedure = db.query(Procedure).filter(Procedure.folio == license_obj.license_folio).first()
            if procedure and procedure.user_id:
                # Map license status to procedure status for notification
                status_mapping = {
                    "active": 2,      # Approved
                    "suspended": 4,   # In Review
                    "cancelled": 3,   # Rejected
                    "expired": 3,     # Rejected/Expired
                    "debt": 4,        # In Review for debt
                    "sanction": 4,    # In Review for sanction
                    "preliminary": 1   # Pending approval
                }
                
                new_status = status_mapping.get(status_data.license_status, 4)  # Default to "In Review"
                previous_status_mapped = status_mapping.get(previous_status, 0)  # Default to "In Process"
                
                # Send notification
                send_procedure_status_notification_sync(
                    db=db,
                    procedure=procedure,
                    previous_status=previous_status_mapped,
                    new_status=new_status,
                    reason=status_data.reason,
                    portal_url="https://visorurbano.jalisco.gob.mx/dashboard"
                )
                logging.info(f"Status change notification sent for license {license_obj.license_folio}")
        except Exception as e:
            logging.error(f"Failed to send license status notification for {license_obj.license_folio}: {str(e)}")
            # Don't fail the main operation if notification fails
        
        return {
            "message": "License status updated successfully", 
            "license": {
                "license_folio": license_obj.license_folio,
                "license_status": license_obj.license_status,
                "reason": license_obj.reason,
                "reason_file": license_obj.reason_file,
                "status_change_date": license_obj.status_change_date.isoformat() if license_obj.status_change_date else None
            }
        }
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating license status: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while updating license status.")

@router.post("/{encoded_license_folio}/upload_status_file")
async def upload_status_file(
    encoded_license_folio: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_sync_db)
):
    """
    Upload a supporting document for license status change.
    """
    
    try:
        # Decode the base64 folio
        license_folio = decode_folio_from_base64(encoded_license_folio)
        
        logging.info(f"Uploading status file for decoded folio: {license_folio}")
        
        # Find the license by folio
        license_obj = db.query(BusinessLicense)\
            .filter(BusinessLicense.license_folio == license_folio)\
            .filter(BusinessLicense.deleted_at.is_(None))\
            .first()
        
        if not license_obj:
            raise HTTPException(status_code=404, detail="License not found")
        
        # Create upload directory if it doesn't exist
        upload_dir = "uploads/status_documents"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Sanitize folio for filename using robust sanitization
        safe_folio = sanitize_filename(license_folio)
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        unique_filename = f"{safe_folio}_status_{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "success": True,
            "message": "Status document uploaded successfully",
            "file_path": file_path,
            "filename": unique_filename
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error uploading status document: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while uploading document.")

@router.post("/{encoded_license_folio}/upload_receipt")
async def upload_receipt(
    encoded_license_folio: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_sync_db)
):
    """
    Upload a payment receipt for a business license.
    """
    
    try:
        # Decode the base64 folio
        license_folio = decode_folio_from_base64(encoded_license_folio)
        
        logging.info(f"Uploading receipt for decoded folio: {license_folio}")
        
        # Find the license by folio
        license_obj = db.query(BusinessLicense)\
            .filter(BusinessLicense.license_folio == license_folio)\
            .filter(BusinessLicense.deleted_at.is_(None))\
            .first()
        
        if not license_obj:
            raise HTTPException(status_code=404, detail="License not found")
        
        # Create upload directory if it doesn't exist
        upload_dir = "uploads/payment_receipts"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Sanitize folio for filename using robust sanitization
        safe_folio = sanitize_filename(license_folio)
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        unique_filename = f"{safe_folio}_receipt_{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Update license with receipt file path and payment status
        license_obj.payment_receipt_file = file_path
        license_obj.payment_status = 1  # Mark as paid when receipt is uploaded
        license_obj.payment_date = datetime.now()  # Set payment date
        db.commit()
        
        return {
            "success": True,
            "message": "Payment receipt uploaded successfully and payment status updated",
            "file_path": file_path,
            "filename": unique_filename,
            "payment_status": "paid"
        }
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logging.error(f"Error uploading payment receipt: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while uploading payment receipt.")

@router.get("/{encoded_license_folio}/status_history")
def get_license_status_history(
    encoded_license_folio: str,
    db: Session = Depends(get_sync_db)
):
    """
    Get the status change history for a business license.
    """
    
    try:
        # Decode the base64 folio
        license_folio = decode_folio_from_base64(encoded_license_folio)
        
        logging.info(f"Getting status history for decoded folio: {license_folio}")
        
        # Find the license by folio
        license_obj = db.query(BusinessLicense)\
            .filter(BusinessLicense.license_folio == license_folio)\
            .filter(BusinessLicense.deleted_at.is_(None))\
            .first()
        
        if not license_obj:
            raise HTTPException(status_code=404, detail="License not found")
        
        # Get status logs with user information
        status_logs = db.query(BusinessLicenseStatusLog)\
            .outerjoin(UserModel, BusinessLicenseStatusLog.changed_by_user_id == UserModel.id)\
            .outerjoin(UserRoleModel, UserModel.role_id == UserRoleModel.id)\
            .filter(BusinessLicenseStatusLog.license_id == license_obj.id)\
            .add_columns(UserModel.name, UserModel.paternal_last_name, UserRoleModel.name.label('role_name'))\
            .order_by(desc(BusinessLicenseStatusLog.changed_at))\
            .all()
        
        # Format the response
        history = []
        for row in status_logs:
            log = row[0]  # BusinessLicenseStatusLog
            user_name = row[1]  # UserModel.name
            user_lastname = row[2]  # UserModel.paternal_last_name
            role_name = row[3]  # UserRoleModel.name
            
            user_info = None
            if user_name:
                full_name = f"{user_name} {user_lastname or ''}".strip()
                user_info = {
                    "id": log.changed_by_user_id,
                    "name": full_name,
                    "role_name": role_name or "N/A"
                }
            
            history.append({
                "id": log.id,
                "previous_status": log.previous_status,
                "new_status": log.new_status,
                "reason": log.reason,
                "reason_file": log.reason_file,
                "changed_by_user_id": log.changed_by_user_id,
                "changed_by_user": user_info,
                "changed_at": log.changed_at.isoformat() if log.changed_at else None,
                "created_at": log.created_at.isoformat() if log.created_at else None
            })
        
        return {
            "license_folio": license_folio,
            "current_status": license_obj.license_status,
            "status_history": history
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error retrieving status history: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving status history.")