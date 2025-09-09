from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey('users.id'), nullable=True)
    review_id = Column("review_id", BigInteger, ForeignKey('dependency_reviews.id'), nullable=True)
    prevention_request_id = Column("prevention_request_id", Integer, ForeignKey('prevention_requests.id'), nullable=True)
    folio = Column("folio", String(255), nullable=False)
    applicant_email = Column("applicant_email", String(255), nullable=False)
    comment = Column("comment", String(300), nullable=True)
    comments = Column("comments", Text, nullable=True)
    file = Column("file", Text, nullable=True)
    creation_date = Column("creation_date", DateTime, nullable=False)
    seen_date = Column("seen_date", DateTime, nullable=True)
    dependency_file = Column("dependency_file", Text, nullable=True)
    notified = Column("notified", Integer, nullable=True)
    is_notified = Column("is_notified", Integer, default=0)
    notifying_department = Column("notifying_department", Integer, nullable=True)
    notification_type = Column("notification_type", Integer, nullable=True)
    resolution_id = Column("resolution_id", Integer, nullable=True, default=0)
    email_sent = Column("email_sent", Boolean, default=False)
    email_sent_at = Column("email_sent_at", DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    user = relationship("UserModel", back_populates="notifications")
    review = relationship("DependencyReview")
    prevention_request = relationship("PreventionRequest")
