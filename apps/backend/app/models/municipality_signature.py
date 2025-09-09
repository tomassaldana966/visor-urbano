from sqlalchemy import Column, BigInteger, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class MunicipalitySignature(Base):
    __tablename__ = 'municipality_signatures'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    signer_name = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)  # Este es el cargo/position_title
    orden = Column(Integer, nullable=False)  # Este es el order_index
    signature = Column(String(255), nullable=True)  # Esta es la signature_image
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    # Properties para mantener compatibilidad con el schema
    @property
    def position_title(self):
        return self.department
    
    @position_title.setter
    def position_title(self, value):
        self.department = value
    
    @property
    def order_index(self):
        return self.orden
    
    @order_index.setter
    def order_index(self, value):
        self.orden = value
        
    @property
    def signature_image(self):
        return self.signature
    
    @signature_image.setter
    def signature_image(self, value):
        self.signature = value
        
    @property
    def is_active(self):
        return 'Y'  # Por defecto siempre activo
    
    # Relationship back to municipality
    municipality = relationship("Municipality", back_populates="signatures")
