from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from config.settings import Base
from sqlalchemy.orm import relationship

class DependencyRevision(Base):
    __tablename__ = 'dependency_revisions'  
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dependency_id = Column(Integer, ForeignKey('requirements_querys.id'), nullable=False)  
    revision_notes = Column(Text, nullable=True)      
    revised_at = Column(DateTime, server_default=func.now(), nullable=False)  
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    requirements_query = relationship("RequirementsQuery", backref="dependency_revisions")