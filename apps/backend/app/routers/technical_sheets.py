from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from app.schemas.technical_sheets import (
    TechnicalSheetsByMunicipalityResponse,
    MunicipalityStat,
    TechnicalSheetStatsResponse,
    DailyStatistic,
    TechnicalSheetCreate, 
    TechnicalSheetResponse
)
from app.models.technical_sheets import TechnicalSheet
from config.settings import get_db, settings
from app.models.zoning_control_regulations import ZoningControlRegulation
from app.models.municipality import Municipality
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from uuid import uuid4, UUID
import base64
import json
import qrcode
import requests
from io import BytesIO
from datetime import datetime
import logging

router = APIRouter()
env = Environment(loader=FileSystemLoader("templates"))

@router.get("/admin-stats", response_model=TechnicalSheetStatsResponse)
async def get_admin_statistics(db: AsyncSession = Depends(get_db)):
    start_date = datetime(2021, 9, 13)

    query = text("""
        SELECT 
            COUNT(*) AS count,
            EXTRACT(YEAR FROM created_at) AS year,
            EXTRACT(MONTH FROM created_at) AS month,
            EXTRACT(DAY FROM created_at) AS day
        FROM technical_sheets
        WHERE created_at > :start_date
        GROUP BY year, month, day
        ORDER BY year DESC, month DESC, day DESC
    """)

    result = await db.execute(query, {"start_date": start_date})
    rows = result.fetchall()

    daily_stats = [
        DailyStatistic(
            year=int(row.year),
            month=int(row.month),
            day=int(row.day),
            count=row.count
        )
        for row in rows
    ]

    total_query = text("SELECT COUNT(*) FROM technical_sheets WHERE created_at > :start_date")
    total_result = await db.execute(total_query, {"start_date": start_date})
    total = total_result.scalar()

    return {"total": total, "days": daily_stats}

@router.get("/by-municipality", response_model=TechnicalSheetsByMunicipalityResponse)
async def get_sheets_grouped_by_municipality(db: AsyncSession = Depends(get_db)):
    start_date = datetime(2021, 9, 13)

    query = text("""
        SELECT 
            COUNT(*) AS sheets, 
            municipalities.name AS municipality
        FROM technical_sheets
        JOIN municipalities ON technical_sheets.municipality_id = municipalities.id
        WHERE technical_sheets.created_at > :start_date
        GROUP BY municipality
        ORDER BY sheets DESC
    """)

    result = await db.execute(query, {"start_date": start_date})
    rows = result.fetchall()

    total = sum(row.sheets for row in rows)
    sheets = [MunicipalityStat(municipality=row.municipality, sheets=row.sheets) for row in rows]

    return {"sheets": sheets, "total": total}

@router.get("/admin-stats/{municipality_id}", response_model=TechnicalSheetStatsResponse)
async def get_daily_stats_by_municipality(
    municipality_id: int = Path(..., description="Municipality ID"),
    db: AsyncSession = Depends(get_db)
):
    start_date = datetime(2021, 9, 13)

    query = text("""
        SELECT 
            COUNT(*) AS count,
            EXTRACT(YEAR FROM created_at) AS year,
            EXTRACT(MONTH FROM created_at) AS month,
            EXTRACT(DAY FROM created_at) AS day
        FROM technical_sheets
        WHERE created_at > :start_date AND municipality_id = :municipality_id
        GROUP BY year, month, day
        ORDER BY year DESC, month DESC, day DESC
    """)

    result = await db.execute(query, {"start_date": start_date, "municipality_id": municipality_id})
    rows = result.fetchall()

    days = [
        DailyStatistic(
            year=int(row.year),
            month=int(row.month),
            day=int(row.day),
            count=row.count
        )
        for row in rows
    ]

    total_query = text("""
        SELECT COUNT(*) 
        FROM technical_sheets 
        WHERE created_at > :start_date AND municipality_id = :municipality_id
    """)
    total_result = await db.execute(total_query, {"start_date": start_date, "municipality_id": municipality_id})
    total = total_result.scalar()

    return {"total": total, "days": days}

