from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, Session
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime
import base64
import logging
import qrcode  # type: ignore
from io import BytesIO
import os
import subprocess
import tempfile
import platform
import jinja2  # type: ignore
from weasyprint import HTML  # type: ignore

from config.settings import get_db, get_sync_db
from app.models.provisional_openings import ProvisionalOpening
from app.models.procedures import Procedure
from app.models.user import UserModel
from app.models.municipality import Municipality
from app.schemas.provisional_openings import (
    ProvisionalOpeningCreate,
    ProvisionalOpeningRead,
    ProvisionalOpeningUpdate,
    ProvisionalOpeningList,
    PDFResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


def _calculate_days_remaining(end_date: datetime) -> int:
    now = datetime.now()
    delta = end_date - now
    return max(0, delta.days)


def _is_expired(end_date: datetime) -> bool:
    return datetime.now() > end_date


def _enrich_provisional_opening(opening: ProvisionalOpening) -> dict:
    data = {
        "id": opening.id,
        "folio": opening.folio,
        "procedure_id": opening.procedure_id,
        "counter": opening.counter,
        "granted_by_user_id": opening.granted_by_user_id,
        "granted_role": opening.granted_role,
        "start_date": opening.start_date,
        "end_date": opening.end_date,
        "status": opening.status,
        "created_at": opening.created_at,
        "updated_at": opening.updated_at,
        "days_remaining": _calculate_days_remaining(opening.end_date),
        "is_expired": _is_expired(opening.end_date),
        "municipality_name": opening.municipality.name if opening.municipality else None,
        "granted_by_user_name": None,
        "procedure_folio": opening.procedure.folio if opening.procedure else None
    }
    if opening.granted_by_user:
        data["granted_by_user_name"] = f"{opening.granted_by_user.name} {opening.granted_by_user.paternal_last_name}"
    return data


@router.get("/", response_model=ProvisionalOpeningList)
async def list_provisional_openings(
    municipality_id: int = Query(..., description="Municipality ID"),
    status: Optional[int] = Query(None, description="Status (1=active, 0=inactive)"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search by folio"),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(ProvisionalOpening).options(
            selectinload(ProvisionalOpening.municipality),
            selectinload(ProvisionalOpening.granted_by_user),
            selectinload(ProvisionalOpening.procedure)
        ).where(ProvisionalOpening.municipality_id == municipality_id)

        if status is not None:
            query = query.where(ProvisionalOpening.status == status)
        if search:
            query = query.where(ProvisionalOpening.folio.ilike(f"%{search}%"))

        # Optimize count query to use SELECT COUNT(*) instead of loading all rows
        count_query = select(func.count(ProvisionalOpening.id)).where(ProvisionalOpening.municipality_id == municipality_id)
        if status is not None:
            count_query = count_query.where(ProvisionalOpening.status == status)
        if search:
            count_query = count_query.where(ProvisionalOpening.folio.ilike(f"%{search}%"))

        total_result = await db.execute(count_query)
        total = total_result.scalar()

        query = query.offset((page - 1) * size).limit(size)
        result = await db.execute(query)
        items = result.scalars().all()

        enriched_items = [_enrich_provisional_opening(item) for item in items]

        return ProvisionalOpeningList(
            total=total,
            items=enriched_items,
            page=page,
            size=size
        )
    except Exception as e:
        logger.error(f"Error listing provisional openings: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/by_folio/{folio}", response_model=ProvisionalOpeningRead)
async def get_provisional_opening_by_folio(
    folio: str = Path(..., description="Base64 encoded folio"),
    db: AsyncSession = Depends(get_db)
):
    try:
        try:
            decoded_folio = base64.b64decode(folio).decode('utf-8')
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid encoded folio")

        query = select(ProvisionalOpening).options(
            selectinload(ProvisionalOpening.municipality),
            selectinload(ProvisionalOpening.granted_by_user),
            selectinload(ProvisionalOpening.procedure)
        ).where(ProvisionalOpening.folio == decoded_folio)

        result = await db.execute(query)
        opening = result.scalars().first()

        if not opening:
            raise HTTPException(status_code=404, detail="Provisional opening not found")

        return _enrich_provisional_opening(opening)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting provisional opening by folio: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/pdf/{folio}", response_model=PDFResponse)
def generate_pdf_for_provisional_opening(
    folio: str = Path(..., description="Base64 encoded folio"),
    db: Session = Depends(get_sync_db)
):
    try:
        try:
            decoded_folio = base64.b64decode(folio).decode('utf-8')
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid encoded folio")

        query = select(ProvisionalOpening).options(
            selectinload(ProvisionalOpening.municipality),
            selectinload(ProvisionalOpening.granted_by_user),
            selectinload(ProvisionalOpening.procedure)
        ).where(ProvisionalOpening.folio == decoded_folio)

        result = db.execute(query)
        opening = result.scalars().first()

        if not opening:
            raise HTTPException(status_code=404, detail="Provisional opening not found")

        verification_url = f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/verify/provisional/{folio}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(verification_url)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode()

        template_data = {
            'opening': opening,
            'municipality': opening.municipality,
            'granted_by': opening.granted_by_user,
            'procedure': opening.procedure,
            'qr_code': qr_base64,
            'verification_url': verification_url,
            'generated_date': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'days_remaining': _calculate_days_remaining(opening.end_date),
            'is_expired': _is_expired(opening.end_date)
        }

        base_path = os.getenv('TEMPLATES_BASE_PATH', os.path.join(os.path.dirname(__file__), '../../templates'))
        template_loader = jinja2.FileSystemLoader(base_path)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template('provisional_opening_certificate.html')
        html_content = template.render(**template_data)

        html_doc = HTML(string=html_content)
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_pdf_path = temp_file.name
            html_doc.write_pdf(temp_pdf_path)

        # Read PDF content for base64 encoding
        with open(temp_pdf_path, 'rb') as pdf_file:
            pdf_content = base64.b64encode(pdf_file.read()).decode()

        # Cross-platform PDF opening
        try:
            if os.name == 'nt':  # Windows
                os.startfile(temp_pdf_path)
            elif os.name == 'posix':  # macOS and Linux
                if platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', temp_pdf_path], check=True)
                else:  # Linux and other Unix-like systems
                    subprocess.run(['xdg-open', temp_pdf_path], check=True)
            logger.info(f"PDF generated and opened: {temp_pdf_path}")
        except Exception as e:
            logger.warning(f"PDF generated but could not be opened automatically: {str(e)}")

        # Return PDF response matching PDFResponse schema
        filename = f"provisional_opening_{decoded_folio.replace('/', '_')}.pdf"
        return PDFResponse(
            pdf_content=pdf_content,
            filename=filename,
            qr_code=qr_base64
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating PDF")


@router.post("/", response_model=ProvisionalOpeningRead)
async def create_provisional_opening(
    payload: ProvisionalOpeningCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        existing_query = select(ProvisionalOpening).where(
            ProvisionalOpening.folio == payload.folio,
            ProvisionalOpening.status == 1
        )
        existing_result = await db.execute(existing_query)
        existing = existing_result.scalars().first()

        if existing:
            logger.info(f"Returning existing provisional opening with folio: {payload.folio}")
            return _enrich_provisional_opening(existing)

        municipality_query = select(Municipality).where(Municipality.id == payload.municipality_id)
        municipality_result = await db.execute(municipality_query)
        municipality = municipality_result.scalars().first()
        if not municipality:
            raise HTTPException(status_code=400, detail="Municipality not found")

        if payload.granted_by_user_id:
            granted_user_query = select(UserModel).where(UserModel.id == payload.granted_by_user_id)
            granted_user_result = await db.execute(granted_user_query)
            granted_user = granted_user_result.scalars().first()
            if not granted_user:
                raise HTTPException(status_code=400, detail="Granting user not found")

        new_opening = ProvisionalOpening(
            folio=payload.folio,
            procedure_id=payload.procedure_id,
            counter=payload.counter,
            granted_by_user_id=payload.granted_by_user_id,
            granted_role=payload.granted_role,
            start_date=payload.start_date,
            end_date=payload.end_date,
            status=payload.status,
            municipality_id=payload.municipality_id,
            created_by=payload.created_by,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        db.add(new_opening)
        await db.commit()
        await db.refresh(new_opening)

        opening_with_relations_query = select(ProvisionalOpening).options(
            selectinload(ProvisionalOpening.municipality),
            selectinload(ProvisionalOpening.granted_by_user),
            selectinload(ProvisionalOpening.procedure)
        ).where(ProvisionalOpening.id == new_opening.id)

        result = await db.execute(opening_with_relations_query)
        opening_with_relations = result.scalars().first()

        logger.info(f"Created new provisional opening with ID: {new_opening.id}")
        return _enrich_provisional_opening(opening_with_relations)
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating provisional opening: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating provisional opening")


@router.patch("/{id}", response_model=ProvisionalOpeningRead)
async def update_provisional_opening(
    id: int = Path(..., description="Provisional opening ID"),
    payload: ProvisionalOpeningUpdate = ...,
    db: AsyncSession = Depends(get_db)
):
    try:
        opening_query = select(ProvisionalOpening).where(ProvisionalOpening.id == id)
        opening_result = await db.execute(opening_query)
        opening = opening_result.scalars().first()

        if not opening:
            raise HTTPException(status_code=404, detail="Provisional opening not found")

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(opening, field, value)

        opening.updated_at = datetime.now()

        await db.commit()
        await db.refresh(opening)

        opening_with_relations_query = select(ProvisionalOpening).options(
            selectinload(ProvisionalOpening.municipality),
            selectinload(ProvisionalOpening.granted_by_user),
            selectinload(ProvisionalOpening.procedure)
        ).where(ProvisionalOpening.id == opening.id)

        result = await db.execute(opening_with_relations_query)
        opening_with_relations = result.scalars().first()

        logger.info(f"Updated provisional opening with ID: {id}")
        return _enrich_provisional_opening(opening_with_relations)
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating provisional opening: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating provisional opening")


@router.delete("/{id}")
async def delete_provisional_opening(
    id: int = Path(..., description="Provisional opening ID"),
    db: AsyncSession = Depends(get_db)
):
    try:
        opening_query = select(ProvisionalOpening).where(ProvisionalOpening.id == id)
        opening_result = await db.execute(opening_query)
        opening = opening_result.scalars().first()

        if not opening:
            raise HTTPException(status_code=404, detail="Provisional opening not found")

        opening.status = 0
        opening.updated_at = datetime.now()

        await db.commit()

        logger.info(f"Soft deleted provisional opening with ID: {id}")
        return {"detail": "Provisional opening marked as inactive", "id": id}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting provisional opening: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting provisional opening")
