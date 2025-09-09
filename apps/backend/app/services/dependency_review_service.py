"""
Service layer for handling dependency review and resolution business logic
"""
import logging
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, func

from app.models.dependency_reviews import DependencyReview
from app.models.dependency_resolutions import DependencyResolution
from app.models.issue_resolution import IssueResolution
from app.models.user import UserModel as User
from app.models.municipality import Municipality
from app.models.notifications import NotificationUser
from app.models.procedures import Procedure
from app.services.emails.sendgrid_client import send_email, render_email_template

logger = logging.getLogger(__name__)

class DependencyReviewService:
    
    @staticmethod
    async def process_resolution(
        db: AsyncSession,
        folio: str,
        resolution_status: int,
        resolution_text: str,
        file_path: str,
        current_user: User,
        role: int
    ) -> dict:
        """
        Processes a resolution according to legacy flow
        """
        try:
            # Find the review
            review = await db.execute(
                select(DependencyReview).where(
                    and_(
                        DependencyReview.folio == folio,
                        DependencyReview.role == role
                    )
                )
            )
            review = review.scalars().first()
            
            if not review:
                raise ValueError("Review not found")
            
            # Update review
            review.current_status = resolution_status
            review.update_date = datetime.now(timezone.utc)
            review.current_file = file_path
            review.user_id = current_user.id
            
            # Create resolution
            resolution = DependencyResolution(
                procedure_id=review.procedure_id,
                role=role,
                user_id=current_user.id,
                resolution_status=resolution_status,
                resolution_text=resolution_text,
                resolution_file=file_path
            )
            db.add(resolution)
            
            # Process according to resolution type
            if resolution_status == 1:  # APPROVED
                await DependencyReviewService._handle_approval(db, review, folio, role, current_user)
            elif resolution_status == 2:  # REJECTED
                await DependencyReviewService._handle_rejection(db, review, folio, role)
            elif resolution_status == 3:  # PREVENT
                await DependencyReviewService._handle_prevention(db, review, folio, resolution_text, role, current_user)
            
            await db.commit()
            return {"status": "success", "message": "Resolution processed successfully"}
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error processing resolution: {str(e)}")
            raise
    
    @staticmethod
    async def _handle_approval(db: AsyncSession, review: DependencyReview, folio: str, role: int, current_user: User):
        """Handles the approval flow"""
        if role != 4:  # Not director
            # Check if there are other departments
            all_reviews = await db.execute(
                select(DependencyReview).where(DependencyReview.folio == folio)
            )
            all_reviews = all_reviews.scalars().all()
            
            if len(all_reviews) == 1:
                # Only one department - send directly to director
                await DependencyReviewService._insert_director_review(db, review, folio)
            else:
                # Check if all have responded
                all_completed = all(r.current_status is not None for r in all_reviews)
                if all_completed:
                    await DependencyReviewService._insert_director_review(db, review, folio)
                    
                # Notify if it's special department (role > 6)
                if role > 6:
                    await DependencyReviewService._send_approval_notification(db, folio, current_user)
        
        elif role == 4:  # Director
            # Mark procedure as approved by director
            procedure = await db.execute(
                select(Procedure).where(Procedure.folio == folio)
            )
            procedure = procedure.scalars().first()
            if procedure:
                # Add director approval logic here
                await DependencyReviewService._send_payment_order_notification(db, folio)
    
    @staticmethod
    async def _handle_rejection(db: AsyncSession, review: DependencyReview, folio: str, role: int):
        """Handles the rejection flow"""
        if role != 4:  # Not director
            # If there are multiple departments, check if all have responded
            all_reviews = await db.execute(
                select(DependencyReview).where(DependencyReview.folio == folio)
            )
            all_reviews = all_reviews.scalars().all()
            
            if len(all_reviews) > 1:
                all_completed = all(r.current_status is not None for r in all_reviews)
                if all_completed:
                    # Send to director for final decision
                    await DependencyReviewService._insert_director_review(db, review, folio)
    
    @staticmethod
    async def _handle_prevention(db: AsyncSession, review: DependencyReview, folio: str, resolution_text: str, role: int, current_user: User):
        """Handles the prevention/compliance flow"""
        # Get days to comply from municipality
        municipality = await db.get(Municipality, review.municipality_id)
        compliance_days = getattr(municipality, 'compliance_days', 15)
        
        # Create compliance record using IssueResolution model
        issue_resolution = IssueResolution(
            procedure_id=review.procedure_id,
            role=role,
            user_id=current_user.id,
            comment=resolution_text,
            maximum_resolution_date=DependencyReviewService._calculate_business_days(
                datetime.now(timezone.utc), compliance_days
            )
        )
        db.add(issue_resolution)
        
        # Send notification to citizen
        await DependencyReviewService._send_prevention_notification(db, folio, resolution_text, issue_resolution.id, role)
        
        # Check if all departments have responded
        all_reviews = await db.execute(
            select(DependencyReview).where(DependencyReview.folio == folio)
        )
        all_reviews = all_reviews.scalars().all()
        
        if len(all_reviews) > 1:
            all_completed = all(r.current_status is not None for r in all_reviews)
            if all_completed:
                await DependencyReviewService._insert_director_review(db, review, folio)
    
    @staticmethod
    async def _insert_director_review(db: AsyncSession, review: DependencyReview, folio: str):
        """Inserts a review for the director"""
        director_review = DependencyReview(
            procedure_id=review.procedure_id,
            municipality_id=review.municipality_id,
            folio=folio,
            role=4,  # Director role
            start_date=datetime.now(timezone.utc),
            current_status=None  # Pending
        )
        db.add(director_review)
    
    @staticmethod
    def _calculate_business_days(start_date: datetime, business_days: int) -> datetime:
        """Calculates business days excluding weekends"""
        current_date = start_date
        days_added = 0
        
        while days_added < business_days:
            current_date += timedelta(days=1)
            if current_date.weekday() < 5:  # Monday=0, Friday=4
                days_added += 1
                
        return current_date
    
    @staticmethod
    async def _send_approval_notification(db: AsyncSession, folio: str, current_user: User):
        """Sends approval notification"""
        # Implement notification logic
        pass
    
    @staticmethod
    async def _send_payment_order_notification(db: AsyncSession, folio: str):
        """Sends payment order ready notification"""
        # Implement notification logic
        pass
    
    @staticmethod
    async def _send_prevention_notification(db: AsyncSession, folio: str, resolution_text: str, issue_resolution_id: int, role: int):
        """Sends prevention/compliance notification"""
        # Implement notification logic
        pass
