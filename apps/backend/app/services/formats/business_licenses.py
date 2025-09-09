import base64
import io
import os
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.services.data.business_license_data import get_unsigned_receipt_data_async, get_responsible_letter_data
from fastapi import HTTPException
from config.settings import settings
from sqlalchemy import select
from datetime import datetime
import base64
import os
import qrcode
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.requirements_query import RequirementsQuery
from fastapi import HTTPException, status
from app.models.provisional_openings import ProvisionalOpening as ProvisionalOpeningModel

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "../../../templates")
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"])
)

async def generate_unsigned_receipt_pdf(folio: str, db) -> bytes:

    data = await get_unsigned_receipt_data_async(folio, db)

    if not data:
        raise HTTPException(status_code=404, detail="Folio not found")


    qr_url = f"{settings.APP_BASE_URL}v1/unsigned_receipt/{folio}"
        
    data["qr_link"] = qr_url

    template = env.get_template("unsigned_receipt_template.html")
    html_content = template.render(data=data)

    pdf = HTML(string=html_content).write_pdf(stylesheets=[
        CSS(string='@page { size: A4; margin: 2cm } body { font-family: sans-serif; }')
    ])
    return pdf


async def generate_signed_receipt_pdf(folio: str, db: AsyncSession):

    decoded_folio = base64.b64decode(folio).decode("utf-8")
    
    query = await db.execute(
        select(RequirementsQuery).filter(RequirementsQuery.folio == decoded_folio)
    )
    row = query.scalars().first()
    if not row:
        raise Exception("Folio not found")

    # Generate QR code
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(f"{settings.APP_URL}/business_licenses/signed_receipt/{folio}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code = base64.b64encode(buffered.getvalue()).decode()

    logo_url = row.municipality.logo_url if hasattr(row.municipality, "logo_url") and row.municipality.logo_url else "https://visorurbano.com/assets/img/logo.png"
    
    answers = row.answers if hasattr(row, "answers") else []  

    data = {
        "result": [{
            "folio": row.folio,
            "municipality": row.municipality_name,
            "created_at": row.created_at.strftime("%d/%m/%Y") if row.created_at else ""
        }],
        "name": row.applicant_name or "Citizen",
        "domicilio": {
            "calle": row.street,
            "exterior": "",  # Add if available
            "interior": "",  # Add if available
            "colonia": row.neighborhood
        },
        "data": answers,
    }

    template = env.get_template("signed_receipt_template.html")
    html_out = template.render(data=data, logo=logo_url, qrCode=qr_code)

    pdf = HTML(string=html_out, base_url=".").write_pdf()

    return pdf

async def generate_responsible_letter_pdf(db: AsyncSession, folio: str) -> bytes:    
    data = await get_responsible_letter_data(db, folio)
    if not data:
        raise HTTPException(status_code=404, detail="Folio not found")
    
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("responsible_letter.html")
    
    html_content = template.render(
        government_logo=data["government_logo"],
        logo_url=data["logo_url"],
        municipality=data["municipality"],
        date=data["date"],
        applicant=data["applicant"],
        scian_name=data["scian_name"],
        address=data["address"], 
    )
    
    pdf_bytes = HTML(string=html_content).write_pdf()

    return pdf_bytes

async def generate_provisional_opening_pdf(db: AsyncSession, folio: str) -> bytes:    
    try:
        decoded = base64.b64decode(folio).decode()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid folio encoding")

    result = await db.execute(
        select(ProvisionalOpeningModel).where(
            ProvisionalOpeningModel.folio == decoded,
            ProvisionalOpeningModel.counter == 1 
        )
    )
    apertura = result.scalars().first()
    if not apertura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provisional opening not found")
    
    rq = await db.execute(
        select(RequirementsQuery).where(RequirementsQuery.folio == decoded)
    )
    req = rq.scalars().first()
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requirements not found")

    address = f"{req.street} No. {req.property_exterior_number or ''} {req.property_interior_number or ''}, {req.neighborhood}"    
    
    qr = qrcode.make(req.minimap_url or "https://visorurbano.com/assets/img/default_map.png")
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode()
    
    try:
        template = env.get_template("provisional_opening_template.html")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Template not found")
    html_out = template.render(
        logo=req.minimap_url,
        data=apertura,
        owner=req.applicant_name,
        address=address,
        qrCode=qr_b64
    )

    pdf_bytes = HTML(string=html_out).write_pdf(stylesheets=[])
    return pdf_bytes