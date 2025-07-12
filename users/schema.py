from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class UserItem(BaseModel):
    id: int
    email: EmailStr = Field(..., min_length=1, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)
    role: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr = Field(..., min_length=1, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)
    password: str = Field(..., min_length=8)

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, min_length=1, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8)

    class Config:
        from_attributes = True

class ResetPasswordIn(BaseModel):
    token: str = Field(..., description="Password reset token from email link")
    new_password: str = Field(..., min_length=8, description="New desired password")

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[UserItem]

    class Config:
        from_attributes = True
