"""Pydantic schemas for tenant management."""

from datetime import datetime
from pydantic import BaseModel


class TenantCreate(BaseModel):
    """Request to create a new tenant."""
    
    name: str


class TenantResponse(BaseModel):
    """Tenant information response."""
    
    id: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True
