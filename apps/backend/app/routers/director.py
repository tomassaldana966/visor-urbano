from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, extract, text, desc
from config.settings import get_db, settings
from config.security import get_current_user
from typing import List, Optional
from datetime import datetime, date, timedelta
import logging
from pydantic import BaseModel

from app.models.procedures import Procedure
from app.models.requirements_query import RequirementsQuery
from app.models.business_license import BusinessLicense
from app.models.user import UserModel
from app.utils.role_validation import require_director_role

logger = logging.getLogger(__name__)

router = APIRouter()

# Response schemas
class DirectorFacetsResponse(BaseModel):
    total_procedures_this_month: int
    pending_procedures: int
    procedures_completed_today: int
    procedures_by_type: dict

# Enhanced response schemas
class RecentActivityItem(BaseModel):
    id: str
    type: str
    title: str
    description: str
    timestamp: datetime
    folio: Optional[str] = None
    user_name: Optional[str] = None
    priority: Optional[str] = None

class DirectorDashboardResponse(BaseModel):
    total_procedures_this_month: int
    pending_procedures: int
    licenses_issued_today: int  # Changed from procedures_completed_today
    licenses_trend: int  # Difference compared to yesterday
    average_processing_time: float  # in days
    procedures_by_type: dict
    recent_activities: List[RecentActivityItem]
    pending_reviews: int  # Procedures requiring director review
    alerts: int  # High priority alerts/issues

class ProceduresByType(BaseModel):
    construction: int
    commercial: int
    other: int

