"""Service layer for product cost calculations.

This module provides business logic for calculating product costs based on:
1. Recipe-based costing (product linked to recipe → cost from ingredients)
2. Manual pricing (no recipe → cost_source = "manual")

All cost calculations use Decimal(10,2) precision with ROUND_HALF_UP rounding.
"""

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ProductNotFoundError,
    RecipeNotFoundError,
    RawMaterialNotFoundError,
)
from app.repositories.product_cost_repository import ProductCostRepository


class ProductCostService:
    """Service for calculating and retrieving product costs."""

    def __init__(self, db: Session):
        """Initialize service with database session.
        
        Args:
            db: SQLAlchemy session
        """
        self.db = db
        self.repo = ProductCostRepository(db)

    def calculate_product_cost(
        self, product_id: UUID, tenant_id: UUID
    ) -> dict:
        """Calculate the total cost of a product.
        
        Determines cost source (recipe-based or manual) and returns:
        - For recipe-linked products: cost calculated from ingredients
        - For unlinked products: cost_source = "manual" (no calculation)
        
        Args:
            product_id: UUID of the product
            tenant_id: UUID of the tenant (for isolation)
            
        Returns:
            dict: Cost response with structure:
            {
                "product_id": UUID,
                "total_cost": Decimal,
                "currency": str,
                "cost_source": "recipe" | "manual",
                "ingredients": [list of ingredient costs] or None,
                "calculated_at": ISO 8601 timestamp
            }
            
        Raises:
            ProductNotFoundError: If product not found in tenant
            RecipeNotFoundError: If product links to deleted recipe
            RawMaterialNotFoundError: If recipe ingredient references deleted raw material
        """
        # Fetch product with recipe link, enforcing tenant isolation
        product = self._fetch_product_with_recipe(product_id, tenant_id)
        
        if not product:
            raise ProductNotFoundError(f"Product {product_id} not found in tenant {tenant_id}")
        
        # If product has no recipe link, return manual pricing mode
        if not product.recipe_id:
            return {
                "product_id": str(product_id),
                "total_cost": Decimal("0.00"),
                "currency": "USD",
                "cost_source": "manual",
                "ingredients": None,
                "calculated_at": datetime.utcnow().isoformat() + "Z",
            }
        
        # Calculate cost from recipe
        cost_response = self._calculate_recipe_cost(product.recipe_id, tenant_id)
        
        # Augment recipe cost response with product-level metadata
        return {
            "product_id": str(product_id),
            "total_cost": cost_response["total_cost"],
            "currency": cost_response["currency"],
            "cost_source": "recipe",
            "ingredients": cost_response["ingredients"],
            "calculated_at": cost_response["calculated_at"],
        }

    def _fetch_product_with_recipe(
        self, product_id: UUID, tenant_id: UUID
    ) -> Optional[object]:
        """Fetch product with recipe link, enforcing tenant isolation.
        
        Args:
            product_id: UUID of the product
            tenant_id: UUID of the tenant
            
        Returns:
            Product ORM model or None if not found
        """
        return self.repo.get_product_with_recipe(product_id, tenant_id)

    def _calculate_recipe_cost(
        self, recipe_id: UUID, tenant_id: UUID
    ) -> dict:
        """Calculate total cost of a recipe based on current ingredient costs.
        
        Fetches all ingredients and their raw material costs, multiplies quantities
        by unit costs, and sums with half-up rounding.
        
        Args:
            recipe_id: UUID of the recipe
            tenant_id: UUID of the tenant
            
        Returns:
            dict: Recipe cost response with structure:
            {
                "total_cost": Decimal,
                "currency": str,
                "ingredients": [
                    {
                        "raw_material_id": UUID,
                        "raw_material_name": str,
                        "quantity": Decimal,
                        "unit": str,
                        "unit_cost": Decimal,
                        "ingredient_total_cost": Decimal
                    },
                    ...
                ],
                "calculated_at": ISO 8601 timestamp
            }
            
        Raises:
            RecipeNotFoundError: If recipe not found
            RawMaterialNotFoundError: If any ingredient references deleted raw material
        """
        # Fetch recipe cost data (ingredients + raw material costs)
        recipe_data = self.repo.get_recipe_cost_data(recipe_id, tenant_id)
        
        if recipe_data is None:
            raise RecipeNotFoundError(f"Recipe {recipe_id} not found in tenant {tenant_id}")
        
        # recipe_data structure:
        # {
        #     "ingredients": [
        #         {
        #             "raw_material_id": UUID,
        #             "raw_material_name": str,
        #             "quantity": Decimal,
        #             "unit": str,
        #             "unit_cost": Decimal or None (None if raw material deleted)
        #         },
        #         ...
        #     ]
        # }
        
        ingredients_response = []
        total_cost = Decimal("0.00")
        
        for ingredient in recipe_data["ingredients"]:
            # Validate that raw material still exists (cost_per_unit not None)
            if ingredient["unit_cost"] is None:
                raise RawMaterialNotFoundError(
                    f"Raw material {ingredient['raw_material_id']} referenced in recipe "
                    f"{recipe_id} no longer exists (deleted)"
                )
            
            # Calculate ingredient total cost: quantity × unit_cost
            quantity = Decimal(str(ingredient["quantity"]))
            unit_cost = Decimal(str(ingredient["unit_cost"]))
            ingredient_total = quantity * unit_cost
            
            # Round to 2 decimal places using half-up rounding
            ingredient_total = ingredient_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            # Add to response
            ingredients_response.append({
                "raw_material_id": ingredient["raw_material_id"],
                "raw_material_name": ingredient["raw_material_name"],
                "quantity": quantity,
                "unit": ingredient["unit"],
                "unit_cost": unit_cost,
                "ingredient_total_cost": ingredient_total,
            })
            
            # Accumulate total cost
            total_cost += ingredient_total
        
        # Round final total to 2 decimal places using half-up rounding
        total_cost = total_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        return {
            "total_cost": total_cost,
            "currency": "USD",
            "ingredients": ingredients_response,
            "calculated_at": datetime.utcnow().isoformat() + "Z",
        }
