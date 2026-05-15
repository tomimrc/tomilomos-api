"""API Router for product cost calculation endpoint.

This router provides the `/api/v1/products/{id}/cost` endpoint for calculating
product costs based on recipe-based or manual pricing modes.

All endpoints require authentication (JWT token) and enforce multi-tenant isolation.
"""

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from app.services.product_cost_service import ProductCostService
from core.exceptions import (
    ProductNotFoundError,
    RecipeNotFoundError,
    RawMaterialNotFoundError,
    APIException,
)
from app.core.dependencies import get_tenant_id


router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.get(
    "/{product_id}/cost",
    summary="Calculate product cost",
    description="Calculate the total cost of a product based on recipe-based or manual pricing mode.",
    responses={
        200: {
            "description": "Product cost calculated successfully",
            "content": {
                "application/json": {
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
                            }
                        ],
                        "calculated_at": "2025-05-13T14:30:00Z"
                    }
                }
            }
        },
        404: {
            "description": "Product not found (respects multi-tenancy)"
        },
        424: {
            "description": "Failed dependency - recipe or raw material missing"
        },
        401: {
            "description": "Unauthorized - invalid or missing JWT token"
        },
    }
)
def get_product_cost(
    product_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> dict:
    """Get the calculated cost of a product.
    
    Supports two pricing modes:
    1. **Recipe-based**: Product linked to recipe → cost calculated from ingredient costs
    2. **Manual**: Product not linked → cost_source = "manual" (no calculation)
    
    Args:
        product_id: UUID of the product
        db: Database session
        tenant_id: Tenant ID from JWT token (enforces multi-tenant isolation)
        
    Returns:
        dict: Cost response with total_cost, cost_source, ingredients (if recipe-based), and calculated_at
        
    Raises:
        HTTPException: 
            - 400 if product_id is invalid UUID format
            - 401 if unauthorized
            - 404 if product not found or belongs to different tenant
            - 424 if recipe or raw material is missing/deleted (failed dependency)
        
    Examples:
        **Recipe-based product:**
        ```
        GET /api/v1/products/550e8400-e29b-41d4-a716-446655440000/cost
        
        Response (200):
        {
            "product_id": "550e8400-e29b-41d4-a716-446655440000",
            "total_cost": "45.99",
            "currency": "USD",
            "cost_source": "recipe",
            "ingredients": [
                {
                    "raw_material_id": "...",
                    "raw_material_name": "tomatoes",
                    "quantity": "2.5",
                    "unit": "kg",
                    "unit_cost": "12.50",
                    "ingredient_total_cost": "31.25"
                }
            ],
            "calculated_at": "2025-05-13T14:30:00Z"
        }
        ```
        
        **Manual pricing product:**
        ```
        GET /api/v1/products/550e8400-e29b-41d4-a716-446655440001/cost
        
        Response (200):
        {
            "product_id": "550e8400-e29b-41d4-a716-446655440001",
            "total_cost": "0.00",
            "currency": "USD",
            "cost_source": "manual",
            "ingredients": null,
            "calculated_at": "2025-05-13T14:31:00Z"
        }
        ```
    """
    try:
        # Validate UUID format
        try:
            product_uuid = UUID(product_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid product ID format: {product_id}. Expected UUID."
            )
        
        # Convert tenant_id to UUID as well
        try:
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid tenant ID format. Expected UUID."
            )
        
        # Calculate product cost
        service = ProductCostService(db)
        cost_response = service.calculate_product_cost(product_uuid, tenant_uuid)
        
        # Convert Decimal values to strings for JSON serialization
        cost_response = _serialize_decimals(cost_response)
        
        return cost_response
        
    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=e.http_status_code,
            detail=e.message
        )
    except RecipeNotFoundError as e:
        raise HTTPException(
            status_code=e.http_status_code,
            detail=e.message
        )
    except RawMaterialNotFoundError as e:
        raise HTTPException(
            status_code=e.http_status_code,
            detail=e.message
        )
    except APIException as e:
        raise HTTPException(
            status_code=e.http_status_code,
            detail=e.message
        )
    except Exception as e:
        # Log unexpected errors and return 500
        raise HTTPException(
            status_code=500,
            detail="Failed to calculate product cost"
        )


def _serialize_decimals(obj: dict) -> dict:
    """Recursively convert Decimal values to strings for JSON serialization.
    
    Args:
        obj: Dictionary (possibly nested) with Decimal values
        
    Returns:
        dict: Same structure with Decimals converted to strings
    """
    if isinstance(obj, dict):
        return {k: _serialize_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_serialize_decimals(item) for item in obj]
    elif isinstance(obj, Decimal):
        return str(obj)
    else:
        return obj
