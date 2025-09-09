
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.requirements_query import RequirementsQuery
from app.models.business_license import BusinessLicense
from datetime import datetime
from sqlalchemy.orm import joinedload

async def get_unsigned_receipt_data_async(folio: str, db: AsyncSession) -> dict | None:
    stmt = select(RequirementsQuery).where(RequirementsQuery.folio == folio)
    result = await db.execute(stmt)
    rq = result.scalars().first()

    if not rq:
        return None

    return {
        "folio": rq.folio,
        "street": rq.street,
        "neighborhood": rq.neighborhood,
        "municipality_name": rq.municipality_name,
        "scian_code": rq.scian_code,
        "scian_name": rq.scian_name,
        "applicant_name": rq.applicant_name or "N/A",
        "applicant_character": rq.applicant_character or "N/A",
        "person_type": rq.person_type or "N/A",
        "property_area": rq.property_area,
        "activity_area": rq.activity_area,
        "alcohol_sales": bool(rq.alcohol_sales),
        "created_at": rq.created_at.isoformat() if rq.created_at else None,
    }
    
async def get_responsible_letter_data(db: AsyncSession, folio: str) -> dict:
    """
    Fetch and assemble data needed for the Responsible Letter PDF using the BusinessLicense model.
    """
    # 1) Query the BusinessLicense by license_folio
    result = await db.execute(
        select(BusinessLicense)
        .where(BusinessLicense.license_folio == folio)
        .options(joinedload(BusinessLicense.municipality))
    )
    license_obj = result.scalars().first()
    if not license_obj:
        return None

    municipality = license_obj.municipality

    date_str = datetime.now().strftime("%d/%m/%Y")
    full_name = " ".join(filter(None, [
        license_obj.owner,
        license_obj.owner_last_name_p,
        license_obj.owner_last_name_m
    ]))

    applicant = {
        "name": full_name,
        "id_type": "National ID",
        "id_number": license_obj.national_id or "",
        "id_issuer": "",
    }

    address = {
        "neighborhood": municipality.address or "",
        "cp": "",
    }

    return {
        "government_logo": municipality.image or "https://visorurbano.com/assets/img/logo.png",
        "logo_url": license_obj.logo_image or "https://visorurbano.com/assets/img/logo.png",
        "municipality": municipality.name,
        "date": date_str,
        "applicant": applicant,
        "scian_name": license_obj.commercial_activity,
        "address": address,
    }

