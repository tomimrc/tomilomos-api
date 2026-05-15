"""Pydantic schemas for recipes API.

These schemas define request/response validation and serialization for recipes operations.
"""

from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


# Valid units of measurement (inherited from raw materials)
VALID_UNITS = {"kg", "g", "L", "mL", "units", "pieces", "boxes"}


class RecipeCreate(BaseModel):
    """Schema for creating a new recipe."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Recipe name (unique within tenant)")
    description: Optional[str] = Field(None, max_length=1000, description="Optional recipe description")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Lomito Completo",
                "description": "Classic complete beef sandwich with all toppings"
            }
        }


class RecipeUpdate(BaseModel):
    """Schema for updating a recipe (all fields optional)."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Recipe name")
    description: Optional[str] = Field(None, max_length=1000, description="Recipe description")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Lomito Premium",
                "description": "Premium version with better beef cut"
            }
        }


class RecipeIngredientCreate(BaseModel):
    """Schema for adding an ingredient to a recipe."""
    
    raw_material_id: str = Field(..., description="ID of the raw material")
    quantity: Decimal = Field(..., description="Quantity of the ingredient")
    unit: str = Field(..., description="Unit of measurement")
    
    @validator('quantity')
    def validate_quantity(cls, v):
        """Ensure quantity is positive."""
        if v <= 0:
            raise ValueError('quantity must be greater than 0')
        return v
    
    @validator('unit')
    def validate_unit(cls, v):
        """Ensure unit is in valid list."""
        if v not in VALID_UNITS:
            raise ValueError(f'unit must be one of: {", ".join(sorted(VALID_UNITS))}')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "raw_material_id": "550e8400-e29b-41d4-a716-446655440000",
                "quantity": "250",
                "unit": "g"
            }
        }


class RecipeIngredientUpdate(BaseModel):
    """Schema for updating an ingredient in a recipe."""
    
    quantity: Optional[Decimal] = Field(None, description="Quantity of the ingredient")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    
    @validator('quantity')
    def validate_quantity(cls, v):
        """Ensure quantity is positive if provided."""
        if v is not None and v <= 0:
            raise ValueError('quantity must be greater than 0')
        return v
    
    @validator('unit')
    def validate_unit(cls, v):
        """Ensure unit is valid if provided."""
        if v is not None and v not in VALID_UNITS:
            raise ValueError(f'unit must be one of: {", ".join(sorted(VALID_UNITS))}')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "quantity": "300",
                "unit": "g"
            }
        }


class RecipeIngredientResponse(BaseModel):
    """Schema for returning an ingredient in a recipe response."""
    
    id: str
    recipe_id: str
    raw_material_id: str
    quantity: Decimal
    unit: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RecipeResponse(BaseModel):
    """Schema for returning a recipe."""
    
    id: str
    tenant_id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RecipeCostDetailItem(BaseModel):
    """Schema for itemized ingredient cost in recipe costing response."""
    
    raw_material_id: str
    raw_material_name: str
    quantity: Decimal
    unit: str
    unit_cost: Decimal
    ingredient_total_cost: Decimal


class RecipeCostResponse(BaseModel):
    """Schema for recipe cost calculation response."""
    
    total_cost: Decimal = Field(..., description="Total recipe cost in 2 decimal places")
    currency: str = Field(default="USD", description="Currency code")
    ingredients: List[RecipeCostDetailItem] = Field(..., description="Itemized breakdown by ingredient")
    calculated_at: datetime = Field(..., description="Timestamp of calculation (ISO 8601)")
    
    class Config:
        schema_extra = {
            "example": {
                "total_cost": "15.75",
                "currency": "USD",
                "ingredients": [
                    {
                        "raw_material_id": "550e8400-e29b-41d4-a716-446655440000",
                        "raw_material_name": "Beef",
                        "quantity": "250",
                        "unit": "g",
                        "unit_cost": "8.00",
                        "ingredient_total_cost": "2.00"
                    }
                ],
                "calculated_at": "2026-05-12T10:30:00Z"
            }
        }
