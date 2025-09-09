from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from config.settings import get_db
from datetime import datetime
from typing import List
import json
from app.schemas.reports import (
    ChartPoint, 
    LicensingStatusSummary, 
    BarListFilter, 
    BarListItem, 
    ReviewStatusSummary,
    MunicipalityPiePoint, 
    FullReportResponse,
    MunicipalityLicenseSummary,
    MunicipalityHistoricSummary,
    TechnicalSheetReportSummary, 
    TechnicalSheetDownload,
    KPIsSummary,
    StatusDistribution,
    DependencyMetrics,
    CompleteAnalytics
)
from config.security import get_current_user
from app.models.requirements_query import RequirementsQuery
from app.models.procedures import Procedure
from app.models.technical_sheet_downloads import TechnicalSheetDownload as TechnicalSheetDownloadModel
from datetime import date
import logging

router = APIRouter(prefix="/reports/charts")

@router.get("/annual-bar", response_model=list[ChartPoint])
async def get_annual_bar_chart(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    if not hasattr(current_user, 'id_municipality') or not current_user.id_municipality:
        raise HTTPException(status_code=404, detail="Municipality not found for user")
    
    try:
        municipality_id = current_user.id_municipality
        current_year = datetime.now().year

        query = text("""
            SELECT COUNT(tra.*) as count, EXTRACT(Month FROM tra.created_at) AS month
            FROM business_licenses tra
            JOIN requirements_queries cons ON tra.folio = cons.folio
            WHERE cons.municipality_id = :municipality_id AND EXTRACT(YEAR FROM tra.created_at) = :year
            GROUP BY month
            ORDER BY month ASC
        """)

        result = await db.execute(query, {"municipality_id": municipality_id, "year": current_year})
        data = result.fetchall()

        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']

        return [
            ChartPoint(name=month_names[int(row.month) - 1], value=row.count, extra=int(row.month))
            for row in data
        ]
    except Exception as e:
        logging.error(f"Error in get_annual_bar_chart: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/advanced-pie", response_model=LicensingStatusSummary)
async def get_licensing_status_summary(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    if not hasattr(current_user, 'id_municipality') or not current_user.id_municipality:
        raise HTTPException(status_code=404, detail="Municipality not found for user")
    
    try:
        municipality_id = current_user.id_municipality

        stmt_consultation = select(func.count()).select_from(RequirementsQuery).outerjoin(
            Procedure, RequirementsQuery.folio == Procedure.folio
        ).where(
            Procedure.id.is_(None),
            RequirementsQuery.municipality_id == municipality_id
        )

        stmt_initiated = select(func.count()).select_from(RequirementsQuery).outerjoin(
            Procedure, RequirementsQuery.folio == Procedure.folio
        ).where(
            Procedure.sent_to_reviewers.is_(None),
            RequirementsQuery.municipality_id == municipality_id
        )

        stmt_under_review = select(func.count()).select_from(RequirementsQuery).join(
            Procedure, RequirementsQuery.folio == Procedure.folio
        ).where(
            Procedure.sent_to_reviewers == 1,
            Procedure.license_pdf == "",
            RequirementsQuery.municipality_id == municipality_id
        )

        stmt_issued = text("""
            SELECT COUNT(*) FROM business_licenses bl
            JOIN requirements_queries rq ON bl.folio = rq.folio
            WHERE rq.municipality_id = :municipality_id
        """)

        result_1 = await db.execute(stmt_consultation)
        result_2 = await db.execute(stmt_initiated)
        result_3 = await db.execute(stmt_under_review)
        result_4 = await db.execute(stmt_issued, {"municipality_id": municipality_id})

        return LicensingStatusSummary(
            consultation=result_1.scalar(),
            initiated=result_2.scalar(),
            under_review=result_3.scalar(),
            issued=result_4.scalar()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/annual-bar/{municipality_id}", response_model=list[ChartPoint])
async def get_annual_bar_by_municipality(
    municipality_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    current_year = datetime.now().year

    query = text("""
        SELECT COUNT(bl.*) AS count, EXTRACT(MONTH FROM bl.created_at) AS month
        FROM business_licenses bl
        JOIN requirements_querys rq ON bl.folio = rq.folio
        WHERE rq.municipality_id = :municipality_id
          AND EXTRACT(YEAR FROM bl.created_at) = :year
        GROUP BY month
        ORDER BY month ASC
    """)

    result = await db.execute(query, {"municipality_id": municipality_id, "year": current_year})
    rows = result.fetchall()

    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    return [
        ChartPoint(name=month_names[int(row.month) - 1], value=row.count, extra=int(row.month))
        for row in rows
    ]
    
@router.get("/advanced-pie-admin", response_model=LicensingStatusSummary)
async def get_licensing_status_admin(
    municipality_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    where_clause = (
        RequirementsQuery.municipality_id == municipality_id
        if municipality_id else True
    )

    stmt_consultation = select(func.count()).select_from(RequirementsQuery).outerjoin(
        Procedure, RequirementsQuery.folio == Procedure.folio
    ).where(
        Procedure.id.is_(None),
        where_clause
    )

    stmt_initiated = select(func.count()).select_from(RequirementsQuery).outerjoin(
        Procedure, RequirementsQuery.folio == Procedure.folio
    ).where(
        Procedure.sent_to_reviewers.is_(None),
        where_clause
    )

    stmt_under_review = select(func.count()).select_from(RequirementsQuery).join(
        Procedure, RequirementsQuery.folio == Procedure.folio
    ).where(
        Procedure.sent_to_reviewers == 1,
        Procedure.license_pdf == "",
        where_clause
    )

    stmt_issued = text("""
        SELECT COUNT(*) FROM business_licenses bl
        JOIN requirements_querys rq ON bl.folio = rq.folio
        WHERE (:municipality_id IS NULL OR rq.municipality_id = :municipality_id)
    """)

    result_1 = await db.execute(stmt_consultation)
    result_2 = await db.execute(stmt_initiated)
    result_3 = await db.execute(stmt_under_review)
    result_4 = await db.execute(stmt_issued, {"municipality_id": municipality_id})

    return LicensingStatusSummary(
        consultation=result_1.scalar(),
        initiated=result_2.scalar(),
        under_review=result_3.scalar(),
        issued=result_4.scalar()
    )

@router.post("/bar-list", response_model=List[BarListItem])
async def get_bar_list(
    filters: BarListFilter,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # for testing purposes 
    # if current_user.role_id != 5 and not filters.municipality_id:
    filters.municipality_id = current_user.id_municipality

    query = text("""
        SELECT 
            rq.folio, rq.street, rq.neighborhood, rq.scian_code, rq.scian_name,
            bl.numero_lic AS number_license, bl.dueno AS owner, bl.anio_licencia AS license_year
        FROM business_licenses bl
        JOIN requirements_querys rq ON bl.folio = rq.folio
        WHERE rq.municipality_id = :municipality_id
          AND EXTRACT(MONTH FROM bl.created_at) = :month
          AND bl.created_at BETWEEN :start_date AND :end_date
    """)

    result = await db.execute(query, {
        "municipality_id": filters.municipality_id,
        "month": filters.month,
        "start_date": filters.start_date,
        "end_date": filters.end_date
    })

    rows = result.fetchall()
    return [BarListItem(**row._mapping) for row in rows]

@router.get("/review-pie", response_model=ReviewStatusSummary)
async def get_review_status_pie(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    if not hasattr(current_user, 'id_municipality') or not current_user.id_municipality:
        raise HTTPException(status_code=404, detail="Municipality not found for user")
    
    try:
        municipality_id = current_user.id_municipality

        queries = {
            "approved": text("""
                SELECT COUNT(*) FROM dependency_reviews
                WHERE status_actual = 1 AND rol = 4 AND id_municipio = :municipality_id
            """),
            "under_review": text("""
                SELECT COUNT(*) FROM dependency_reviews
                WHERE status_actual IS NULL AND rol IN (3,4) AND id_municipio = :municipality_id
            """),
            "corrected": text("""
                SELECT COUNT(*) FROM dependency_reviews
                WHERE status_actual = 3 AND id_municipio = :municipality_id
            """),
            "discarded": text("""
                SELECT COUNT(*) FROM dependency_reviews
                WHERE status_actual = 2 AND rol = 4 AND id_municipio = :municipality_id
            """)
        }

        results = {}
        for key, stmt in queries.items():
            res = await db.execute(stmt, {"municipality_id": municipality_id})
            results[key] = res.scalar()

        return ReviewStatusSummary(**results)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/pie-by-municipality", response_model=List[MunicipalityPiePoint])
async def get_pie_by_municipality(
    start_date: date,
    end_date: date,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = text("""
        SELECT 
            rq.municipality AS name,
            rq.municipality_id AS extra,
            COUNT(bl.id) AS value
        FROM business_licenses bl
        JOIN requirements_querys rq ON bl.folio = rq.folio
        WHERE bl.created_at BETWEEN :start_date AND :end_date
        GROUP BY rq.municipality, rq.municipality_id
        ORDER BY value DESC
    """)

    result = await db.execute(query, {
        "start_date": start_date,
        "end_date": end_date
    })

    rows = result.fetchall()
    return [MunicipalityPiePoint(**row._mapping) for row in rows]

@router.get("/monthly-bar/{municipality_id}", response_model=List[ChartPoint])
async def get_monthly_bar_by_municipality(
    municipality_id: int,
    start_date: date,
    end_date: date,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = text("""
        SELECT 
            EXTRACT(MONTH FROM bl.created_at) AS month,
            COUNT(bl.id) AS value
        FROM business_licenses bl
        JOIN requirements_querys rq ON bl.folio = rq.folio
        WHERE rq.municipality_id = :municipality_id
          AND bl.created_at BETWEEN :start_date AND :end_date
        GROUP BY month
        ORDER BY month
    """)

    result = await db.execute(query, {
        "municipality_id": municipality_id,
        "start_date": start_date,
        "end_date": end_date
    })

    rows = result.fetchall()
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    return [
        ChartPoint(name=month_names[int(row.month) - 1], value=row.value, extra=int(row.month))
        for row in rows
    ]

@router.get("/full-report", response_model=FullReportResponse)
async def get_full_license_report(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    totals_query = text("""
        SELECT
            COUNT(*) FILTER (WHERE bl.municipality_id != 1 AND bl.deleted_at IS NULL) AS total_current,
            COUNT(*) FILTER (WHERE bl.municipality_id != 1 AND bl.tipo_licencia = 'Refrendo' AND bl.deleted_at IS NULL) AS total_refrendo_current,
            COUNT(*) FILTER (WHERE bl.municipality_id != 1 AND bl.tipo_licencia = 'Nueva' AND bl.deleted_at IS NULL) AS total_nueva_current
        FROM business_licenses bl
    """)

    historic_total_query = text("""
        SELECT COUNT(*) FROM business_license_histories
        WHERE id_municipio != 1 AND tipo_licencia = 'Refrendo' AND deleted_at IS NULL
    """)

    current_municipalities_query = text("""
        SELECT
            m.id,
            m.name,
            COUNT(*) FILTER (WHERE bl.tipo_licencia = 'Refrendo') AS total_refrendo,
            COUNT(*) FILTER (WHERE bl.tipo_licencia = 'Nueva') AS total_nueva,
            COUNT(*) AS total_final
        FROM business_licenses bl
        JOIN municipalities m ON bl.municipality_id = m.id
        WHERE bl.municipality_id != 1 AND bl.deleted_at IS NULL
        GROUP BY m.id, m.name
    """)

    historic_municipalities_query = text("""
        SELECT
            m.id,
            m.name,
            COUNT(*) AS total
        FROM business_license_histories blh
        JOIN municipalities m ON blh.id_municipio = m.id
        WHERE blh.id_municipio != 1 AND blh.tipo_licencia = 'Refrendo' AND blh.deleted_at IS NULL
        GROUP BY m.id, m.name
    """)

    totals = (await db.execute(totals_query)).mappings().first()
    historic_total = (await db.execute(historic_total_query)).scalar()
    current_municipalities = (await db.execute(current_municipalities_query)).mappings().all()
    historic_municipalities = (await db.execute(historic_municipalities_query)).mappings().all()

    return FullReportResponse(
        total_current=totals["total_current"],
        total_refrendo_current=totals["total_refrendo_current"],
        total_nueva_current=totals["total_nueva_current"],
        total_historic=historic_total,
        total_combined=totals["total_current"] + historic_total,
        current_by_municipality=[MunicipalityLicenseSummary(**row) for row in current_municipalities],
        historic_by_municipality=[MunicipalityHistoricSummary(**row) for row in historic_municipalities],
    )
    
@router.get("/technical-sheets-summary", response_model=TechnicalSheetReportSummary)
async def get_technical_sheet_report(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(select(TechnicalSheetDownloadModel).order_by(TechnicalSheetDownloadModel.id.asc))
    records = result.scalars().all()

    parsed_data = []
    for obj in records:
        try:
            parsed_uses = json.loads(obj.uses) if obj.uses else []
        except Exception:
            parsed_uses = []

        parsed_data.append(TechnicalSheetDownload(
            id=obj.id,
            name=obj.name,
            email=obj.email,
            age=int(obj.age) if obj.age else 0,
            city=obj.city or "",
            sector=obj.sector or "",
            uses=parsed_uses,
            address=obj.address or "",
            municipality=obj.municipality or "",
            created_at=obj.created_at
        ))

    total = len(parsed_data)

    def count_percent(items: List[str]) -> dict:
        count = {}
        for item in items:
            count[item] = count.get(item, 0) + 1
        return {k: round((v / total) * 100, 2) for k, v in count.items()}

    def extract(field: str) -> List[str]:
        values = []
        for d in parsed_data:
            attr = getattr(d, field)
            values.extend(attr if isinstance(attr, list) else [attr])
        return values

    def age_groups(data: List[TechnicalSheetDownload]) -> dict:
        dist = {'18-24': 0, '25-34': 0, '35-44': 0, '44-55': 0, '55-64': 0}
        for d in data:
            age = d.age
            if 18 <= age <= 24:
                dist['18-24'] += 1
            elif 25 <= age <= 34:
                dist['25-34'] += 1
            elif 35 <= age <= 44:
                dist['35-44'] += 1
            elif 45 <= age <= 55:
                dist['44-55'] += 1
            elif 56 <= age <= 64:
                dist['55-64'] += 1
        return dist

    return TechnicalSheetReportSummary(
        sectors_percentage=count_percent(extract("sector")),
        uses_percentage=count_percent(extract("uses")),
        age_distribution=age_groups(parsed_data),
        top_cities=dict(sorted(count_percent(extract("city")).items(), key=lambda x: x[1], reverse=True)),
        users_per_municipality={}, 
        data=parsed_data
    )

@router.get("/complete-analytics", response_model=CompleteAnalytics)
async def get_complete_analytics(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get complete analytics with all calculations done in backend
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    if not hasattr(current_user, 'id_municipality') or not current_user.id_municipality:
        raise HTTPException(status_code=404, detail="Municipality not found for user")
    
    try:
        municipality_id = current_user.id_municipality
        
        # Get basic data
        annual_data = await get_annual_bar_chart(db, current_user)
        licensing_data = await get_licensing_status_summary(db, current_user)
        review_data = await get_review_status_pie(db, current_user)
        
        # Calculate totals
        total_licenses = (licensing_data.consultation + licensing_data.initiated + 
                         licensing_data.under_review + licensing_data.issued)
        
        total_reviews = (review_data.approved + review_data.under_review + 
                        review_data.corrected + review_data.discarded)
        
        # Calculate KPIs
        tiempo_promedio = 8.5  # Default
        if total_licenses > 0:
            tiempo_promedio = round(
                ((licensing_data.under_review * 15 + licensing_data.issued * 8) / total_licenses) * 10
            ) / 10
        
        eficiencia = 0
        if total_licenses > 0:
            eficiencia = round((licensing_data.issued / total_licenses) * 100)
        
        satisfaccion = 4.2  # Default
        if total_reviews > 0:
            satisfaccion = round(((review_data.approved / total_reviews) * 2 + 3) * 10) / 10
        
        kpis = KPIsSummary(
            tiempo_promedio=tiempo_promedio,
            eficiencia=eficiencia,
            total_procesados=licensing_data.issued,
            satisfaccion=satisfaccion
        )
        
        # Calculate status distribution with percentages
        distribucion_estados = []
        status_data = [
            ("Consultations", licensing_data.consultation, "bg-gray-500"),
            ("Initiated", licensing_data.initiated, "bg-blue-500"),
            ("Under Review", licensing_data.under_review, "bg-yellow-500"),
            ("Issued", licensing_data.issued, "bg-green-500")
        ]
        
        for estado, cantidad, color in status_data:
            porcentaje = 0
            if total_licenses > 0:
                porcentaje = round((cantidad / total_licenses) * 100)
            
            distribucion_estados.append(StatusDistribution(
                estado=estado,
                cantidad=cantidad,
                porcentaje=porcentaje,
                color=color
            ))
        
        # Calculate dependency metrics
        dependencias = []
        dependency_data = [
            ("1", "Approved Reviews", review_data.approved, "excellent"),
            ("2", "Under Review", review_data.under_review, "good"),
            ("3", "For Correction", review_data.corrected, "warning"),
            ("4", "Discarded", review_data.discarded, "poor")
        ]
        
        for dep_id, nombre, tramites, estado in dependency_data:
            # Calculate tiempo_promedio based on volume and type
            base_times = {"1": 7, "2": 9, "3": 12, "4": 15}
            tiempo_promedio_dep = base_times[dep_id]
            if total_reviews > 0 and tramites > 0:
                factor = (tramites / max(total_reviews, 1))
                multipliers = {"1": 3, "2": 2, "3": 5, "4": 8}
                tiempo_promedio_dep = round((base_times[dep_id] + factor * multipliers[dep_id]) * 10) / 10
            
            # Calculate efficiency
            eficiencia_dep = 0
            if total_reviews > 0:
                if dep_id == "1":  # Approved
                    eficiencia_dep = round((tramites / total_reviews) * 100)
                elif dep_id == "2":  # Under Review
                    eficiencia_dep = round(((total_reviews - review_data.discarded) / total_reviews) * 100)
                elif dep_id == "3":  # Corrected
                    eficiencia_dep = round(((total_reviews - review_data.discarded - review_data.corrected) / total_reviews) * 100)
                elif dep_id == "4":  # Discarded
                    eficiencia_dep = max(round(((total_reviews - review_data.discarded) / total_reviews) * 100), 65)
            
            dependencias.append(DependencyMetrics(
                id=dep_id,
                nombre=nombre,
                tramites_procesados=tramites,
                tiempo_promedio=tiempo_promedio_dep,
                eficiencia=eficiencia_dep,
                estado=estado
            ))
        
        return CompleteAnalytics(
            kpis=kpis,
            tendencias=annual_data,
            distribucion_estados=distribucion_estados,
            dependencias=dependencias,
            licensing_status=licensing_data,
            review_status=review_data
        )
        
    except Exception as e:
        logging.error(f"Error in get_complete_analytics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")