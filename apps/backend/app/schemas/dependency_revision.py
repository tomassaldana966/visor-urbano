from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class DependencyRevisionBase(BaseModel):
    dependency_id: int = Field(..., description="ID of the related dependency")
    revision_notes: Optional[str] = Field(None, description="Notes or comments from the revision")
    revised_at: Optional[datetime] = Field(None, description="Timestamp when the revision was made")


class DependencyRevisionCreate(DependencyRevisionBase):
    pass


class DependencyRevisionUpdate(BaseModel):
    revision_notes: Optional[str] = Field(None, description="Updated notes from the revision")


class DependencyRevisionRead(DependencyRevisionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)