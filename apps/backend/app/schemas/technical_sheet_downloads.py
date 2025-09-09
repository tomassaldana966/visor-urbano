from pydantic import BaseModel, field_validator
from typing import Optional, List, Union
import re

class TechnicalSheetDownloadCreate(BaseModel):
    city: str
    email: Optional[str] = ""
    age: Union[str, int]
    name: Optional[str] = ""
    sector: str
    uses: List[str]
    municipality_id: int 
    address: Optional[str] = None
    
    @field_validator('age', mode='before')
    @classmethod
    def convert_age_to_string(cls, v):
        if isinstance(v, int):
            return str(v)
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v and v != "":  # Only validate if email is provided and not empty
            # More permissive pattern to allow international domains and IDNs
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_pattern, v):
                raise ValueError('Invalid email format')
        return v

class TechnicalSheetDownloadResponse(BaseModel):
    id: Optional[int] = None
