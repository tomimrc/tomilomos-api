"""Repository layer for recipes.

This layer handles all database operations for recipes and recipe ingredients.
"""

from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from db.models import Recipe, RecipeIngredient, RawMaterial


class RecipeRepository:
    """Repository for recipe database operations."""
    
    def __init__(self, session: Session):
        """Initialize the repository with a database session.
        
        Args:
            session: SQLAlchemy session for database operations
        """
        self.session = session
    
    # ===== RECIPE CRUD METHODS =====
    
    def create_recipe(
        self,
        tenant_id: str,
        recipe_id: str,
        name: str,
        description: Optional[str] = None
    ) -> Recipe:
        """Create a new recipe record.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID for the new recipe
            name: Recipe name (unique within tenant)
            description: Optional recipe description
            
        Returns:
            Created Recipe instance
            
        Raises:
            IntegrityError: If database constraints are violated
        """
        recipe = Recipe(
            id=recipe_id,
            tenant_id=tenant_id,
            name=name,
            description=description or ""
        )
        self.session.add(recipe)
        self.session.flush()
        return recipe
    
    def get_recipe_by_id(self, tenant_id: str, recipe_id: str) -> Optional[Recipe]:
        """Get a recipe by ID, enforcing tenant isolation.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            
        Returns:
            Recipe instance or None if not found
        """
        return self.session.query(Recipe).filter(
            and_(
                Recipe.id == recipe_id,
                Recipe.tenant_id == tenant_id
            )
        ).first()
    
    def find_by_tenant_and_name(self, tenant_id: str, name: str) -> Optional[Recipe]:
        """Find a recipe by tenant and name.
        
        Args:
            tenant_id: ID of the tenant
            name: Recipe name to search for
            
        Returns:
            Recipe instance or None if not found
        """
        return self.session.query(Recipe).filter(
            and_(
                Recipe.tenant_id == tenant_id,
                Recipe.name == name
            )
        ).first()
    
    def find_all_by_tenant(
        self,
        tenant_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Recipe]:
        """List recipes for a tenant with pagination.
        
        Args:
            tenant_id: ID of the tenant
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Recipe instances
        """
        return self.session.query(Recipe).filter(
            Recipe.tenant_id == tenant_id
        ).offset(skip).limit(limit).all()
    
    def update_recipe(
        self,
        tenant_id: str,
        recipe_id: str,
        **updates
    ) -> Optional[Recipe]:
        """Update a recipe record, enforcing tenant isolation.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            **updates: Fields to update
            
        Returns:
            Updated Recipe instance or None if not found
        """
        recipe = self.get_recipe_by_id(tenant_id, recipe_id)
        if not recipe:
            return None
        
        # Update allowed fields
        allowed_fields = {'name', 'description'}
        for field, value in updates.items():
            if field in allowed_fields and value is not None:
                setattr(recipe, field, value)
        
        self.session.flush()
        return recipe
    
    def delete_recipe(self, tenant_id: str, recipe_id: str) -> bool:
        """Delete a recipe record and cascade delete its ingredients.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            
        Returns:
            True if deleted, False if not found
        """
        recipe = self.get_recipe_by_id(tenant_id, recipe_id)
        if not recipe:
            return False
        
        self.session.delete(recipe)
        self.session.flush()
        return True
    
    # ===== RECIPE INGREDIENT METHODS =====
    
    def add_ingredient(
        self,
        recipe_id: str,
        ingredient_id: str,
        raw_material_id: str,
        quantity: Decimal,
        unit: str
    ) -> RecipeIngredient:
        """Add an ingredient to a recipe.
        
        Args:
            recipe_id: ID of the recipe
            ingredient_id: ID for the new ingredient
            raw_material_id: ID of the raw material
            quantity: Quantity of the ingredient
            unit: Unit of measurement
            
        Returns:
            Created RecipeIngredient instance
        """
        ingredient = RecipeIngredient(
            id=ingredient_id,
            recipe_id=recipe_id,
            raw_material_id=raw_material_id,
            quantity=quantity,
            unit=unit
        )
        self.session.add(ingredient)
        self.session.flush()
        return ingredient
    
    def get_ingredient_by_id(
        self,
        recipe_id: str,
        ingredient_id: str
    ) -> Optional[RecipeIngredient]:
        """Get an ingredient by ID (within recipe context).
        
        Args:
            recipe_id: ID of the recipe
            ingredient_id: ID of the ingredient
            
        Returns:
            RecipeIngredient instance or None
        """
        return self.session.query(RecipeIngredient).filter(
            and_(
                RecipeIngredient.id == ingredient_id,
                RecipeIngredient.recipe_id == recipe_id
            )
        ).first()
    
    def remove_ingredient(self, recipe_id: str, ingredient_id: str) -> bool:
        """Remove an ingredient from a recipe.
        
        Args:
            recipe_id: ID of the recipe
            ingredient_id: ID of the ingredient
            
        Returns:
            True if deleted, False if not found
        """
        ingredient = self.get_ingredient_by_id(recipe_id, ingredient_id)
        if not ingredient:
            return False
        
        self.session.delete(ingredient)
        self.session.flush()
        return True
    
    def list_ingredients(self, recipe_id: str) -> List[RecipeIngredient]:
        """List all ingredients for a recipe.
        
        Args:
            recipe_id: ID of the recipe
            
        Returns:
            List of RecipeIngredient instances
        """
        return self.session.query(RecipeIngredient).filter(
            RecipeIngredient.recipe_id == recipe_id
        ).all()
    
    def update_ingredient(
        self,
        recipe_id: str,
        ingredient_id: str,
        **updates
    ) -> Optional[RecipeIngredient]:
        """Update an ingredient in a recipe.
        
        Args:
            recipe_id: ID of the recipe
            ingredient_id: ID of the ingredient
            **updates: Fields to update
            
        Returns:
            Updated RecipeIngredient instance or None
        """
        ingredient = self.get_ingredient_by_id(recipe_id, ingredient_id)
        if not ingredient:
            return None
        
        # Update allowed fields
        allowed_fields = {'quantity', 'unit'}
        for field, value in updates.items():
            if field in allowed_fields and value is not None:
                setattr(ingredient, field, value)
        
        self.session.flush()
        return ingredient
    
    def get_ingredients_with_costs(self, recipe_id: str) -> List[dict]:
        """Fetch all ingredients with their current raw material costs (for costing).
        
        Args:
            recipe_id: ID of the recipe
            
        Returns:
            List of dicts with ingredient + cost data: {
                'ingredient': RecipeIngredient,
                'raw_material': RawMaterial,
                'unit_cost': Decimal
            }
        """
        ingredients = self.session.query(RecipeIngredient).filter(
            RecipeIngredient.recipe_id == recipe_id
        ).all()
        
        result = []
        for ingredient in ingredients:
            raw_material = self.session.query(RawMaterial).filter(
                RawMaterial.id == ingredient.raw_material_id
            ).first()
            
            if raw_material:
                result.append({
                    'ingredient': ingredient,
                    'raw_material': raw_material,
                    'unit_cost': raw_material.cost_per_unit
                })
        
        return result
    
    def verify_raw_material_in_tenant(
        self,
        tenant_id: str,
        raw_material_id: str
    ) -> bool:
        """Verify that a raw material exists and belongs to the tenant (foreign key validation).
        
        Args:
            tenant_id: ID of the tenant
            raw_material_id: ID of the raw material
            
        Returns:
            True if raw material exists in tenant, False otherwise
        """
        return self.session.query(RawMaterial).filter(
            and_(
                RawMaterial.id == raw_material_id,
                RawMaterial.tenant_id == tenant_id
            )
        ).first() is not None
