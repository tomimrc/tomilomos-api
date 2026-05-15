"""Pydantic schemas for sales API.

These schemas define request/response validation and serialization for sales operations.
"""

from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class SaleCreate(BaseModel):
    """Schema for creating a new sale."""
    
    product_id: str = Field(..., description="ID of the product being sold")
    quantity: int = Field(..., description="Number of units sold (positive integer)")
    
    @validator('quantity')
    def validate_quantity(cls, v):
        """Ensure quantity is a positive integer."""
        if v <= 0:
            raise ValueError('quantity must be greater than 0')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "product_id": "550e8400-e29b-41d4-a716-446655440000",
                "quantity": 2
            }
        }


class SaleRead(BaseModel):
    """Schema for API responses (read operations)."""
    
    id: str = Field(..., description="Sale ID")
    tenant_id: str = Field(..., description="Tenant ID")
    product_id: str = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name at time of sale")
    quantity: int = Field(..., description="Number of units sold")
    unit_price: Decimal = Field(..., description="Sale price per unit (snapshot)")
    total_price: Decimal = Field(..., description="Total sale price (unit_price × quantity)")
    total_cost: Optional[Decimal] = Field(None, description="Total recipe cost × quantity, or None if no recipe")
    margin: Optional[Decimal] = Field(None, description="total_price - total_cost, or None if no cost")
    created_at: datetime = Field(..., description="When the sale was registered")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "sale-123",
                "tenant_id": "tenant-456",
                "product_id": "prod-789",
                "product_name": "Lomito Completo",
                "quantity": 2,
                "unit_price": "45.99",
                "total_price": "91.98",
                "total_cost": "57.00",
                "margin": "34.98",
                "created_at": "2026-05-14T15:30:00"
            }
        }
