"""Data access layer for product cost queries.

This module provides efficient, indexed queries for:
1. Fetching products with recipe links
2. Fetching recipe cost data (ingredients + raw material costs)
3. Multi-tenant isolation enforcement
"""

from typing import Optional, Dict, List, Any
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.orm import Session, joinedload

from app.db.models import Product, Recipe, RecipeIngredient, RawMaterial


class ProductCostRepository:
    """Repository for product cost-related queries."""

    def __init__(self, db: Session):
        """Initialize repository with database session.
        
        Args:
            db: SQLAlchemy session
        """
        self.db = db

    def get_product_with_recipe(
        self, product_id: UUID, tenant_id: UUID
    ) -> Optional[Product]:
        """Fetch product with recipe link, enforcing tenant isolation.
        
        Uses joinedload to eagerly load the recipe relationship to avoid N+1.
        
        Args:
            product_id: UUID of the product
            tenant_id: UUID of the tenant
            
        Returns:
            Product ORM model with recipe relationship loaded, or None if not found
            
        Note:
            Enforces tenant_id isolation — returns None if product belongs to different tenant.
        """
        query = select(Product).where(
            and_(
                Product.id == product_id,
                Product.tenant_id == tenant_id,
            )
        ).options(joinedload(Product.recipe))
        
        return self.db.execute(query).scalars().first()

    def get_recipe_cost_data(
        self, recipe_id: UUID, tenant_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Fetch recipe cost data: ingredients with their raw material costs.
        
        Returns structured data suitable for cost calculation:
        {
            "ingredients": [
                {
                    "raw_material_id": UUID,
                    "raw_material_name": str,
                    "quantity": Decimal,
                    "unit": str,
                    "unit_cost": Decimal (or None if raw material deleted)
                },
                ...
            ]
        }
        
        Args:
            recipe_id: UUID of the recipe
            tenant_id: UUID of the tenant
            
        Returns:
            dict with ingredients data, or None if recipe not found in tenant
            
        Note:
            - Enforces tenant_id isolation for recipe lookup
            - Returns raw_material_id even if raw_material was deleted (cost_per_unit = None)
              so that service layer can detect and report the error
            - Uses efficient query with joins (no N+1)
        """
        # First, verify recipe exists and belongs to tenant
        recipe_query = select(Recipe).where(
            and_(
                Recipe.id == recipe_id,
                Recipe.tenant_id == tenant_id,
            )
        ).options(
            joinedload(Recipe.ingredients).joinedload(RecipeIngredient.raw_material)
        )
        
        recipe = self.db.execute(recipe_query).scalars().first()
        
        if recipe is None:
            return None
        
        # Build ingredients response
        ingredients = []
        for ingredient in recipe.ingredients:
            # ingredient.raw_material could be None if it was deleted (due to cascade behavior)
            # We still include it so service layer can detect and raise error
            unit_cost = None
            raw_material_name = "DELETED"
            
            if ingredient.raw_material is not None:
                unit_cost = ingredient.raw_material.cost_per_unit
                raw_material_name = ingredient.raw_material.name
            
            ingredients.append({
                "raw_material_id": ingredient.raw_material_id,
                "raw_material_name": raw_material_name,
                "quantity": ingredient.quantity,
                "unit": ingredient.unit,
                "unit_cost": unit_cost,
            })
        
        return {
            "ingredients": ingredients,
        }

    def add_product_indexes_if_not_exist(self) -> None:
        """Verify that required indexes exist on products table.
        
        This is a helper for migration/setup purposes.
        In production, indexes should be created via Alembic migrations.
        
        Current indexes required:
        - products(tenant_id, recipe_id) for fast product cost queries
        - products(tenant_id, id) for multi-tenant lookups
        - products(recipe_id) for recipe deletion cascade checks
        
        Note:
            This method does NOT create indexes (SQLAlchemy doesn't provide that easily).
            It's here for documentation. Indexes must be created via Alembic or raw SQL.
        """
        # Placeholder: in production, run raw SQL or Alembic migrations
        # Example SQL to verify/create indexes:
        # CREATE INDEX IF NOT EXISTS ix_products_tenant_recipe ON products(tenant_id, recipe_id);
        # CREATE INDEX IF NOT EXISTS ix_products_tenant_id ON products(tenant_id);
        pass
