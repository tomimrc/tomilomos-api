"""Service layer for recipes business logic.

This layer contains all business logic for recipes operations.
Repositories handle persistence; services handle validation, orchestration, and costing.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, List
from datetime import datetime
import uuid

from sqlalchemy.orm import Session

from repositories.recipe_repository import RecipeRepository
from schemas.recipes import (
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
    RecipeIngredientCreate,
    RecipeIngredientUpdate,
    RecipeIngredientResponse,
    RecipeCostResponse,
    RecipeCostDetailItem,
)
from db.models import Recipe, RecipeIngredient, RawMaterial


# Custom exceptions for recipe operations
class RecipeNotFound(Exception):
    """Raised when a recipe is not found."""
    pass


class RecipeNameAlreadyExists(Exception):
    """Raised when a recipe name already exists in the tenant."""
    pass


class UnauthorizedAccess(Exception):
    """Raised when a user attempts unauthorized access."""
    pass


class RawMaterialNotFound(Exception):
    """Raised when a raw material is not found."""
    pass


class RecipeService:
    """Service for recipes business logic."""
    
    def __init__(self, session: Session):
        """Initialize the service with a database session.
        
        Args:
            session: SQLAlchemy session for database operations
        """
        self.repository = RecipeRepository(session)
        self.session = session
    
    # ===== RECIPE CRUD METHODS (Tasks 3.1-3.6) =====
    
    def create_recipe(
        self,
        tenant_id: str,
        data: RecipeCreate
    ) -> RecipeResponse:
        """Create a new recipe with validation.
        
        Args:
            tenant_id: ID of the tenant
            data: RecipeCreate schema with validated data
            
        Returns:
            RecipeResponse schema with created data
            
        Raises:
            RecipeNameAlreadyExists: If recipe name already exists in tenant
        """
        # Validate unique name within tenant
        existing = self.repository.find_by_tenant_and_name(tenant_id, data.name)
        if existing:
            raise RecipeNameAlreadyExists(
                f"Recipe name '{data.name}' already exists in your tenant"
            )
        
        # Generate UUID for recipe
        recipe_id = str(uuid.uuid4())
        
        # Create via repository
        recipe = self.repository.create_recipe(
            tenant_id=tenant_id,
            recipe_id=recipe_id,
            name=data.name,
            description=data.description
        )
        
        return RecipeResponse.from_orm(recipe)
    
    def get_recipe(
        self,
        tenant_id: str,
        recipe_id: str
    ) -> RecipeResponse:
        """Get a recipe by ID with tenant isolation.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            
        Returns:
            RecipeResponse schema
            
        Raises:
            RecipeNotFound: If recipe not found or unauthorized
        """
        recipe = self.repository.get_recipe_by_id(tenant_id, recipe_id)
        if not recipe:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        return RecipeResponse.from_orm(recipe)
    
    def list_recipes(
        self,
        tenant_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[RecipeResponse]:
        """List recipes for a tenant with pagination.
        
        Args:
            tenant_id: ID of the tenant
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of RecipeResponse schemas
        """
        recipes = self.repository.find_all_by_tenant(tenant_id, skip, limit)
        return [RecipeResponse.from_orm(r) for r in recipes]
    
    def update_recipe(
        self,
        tenant_id: str,
        recipe_id: str,
        data: RecipeUpdate
    ) -> RecipeResponse:
        """Update a recipe with validation.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            data: RecipeUpdate schema with validated data
            
        Returns:
            RecipeResponse schema with updated data
            
        Raises:
            RecipeNotFound: If recipe not found
            RecipeNameAlreadyExists: If new name already exists
        """
        # Get existing recipe
        existing = self.repository.get_recipe_by_id(tenant_id, recipe_id)
        if not existing:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        
        # Validate unique name if being updated
        if data.name and data.name != existing.name:
            conflict = self.repository.find_by_tenant_and_name(tenant_id, data.name)
            if conflict:
                raise RecipeNameAlreadyExists(
                    f"Recipe name '{data.name}' already exists in your tenant"
                )
        
        # Update via repository
        updates = {}
        if data.name is not None:
            updates['name'] = data.name
        if data.description is not None:
            updates['description'] = data.description
        
        updated = self.repository.update_recipe(tenant_id, recipe_id, **updates)
        return RecipeResponse.from_orm(updated)
    
    def delete_recipe(
        self,
        tenant_id: str,
        recipe_id: str
    ) -> bool:
        """Delete a recipe with cascading deletion of ingredients.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            
        Returns:
            True if deleted
            
        Raises:
            RecipeNotFound: If recipe not found
        """
        # Verify recipe exists
        existing = self.repository.get_recipe_by_id(tenant_id, recipe_id)
        if not existing:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        
        # Delete via repository (cascade handles ingredients)
        return self.repository.delete_recipe(tenant_id, recipe_id)
    
    # ===== INGREDIENT METHODS (Tasks 4.1-4.7) =====
    
    def add_ingredient(
        self,
        tenant_id: str,
        recipe_id: str,
        data: RecipeIngredientCreate
    ) -> RecipeIngredientResponse:
        """Add an ingredient to a recipe with validation.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            data: RecipeIngredientCreate schema
            
        Returns:
            RecipeIngredientResponse schema
            
        Raises:
            RecipeNotFound: If recipe not found
            RawMaterialNotFound: If raw material not found or not in tenant
        """
        # Verify recipe exists in tenant
        recipe = self.repository.get_recipe_by_id(tenant_id, recipe_id)
        if not recipe:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        
        # Validate raw material exists in same tenant (Task 4.6)
        if not self.repository.verify_raw_material_in_tenant(tenant_id, data.raw_material_id):
            raise RawMaterialNotFound(
                f"Raw material {data.raw_material_id} not found or not in your tenant"
            )
        
        # Validate quantity > 0 (Task 4.7)
        if data.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        # Generate UUID for ingredient
        ingredient_id = str(uuid.uuid4())
        
        # Add via repository
        ingredient = self.repository.add_ingredient(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            raw_material_id=data.raw_material_id,
            quantity=data.quantity,
            unit=data.unit
        )
        
        return RecipeIngredientResponse.from_orm(ingredient)
    
    def get_ingredient(
        self,
        tenant_id: str,
        recipe_id: str,
        ingredient_id: str
    ) -> RecipeIngredientResponse:
        """Get an ingredient from a recipe.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            ingredient_id: ID of the ingredient
            
        Returns:
            RecipeIngredientResponse schema
            
        Raises:
            RecipeNotFound: If recipe not found
            Exception: If ingredient not found
        """
        # Verify recipe exists in tenant
        recipe = self.repository.get_recipe_by_id(tenant_id, recipe_id)
        if not recipe:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        
        # Get ingredient
        ingredient = self.repository.get_ingredient_by_id(recipe_id, ingredient_id)
        if not ingredient:
            raise Exception(f"Ingredient {ingredient_id} not found")
        
        return RecipeIngredientResponse.from_orm(ingredient)
    
    def remove_ingredient(
        self,
        tenant_id: str,
        recipe_id: str,
        ingredient_id: str
    ) -> bool:
        """Remove an ingredient from a recipe.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            ingredient_id: ID of the ingredient
            
        Returns:
            True if deleted
            
        Raises:
            RecipeNotFound: If recipe not found
            Exception: If ingredient not found
        """
        # Verify recipe exists in tenant
        recipe = self.repository.get_recipe_by_id(tenant_id, recipe_id)
        if not recipe:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        
        # Remove via repository
        if not self.repository.remove_ingredient(recipe_id, ingredient_id):
            raise Exception(f"Ingredient {ingredient_id} not found")
        
        return True
    
    def list_ingredients(
        self,
        tenant_id: str,
        recipe_id: str
    ) -> List[RecipeIngredientResponse]:
        """List all ingredients in a recipe.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            
        Returns:
            List of RecipeIngredientResponse schemas
            
        Raises:
            RecipeNotFound: If recipe not found
        """
        # Verify recipe exists in tenant
        recipe = self.repository.get_recipe_by_id(tenant_id, recipe_id)
        if not recipe:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        
        # List ingredients
        ingredients = self.repository.list_ingredients(recipe_id)
        return [RecipeIngredientResponse.from_orm(i) for i in ingredients]
    
    def update_ingredient(
        self,
        tenant_id: str,
        recipe_id: str,
        ingredient_id: str,
        data: RecipeIngredientUpdate
    ) -> RecipeIngredientResponse:
        """Update an ingredient in a recipe.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            ingredient_id: ID of the ingredient
            data: RecipeIngredientUpdate schema
            
        Returns:
            RecipeIngredientResponse schema
            
        Raises:
            RecipeNotFound: If recipe not found
            Exception: If ingredient not found
        """
        # Verify recipe exists in tenant
        recipe = self.repository.get_recipe_by_id(tenant_id, recipe_id)
        if not recipe:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        
        # Get existing ingredient
        existing = self.repository.get_ingredient_by_id(recipe_id, ingredient_id)
        if not existing:
            raise Exception(f"Ingredient {ingredient_id} not found")
        
        # Validate updated quantity if provided
        if data.quantity is not None and data.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        # Update via repository
        updates = {}
        if data.quantity is not None:
            updates['quantity'] = data.quantity
        if data.unit is not None:
            updates['unit'] = data.unit
        
        updated = self.repository.update_ingredient(recipe_id, ingredient_id, **updates)
        return RecipeIngredientResponse.from_orm(updated)
    
    # ===== RECIPE COSTING METHODS (Tasks 5.1-5.8) =====
    
    def calculate_recipe_cost(
        self,
        tenant_id: str,
        recipe_id: str
    ) -> RecipeCostResponse:
        """Calculate total cost of a recipe based on current raw material prices.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            
        Returns:
            RecipeCostResponse with itemized breakdown
            
        Raises:
            RecipeNotFound: If recipe not found
            Exception: If required raw materials are missing
        """
        # Verify recipe exists in tenant (Task 5.1)
        recipe = self.repository.get_recipe_by_id(tenant_id, recipe_id)
        if not recipe:
            raise RecipeNotFound(f"Recipe {recipe_id} not found")
        
        # Fetch ingredients with current costs (Task 5.2)
        ingredients_with_costs = self.repository.get_ingredients_with_costs(recipe_id)
        
        # Build itemized breakdown and calculate totals
        total_cost = Decimal("0.00")
        ingredients_detail = []
        
        for item in ingredients_with_costs:
            ingredient = item['ingredient']
            raw_material = item['raw_material']
            unit_cost = item['unit_cost']
            
            # Handle missing raw material (Task 5.6)
            if not raw_material:
                raise Exception(
                    f"Raw material {ingredient.raw_material_id} referenced in recipe is no longer available"
                )
            
            # Calculate ingredient cost: quantity × unit_cost (Task 5.3)
            ingredient_cost = (ingredient.quantity * unit_cost).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
            
            # Sum to total (Task 5.4)
            total_cost = (total_cost + ingredient_cost).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
            
            # Add to breakdown (Task 5.5)
            ingredients_detail.append(
                RecipeCostDetailItem(
                    raw_material_id=raw_material.id,
                    raw_material_name=raw_material.name,
                    quantity=ingredient.quantity,
                    unit=ingredient.unit,
                    unit_cost=unit_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                    ingredient_total_cost=ingredient_cost
                )
            )
        
        # Handle empty recipe (Task 5.9 per spec)
        if not ingredients_detail:
            total_cost = Decimal("0.00")
        
        # Build response (Task 5.5 & 5.8)
        return RecipeCostResponse(
            total_cost=total_cost,
            currency="USD",
            ingredients=ingredients_detail,
            calculated_at=datetime.utcnow()
        )
    
    def get_recipe_cost_structure(
        self,
        tenant_id: str,
        recipe_id: str
    ) -> RecipeCostResponse:
        """Get recipe cost structure for API response formatting.
        
        This is an alias for calculate_recipe_cost used for clarity in routing.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            
        Returns:
            RecipeCostResponse with full cost breakdown
        """
        return self.calculate_recipe_cost(tenant_id, recipe_id)
