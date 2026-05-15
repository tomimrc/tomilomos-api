"""API Router for products endpoints.

This router handles all CRUD operations for products.
All endpoints require authentication (JWT token) and enforce multi-tenant isolation.
"""

from typing import List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.session import get_db
from services.products_service import ProductService
from schemas.products import (
    ProductCreate,
    ProductUpdate,
    ProductRead,
)
from app.core.dependencies import get_tenant_id


router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.post(
    "",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    description="Create a new product (sellable item) in the tenant's catalog."
)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> ProductRead:
    """Create a new product.
    
    Args:
        data: ProductCreate schema with name, sale_price, and optional is_active
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        ProductRead: Created product with id and timestamps
        
    Raises:
        HTTPException: 400 if validation fails, 401 if unauthorized
    """
    service = ProductService(db)
    try:
        result = service.create_product(tenant_id, data)
        db.commit()
        return result
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create product")


@router.get(
    "",
    response_model=List[ProductRead],
    summary="List products",
    description="Retrieve all products for the tenant with pagination support."
)
def list_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> List[ProductRead]:
    """List products for the tenant.
    
    Args:
        skip: Pagination offset
        limit: Pagination limit
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        List[ProductRead]: List of products
    """
    service = ProductService(db)
    return service.list_products(tenant_id, skip, limit)


@router.get(
    "/{product_id}",
    response_model=ProductRead,
    summary="Get a product",
    description="Retrieve a specific product by ID."
)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> ProductRead:
    """Get a single product by ID.
    
    Args:
        product_id: ID of the product
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        ProductRead: Product data
        
    Raises:
        HTTPException: 404 if not found
    """
    service = ProductService(db)
    result = service.get_product(tenant_id, product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@router.put(
    "/{product_id}",
    response_model=ProductRead,
    summary="Update a product",
    description="Update fields of a product (name, sale_price, is_active)."
)
def update_product(
    product_id: str,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> ProductRead:
    """Update a product.
    
    Args:
        product_id: ID of the product
        data: ProductUpdate schema with fields to update (partial updates supported)
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        ProductRead: Updated product data
        
    Raises:
        HTTPException: 400 if validation fails, 404 if not found
    """
    service = ProductService(db)
    try:
        result = service.update_product(tenant_id, product_id, data)
        if not result:
            raise HTTPException(status_code=404, detail="Product not found")
        db.commit()
        return result
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update product")


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product",
    description="Delete a specific product by ID."
)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> None:
    """Delete a product.
    
    Args:
        product_id: ID of the product
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Raises:
        HTTPException: 404 if not found
    """
    service = ProductService(db)
    deleted = service.delete_product(tenant_id, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    db.commit()
