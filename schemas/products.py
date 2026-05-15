"""Pydantic schemas for products API.

These schemas define request/response validation and serialization for products operations.
"""

from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class ProductCreate(BaseModel):
    """Schema for creating a new product."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Product name (e.g., 'Lomito Completo')")
    sale_price: Decimal = Field(..., description="Selling price in home currency")
    is_active: Optional[bool] = Field(True, description="Whether the product is active/available (defaults to true)")
    recipe_id: Optional[str] = Field(None, description="Optional recipe ID for recipe-based costing")
    
    @validator('sale_price')
    def validate_sale_price(cls, v):
        """Ensure sale_price is positive."""
        if v <= 0:
            raise ValueError('sale_price must be greater than 0')
        if v > 99999999.99:
            raise ValueError('sale_price cannot exceed 99,999,999.99')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Lomito Completo",
                "sale_price": "45.99",
                "is_active": True,
                "recipe_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields optional)."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Product name")
    sale_price: Optional[Decimal] = Field(None, description="Selling price")
    is_active: Optional[bool] = Field(None, description="Availability flag")
    recipe_id: Optional[str] = Field(None, description="Recipe ID for recipe-based costing (set to null to unlink)")
    
    @validator('sale_price')
    def validate_sale_price(cls, v):
        """Ensure sale_price is positive if provided."""
        if v is not None:
            if v <= 0:
                raise ValueError('sale_price must be greater than 0')
            if v > 99999999.99:
                raise ValueError('sale_price cannot exceed 99,999,999.99')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Lomito Premium",
                "sale_price": "49.99",
                "recipe_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class ProductRead(BaseModel):
    """Schema for API responses (read operations)."""
    
    id: str = Field(..., description="Product ID")
    tenant_id: str = Field(..., description="Tenant ID")
    name: str = Field(..., description="Product name")
    sale_price: Decimal = Field(..., description="Selling price")
    is_active: bool = Field(..., description="Availability flag")
    recipe_id: Optional[str] = Field(None, description="Linked recipe ID (if any)")
    cost_price: Optional[Decimal] = Field(None, description="Calculated cost price from recipe (if recipe_id is set)")
    created_at: datetime = Field(..., description="When the product was created")
    updated_at: datetime = Field(..., description="When the product was last updated")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "prod-123",
                "tenant_id": "tenant-456",
                "name": "Lomito Completo",
                "sale_price": "45.99",
                "is_active": True,
                "recipe_id": "550e8400-e29b-41d4-a716-446655440000",
                "cost_price": "28.50",
                "created_at": "2026-05-12T10:00:00",
                "updated_at": "2026-05-12T10:00:00"
            }
        }
