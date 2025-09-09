"""
Fixed notification service for procedure status changes and license notifications
"""
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import UserModel
from app.models.procedures import Procedure
from app.models.notifications import Notification
from app.services.emails.sendgrid_client import send_email, render_email_template
from app.utils.translations import (
    get_status_text, 
    get_email_subject, 
    get_notification_message, 
    get_user_language
)

logger = logging.getLogger(__name__)

# Deprecated - use translations.py instead
STATUS_TEXT_MAP = {
    0: "En Proceso",
    1: "Pendiente de Aprobación", 
    2: "Aprobado",
    3: "Rechazado",
    4: "En Revisión",
    7: "Licencia Emitida"
}

def get_status_text_legacy(status: int) -> str:
    """Get human-readable status text (deprecated - use translations.py)"""
    return STATUS_TEXT_MAP.get(status, f"Estado {status}")

async def send_procedure_status_notification(
    db: AsyncSession,
    procedure: Procedure,
    previous_status: int,
    new_status: int,
    reason: Optional[str] = None,
    portal_url: Optional[str] = None
) -> bool:
    """
    Send email notification when procedure status changes
    
    Args:
        db: Database session
        procedure: The procedure that changed status
        previous_status: Previous status code
        new_status: New status code
        reason: Optional reason for status change
        portal_url: Optional URL to portal
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get user email from procedure
        if not procedure.user_id:
            logger.warning(f"Procedure {procedure.folio} has no user_id, cannot send notification")
            return False
            
        # Get user details
        user_query = select(UserModel).where(UserModel.id == procedure.user_id)
        user_result = await db.execute(user_query)
        user = user_result.scalars().first()
        
        if not user or not user.email:
            logger.warning(f"No valid email found for user_id {procedure.user_id}")
            return False
        
        # Get user's preferred language
        user_language = get_user_language(user)
            
        # Prepare email context
        context = {
            "folio": procedure.folio,
            "procedure_type": procedure.procedure_type or "Licencia de Funcionamiento",
            "previous_status": previous_status,
            "previous_status_text": get_status_text(previous_status, user_language),
            "new_status": new_status,
            "new_status_text": get_status_text(new_status, user_language),
            "update_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "reason": reason,
            "portal_url": portal_url or "https://visorurbano.jalisco.gob.mx/",
            "current_year": datetime.now().year,
            "applicant_name": user.name
        }
        
        # Render email template
        html_content = render_email_template("procedure_status_notification.html", context)
        
        # Determine subject based on status
        if new_status == 2:
            subject = get_email_subject("approved", procedure.folio, user_language)
        elif new_status == 3:
            subject = get_email_subject("rejected", procedure.folio, user_language)
        elif new_status == 7:
            subject = get_email_subject("license_issued", procedure.folio, user_language)
        else:
            subject = get_email_subject("status_update", procedure.folio, user_language)
        
        # Send email
        result = send_email(user.email, subject, html_content)
        
        if isinstance(result, dict) and result.get("status_code") == 202:
            logger.info(f"Status notification sent successfully to {user.email} for procedure {procedure.folio}")
            
            # Also create in-app notification  
            if reason:
                message = get_notification_message("status_change_with_reason", procedure.folio, 
                                                 get_status_text(new_status, user_language), reason, user_language)
            else:
                message = get_notification_message("status_change", procedure.folio, 
                                                 get_status_text(new_status, user_language), "", user_language)
            
            await create_in_app_notification_async(
                db=db,
                user_id=procedure.user_id,
                folio=procedure.folio,
                message=message,
                notification_type=1  # Status change
            )
            
            return True
        else:
            logger.error(f"Failed to send status notification: {result}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending procedure status notification: {str(e)}")
        return False

async def send_license_download_notification(
    db: AsyncSession,
    procedure: Procedure,
    license_data: Optional[Dict[str, Any]] = None,
    portal_url: Optional[str] = None,
    license_url: Optional[str] = None
) -> bool:
    """
    Send email notification when license is ready for download
    
    Args:
        db: Database session
        procedure: The procedure with issued license
        license_data: Optional license data (number, etc.)
        portal_url: Optional URL to portal
        license_url: Optional direct download URL
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get user email from procedure
        if not procedure.user_id:
            logger.warning(f"Procedure {procedure.folio} has no user_id, cannot send notification")
            return False
            
        # Get user details
        user_query = select(UserModel).where(UserModel.id == procedure.user_id)
        user_result = await db.execute(user_query)
        user = user_result.scalars().first()
        
        if not user or not user.email:
            logger.warning(f"No valid email found for user_id {procedure.user_id}")
            return False
        
        # Get user's preferred language
        user_language = get_user_language(user)
            
        # Prepare email context
        context = {
            "folio": procedure.folio,
            "license_type": procedure.procedure_type or "Licencia de Funcionamiento",
            "applicant_name": procedure.official_applicant_name or user.name,
            "issue_date": datetime.now().strftime("%d/%m/%Y"),
            "license_number": license_data.get("license_number") if license_data else None,
            "portal_url": portal_url or "https://visorurbano.jalisco.gob.mx/",
            "license_url": license_url,
            "current_year": datetime.now().year,
            "contact_info": True
        }
        
        # Render email template
        html_content = render_email_template("license_download_notification.html", context)
        
        subject = get_email_subject("license_download", procedure.folio, user_language)
        
        # Send email
        result = send_email(user.email, subject, html_content)
        
        if isinstance(result, dict) and result.get("status_code") == 202:
            logger.info(f"License download notification sent successfully to {user.email} for procedure {procedure.folio}")
            
            # Also create in-app notification
            message = get_notification_message("license_ready", procedure.folio, "", "", user_language)
            
            await create_in_app_notification_async(
                db=db,
                user_id=procedure.user_id,
                folio=procedure.folio,
                message=message,
                notification_type=2  # License ready
            )
            
            return True
        else:
            logger.error(f"Failed to send license download notification: {result}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending license download notification: {str(e)}")
        return False

