import base64
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import unquote
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Path, Query, UploadFile
from sqlalchemy import and_, desc, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.dependency_resolutions import DependencyResolution
from app.models.dependency_reviews import DependencyReview, DirectorApproval, PreventionRequest
from app.models.notifications import Notification as UserNotification
from app.models.procedures import Procedure
from app.models.technical_sheet_downloads import TechnicalSheetDownload
from app.models.user import UserModel as User
from app.schemas.dependency_reviews import (
    AnalyticsRequest,
    AnalyticsResponse,
    BulkResolutionUpdate,
    BusinessDaysCalculation,
    DependencyResolutionCreate,
    DependencyResolutionResponse,
    DependencyResolutionUpdate,
    DependencyReviewCreate,
    DependencyReviewFilter,
    DependencyReviewResponse,
    DependencyReviewUpdate,
    DirectorApprovalCreate,
    DirectorApprovalResponse,
    DirectorInsertRequest,
    FileUploadRequest,
    LicenseEmissionRequest,
    NotificationCreate,
    NotificationEmailRequest,
    NotificationResponse,
    PreventionRequestCreate,
    PreventionRequestResponse,
    ResolutionInfoResponse,
    ResolutionStatistics,
)
from app.services.emails.sendgrid_client import render_email_template, send_email
from app.services.procedure_notifications import send_procedure_status_notification
from app.utils.role_validation import (
    validate_admin_role,
    validate_director_role,
    validate_reviewer_role,
)
from config.security import get_current_user
from config.settings import get_db

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger.addHandler(handler)

router = APIRouter(prefix="/dependency_reviews")


@router.get("/by_folio/{folio}", response_model=DependencyReviewResponse)
async def get_review_by_folio(
    folio: str = Path(..., description="Unique folio of the dependency review"),
    db: AsyncSession = Depends(get_db)
):
    try:
        stmt = select(DependencyReview).options(
            selectinload(DependencyReview.procedure),
            selectinload(DependencyReview.municipality),
            selectinload(DependencyReview.user),
            selectinload(DependencyReview.resolutions),
            selectinload(DependencyReview.prevention_requests),
            selectinload(DependencyReview.notifications)
        ).where(DependencyReview.folio == folio)

        result = await db.execute(stmt)
        review = result.scalars().first()

        if not review:
            raise HTTPException(status_code=404, detail="Dependency review not found")

        return review

    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error retrieving dependency review by folio {folio}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving dependency review: {str(e)}")


