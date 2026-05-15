"""Pydantic schemas for user management."""

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Request to create a new user."""
    
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User information response."""
    
    id: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True
