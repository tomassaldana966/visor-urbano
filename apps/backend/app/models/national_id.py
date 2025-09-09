from sqlalchemy import Column, String, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class UserNationalID(Base):
    __tablename__ = 'national_id'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    national_id_number = Column(String(30), nullable=True)
    national_id_type = Column(Enum(
        'CURP', 'SSN', 'DNI', 'CEDULA', 'RUN', 'SIN', 'OTHER',
        name='national_id_types'
    ), nullable=True)

    user = relationship("UserModel", back_populates="national_id_relation")
