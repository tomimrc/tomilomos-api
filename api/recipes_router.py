"""API Router for recipes endpoints.

This router handles all CRUD operations for recipes and recipe ingredients.
All endpoints require authentication (JWT token) and enforce multi-tenant isolation.
"""

from typing import List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.session import get_db
from services.recipe_service import (
    RecipeService,
    RecipeNotFound,
    RecipeNameAlreadyExists,
    RawMaterialNotFound,
)
from schemas.recipes import (
    RecipeCreate,
    RecipeUpdate,
    RecipeResponse,
    RecipeIngredientCreate,
    RecipeIngredientUpdate,
    RecipeIngredientResponse,
    RecipeCostResponse,
)
from app.core.dependencies import get_tenant_id


router = APIRouter(prefix="/api/v1/recipes", tags=["Recipes"])


# ===== RECIPE CRUD ENDPOINTS (Tasks 6.1-6.7) =====

@router.post(
    "",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new recipe",
    description="Create a new recipe with name and optional description."
)
def create_recipe(
    data: RecipeCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RecipeResponse:
    """Create a new recipe.
    
    Args:
        data: RecipeCreate schema with name and optional description
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RecipeResponse: Created recipe with id and timestamps
        
    Raises:
        HTTPException: 400 if validation fails, 409 if name exists, 401 if unauthorized
    """
    service = RecipeService(db)
    try:
        result = service.create_recipe(tenant_id, data)
        db.commit()
        return result
    except RecipeNameAlreadyExists as e:
        db.rollback()
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create recipe")


@router.get(
    "",
    response_model=List[RecipeResponse],
    summary="List recipes",
    description="Retrieve all recipes for the tenant with pagination support."
)
def list_recipes(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> List[RecipeResponse]:
    """List recipes for the tenant.
    
    Args:
        skip: Pagination offset
        limit: Pagination limit
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        List of RecipeResponse schemas (may be empty)
    """
    service = RecipeService(db)
    try:
        return service.list_recipes(tenant_id, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to list recipes")


@router.get(
    "/{recipe_id}",
    response_model=RecipeResponse,
    summary="Get a specific recipe",
    description="Retrieve a single recipe by ID."
)
def get_recipe(
    recipe_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RecipeResponse:
    """Get a recipe by ID.
    
    Args:
        recipe_id: ID of the recipe
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RecipeResponse: The recipe data
        
    Raises:
        HTTPException: 404 if recipe not found or unauthorized
    """
    service = RecipeService(db)
    try:
        return service.get_recipe(tenant_id, recipe_id)
    except RecipeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get recipe")


@router.put(
    "/{recipe_id}",
    response_model=RecipeResponse,
    summary="Update a recipe",
    description="Update recipe name or description."
)
def update_recipe(
    recipe_id: str,
    data: RecipeUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RecipeResponse:
    """Update a recipe.
    
    Args:
        recipe_id: ID of the recipe
        data: RecipeUpdate schema with fields to update
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RecipeResponse: Updated recipe
        
    Raises:
        HTTPException: 404 if recipe not found, 409 if name conflict, 400 if validation fails
    """
    service = RecipeService(db)
    try:
        result = service.update_recipe(tenant_id, recipe_id, data)
        db.commit()
        return result
    except RecipeNotFound as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    except RecipeNameAlreadyExists as e:
        db.rollback()
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update recipe")


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a recipe",
    description="Delete a recipe and all associated ingredients."
)
def delete_recipe(
    recipe_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
):
    """Delete a recipe.
    
    Args:
        recipe_id: ID of the recipe
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Raises:
        HTTPException: 404 if recipe not found or unauthorized
    """
    service = RecipeService(db)
    try:
        service.delete_recipe(tenant_id, recipe_id)
        db.commit()
    except RecipeNotFound as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete recipe")


# ===== RECIPE INGREDIENT ENDPOINTS (Tasks 7.1-7.6) =====

@router.post(
    "/{recipe_id}/ingredients",
    response_model=RecipeIngredientResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add ingredient to recipe",
    description="Add a raw material ingredient to a recipe with quantity and unit."
)
def add_ingredient(
    recipe_id: str,
    data: RecipeIngredientCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RecipeIngredientResponse:
    """Add an ingredient to a recipe.
    
    Args:
        recipe_id: ID of the recipe
        data: RecipeIngredientCreate schema with raw_material_id, quantity, unit
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RecipeIngredientResponse: Created ingredient
        
    Raises:
        HTTPException: 404 if recipe/material not found, 400 if validation fails
    """
    service = RecipeService(db)
    try:
        result = service.add_ingredient(tenant_id, recipe_id, data)
        db.commit()
        return result
    except (RecipeNotFound, RawMaterialNotFound) as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add ingredient")


@router.get(
    "/{recipe_id}/ingredients",
    response_model=List[RecipeIngredientResponse],
    summary="List ingredients in recipe",
    description="Retrieve all ingredients for a recipe."
)
def list_ingredients(
    recipe_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> List[RecipeIngredientResponse]:
    """List ingredients for a recipe.
    
    Args:
        recipe_id: ID of the recipe
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        List of RecipeIngredientResponse schemas (may be empty)
        
    Raises:
        HTTPException: 404 if recipe not found
    """
    service = RecipeService(db)
    try:
        return service.list_ingredients(tenant_id, recipe_id)
    except RecipeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to list ingredients")


@router.get(
    "/{recipe_id}/ingredients/{ingredient_id}",
    response_model=RecipeIngredientResponse,
    summary="Get a specific ingredient",
    description="Retrieve a single ingredient from a recipe."
)
def get_ingredient(
    recipe_id: str,
    ingredient_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RecipeIngredientResponse:
    """Get an ingredient from a recipe.
    
    Args:
        recipe_id: ID of the recipe
        ingredient_id: ID of the ingredient
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RecipeIngredientResponse: The ingredient data
        
    Raises:
        HTTPException: 404 if recipe or ingredient not found
    """
    service = RecipeService(db)
    try:
        return service.get_ingredient(tenant_id, recipe_id, ingredient_id)
    except RecipeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{recipe_id}/ingredients/{ingredient_id}",
    response_model=RecipeIngredientResponse,
    summary="Update an ingredient",
    description="Update ingredient quantity or unit."
)
def update_ingredient(
    recipe_id: str,
    ingredient_id: str,
    data: RecipeIngredientUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RecipeIngredientResponse:
    """Update an ingredient in a recipe.
    
    Args:
        recipe_id: ID of the recipe
        ingredient_id: ID of the ingredient
        data: RecipeIngredientUpdate schema
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RecipeIngredientResponse: Updated ingredient
        
    Raises:
        HTTPException: 404 if recipe/ingredient not found, 400 if validation fails
    """
    service = RecipeService(db)
    try:
        result = service.update_ingredient(tenant_id, recipe_id, ingredient_id, data)
        db.commit()
        return result
    except RecipeNotFound as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{recipe_id}/ingredients/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove ingredient from recipe",
    description="Delete an ingredient from a recipe."
)
def delete_ingredient(
    recipe_id: str,
    ingredient_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
):
    """Delete an ingredient from a recipe.
    
    Args:
        recipe_id: ID of the recipe
        ingredient_id: ID of the ingredient
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Raises:
        HTTPException: 404 if recipe or ingredient not found
    """
    service = RecipeService(db)
    try:
        service.remove_ingredient(tenant_id, recipe_id, ingredient_id)
        db.commit()
    except RecipeNotFound as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))


# ===== RECIPE COSTING & INTEGRATION ENDPOINTS (Tasks 8.1-8.6) =====

@router.get(
    "/{recipe_id}/cost",
    response_model=RecipeCostResponse,
    summary="Calculate recipe cost",
    description="Calculate the total cost of a recipe based on current raw material prices."
)
def get_recipe_cost(
    recipe_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RecipeCostResponse:
    """Calculate recipe cost.
    
    Args:
        recipe_id: ID of the recipe
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RecipeCostResponse: Total cost with itemized breakdown
        
    Raises:
        HTTPException: 404 if recipe not found, 424 if required materials missing
    """
    service = RecipeService(db)
    try:
        return service.get_recipe_cost_structure(tenant_id, recipe_id)
    except RecipeNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Check if it's a missing raw material (Task 8.1 per spec)
        if "no longer available" in str(e):
            raise HTTPException(status_code=424, detail=str(e))
        raise HTTPException(status_code=500, detail="Failed to calculate recipe cost")