@router.get("/dashboard", response_model=DirectorDashboardResponse)
async def get_director_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get complete director dashboard data including:
    - Total procedures this month
    - Pending procedures 
    - Licenses issued today (vs yesterday comparison)
    - Average processing time in days
    - Procedures by type (construction, commercial, other)
    - Recent activities with real data
    
    This endpoint requires director role permissions.
    """
    # Validate director permissions
    require_director_role(current_user)
    
    try:
        # Get current month start and end dates
        now = datetime.now()
        current_month_start = datetime(now.year, now.month, 1)
        if now.month == 12:
            next_month_start = datetime(now.year + 1, 1, 1)
        else:
            next_month_start = datetime(now.year, now.month + 1, 1)
        
        # Get today's dates
        today_start = datetime(now.year, now.month, now.day)
        today_end = datetime(now.year, now.month, now.day, 23, 59, 59)
        
        # Get municipality_id from current user
        municipality_id = getattr(current_user, 'municipality_id', None) or getattr(current_user, 'id_municipality', None)
        
        # Base query for procedures in the user's municipality
        base_query_conditions = []
        if municipality_id:
            base_query_conditions.append(Procedure.municipality_id == municipality_id)
        
        # 1. Total procedures this month
        total_procedures_this_month_query = select(func.count(Procedure.id)).where(
            and_(
                Procedure.created_at >= current_month_start,
                Procedure.created_at < next_month_start,
                *base_query_conditions
            )
        )
        total_procedures_this_month_result = await db.execute(total_procedures_this_month_query)
        total_procedures_this_month = total_procedures_this_month_result.scalar() or 0
        
        # 2. Pending procedures (status 1 = pending_review)
        pending_procedures_query = select(func.count(Procedure.id)).where(
            and_(
                Procedure.status == 1,  # pending_review status
                or_(
                    Procedure.director_approval == 0,
                    Procedure.director_approval.is_(None),
                    Procedure.window_license_generated == 0,
                    Procedure.window_license_generated.is_(None)
                ),
                *base_query_conditions
            )
        )
        pending_procedures_result = await db.execute(pending_procedures_query)
        pending_procedures = pending_procedures_result.scalar() or 0
        
        # 3. Licenses issued today (window_license_generated = 1 and license_delivered_date is today)
        licenses_issued_today_query = select(func.count(Procedure.id)).where(
            and_(
                Procedure.license_delivered_date >= today_start,
                Procedure.license_delivered_date <= today_end,
                Procedure.window_license_generated == 1,  # Specifically licenses that were issued
                *base_query_conditions
            )
        )
        licenses_issued_today_result = await db.execute(licenses_issued_today_query)
        licenses_issued_today = licenses_issued_today_result.scalar() or 0
        
        # Get licenses issued yesterday for comparison
        yesterday_start = today_start - timedelta(days=1)
        yesterday_end = yesterday_start.replace(hour=23, minute=59, second=59)
        
        licenses_issued_yesterday_query = select(func.count(Procedure.id)).where(
            and_(
                Procedure.license_delivered_date >= yesterday_start,
                Procedure.license_delivered_date <= yesterday_end,
                Procedure.window_license_generated == 1,
                *base_query_conditions
            )
        )
        licenses_issued_yesterday_result = await db.execute(licenses_issued_yesterday_query)
        licenses_issued_yesterday = licenses_issued_yesterday_result.scalar() or 0
        
        # Calculate difference for trend
        licenses_trend = licenses_issued_today - licenses_issued_yesterday
        
        # 4. Calculate average processing time
        # Get completed procedures with creation and completion dates
        completed_procedures_query = select(
            func.extract('epoch', Procedure.updated_at - Procedure.created_at) / 86400
        ).where(
            and_(
                or_(
                    Procedure.director_approval == 1,
                    Procedure.window_license_generated == 1
                ),
                Procedure.created_at.is_not(None),
                Procedure.updated_at.is_not(None),
                Procedure.updated_at >= current_month_start - timedelta(days=settings.DASHBOARD_HISTORICAL_PERIOD_DAYS),
                *base_query_conditions
            )
        )
        
        completed_procedures_result = await db.execute(completed_procedures_query)
        processing_times = completed_procedures_result.scalars().all()
        
        if processing_times:
            average_processing_time = sum(processing_times) / len(processing_times)
        else:
            average_processing_time = settings.DASHBOARD_DEFAULT_PROCESSING_TIME_DAYS
        
        # 5. Procedures by type (same logic as facets endpoint)
        construction_query = select(func.count(Procedure.id)).where(
            and_(
                or_(
                    Procedure.procedure_type.ilike('%permits_building_license%'),
                    Procedure.procedure_type.ilike('%licencia_construccion%'),
                    Procedure.folio.ilike('CONS-%')
                ),
                *base_query_conditions
            )
        )
        construction_result = await db.execute(construction_query)
        construction_count = construction_result.scalar() or 0
        
        commercial_query = select(func.count(Procedure.id)).where(
            and_(
                or_(
                    Procedure.procedure_type.ilike('%business_license%'),
                    Procedure.procedure_type.ilike('%comercial%'),
                    Procedure.folio.in_(
                        select(BusinessLicense.license_folio).where(
                            BusinessLicense.license_folio.is_not(None)
                        )
                    )
                ),
                and_(
                    ~Procedure.procedure_type.ilike('%construccion%'),
                    ~Procedure.procedure_type.ilike('%licencia_construccion%'),
                    ~Procedure.folio.ilike('CONS-%')
                ),
                *base_query_conditions
            )
        )
        commercial_result = await db.execute(commercial_query)
        commercial_count = commercial_result.scalar() or 0
        
        total_procedures_query = select(func.count(Procedure.id)).where(
            and_(*base_query_conditions) if base_query_conditions else True
        )
        total_procedures_result = await db.execute(total_procedures_query)
        total_procedures = total_procedures_result.scalar() or 0
        
        other_count = max(0, total_procedures - construction_count - commercial_count)
        
        # 6. Get recent activities
        recent_activities_query = select(
            Procedure.id,
            Procedure.folio,
            Procedure.official_applicant_name,
            Procedure.procedure_type,
            Procedure.status,
            Procedure.director_approval,
            Procedure.window_license_generated,
            Procedure.created_at,
            Procedure.updated_at
        ).where(
            and_(*base_query_conditions) if base_query_conditions else True
        ).order_by(desc(Procedure.updated_at)).limit(settings.DASHBOARD_RECENT_ACTIVITIES_LIMIT)
        
        recent_activities_result = await db.execute(recent_activities_query)
        recent_procedures = recent_activities_result.fetchall()
        
        # Transform recent activities into structured data
        recent_activities = []
        for proc in recent_procedures:
            activity_type = "submission"
            title = "New Application"
            description = "A new procedure application was registered"
            priority = None
            
            # Determine activity type based on procedure state
            if proc.director_approval == 1:
                activity_type = "approval"
                title = "License Approved"
                description = "Application was approved by director"
                priority = "high"
            elif proc.window_license_generated == 1:
                activity_type = "approval"
                title = "License Generated"
                description = "License was generated at service window"
                priority = "medium"
            elif proc.status == 1 and (proc.director_approval == 0 or proc.director_approval is None):
                activity_type = "review"
                title = "Awaiting Review"
                description = "Procedure pending director review"
                priority = "medium"
            elif proc.status == 2:
                activity_type = "approval"
                title = "Procedure Approved"
                description = "The procedure was approved"
                priority = "high"
            elif proc.status == 3:
                activity_type = "rejection"
                title = "Procedure Rejected"
                description = "The procedure was rejected"
                priority = "low"
            elif proc.status == 0:
                activity_type = "submission"
                title = "Draft Procedure"
                description = "Procedure in draft or incomplete state"
                priority = "low"
            
            recent_activities.append(RecentActivityItem(
                id=str(proc.id),
                type=activity_type,
                title=title,
                description=description,
                timestamp=proc.updated_at,
                folio=proc.folio,
                user_name=proc.official_applicant_name or "User not specified",
                priority=priority
            ))
        
        # 7. Calculate pending reviews (procedures waiting for director review)
        pending_reviews_query = select(func.count(Procedure.id)).where(
            and_(
                Procedure.status == 1,
                or_(
                    Procedure.director_approval == 0,
                    Procedure.director_approval.is_(None)
                ),
                Procedure.window_license_generated != 1,  # Not yet completed
                *base_query_conditions
            )
        )
        pending_reviews_result = await db.execute(pending_reviews_query)
        pending_reviews = pending_reviews_result.scalar() or 0
        
        # 8. Calculate alerts (high priority issues)
        # Consider as alerts: procedures older than threshold days without director approval
        alert_date_threshold = now - timedelta(days=settings.DASHBOARD_ALERT_THRESHOLD_DAYS)
        alerts_query = select(func.count(Procedure.id)).where(
            and_(
                Procedure.status == 1,
                or_(
                    Procedure.director_approval == 0,
                    Procedure.director_approval.is_(None)
                ),
                Procedure.created_at < alert_date_threshold,
                *base_query_conditions
            )
        )
        alerts_result = await db.execute(alerts_query)
        alerts = alerts_result.scalar() or 0

        # Prepare response
        response = DirectorDashboardResponse(
            total_procedures_this_month=total_procedures_this_month,
            pending_procedures=pending_procedures,
            licenses_issued_today=licenses_issued_today,
            licenses_trend=licenses_trend,
            average_processing_time=round(average_processing_time, 1),
            procedures_by_type={
                "construction": construction_count,
                "commercial": commercial_count,
                "others": other_count
            },
            recent_activities=recent_activities,
            pending_reviews=pending_reviews,
            alerts=alerts
        )
        
        logger.info(f"Director dashboard data retrieved for user {current_user.id} in municipality {municipality_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error retrieving director dashboard data for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving director dashboard data: {str(e)}"
        )

@router.get("/facets", response_model=DirectorFacetsResponse)
async def get_director_facets(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get director dashboard facets including:
    - Total procedures this month
    - Pending procedures 
    - Procedures completed today
    - Procedures by type (construction, commercial, other)
    
    This endpoint requires director role permissions.
    """
    # Validate director permissions
    require_director_role(current_user)
    
    try:
        # Get current month start and end dates
        now = datetime.now()
        current_month_start = datetime(now.year, now.month, 1)
        if now.month == 12:
            next_month_start = datetime(now.year + 1, 1, 1)
        else:
            next_month_start = datetime(now.year, now.month + 1, 1)
        
        # Get today's dates
        today_start = datetime(now.year, now.month, now.day)
        today_end = datetime(now.year, now.month, now.day, 23, 59, 59)
        
        # Get municipality_id from current user
        municipality_id = getattr(current_user, 'municipality_id', None) or getattr(current_user, 'id_municipality', None)
        
        # Base query for procedures in the user's municipality
        base_query_conditions = []
        if municipality_id:
            base_query_conditions.append(Procedure.municipality_id == municipality_id)
        
        # 1. Total procedures this month
        total_procedures_this_month_query = select(func.count(Procedure.id)).where(
            and_(
                Procedure.created_at >= current_month_start,
                Procedure.created_at < next_month_start,
                *base_query_conditions
            )
        )
        total_procedures_this_month_result = await db.execute(total_procedures_this_month_query)
        total_procedures_this_month = total_procedures_this_month_result.scalar() or 0
        
        # 2. Pending procedures (status 1 = pending_review)
        pending_procedures_query = select(func.count(Procedure.id)).where(
            and_(
                Procedure.status == 1,  # pending_review status
                or_(
                    Procedure.director_approval == 0,
                    Procedure.director_approval.is_(None),
                    Procedure.window_license_generated == 0,
                    Procedure.window_license_generated.is_(None)
                ),
                *base_query_conditions
            )
        )
        pending_procedures_result = await db.execute(pending_procedures_query)
        pending_procedures = pending_procedures_result.scalar() or 0
        
        # 3. Procedures completed today (where window_license_generated = 1 or director_approval = 1)
        procedures_completed_today_query = select(func.count(Procedure.id)).where(
            and_(
                Procedure.updated_at >= today_start,
                Procedure.updated_at <= today_end,
                or_(
                    Procedure.director_approval == 1,
                    Procedure.window_license_generated == 1
                ),
                *base_query_conditions
            )
        )
        procedures_completed_today_result = await db.execute(procedures_completed_today_query)
        procedures_completed_today = procedures_completed_today_result.scalar() or 0
        
        # 4. Procedures by type
        # Construction procedures: identified by procedure_type containing "construccion" or "licencia_construccion"
        # or by folio patterns starting with "CONS-"
        construction_query = select(func.count(Procedure.id)).where(
            and_(
                or_(
                    Procedure.procedure_type.ilike('%permits_building_license%'),
                    Procedure.procedure_type.ilike('%licencia_construccion%'),
                    Procedure.folio.ilike('CONS-%')
                ),
                *base_query_conditions
            )
        )
        construction_result = await db.execute(construction_query)
        construction_count = construction_result.scalar() or 0
        
        # Commercial procedures: identified by procedure_type containing "giro" or "comercial"
        commercial_query = select(func.count(Procedure.id)).where(
            and_(
                or_(
                    Procedure.procedure_type.ilike('%business_license%'),
                    Procedure.procedure_type.ilike('%comercial%'),
                    # Also check if we have a business license associated with this folio
                    Procedure.folio.in_(
                        select(BusinessLicense.license_folio).where(
                            BusinessLicense.license_folio.is_not(None)
                        )
                    )
                ),
                # Exclude construction procedures
                and_(
                    ~Procedure.procedure_type.ilike('%construccion%'),
                    ~Procedure.procedure_type.ilike('%licencia_construccion%'),
                    ~Procedure.folio.ilike('CONS-%')
                ),
                *base_query_conditions
            )
        )
        commercial_result = await db.execute(commercial_query)
        commercial_count = commercial_result.scalar() or 0
        
        # Other procedures: all procedures not classified as construction or commercial
        total_procedures_query = select(func.count(Procedure.id)).where(
            and_(*base_query_conditions) if base_query_conditions else True
        )
        total_procedures_result = await db.execute(total_procedures_query)
        total_procedures = total_procedures_result.scalar() or 0
        
        other_count = max(0, total_procedures - construction_count - commercial_count)
        
        # Prepare response
        response = DirectorFacetsResponse(
            total_procedures_this_month=total_procedures_this_month,
            pending_procedures=pending_procedures,
            procedures_completed_today=procedures_completed_today,
            procedures_by_type={
                "construction": construction_count,
                "commercial": commercial_count,
                "others": other_count
            }
        )
        
        logger.info(f"Director facets retrieved for user {current_user.id} in municipality {municipality_id}: {response}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error retrieving director facets for user {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving director dashboard data: {str(e)}"
        )
