from pydantic import BaseModel, Field
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    email: str
    role: str

    class Config:
        from_attributes = True
