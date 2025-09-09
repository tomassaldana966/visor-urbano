from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import date

class BlogBase(BaseModel):
    title: str
    slug: Optional[str] = None  # For SEO-friendly URLs
    summary: str
    image: str
    link: str
    news_date: date
    blog_type: Optional[int] = None
    body: Optional[str] = None
    municipality_id: Optional[int] = 2  # Default to municipality 2

    @field_validator('title', 'summary', 'image', 'link')
    @classmethod
    def validate_non_empty_strings(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v

    @field_validator('municipality_id')
    @classmethod
    def validate_municipality_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Municipality ID must be positive')
        return v

class BlogCreate(BlogBase):
    password: str

class BlogUpdate(BlogBase):
    password: str

class BlogResponse(BlogBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
