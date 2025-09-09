from sqlalchemy import Column, BigInteger, Integer, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class Blog(Base):
    __tablename__ = 'blog'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    slug = Column(Text, nullable=True)  # For SEO-friendly URLs
    image = Column(Text, nullable=False)
    link = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    news_date = Column(Date, nullable=False)
    blog_type = Column(Integer, nullable=True)
    body = Column(Text, nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False, default=2)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationship
    municipality = relationship("Municipality", back_populates="blogs")