@router.get("/resolution_info/{folio}", response_model=ResolutionInfoResponse)
async def get_resolution_info(
    folio: str = Path(..., description="Folio to get resolution information"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        try:
            decoded_folio = folio
            if len(folio) % 4 == 0:
                decoded_folio = base64.b64decode(folio).decode('utf-8')
        except:
            decoded_folio = folio

        stmt = select(DependencyReview).options(
            selectinload(DependencyReview.procedure),
            selectinload(DependencyReview.municipality),
            selectinload(DependencyReview.user),
            selectinload(DependencyReview.resolutions),
            selectinload(DependencyReview.prevention_requests),
            selectinload(DependencyReview.notifications)
        ).where(DependencyReview.folio == decoded_folio)

        review_result = await db.execute(stmt)
        review = review_result.scalars().first()

        if not review:
            raise HTTPException(status_code=404, detail="Dependency review not found")

        resolutions_stmt = select(DependencyResolution).options(selectinload(DependencyResolution.user)).where(
            DependencyResolution.procedure_id == review.procedure_id
        )
        resolutions_result = await db.execute(resolutions_stmt)
        resolutions = resolutions_result.scalars().all()

        resolutions_with_user = []
        for r in resolutions:
            user_name = None
            user_obj = r.user
            if not user_obj and r.user_id:
                user_result = await db.execute(select(User).where(User.id == r.user_id))
                user_obj = user_result.scalars().first()
            if user_obj:
                name = getattr(user_obj, 'name', '') or ''
                paternal = getattr(user_obj, 'paternal_last_name', '') or ''
                maternal = getattr(user_obj, 'maternal_last_name', '') or ''
                user_name = f"{name} {paternal} {maternal}".strip()
            res_dict = r.__dict__.copy()
            res_dict['user_name'] = user_name
            res_dict.pop('_sa_instance_state', None)
            resolutions_with_user.append(res_dict)

        return {
            "review": review,
            "resolutions": resolutions_with_user,
            "prevention_requests": review.prevention_requests,
            "director_approval": None,
            "procedure_info": {
                "procedure_id": review.procedure_id,
                "municipality_id": review.municipality_id,
                "current_status": review.current_status,
                "director_approved": review.director_approved,
            },
        }

    except Exception as e:
        logger.error(f"Error retrieving resolution info for folio {folio}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving resolution info: {str(e)}")


@router.post("/create_resolution")
async def create_resolution(
    resolution_data: DependencyResolutionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        resolution = DependencyResolution(**resolution_data.dict())
        resolution.user_id = current_user.id

        db.add(resolution)
        await db.commit()
        await db.refresh(resolution)

        return {"detail": "Resolution created successfully", "resolution_id": resolution.id}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating resolution: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating resolution: {str(e)}")


@router.post("/update_resolution/{folio}")
async def update_resolution(
    folio: str,
    resolution_data: DependencyReviewUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        decoded_folio = folio
        try:
            folio_unquoted = unquote(folio)
            if (len(folio_unquoted) % 4 == 0) and ("=" in folio_unquoted):
                decoded_folio = base64.b64decode(folio_unquoted).decode('utf-8')
            else:
                decoded_folio = folio_unquoted
        except Exception:
            decoded_folio = folio

        review_stmt = select(DependencyReview).where(DependencyReview.folio == decoded_folio)
        review_result = await db.execute(review_stmt)
        review = review_result.scalars().first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        user_role = None
        if hasattr(current_user, "roles") and current_user.roles:
            first_role = current_user.roles[0]
            if hasattr(first_role, "id"):
                user_role = first_role.id
            elif isinstance(first_role, dict) and "id" in first_role:
                user_role = first_role["id"]
            else:
                user_role = first_role
        elif hasattr(current_user, "role"):
            user_role = current_user.role
        elif hasattr(current_user, "role_id"):
            user_role = current_user.role_id
        elif isinstance(current_user, dict) and "role" in current_user:
            user_role = current_user["role"]
        elif isinstance(current_user, dict) and "role_id" in current_user:
            user_role = current_user["role_id"]

        resolution_stmt = select(DependencyResolution).where(
            and_(
                DependencyResolution.review_id == review.id,
                DependencyResolution.role == user_role,
                DependencyResolution.user_id == current_user.id
            )
        )
        resolution_result = await db.execute(resolution_stmt)
        resolution = resolution_result.scalars().first()
        now_naive = datetime.utcnow().replace(tzinfo=None)

        if resolution:
            resolution.resolution_status = resolution_data.resolution_status
            resolution.resolution_text = resolution_data.resolution_text
            resolution.resolution_file = resolution_data.resolution_file
            if hasattr(resolution_data, 'additional_files'):
                resolution.additional_files = ','.join(resolution_data.additional_files) if resolution_data.additional_files else None
            resolution.updated_at = now_naive
        else:
            resolution = DependencyResolution(
                review_id=review.id,
                procedure_id=review.procedure_id,
                role=user_role,
                user_id=current_user.id,
                resolution_status=resolution_data.resolution_status,
                resolution_text=resolution_data.resolution_text,
                resolution_file=resolution_data.resolution_file,
                additional_files=','.join(resolution_data.additional_files) if resolution_data.additional_files else None,
                updated_at=now_naive
            )
            db.add(resolution)

        review.current_status = resolution_data.resolution_status
        review.update_date = now_naive
        review.user_id = current_user.id

        # Update the main procedure status based on resolution status
        procedure_stmt = select(Procedure).where(Procedure.id == review.procedure_id)
        procedure_result = await db.execute(procedure_stmt)
        procedure = procedure_result.scalars().first()
        
        if procedure:
            old_status = procedure.status
            if resolution_data.resolution_status == 1:  # Approved
                procedure.status = 2  # Set to approved
                procedure.updated_at = now_naive
            elif resolution_data.resolution_status == 2:  # Rejected
                procedure.status = 3  # Set to rejected
                procedure.updated_at = now_naive
            elif resolution_data.resolution_status == 3:  # Prevention
                procedure.status = 3  # Set to prevention/rejected
                procedure.updated_at = now_naive
            
            logger.info(f"Updated procedure {procedure.id} status from {old_status} to {procedure.status} for resolution status {resolution_data.resolution_status}")
            
            # Send notification if status changed
            if old_status != procedure.status:
                try:
                    await send_procedure_status_notification(
                        db=db,
                        procedure=procedure,
                        previous_status=old_status,
                        new_status=procedure.status,
                        reason=resolution_data.resolution_text,
                        portal_url=None
                    )
                    logger.info(f"Sent status change notification for procedure {procedure.id} from {old_status} to {procedure.status}")
                except Exception as e:
                    logger.error(f"Failed to send notification for procedure {procedure.id}: {str(e)}")
        else:
            logger.warning(f"Procedure not found for review.procedure_id {review.procedure_id}")

        if resolution_data.resolution_status == 3:
            prevention_request = PreventionRequest(
                review_id=review.id,
                procedure_id=review.procedure_id,
                role=user_role,
                user_id=current_user.id,
                comments=resolution_data.resolution_text,
                business_days=15,
                max_resolution_date=await calculate_business_days(now_naive, 15)
            )
            db.add(prevention_request)

        await db.commit()
        await db.refresh(resolution)

        return {"detail": "Resolution updated successfully", "resolution_id": resolution.id}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating resolution for folio {folio}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating resolution: {str(e)}")


@router.post("/update_director_resolution/{folio}")
async def update_director_resolution(
    folio: str,
    resolution_data: DependencyReviewUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if not validate_director_role(current_user):
            raise HTTPException(status_code=403, detail="Director role required")

        review_stmt = select(DependencyReview).where(DependencyReview.folio == folio)
        review_result = await db.execute(review_stmt)
        review = review_result.scalars().first()

        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        review.director_approved = 1 if resolution_data.resolution_status == 1 else 0
        review.current_status = resolution_data.resolution_status
        review.update_date = datetime.now(timezone.utc)
        review.user_id = current_user.id

        # Update the main procedure status based on director resolution
        procedure_stmt = select(Procedure).where(Procedure.id == review.procedure_id)
        procedure_result = await db.execute(procedure_stmt)
        procedure = procedure_result.scalars().first()
        
        if procedure:
            old_status = procedure.status
            if resolution_data.resolution_status == 1:  # Approved by director
                procedure.status = 2  # Set to approved
                procedure.director_approval = 1  # Set director approval flag
                procedure.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            elif resolution_data.resolution_status == 2:  # Rejected by director
                procedure.status = 3  # Set to rejected
                procedure.director_approval = 0
                procedure.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
            
            logger.info(f"Director updated procedure {procedure.id} status from {old_status} to {procedure.status} for resolution status {resolution_data.resolution_status}")
            
            # Send notification if status changed
            if old_status != procedure.status:
                try:
                    await send_procedure_status_notification(
                        db=db,
                        procedure=procedure,
                        previous_status=old_status,
                        new_status=procedure.status,
                        reason=resolution_data.resolution_text,
                        portal_url=None
                    )
                    logger.info(f"Sent director resolution notification for procedure {procedure.id} from {old_status} to {procedure.status}")
                except Exception as e:
                    logger.error(f"Failed to send director resolution notification for procedure {procedure.id}: {str(e)}")
        else:
            logger.warning(f"Procedure not found for review.procedure_id {review.procedure_id}")

        director_approval = DirectorApproval(
            review_id=review.id,
            procedure_id=review.procedure_id,
            municipality_id=review.municipality_id,
            folio=folio,
            director_id=current_user.id,
            approval_status=resolution_data.resolution_status,
            approval_comments=resolution_data.resolution_text,
            approved_at=datetime.now(timezone.utc) if resolution_data.resolution_status == 1 else None
        )
        db.add(director_approval)

        await db.commit()

        return {"detail": "Director resolution updated successfully"}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating director resolution for folio {folio}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating director resolution: {str(e)}")


@router.post("/insert_director_review")
async def insert_director_review(
    director_request: DirectorInsertRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if not validate_director_role(current_user):
            raise HTTPException(status_code=403, detail="Director role required")

        existing_review = await db.execute(
            select(DependencyReview).where(DependencyReview.folio == director_request.folio)
        )

        if existing_review.scalars().first():
            raise HTTPException(status_code=400, detail="Review already exists for this folio")

        review = DependencyReview(
            procedure_id=director_request.procedure_id,
            municipality_id=director_request.municipality_id,
            folio=director_request.folio,
            role=4,
            start_date=datetime.now(timezone.utc),
            current_status=0,
            user_id=current_user.id,
            director_approved=0
        )

        db.add(review)
        await db.commit()
        await db.refresh(review)

        return {"detail": "Director review created successfully", "review_id": review.id}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error inserting director review: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inserting director review: {str(e)}")


@router.post("/emit_license/{folio}")
async def emit_license(
    folio: str,
    license_data: LicenseEmissionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        if not validate_director_role(current_user):
            raise HTTPException(status_code=403, detail="Director role required")

        # Update the dependency review
        review_stmt = select(DependencyReview).where(DependencyReview.folio == folio)
        review_result = await db.execute(review_stmt)
        review = review_result.scalars().first()

        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        review.current_status = 4
        review.license_issued = True
        review.license_pdf = license_data.license_file
        review.update_date = datetime.now(timezone.utc)
        review.user_id = current_user.id

        # Also update the main procedure table to reflect the license emission
        procedure_stmt = select(Procedure).where(Procedure.folio == folio)
        procedure_result = await db.execute(procedure_stmt)
        procedure = procedure_result.scalars().first()

        if procedure:
            # Update the procedure with license emission information
            procedure.window_license_generated = 1
            procedure.license_delivered_date = datetime.now(timezone.utc)
            procedure.updated_at = datetime.now(timezone.utc)
            procedure.status = 7  # Licencia emitida
            logger.info(f"Updated procedure {folio}: window_license_generated=1, license_delivered_date={procedure.license_delivered_date}")
        else:
            logger.warning(f"Procedure with folio {folio} not found while emitting license")

        await db.commit()

        try:
            html_content = render_email_template("license_issued_notification.html", {
                "folio": folio,
                "issued_at": datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S"),
                "current_year": datetime.now().year,
                "additional_instructions": license_data.additional_instructions
            })
            send_email("citizen@example.com", f"License Issued - Folio {folio}", html_content)
        except Exception as e:
            logger.error(f"Failed to send license emission notification: {str(e)}")

        return {"detail": "License successfully issued", "folio": folio}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error emitting license for folio {folio}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error emitting license: {str(e)}")


@router.post("/upload_payment_order/{review_id}")
async def upload_payment_order(
    review_id: int,
    file_url: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        review_stmt = select(DependencyReview).where(DependencyReview.id == review_id)
        review_result = await db.execute(review_stmt)
        review = review_result.scalars().first()

        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        review.payment_order_file = file_url
        review.updated_at = datetime.now(timezone.utc)

        await db.commit()

        return {"detail": "Payment order uploaded successfully"}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error uploading payment order for review {review_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading payment order: {str(e)}")


@router.post("/send_notification_email")
async def send_notification_email(
    email_request: NotificationEmailRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        notification = UserNotification(
            user_id=current_user.id,
            folio=email_request.folio,
            applicant_email=email_request.recipient_email,
            comments=email_request.additional_message,
            creation_date=datetime.now(timezone.utc),
            notification_type=1 if email_request.notification_type == "approval" else
                            2 if email_request.notification_type == "rejection" else
                            3 if email_request.notification_type == "prevention" else 4,
            is_notified=1,
            email_sent=True,
            email_sent_at=datetime.now(timezone.utc)
        )

        db.add(notification)
        await db.commit()

        template_map = {
            "approval": "resolution_approved_notification.html",
            "rejection": "resolution_rejected_notification.html",
            "prevention": "prevention_notification.html",
            "license_issued": "license_issued_notification.html"
        }

        template = template_map.get(email_request.notification_type, "generic_notification.html")

        html_content = render_email_template(template, {
            "folio": email_request.folio,
            "notification_type": email_request.notification_type,
            "additional_message": email_request.additional_message,
            "current_year": datetime.now().year
        })

        subject = f"Notification - Folio {email_request.folio}"
        send_email(email_request.recipient_email, subject, html_content)

        return {"detail": "Notification email sent successfully"}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error sending notification email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error sending notification email: {str(e)}")


async def calculate_business_days(start_date: datetime, business_days: int) -> datetime:
    current_date = start_date
    days_added = 0

    while days_added < business_days:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:
            days_added += 1

    return current_date


@router.get("/business_days_calculation")
async def get_business_days_calculation(
    start_date: datetime = Query(...),
    business_days: int = Query(default=15)
) -> BusinessDaysCalculation:
    end_date = await calculate_business_days(start_date, business_days)
    return BusinessDaysCalculation(
        start_date=start_date,
        business_days=business_days,
        calculated_end_date=end_date
    )


@router.get("/analytics/statistics")
async def get_resolution_statistics(
    analytics_request: AnalyticsRequest = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ResolutionStatistics:
    try:
        query = select(DependencyReview)

        if analytics_request.start_date:
            query = query.where(DependencyReview.created_at >= analytics_request.start_date)
        if analytics_request.end_date:
            query = query.where(DependencyReview.created_at <= analytics_request.end_date)
        if analytics_request.municipality_id:
            query = query.where(DependencyReview.municipality_id == analytics_request.municipality_id)
        if analytics_request.role:
            query = query.where(DependencyReview.role == analytics_request.role)

        result = await db.execute(query)
        reviews = result.scalars().all()

        total_reviews = len(reviews)
        pending_reviews = len([r for r in reviews if r.current_status == 0])
        approved_reviews = len([r for r in reviews if r.current_status == 1])
        rejected_reviews = len([r for r in reviews if r.current_status == 2])
        prevention_reviews = len([r for r in reviews if r.current_status == 3])

        resolved_reviews = [r for r in reviews if r.current_status in [1, 2, 4] and r.start_date and r.update_date]
        avg_time = 0.0
        if resolved_reviews:
            total_time = sum([(r.update_date - r.start_date).days for r in resolved_reviews])
            avg_time = total_time / len(resolved_reviews)

        return ResolutionStatistics(
            total_reviews=total_reviews,
            pending_reviews=pending_reviews,
            approved_reviews=approved_reviews,
            rejected_reviews=rejected_reviews,
            prevention_reviews=prevention_reviews,
            average_resolution_time=avg_time
        )

    except Exception as e:
        logger.error(f"Error retrieving resolution statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving statistics: {str(e)}")


@router.get("/analytics/charts/bar_chart")
async def get_bar_chart_data(
    municipality_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = text("""
            SELECT 
                MONTH(created_at) as month,
                YEAR(created_at) as year,
                current_status,
                COUNT(*) as count
            FROM dependency_reviews
            WHERE 1=1
        """)

        conditions = []
        if municipality_id:
            conditions.append(f"municipality_id = {municipality_id}")
        if start_date:
            conditions.append(f"created_at >= '{start_date}'")
        if end_date:
            conditions.append(f"created_at <= '{end_date}'")

        if conditions:
            query = text(str(query) + " AND " + " AND ".join(conditions))

        query = text(str(query) + " GROUP BY year, month, current_status ORDER BY year, month")

        result = await db.execute(query)
        data = result.fetchall()

        return {"chart_data": [dict(row) for row in data]}

    except Exception as e:
        logger.error(f"Error retrieving bar chart data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving chart data: {str(e)}")


@router.get("/analytics/charts/pie_chart")
async def get_pie_chart_data(
    municipality_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(
            DependencyReview.current_status,
            func.count(DependencyReview.id).label('count')
        ).group_by(DependencyReview.current_status)

        if municipality_id:
            query = query.where(DependencyReview.municipality_id == municipality_id)

        result = await db.execute(query)
        data = result.fetchall()

        status_labels = {
            0: "Pending",
            1: "Approved",
            2: "Rejected",
            3: "Prevention",
            4: "License Issued"
        }

        chart_data = [
            {"status": status_labels.get(row.current_status, "Unknown"), "count": row.count}
            for row in data
        ]

        return {"chart_data": chart_data}

    except Exception as e:
        logger.error(f"Error retrieving pie chart data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving pie chart data: {str(e)}")


@router.get("/resolution_info_renewal/{folio}")
async def get_resolution_info_renewal(
    folio: str = Path(..., description="Folio for renewal process"),
    db: AsyncSession = Depends(get_db)
):
    try:
        stmt = select(DependencyReview).options(
            selectinload(DependencyReview.procedure),
            selectinload(DependencyReview.municipality),
            selectinload(DependencyReview.user)
        ).where(
            and_(
                DependencyReview.folio.ilike(f"%{folio}%"),
                DependencyReview.folio.ilike("%RENEWAL%")
            )
        )

        result = await db.execute(stmt)
        reviews = result.scalars().all()

        if not reviews:
            raise HTTPException(status_code=404, detail="Renewal reviews not found")

        return {
            "reviews": reviews,
            "total": len(reviews),
            "renewal_type": "RENEWAL"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving renewal info: {str(e)}")


@router.get("/", response_model=List[DependencyReviewResponse])
async def get_all_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    municipality_id: Optional[int] = Query(None),
    role: Optional[int] = Query(None),
    status: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        query = select(DependencyReview).options(
            selectinload(DependencyReview.procedure),
            selectinload(DependencyReview.municipality),
            selectinload(DependencyReview.user),
            selectinload(DependencyReview.resolutions),
            selectinload(DependencyReview.prevention_requests),
            selectinload(DependencyReview.notifications)
        )

        if municipality_id:
            query = query.where(DependencyReview.municipality_id == municipality_id)
        if role:
            query = query.where(DependencyReview.role == role)
        if status is not None:
            query = query.where(DependencyReview.current_status == status)

        query = query.order_by(desc(DependencyReview.created_at)).offset(skip).limit(limit)

        result = await db.execute(query)
        reviews = result.scalars().all()

        return reviews

    except Exception as e:
        logger.error(f"Error retrieving all reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving reviews: {str(e)}")


@router.post("/bulk_update")
async def bulk_update_resolutions(
    bulk_update: BulkResolutionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        query = select(DependencyReview).where(
            DependencyReview.id.in_(bulk_update.review_ids)
        )
        result = await db.execute(query)
        reviews = result.scalars().all()

        for review in reviews:
            review.current_status = bulk_update.resolution_status
            review.update_date = datetime.now(timezone.utc)
            review.user_id = current_user.id

            resolution = DependencyResolution(
                review_id=review.id,
                procedure_id=review.procedure_id,
                role=current_user.roles[0].id if current_user.roles else 1,
                user_id=current_user.id,
                resolution_status=bulk_update.resolution_status,
                resolution_text=bulk_update.resolution_text,
                resolution_file=bulk_update.resolution_file
            )
            db.add(resolution)
            
            # Update the main procedure status for bulk update
            procedure_stmt = select(Procedure).where(Procedure.id == review.procedure_id)
            procedure_result = await db.execute(procedure_stmt)
            procedure = procedure_result.scalars().first()
            
            if procedure:
                old_status = procedure.status
                if bulk_update.resolution_status == 1:  # Approved
                    procedure.status = 2  # Set to approved
                elif bulk_update.resolution_status == 2:  # Rejected
                    procedure.status = 3  # Set to rejected
                elif bulk_update.resolution_status == 3:  # Prevention
                    procedure.status = 3  # Set to prevention/rejected
                
                procedure.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
                
                # Send notification if status changed
                if old_status != procedure.status:
                    try:
                        await send_procedure_status_notification(
                            db=db,
                            procedure=procedure,
                            previous_status=old_status,
                            new_status=procedure.status,
                            reason=bulk_update.resolution_text,
                            portal_url=None
                        )
                        logger.info(f"Sent bulk update notification for procedure {procedure.id} from {old_status} to {procedure.status}")
                    except Exception as e:
                        logger.error(f"Failed to send bulk update notification for procedure {procedure.id}: {str(e)}")

        await db.commit()

        return {"detail": f"Successfully updated {len(reviews)} reviews"}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error in bulk update: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in bulk update: {str(e)}")


@router.get("/full_report")
async def get_full_report(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    municipality_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        validate_admin_role(current_user)
        
        query = select(DependencyReview).options(
            selectinload(DependencyReview.procedure),
            selectinload(DependencyReview.municipality),
            selectinload(DependencyReview.user),
            selectinload(DependencyReview.resolutions)
        )

        if start_date:
            query = query.where(DependencyReview.created_at >= start_date)
        if end_date:
            query = query.where(DependencyReview.created_at <= end_date)
        if municipality_id:
            query = query.where(DependencyReview.municipality_id == municipality_id)

        result = await db.execute(query)
        reviews = result.scalars().all()

        report_data = []
        for review in reviews:
            report_data.append({
                "folio": review.folio,
                "municipality": review.municipality.name if review.municipality else "N/A",
                "status": review.current_status,
                "created_at": review.created_at.isoformat() if review.created_at else None,
                "updated_at": review.updated_at.isoformat() if review.updated_at else None,
                "director_approved": review.director_approved,
                "license_issued": review.license_issued,
                "resolutions_count": len(review.resolutions)
            })

        return {"report_data": report_data, "total_records": len(report_data)}

    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error generating full report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@router.get("/technical_sheet_downloads")
async def get_technical_sheet_downloads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        validate_admin_role(current_user)
        
        query = select(TechnicalSheetDownload).order_by(
            desc(TechnicalSheetDownload.created_at)
        ).offset(skip).limit(limit)

        result = await db.execute(query)
        downloads = result.scalars().all()

        return {
            "downloads": [
                {
                    "id": d.id,
                    "technical_sheet_uuid": d.technical_sheet_uuid,
                    "user_email": d.user_email,
                    "download_count": d.download_count,
                    "created_at": d.created_at.isoformat() if d.created_at else None,
                    "updated_at": d.updated_at.isoformat() if d.updated_at else None
                } for d in downloads
            ]
        }

    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving technical sheet downloads: {str(e)}")


@router.get("/countersign/{folio}", response_model=DependencyReviewResponse)
async def get_countersign_review(
    folio: str = Path(..., description="Folio string containing countersign 'REFRENDO'"),
    db: AsyncSession = Depends(get_db)
):
    try:
        stmt = select(DependencyReview).options(
            selectinload(DependencyReview.procedure),
            selectinload(DependencyReview.municipality),
            selectinload(DependencyReview.user)
        ).where(
            and_(
                DependencyReview.folio == folio,
                DependencyReview.folio.ilike("%REFRENDO%")
            )
        )

        result = await db.execute(stmt)
        review = result.scalars().first()

        if not review:
            raise HTTPException(status_code=404, detail="Countersign review not found")

        return review

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving countersign review: {str(e)}")


@router.get("/line_time")
async def get_line_time(db: AsyncSession = Depends(get_db)):
    try:
        stmt = (
            select(
                func.extract("month", DependencyReview.created_at).label("month"),
                func.extract("year", DependencyReview.created_at).label("year"),
                DependencyReview.role,
                func.count().label("total")
            )
            .group_by("month", "year", DependencyReview.role)
            .order_by("year", "month")
        )

        result = await db.execute(stmt)
        data = result.all()

        response = [
            {
                "month": int(row.month),
                "year": int(row.year),
                "role": row.role,
                "total": row.total
            }
            for row in data
        ]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving line time data: {str(e)}")


@router.get("/line_time_admin")
async def get_line_time_admin(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_admin_role(current_user)

    try:
        stmt = (
            select(
                func.extract("month", DependencyReview.created_at).label("month"),
                func.extract("year", DependencyReview.created_at).label("year"),
                DependencyReview.role,
                func.count().label("total")
            )
            .group_by("month", "year", DependencyReview.role)
            .order_by("year", "month")
        )

        result = await db.execute(stmt)
        data = result.all()

        response = [
            {
                "month": int(row.month),
                "year": int(row.year),
                "role": row.role,
                "total": row.total
            }
            for row in data
        ]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving admin line time data: {str(e)}")


@router.get("/bar_chart")
async def get_bar_chart(db: AsyncSession = Depends(get_db)):
    try:
        stmt = (
            select(
                DependencyReview.current_status,
                DependencyReview.role,
                func.count().label("total")
            )
            .group_by(DependencyReview.current_status, DependencyReview.role)
            .order_by(DependencyReview.role)
        )

        result = await db.execute(stmt)
        data = result.all()

        response = [
            {
                "status": row.current_status,
                "role": row.role,
                "total": row.total
            }
            for row in data
        ]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving bar chart data: {str(e)}")


@router.post("/bar_chart_list")
async def get_bar_chart_list(
    filters: DependencyReviewFilter,
    db: AsyncSession = Depends(get_db)
):
    try:
        conditions = []

        if filters.start_date:
            conditions.append(DependencyReview.created_at >= filters.start_date)
        if filters.end_date:
            conditions.append(DependencyReview.created_at <= filters.end_date)
        if filters.municipality_id:
            conditions.append(DependencyReview.municipality_id == filters.municipality_id)
        if filters.current_status is not None:
            conditions.append(DependencyReview.current_status == filters.current_status)
        if filters.role is not None:
            conditions.append(DependencyReview.role == filters.role)

        stmt = (
            select(
                DependencyReview.current_status,
                DependencyReview.role,
                func.count().label("total")
            )
            .where(and_(*conditions)) if conditions else
            select(
                DependencyReview.current_status,
                DependencyReview.role,
                func.count().label("total")
            )
        ).group_by(
            DependencyReview.current_status,
            DependencyReview.role
        ).order_by(
            DependencyReview.role
        )

        result = await db.execute(stmt)
        rows = result.all()

        response = [
            {
                "status": row.current_status,
                "role": row.role,
                "total": row.total
            }
            for row in rows
        ]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating bar chart list: {str(e)}")


@router.get("/pie_review")
async def get_pie_review(db: AsyncSession = Depends(get_db)):
    try:
        stmt = (
            select(
                DependencyReview.current_status,
                func.count().label("total")
            )
            .group_by(DependencyReview.current_status)
            .order_by(DependencyReview.current_status)
        )

        result = await db.execute(stmt)
        data = result.all()

        response = [
            {
                "status": row.current_status,
                "total": row.total
            }
            for row in data
        ]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating pie review data: {str(e)}")


@router.get("/municipality_pie")
async def get_municipality_pie(db: AsyncSession = Depends(get_db)):
    try:
        stmt = (
            select(
                DependencyReview.municipality_id,
                func.count().label("total")
            )
            .group_by(DependencyReview.municipality_id)
            .order_by(DependencyReview.municipality_id)
        )

        result = await db.execute(stmt)
        rows = result.all()

        response = [
            {
                "municipality_id": row.municipality_id,
                "total": row.total
            }
            for row in rows
        ]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating municipality pie data: {str(e)}")


@router.get("/municipality_bar/{id}")
async def get_municipality_bar(
    id: int = Path(..., description="Municipality ID"),
    db: AsyncSession = Depends(get_db)
):
    try:
        stmt = (
            select(
                DependencyReview.current_status,
                func.count().label("total")
            )
            .where(DependencyReview.municipality_id == id)
            .group_by(DependencyReview.current_status)
            .order_by(DependencyReview.current_status)
        )

        result = await db.execute(stmt)
        data = result.all()

        response = [
            {
                "status": row.current_status,
                "total": row.total
            }
            for row in data
        ]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving municipality bar data: {str(e)}")


@router.post("/update/{folio}")
async def update_dependency_review(
    folio: str,
    data: DependencyReviewUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        stmt = select(DependencyReview).where(DependencyReview.folio == folio)
        result = await db.execute(stmt)
        review = result.scalars().first()

        if not review:
            raise HTTPException(status_code=404, detail="Dependency review not found")

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        for field, value in update_data.items():
            setattr(review, field, value)

        await db.commit()
        await db.refresh(review)

        return {"detail": "Review successfully updated"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating review: {str(e)}")


@router.post("/update_director/{folio}")
async def update_director_review(
    folio: str,
    data: DependencyReviewUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    validate_director_role(current_user)

    try:
        stmt = select(DependencyReview).where(DependencyReview.folio == folio)
        result = await db.execute(stmt)
        review = result.scalars().first()

        if not review:
            raise HTTPException(status_code=404, detail="Dependency review not found")

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        for field, value in update_data.items():
            setattr(review, field, value)

        await db.commit()
        await db.refresh(review)

        return {"detail": "Review successfully updated by director"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating review as director: {str(e)}")


@router.post("/upload_files/{folio}")
async def upload_files(
    folio: str,
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        decoded_folio = folio
        try:
            folio_unquoted = unquote(folio)
            if (len(folio_unquoted) % 4 == 0) and ("=" in folio_unquoted):
                decoded_folio = base64.b64decode(folio_unquoted).decode('utf-8')
            else:
                decoded_folio = folio_unquoted
        except Exception:
            decoded_folio = folio

        stmt = select(DependencyReview).where(DependencyReview.folio == decoded_folio)
        result = await db.execute(stmt)
        review = result.scalars().first()

        if not review:
            raise HTTPException(status_code=404, detail="Dependency review not found")

        saved_files = []
        last_file_path = None
        for upload in files:
            filename = f"{uuid4().hex}_{upload.filename}"
            file_path = os.path.join("uploads/dependency_reviews", filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as buffer:
                content = await upload.read()
                buffer.write(content)
            saved_files.append(file_path)
            last_file_path = file_path

        review.current_file = last_file_path if saved_files else None
        await db.commit()
        await db.refresh(review)

        if last_file_path:
            res_stmt = select(DependencyResolution).where(DependencyResolution.review_id == review.id).order_by(DependencyResolution.created_at.desc())
            res_result = await db.execute(res_stmt)
            last_resolution = res_result.scalars().first()
            if last_resolution:
                last_resolution.resolution_file = last_file_path
                await db.commit()
                await db.refresh(last_resolution)

        return {
            "detail": f"{len(saved_files)} file(s) uploaded successfully",
            "files": saved_files
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")


@router.post("/upload_files_history/{folio}")
async def upload_files_history(
    folio: str,
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        stmt = select(DependencyReview).where(DependencyReview.folio == folio)
        result = await db.execute(stmt)
        review = result.scalars().first()

        if not review:
            raise HTTPException(status_code=404, detail="Dependency review not found")

        saved_files = []

        for upload in files:
            filename = f"{uuid4().hex}_{upload.filename}"
            file_path = os.path.join("uploads/dependency_reviews/history", filename)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "wb") as buffer:
                content = await upload.read()
                buffer.write(content)

            saved_files.append(file_path)

        return {
            "detail": f"{len(saved_files)} historical file(s) uploaded successfully",
            "files": saved_files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading historical files: {str(e)}")
