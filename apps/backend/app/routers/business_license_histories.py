from fastapi import APIRouter, Depends, HTTPException, Query, Path, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import io
import logging
import pandas as pd # type: ignore
from weasyprint import HTML # type: ignore
from jinja2 import Environment, FileSystemLoader # type: ignore
from qrcode import make as make_qr # type: ignore
import base64
import os

from config.settings import get_sync_db as get_db, settings
from app.models.business_license_histories import BusinessLicenseHistory
from app.schemas.business_license_histories import (
    BusinessLicenseHistoryCreate,
    BusinessLicenseHistoryRead,
    BusinessLicenseHistoryUpdate,
    BusinessLicenseHistoryStatusUpdate,
    BusinessLicenseHistoryPaymentUpdate,
    BusinessLicenseHistoryRenewalRequest,
    FileListResponse
)

router = APIRouter()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "../../templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

@router.get("/", response_model=List[BusinessLicenseHistoryRead])
def list_business_license_histories(
    municipality_id: int = Query(..., description="Municipality ID"),
    status: int = Query(1, description="Record status (1=active, 0=inactive)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    try:
        results = db.query(BusinessLicenseHistory)\
            .filter(BusinessLicenseHistory.municipality_id == municipality_id)\
            .filter(BusinessLicenseHistory.status == status)\
            .filter(BusinessLicenseHistory.deleted_at.is_(None))\
            .offset(skip)\
            .limit(limit)\
            .all()
        return results
    except Exception as e:
        logging.error(f"Error retrieving business license histories: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving business license histories.")

@router.get("/export")
def export_business_license_histories(
    municipality_id: int = Query(..., description="Municipality ID"),
    status: int = Query(1, description="Record status (1=active, 0=inactive)"),
    db: Session = Depends(get_db)
):
    records = db.query(BusinessLicenseHistory).filter(
        BusinessLicenseHistory.municipality_id == municipality_id,
        BusinessLicenseHistory.status == status,
        BusinessLicenseHistory.deleted_at.is_(None)
    ).all()

    export_data = [
        {
            "License Folio": r.license_folio,
            "Issue Date": r.issue_date,
            "Business Line": r.business_line,
            "Business Line Code": r.business_line_code,
            "Business Name": r.business_name,
            "Owner": f"{r.owner_first_name or ''} {r.owner_last_name_p or ''} {r.owner_last_name_m or ''}",
            "Municipality ID": r.municipality_id,
            "Status": r.status,
            "License Type": r.license_type,
            "License Status": r.license_status,
        } for r in records
    ]

    df = pd.DataFrame(export_data)
    stream = io.BytesIO()
    df.to_excel(stream, index=False, engine='openpyxl')
    stream.seek(0)

    filename = f"business_license_histories_{datetime.now().date()}.xlsx"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}

    return StreamingResponse(stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

@router.get("/{id}", response_model=BusinessLicenseHistoryRead)
def get_business_license_history(
    id: int = Path(...),
    db: Session = Depends(get_db)
):
    item = db.query(BusinessLicenseHistory)\
        .filter(BusinessLicenseHistory.id == id)\
        .filter(BusinessLicenseHistory.deleted_at.is_(None))\
        .first()
    if not item:
        raise HTTPException(status_code=404, detail="Record not found")
    return item

@router.post("/", response_model=BusinessLicenseHistoryRead)
def create_business_license_history(
    payload: BusinessLicenseHistoryCreate,
    db: Session = Depends(get_db)
):
    try:
        new_entry = BusinessLicenseHistory(**payload.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating business license history: {str(e)}")
        raise HTTPException(status_code=400, detail="An error occurred while creating the business license history.")

@router.patch("/{id}", response_model=BusinessLicenseHistoryRead)
def update_business_license_history(
    payload: BusinessLicenseHistoryUpdate,
    id: int = Path(..., description="Business license history ID"),
    db: Session = Depends(get_db)
):
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    entry = db.query(BusinessLicenseHistory).filter(BusinessLicenseHistory.id == id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Record not found")
    
    try:
        for key, value in update_data.items():
            setattr(entry, key, value)
        db.commit()
        db.refresh(entry)
        return entry
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating business license history: {str(e)}")
        raise HTTPException(status_code=400, detail="An error occurred while updating the business license history.")

@router.delete("/{id}")
def delete_business_license_history(
    id: int = Path(...),
    db: Session = Depends(get_db)
):
    entry = db.query(BusinessLicenseHistory).filter(BusinessLicenseHistory.id == id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Record not found")
    
    try:
        entry.status = 0
        db.commit()
        return {"detail": "Record marked as inactive"}
    except Exception as e:
        db.rollback()
        logging.error(f"Error deactivating business license history: {str(e)}")
        raise HTTPException(status_code=400, detail="An error occurred while deactivating the business license history.")

@router.get("/pdf/{encoded_id}/{year}/{type}")
def generate_business_license_pdf(
    encoded_id: str,
    year: str,
    type: str,
    db: Session = Depends(get_db)
):
    try:
        license_id = int(encoded_id)
        record = db.query(BusinessLicenseHistory).filter(BusinessLicenseHistory.id == license_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="License history not found")

        url = f"{settings.APP_URL}v1/business_license_histories/pdf/{encoded_id}/{year}/{type}"
        qr_img = make_qr(url)
        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        template = env.get_template("licenses/business_license_history.html")
        html_content = template.render(record=record, year=year, type=type, qr_code=qr_code_base64)

        pdf_file = HTML(string=html_content).write_pdf()
        filename = f"license_{encoded_id}_{year}_{type}.pdf"
        return StreamingResponse(io.BytesIO(pdf_file), media_type="application/pdf", headers={
            "Content-Disposition": f"inline; filename={filename}"
        })
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error generating PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the PDF.")

@router.post("/import")
def import_business_license_histories(
    municipality_id: int = Query(..., description="Municipality ID"),
    file: UploadFile = File(..., description="Excel file to import"),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files are supported")

    try:
        df = pd.read_excel(file.file)
        created = 0
        for _, row in df.iterrows():
            owner_name = str(row.get("Owner") or "").strip()
            name_parts = owner_name.split(" ") if owner_name else []
            
            owner_first_name = name_parts[0] if len(name_parts) > 0 else None
            owner_last_name_p = name_parts[1] if len(name_parts) > 1 else None
            owner_last_name_m = name_parts[2] if len(name_parts) > 2 else None
            
            record = BusinessLicenseHistory(
                license_folio=row.get("License Folio"),
                issue_date=row.get("Issue Date"),
                business_line=row.get("Business Line"),
                business_line_code=row.get("Business Line Code"),
                business_name=row.get("Business Name"),
                owner_first_name=owner_first_name,
                owner_last_name_p=owner_last_name_p,
                owner_last_name_m=owner_last_name_m,
                municipality_id=municipality_id,
                status=1
            )
            db.add(record)
            created += 1
        db.commit()
        return {"detail": f"{created} records successfully imported"}
    except Exception as e:
        db.rollback()
        logging.error(f"Error importing business license histories: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while importing data.")

@router.patch("/{id}/status", response_model=BusinessLicenseHistoryRead)
def update_business_license_status(
    payload: BusinessLicenseHistoryStatusUpdate,
    id: int = Path(..., description="Business license history ID"),
    db: Session = Depends(get_db)
):
    entry = db.query(BusinessLicenseHistory)\
        .filter(BusinessLicenseHistory.id == id)\
        .filter(BusinessLicenseHistory.deleted_at.is_(None))\
        .first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Record not found")
    
    try:
        entry.license_status = payload.license_status
        if payload.reason is not None:
            entry.reason = payload.reason
        if payload.reason_file is not None:
            entry.reason_file = payload.reason_file
        if payload.status_change_date is not None:
            entry.status_change_date = payload.status_change_date
        else:
            entry.status_change_date = datetime.now()
        
        db.commit()
        db.refresh(entry)
        return entry
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating license status: {str(e)}")
        raise HTTPException(status_code=400, detail="An error occurred while updating the license status.")

@router.patch("/{id}/paid", response_model=BusinessLicenseHistoryRead)
def mark_business_license_as_paid(
    payload: BusinessLicenseHistoryPaymentUpdate,
    id: int = Path(..., description="Business license history ID"),
    db: Session = Depends(get_db)
):
    entry = db.query(BusinessLicenseHistory)\
        .filter(BusinessLicenseHistory.id == id)\
        .filter(BusinessLicenseHistory.deleted_at.is_(None))\
        .first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Record not found")
    
    try:
        entry.payment_status = payload.payment_status
        if payload.payment_user_id is not None:
            entry.payment_user_id = payload.payment_user_id
        if payload.payment_date is not None:
            entry.payment_date = payload.payment_date
        else:
            entry.payment_date = datetime.now()
        
        db.commit()
        db.refresh(entry)
        return entry
    except Exception as e:
        db.rollback()
        logging.error(f"Error marking license as paid: {str(e)}")
        raise HTTPException(status_code=400, detail="An error occurred while updating the payment status.")

@router.get("/{id}/files", response_model=FileListResponse)
def get_business_license_files(
    id: int = Path(..., description="Business license history ID"),
    db: Session = Depends(get_db)
):
    entry = db.query(BusinessLicenseHistory)\
        .filter(BusinessLicenseHistory.id == id)\
        .filter(BusinessLicenseHistory.deleted_at.is_(None))\
        .first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Record not found")
    
    try:
        files = []
        if entry.scanned_pdf:
            files.append({
                "filename": f"license_{id}_scanned.pdf",
                "url": entry.scanned_pdf,
                "uploaded_at": entry.created_at or datetime.now()
            })
        if entry.reason_file:
            files.append({
                "filename": f"license_{id}_reason_file",
                "url": entry.reason_file,
                "uploaded_at": entry.status_change_date or entry.updated_at or datetime.now()
            })
        
        return FileListResponse(files=files, total_count=len(files))
    except Exception as e:
        logging.error(f"Error retrieving license files: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the files.")

@router.delete("/{id}/files/{file_type}")
def delete_business_license_file(
    id: int = Path(..., description="Business license history ID"),
    file_type: str = Path(..., description="Type of file to delete (scanned_pdf, reason_file)"),
    db: Session = Depends(get_db)
):
    entry = db.query(BusinessLicenseHistory)\
        .filter(BusinessLicenseHistory.id == id)\
        .filter(BusinessLicenseHistory.deleted_at.is_(None))\
        .first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Record not found")
    
    if file_type not in ["scanned_pdf", "reason_file"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Must be 'scanned_pdf' or 'reason_file'")
    
    try:
        if file_type == "scanned_pdf":
            if not entry.scanned_pdf:
                raise HTTPException(status_code=404, detail="Scanned PDF file not found")
            entry.scanned_pdf = None
        elif file_type == "reason_file":
            if not entry.reason_file:
                raise HTTPException(status_code=404, detail="Reason file not found")
            entry.reason_file = None
        
        db.commit()
        return {"detail": f"{file_type} successfully deleted"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logging.error(f"Error deleting license file: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the file.")

@router.post("/{id}/refrendo", response_model=BusinessLicenseHistoryRead)
def create_business_license_renewal(
    payload: BusinessLicenseHistoryRenewalRequest,
    id: int = Path(..., description="Original business license history ID"),
    db: Session = Depends(get_db)
):
    original_entry = db.query(BusinessLicenseHistory)\
        .filter(BusinessLicenseHistory.id == id)\
        .filter(BusinessLicenseHistory.deleted_at.is_(None))\
        .first()
    
    if not original_entry:
        raise HTTPException(status_code=404, detail="Original license record not found")
    
    try:
        renewal_data = {
            "business_line": original_entry.business_line,
            "detailed_description": original_entry.detailed_description,
            "business_line_code": original_entry.business_line_code,
            "business_area": original_entry.business_area,
            "street": original_entry.street,
            "exterior_number": original_entry.exterior_number,
            "interior_number": original_entry.interior_number,
            "neighborhood": original_entry.neighborhood,
            "cadastral_key": original_entry.cadastral_key,
            "reference": original_entry.reference,
            "coordinate_x": original_entry.coordinate_x,
            "coordinate_y": original_entry.coordinate_y,
            "owner_first_name": original_entry.owner_first_name,
            "owner_last_name_p": original_entry.owner_last_name_p,
            "owner_last_name_m": original_entry.owner_last_name_m,
            "user_tax_id": original_entry.user_tax_id,
            "national_id": original_entry.national_id,
            "owner_phone": original_entry.owner_phone,
            "business_name": original_entry.business_name,
            "owner_email": original_entry.owner_email,
            "owner_street": original_entry.owner_street,
            "owner_exterior_number": original_entry.owner_exterior_number,
            "owner_interior_number": original_entry.owner_interior_number,
            "owner_neighborhood": original_entry.owner_neighborhood,
            "alcohol_sales": original_entry.alcohol_sales,
            "schedule": original_entry.schedule,
            "municipality_id": original_entry.municipality_id,
            "business_trade_name": original_entry.business_trade_name,
            "investment": original_entry.investment,
            "number_of_employees": original_entry.number_of_employees,
            "number_of_parking_spaces": original_entry.number_of_parking_spaces,
            "opening_time": original_entry.opening_time,
            "closing_time": original_entry.closing_time,
            "property_street": original_entry.property_street,
            "property_neighborhood": original_entry.property_neighborhood,
            "property_interior_number": original_entry.property_interior_number,
            "property_exterior_number": original_entry.property_exterior_number,
            "property_postal_code": original_entry.property_postal_code,
            "property_type": original_entry.property_type,
            "owner_postal_code": original_entry.owner_postal_code,
            "license_year": payload.license_year,
            "license_type": payload.license_type or "refrendo",
            "license_status": "pending",
            "payment_status": "pending",
            "status": 1,
            "issue_date": datetime.now().strftime("%Y-%m-%d"),
        }
        
        renewal_entry = BusinessLicenseHistory(**renewal_data)
        db.add(renewal_entry)
        db.commit()
        db.refresh(renewal_entry)
        
        return renewal_entry
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating license renewal: {str(e)}")
        raise HTTPException(status_code=400, detail="An error occurred while creating the license renewal.")
