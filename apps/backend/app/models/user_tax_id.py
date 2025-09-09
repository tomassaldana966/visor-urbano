from sqlalchemy import Column, String, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class ClientTaxID(Base):
    __tablename__ = 'user_tax_id'

    id = Column(Integer, primary_key=True)
    tax_id_number = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tax_id_type = Column(Enum(
        'RFC', 'TIN', 'SSN', 'NIF', 'RNC', 'RUT', 'SIN', 'BN', 'OTHER',
        name='tax_id_types'
    ), nullable=True)
    
    user = relationship("UserModel", back_populates="tax_id_relation")