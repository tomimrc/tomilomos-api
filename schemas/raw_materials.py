"""Pydantic schemas for raw materials API.

These schemas define request/response validation and serialization for raw materials operations.
"""

from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


# Valid units of measurement for raw materials
VALID_UNITS = {"kg", "g", "L", "mL", "units", "pieces", "boxes"}


class RawMaterialCreate(BaseModel):
    """Schema for creating a new raw material."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Name of the raw material")
    unit_of_measurement: str = Field(..., description="Unit type (kg, g, L, mL, units, pieces, boxes)")
    cost_per_unit: Decimal = Field(..., description="Cost per unit in home currency")
    supplier: Optional[str] = Field(None, max_length=255, description="Optional supplier name or reference")
    
    @validator('cost_per_unit')
    def validate_cost(cls, v):
        """Ensure cost_per_unit is positive."""
        if v <= 0:
            raise ValueError('cost_per_unit must be greater than 0')
        return v
    
    @validator('unit_of_measurement')
    def validate_unit(cls, v):
        """Ensure unit_of_measurement is in valid list."""
        if v not in VALID_UNITS:
            raise ValueError(f'unit_of_measurement must be one of: {", ".join(sorted(VALID_UNITS))}')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Tomatoes",
                "unit_of_measurement": "kg",
                "cost_per_unit": "2.50",
                "supplier": "Local Farm"
            }
        }


class RawMaterialUpdate(BaseModel):
    """Schema for updating a raw material (all fields optional)."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Name of the raw material")
    unit_of_measurement: Optional[str] = Field(None, description="Unit type")
    cost_per_unit: Optional[Decimal] = Field(None, description="Cost per unit")
    supplier: Optional[str] = Field(None, max_length=255, description="Supplier name or reference")
    current_stock: Optional[Decimal] = Field(None, description="Current stock level (read-only, use add-stock/remove-stock)")
    
    @validator('cost_per_unit')
    def validate_cost(cls, v):
        """Ensure cost_per_unit is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError('cost_per_unit must be greater than 0')
        return v
    
    @validator('unit_of_measurement')
    def validate_unit(cls, v):
        """Ensure unit_of_measurement is valid if provided."""
        if v is not None and v not in VALID_UNITS:
            raise ValueError(f'unit_of_measurement must be one of: {", ".join(sorted(VALID_UNITS))}')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Premium Tomatoes",
                "cost_per_unit": "3.00"
            }
        }


class RawMaterialRead(BaseModel):
    """Schema for API responses (read operations)."""
    
    id: str = Field(..., description="Raw material ID")
    tenant_id: str = Field(..., description="Tenant ID")
    name: str = Field(..., description="Name of the raw material")
    unit_of_measurement: str = Field(..., description="Unit type")
    cost_per_unit: Decimal = Field(..., description="Cost per unit")
    supplier: Optional[str] = Field(None, description="Supplier name")
    current_stock: Decimal = Field(..., description="Current stock level")
    created_at: datetime = Field(..., description="When the raw material was created")
    updated_at: datetime = Field(..., description="When the raw material was last updated")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "raw-mat-123",
                "tenant_id": "tenant-456",
                "name": "Tomatoes",
                "unit_of_measurement": "kg",
                "cost_per_unit": "2.50",
                "supplier": "Local Farm",
                "current_stock": "10.50",
                "created_at": "2026-05-11T10:00:00",
                "updated_at": "2026-05-11T10:00:00"
            }
        }


class StockAdjustmentRequest(BaseModel):
    """Schema for stock adjustment requests (add/remove stock)."""
    
    quantity: Decimal = Field(..., gt=0, description="Quantity to add or remove (must be positive)")
    reason: Optional[str] = Field(None, max_length=255, description="Reason for adjustment (e.g., purchase, sale, waste)")
    
    class Config:
        schema_extra = {
            "example": {
                "quantity": "5.50",
                "reason": "purchase"
            }
        }


class StockLevel(BaseModel):
    """Schema for stock level responses."""
    
    id: str = Field(..., description="Raw material ID")
    current_stock: Decimal = Field(..., description="Current stock level")
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "raw-mat-123",
                "current_stock": "10.50"
            }
        }
