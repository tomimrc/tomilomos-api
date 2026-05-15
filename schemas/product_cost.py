"""Pydantic schemas for product cost calculation API.

These schemas define request/response validation and serialization for product cost operations.
All costs use Decimal(10,2) precision to ensure accuracy without floating-point errors.
"""

from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class CostSourceEnum(str, Enum):
    """Enumeration of cost source types."""
    RECIPE = "recipe"
    MANUAL = "manual"


class IngredientCostDetail(BaseModel):
    """Schema for ingredient cost breakdown in recipe-based costing.
    
    Represents a single ingredient in a recipe with its current cost calculation.
    """
    
    raw_material_id: str = Field(..., description="ID of the raw material")
    raw_material_name: str = Field(..., description="Name of the raw material")
    quantity: Decimal = Field(..., description="Quantity of the ingredient used in recipe")
    unit: str = Field(..., description="Unit of measurement (kg, g, L, mL, units, pieces, boxes)")
    unit_cost: Decimal = Field(..., description="Current cost per unit")
    ingredient_total_cost: Decimal = Field(..., description="Quantity × Unit Cost (ingredient total)")
    
    @validator('unit_cost', 'ingredient_total_cost')
    def validate_decimal_precision(cls, v):
        """Ensure cost values have exactly 2 decimal places."""
        if v is not None:
            # Quantize to 2 decimal places
            v = v.quantize(Decimal("0.01"))
        return v
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "raw_material_id": "550e8400-e29b-41d4-a716-446655440000",
                "raw_material_name": "tomatoes",
                "quantity": "2.5",
                "unit": "kg",
                "unit_cost": "12.50",
                "ingredient_total_cost": "31.25"
            }
        }


class ProductCostResponse(BaseModel):
    """Schema for product cost calculation response.
    
    Response format for GET /api/v1/products/{id}/cost endpoint.
    Includes total cost, cost source (recipe or manual), and itemized breakdown for recipes.
    """
    
    product_id: str = Field(..., description="UUID of the product")
    total_cost: Decimal = Field(..., description="Total calculated cost")
    currency: str = Field(..., description="Currency code (e.g., USD)")
    cost_source: CostSourceEnum = Field(..., description="Source of cost calculation: 'recipe' or 'manual'")
    ingredients: Optional[List[IngredientCostDetail]] = Field(
        None,
        description="Itemized ingredient costs (only for recipe-based products)"
    )
    calculated_at: str = Field(..., description="ISO 8601 timestamp of calculation")
    
    @validator('total_cost')
    def validate_total_cost_precision(cls, v):
        """Ensure total_cost has exactly 2 decimal places."""
        if v is not None:
            v = v.quantize(Decimal("0.01"))
        return v
    
    @validator('ingredients', pre=True, always=True)
    def validate_ingredients_with_cost_source(cls, v, values):
        """Ensure ingredients array is only present for recipe-based costs."""
        cost_source = values.get('cost_source')
        
        if cost_source == CostSourceEnum.RECIPE and v is None:
            raise ValueError("ingredients array must be present for recipe-based costs")
        
        if cost_source == CostSourceEnum.MANUAL and v is not None:
            raise ValueError("ingredients array must be null for manual pricing")
        
        return v
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "product_id": "550e8400-e29b-41d4-a716-446655440000",
                "total_cost": "45.99",
                "currency": "USD",
                "cost_source": "recipe",
                "ingredients": [
                    {
                        "raw_material_id": "550e8400-e29b-41d4-a716-446655440001",
                        "raw_material_name": "tomatoes",
                        "quantity": "2.5",
                        "unit": "kg",
                        "unit_cost": "12.50",
                        "ingredient_total_cost": "31.25"
                    },
                    {
                        "raw_material_id": "550e8400-e29b-41d4-a716-446655440002",
                        "raw_material_name": "onions",
                        "quantity": "1.0",
                        "unit": "kg",
                        "unit_cost": "3.50",
                        "ingredient_total_cost": "3.50"
                    },
                    {
                        "raw_material_id": "550e8400-e29b-41d4-a716-446655440003",
                        "raw_material_name": "olive oil",
                        "quantity": "0.25",
                        "unit": "L",
                        "unit_cost": "10.99",
                        "ingredient_total_cost": "2.75"
                    }
                ],
                "calculated_at": "2025-05-13T14:30:00Z"
            }
        }
