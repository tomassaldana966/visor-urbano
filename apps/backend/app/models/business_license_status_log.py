from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.settings import Base

class BusinessLicenseStatusLog(Base):
    __tablename__ = "business_license_status_logs"

    id = Column(Integer, primary_key=True, index=True)
    license_id = Column(Integer, ForeignKey("business_licenses.id"), nullable=False)
    previous_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    reason = Column(Text, nullable=True)
    reason_file = Column(String(255), nullable=True)
    changed_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    business_license = relationship("BusinessLicense", back_populates="status_logs")
    changed_by_user = relationship("UserModel", foreign_keys=[changed_by_user_id])
