from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AnswerBaseSchema(BaseModel):
    procedure_id: Optional[int] = None
    name: Optional[str] = None
    value: Optional[str] = None
    user_id: Optional[int] = None
    status: Optional[int] = 1

class AnswerCreateSchema(AnswerBaseSchema):    
    pass

class AnswerUpdateSchema(BaseModel):
    procedure_id: Optional[int] = None
    name: Optional[str] = None
    value: Optional[str] = None
    user_id: Optional[int] = None
    status: Optional[int] = None

class AnswerResponseSchema(AnswerBaseSchema):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True  
    )
