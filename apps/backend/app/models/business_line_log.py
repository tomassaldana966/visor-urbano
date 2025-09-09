from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, Index
from sqlalchemy.orm import relationship
from config.settings import Base

class BusinessLineLog(Base):
    __tablename__ = 'business_line_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(255), nullable=False, index=True)
    previous = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    log_type = Column(Integer, nullable=False, index=True)
    procedure_id = Column(Integer, nullable=True, index=True)
    host = Column(String(255), nullable=True)
    user_ip = Column(String(45), nullable=True, index=True)
    role_id = Column(Integer, nullable=True)
    user_agent = Column(Text, nullable=True)
    post_request = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    user = relationship("UserModel", back_populates="business_line_logs")
    
    __table_args__ = (
        Index('idx_business_line_log_type_date', 'log_type', 'created_at'),
        Index('idx_business_line_log_user_date', 'user_id', 'created_at'),
        Index('idx_business_line_log_procedure_date', 'procedure_id', 'created_at'),
    )

    def __repr__(self):
        return f"<BusinessLineLog(id={self.id}, action='{self.action}', log_type={self.log_type})>"