def send_procedure_status_notification_sync(
    db: Session,
    procedure: Procedure,
    previous_status: int,
    new_status: int,
    reason: Optional[str] = None,
    portal_url: Optional[str] = None
) -> bool:
    """
    Synchronous version of procedure status notification
    For use in synchronous contexts where async is not available
    """
    try:
        # Get user email from procedure
        if not procedure.user_id:
            logger.warning(f"Procedure {procedure.folio} has no user_id, cannot send notification")
            return False
            
        # Get user details
        user = db.query(UserModel).filter(UserModel.id == procedure.user_id).first()
        
        if not user or not user.email:
            logger.warning(f"No valid email found for user_id {procedure.user_id}")
            return False
        
        # Get user's preferred language
        user_language = get_user_language(user)
            
        # Prepare email context
        context = {
            "folio": procedure.folio,
            "procedure_type": procedure.procedure_type or "Licencia de Funcionamiento",
            "previous_status": previous_status,
            "previous_status_text": get_status_text(previous_status, user_language),
            "new_status": new_status,
            "new_status_text": get_status_text(new_status, user_language),
            "update_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "reason": reason,
            "portal_url": portal_url or "https://visorurbano.jalisco.gob.mx/",
            "current_year": datetime.now().year,
            "applicant_name": user.name
        }
        
        # Render email template
        html_content = render_email_template("procedure_status_notification.html", context)
        
        # Determine subject based on status
        if new_status == 2:
            subject = get_email_subject("approved", procedure.folio, user_language)
        elif new_status == 3:
            subject = get_email_subject("rejected", procedure.folio, user_language)
        elif new_status == 7:
            subject = get_email_subject("license_issued", procedure.folio, user_language)
        else:
            subject = get_email_subject("status_update", procedure.folio, user_language)
        
        # Send email
        result = send_email(user.email, subject, html_content)
        
        if isinstance(result, dict) and result.get("status_code") == 202:
            logger.info(f"Status notification sent successfully to {user.email} for procedure {procedure.folio}")
            
            # Also create in-app notification
            if reason:
                message = get_notification_message("status_change_with_reason", procedure.folio, 
                                                 get_status_text(new_status, user_language), reason, user_language)
            else:
                message = get_notification_message("status_change", procedure.folio, 
                                                 get_status_text(new_status, user_language), "", user_language)
            
            create_in_app_notification(
                db=db,
                user_id=procedure.user_id,
                folio=procedure.folio,
                message=message,
                notification_type=1  # Status change
            )
            
            return True
        else:
            logger.error(f"Failed to send status notification: {result}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending procedure status notification: {str(e)}")
        return False

def create_in_app_notification(
    db: Session,
    user_id: int,
    folio: str,
    message: str,
    notification_type: int = 1
) -> bool:
    """
    Create an in-app notification for the user
    
    Args:
        db: Database session (sync)
        user_id: User ID to notify
        folio: Procedure folio
        message: Notification message
        notification_type: Type of notification (1 = status change, 2 = license ready)
        
    Returns:
        bool: True if notification created successfully
    """
    try:
        # Get user email
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            logger.warning(f"User {user_id} not found for in-app notification")
            return False
            
        # Create notification
        notification = Notification(
            user_id=user_id,
            folio=folio,
            applicant_email=user.email,
            comment=message,
            creation_date=datetime.now(),
            notification_type=notification_type,
            is_notified=0,  # Mark as unread
            email_sent=True,  # Email was sent
            email_sent_at=datetime.now(),
            notifying_department=0  # System-generated notification
        )
        
        db.add(notification)
        db.commit()
        
        logger.info(f"In-app notification created for user {user_id}, folio {folio}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating in-app notification: {str(e)}")
        db.rollback()
        return False

async def create_in_app_notification_async(
    db: AsyncSession,
    user_id: int,
    folio: str,
    message: str,
    notification_type: int = 1
) -> bool:
    """
    Create an in-app notification for the user (async version)
    """
    try:
        # Get user email
        user_query = select(UserModel).where(UserModel.id == user_id)
        user_result = await db.execute(user_query)
        user = user_result.scalars().first()
        
        if not user:
            logger.warning(f"User {user_id} not found for in-app notification")
            return False
            
        # Create notification
        notification = Notification(
            user_id=user_id,
            folio=folio,
            applicant_email=user.email,
            comment=message,
            creation_date=datetime.now(),
            notification_type=notification_type,
            is_notified=0,  # Mark as unread
            email_sent=True,  # Email was sent
            email_sent_at=datetime.now(),
            notifying_department=0  # System-generated notification
        )
        
        db.add(notification)
        await db.commit()
        
        logger.info(f"In-app notification created for user {user_id}, folio {folio}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating in-app notification: {str(e)}")
        await db.rollback()
        return False