@router.post("/", response_model=TechnicalSheetResponse)
async def create_technical_sheet(data: TechnicalSheetCreate, db: AsyncSession = Depends(get_db)):
    try:
        uuid_str = str(uuid4())

        new_sheet = TechnicalSheet(
            uuid=uuid_str,
            address=data.address,
            square_meters=data.square_meters,
            coordinates=data.coordinates,
            image=data.image,
            municipality_id=data.municipality_id,
            technical_sheet_download_id=data.technical_sheet_download_id
        )
        db.add(new_sheet)
        await db.commit()
        await db.refresh(new_sheet)

        return {"uuid": new_sheet.uuid}
    except Exception as e:
        logging.error("Error occurred while creating technical sheet: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{uuid}")
async def get_technical_sheet_pdf(uuid: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TechnicalSheet).where(TechnicalSheet.uuid == str(uuid)))
    sheet = result.scalar_one_or_none()

    if not sheet:
        raise HTTPException(status_code=404, detail="Technical sheet not found")

    try:
        coords = json.loads(base64.b64decode(sheet.coordinates))
    except Exception:
        coords = []

    qr = qrcode.make(f"{settings.APP_URL}technical_sheets/{uuid}")
    buf = BytesIO()
    qr.save(buf, format="PNG")
    qr_code_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    text_coords = ",".join([f"{c[0]} {c[1]}" for c in coords])
    polygon = f"POLYGON (({text_coords}))"
    geoserver_url = f"{settings.URL_GEOSERVER}ows?service=WFS&request=GetFeature&version=2.0.0&typename=chih_colonias_ine&outputFormat=application/json&cql_filter=INTERSECTS(geom, {polygon})"
    
    georesp = requests.get(geoserver_url)

    if georesp.status_code == 200 and georesp.content:
        try:
            data = georesp.json()
        except Exception:
            data = {}
    else:
        data = {}

    if data.get("numberReturned", 0) == 0:
        template = env.get_template("technical_sheets404.html")
        html = template.render(qr=qr_code_base64, img=sheet.image, direccion=sheet.address)
    else:        
        features = data["features"]
        enriched_features = []

        for feature in features:            
            # Gosererver response is spanish
            # We need to translate it to english
            props = feature["properties"]
            municipio_id = props.get("municipio") or props.get("municipio_id", 19)
            distrito = str(props.get("distrito") or props.get("entidad") or props.get("clasificac", 18))            
            clave_zona = props.get("clasificac") or props.get("clave_de_clasificacion_de_zona_secundaria", "")
            
            clave_zona_str = str(clave_zona)
            claves = [str(c).strip() for c in clave_zona_str.split(",") if str(c).strip()]

            normas = []
            if claves:
                for clave in claves:
                    reg_query = await db.execute(
                        select(ZoningControlRegulation).where(
                            ZoningControlRegulation.municipality_id == municipio_id,
                            ZoningControlRegulation.district == distrito,
                            ZoningControlRegulation.regulation_key == clave
                        )
                    )
                    normas.extend(reg_query.scalars().all())
            else:
                
                normas = []

            props["normas_control_edificacion"] = normas
            props["clave_act"] = clave_zona
            props['districto'] = normas[0].district if normas else None
            props["clave_de_zonificacion"] = clave_zona_str
            enriched_features.append(feature)
            
        try:
            square_meters = json.loads(base64.b64decode(sheet.square_meters).decode())
        except Exception:
            square_meters = None

        municipio = await db.get(Municipality, municipio_id)
                

        template = env.get_template("technical_sheets.html")
        html = template.render(
            logo=settings.APP_LOGO,
            qr=qr_code_base64,
            img=sheet.image,
            municipio=municipio,       
            features=enriched_features,
            metros=square_meters,
            direccion=sheet.address
        )

    pdf_bytes = HTML(string=html).write_pdf()
    return Response(content=pdf_bytes, media_type="application/pdf")