from datetime import datetime
from sqlalchemy.orm import Session
from app.models.notifications import Notification
from app.services.emails.sendgrid_client import send_email, render_email_template


def send_notification(
    db: Session,
    applicant_email: str,
    comment: str = None,
    file: str = None,
    dependency_file: str = None,
    user_id: int = None,
    notifying_department: int = None,
    notification_type: int = None,
    resolution_id: int = None,
    folio: str = None,
    send_email_notification: bool = True
):
    """
    Create a notification record in the database and optionally send an email.
    
    Args:
        db: Database session
        applicant_email: Email of the applicant
        comment: Optional comment for the notification
        file: Optional file path
        dependency_file: Optional dependency file path
        user_id: Optional user ID
        notifying_department: Optional notifying department ID
        notification_type: Optional notification type ID
        resolution_id: Optional resolution ID
        folio: Optional folio number
        send_email_notification: Whether to send email notification
    
    Returns:
        Notification: The created notification object
    """
    try:
        notification = Notification(
            user_id=user_id,
            applicant_email=applicant_email,
            comment=comment,
            file=file,
            creation_date=datetime.now(),
            dependency_file=dependency_file,
            notified=1 if send_email_notification else 0,
            notifying_department=notifying_department,
            notification_type=notification_type,
            resolution_id=resolution_id,
            folio=folio,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        if send_email_notification and comment:
            try:
                email_data = {
                    "comment": comment,
                    "folio": folio or "",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                subject = f"Notification - Folio: {folio}" if folio else "System Notification"
                
                send_email(
                    to_email=applicant_email,
                    subject=subject,
                    html_content=f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2>Notification</h2>
                        <p>{comment}</p>
                        {f"<p><strong>Folio:</strong> {folio}</p>" if folio else ""}
                        <p><strong>Date:</strong> {email_data['date']}</p>
                        <hr>
                        <p style="color: #666; font-size: 12px;">
                            This is an automated notification from Visor Urbano.
                        </p>
                    </div>
                    """
                )
            except Exception as email_error:
                # Failed to send email notification
                notification.notified = 0
                db.commit()
        
        return notification
        
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to create notification: {str(e)}")


def create_notification(
    db: Session,
    applicant_email: str,
    comment: str,
    folio: str,
    user_id: int = None,
    notification_type: int = 1,
    send_email: bool = True
):
    """
    Simplified function to create a notification with common parameters.
    
    Args:
        db: Database session
        applicant_email: Email of the applicant
        comment: Notification comment/message
        folio: Folio number
        user_id: Optional user ID
        notification_type: Notification type (default: 1)
        send_email: Whether to send email notification
    
    Returns:
        Notification: The created notification object
    """
    return send_notification(
        db=db,
        applicant_email=applicant_email,
        comment=comment,
        folio=folio,
        user_id=user_id,
        notification_type=notification_type,
        send_email_notification=send_email
    )
