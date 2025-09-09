from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class AuthToken(Base):
    __tablename__ = 'authtoken_token'
    key = Column(String(40), primary_key=True, nullable=False)
    created = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("UserModel", back_populates="auth_tokens")
