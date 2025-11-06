from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """User entity with validated email."""
    id: Optional[int] = None
    email: EmailStr = Field(..., description="User email (validated)")
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
        schema_extra = {
            "example": {
                "email": "jane.doe@example.com",
                "full_name": "Jane Doe",
                "is_active": True
            }
        }


class UserCreateRequest(BaseModel):
    """Request model to create users."""
    email: EmailStr = Field(..., description="User email (validated)")
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdateRequest(BaseModel):
    """Request model to update users."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)


