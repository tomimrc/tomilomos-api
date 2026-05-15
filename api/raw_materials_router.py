"""API Router for raw materials endpoints.

This router handles all CRUD operations for raw materials and stock management.
All endpoints require authentication (JWT token) and enforce multi-tenant isolation.
"""

from typing import List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.session import get_db
from services.raw_materials_service import RawMaterialService
from schemas.raw_materials import (
    RawMaterialCreate,
    RawMaterialUpdate,
    RawMaterialRead,
    StockAdjustmentRequest,
    StockLevel,
)
from app.core.dependencies import get_tenant_id


router = APIRouter(prefix="/api/v1/raw-materials", tags=["Raw Materials"])


@router.post(
    "",
    response_model=RawMaterialRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new raw material",
    description="Create a new raw material (ingredient) in the tenant's inventory."
)
def create_raw_material(
    data: RawMaterialCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RawMaterialRead:
    """Create a new raw material.
    
    Args:
        data: RawMaterialCreate schema with name, unit, cost, and optional supplier
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RawMaterialRead: Created raw material with id and timestamps
        
    Raises:
        HTTPException: 400 if validation fails, 401 if unauthorized
    """
    service = RawMaterialService(db)
    try:
        result = service.create_raw_material(tenant_id, data)
        db.commit()
        return result
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create raw material")


@router.get(
    "",
    response_model=List[RawMaterialRead],
    summary="List raw materials",
    description="Retrieve all raw materials for the tenant with pagination support."
)
def list_raw_materials(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> List[RawMaterialRead]:
    """List raw materials for the tenant.
    
    Args:
        skip: Pagination offset
        limit: Pagination limit
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        List[RawMaterialRead]: List of raw materials
    """
    service = RawMaterialService(db)
    return service.list_raw_materials(tenant_id, skip, limit)


@router.get(
    "/{raw_material_id}",
    response_model=RawMaterialRead,
    summary="Get a raw material",
    description="Retrieve a specific raw material by ID."
)
def get_raw_material(
    raw_material_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RawMaterialRead:
    """Get a single raw material by ID.
    
    Args:
        raw_material_id: ID of the raw material
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RawMaterialRead: Raw material data
        
    Raises:
        HTTPException: 404 if not found
    """
    service = RawMaterialService(db)
    result = service.get_raw_material(tenant_id, raw_material_id)
    if not result:
        raise HTTPException(status_code=404, detail="Raw material not found")
    return result


@router.put(
    "/{raw_material_id}",
    response_model=RawMaterialRead,
    summary="Update a raw material",
    description="Update fields of a raw material (name, unit, cost, supplier)."
)
def update_raw_material(
    raw_material_id: str,
    data: RawMaterialUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RawMaterialRead:
    """Update a raw material.
    
    Args:
        raw_material_id: ID of the raw material
        data: RawMaterialUpdate schema with fields to update
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RawMaterialRead: Updated raw material
        
    Raises:
        HTTPException: 400 if validation fails, 404 if not found
    """
    service = RawMaterialService(db)
    try:
        result = service.update_raw_material(tenant_id, raw_material_id, data)
        if not result:
            raise HTTPException(status_code=404, detail="Raw material not found")
        db.commit()
        return result
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update raw material")


@router.delete(
    "/{raw_material_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a raw material",
    description="Delete a raw material permanently."
)
def delete_raw_material(
    raw_material_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
):
    """Delete a raw material.
    
    Args:
        raw_material_id: ID of the raw material
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Raises:
        HTTPException: 404 if not found
    """
    service = RawMaterialService(db)
    try:
        success = service.delete_raw_material(tenant_id, raw_material_id)
        if not success:
            raise HTTPException(status_code=404, detail="Raw material not found")
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete raw material")


@router.post(
    "/{raw_material_id}/add-stock",
    response_model=RawMaterialRead,
    summary="Add stock",
    description="Add stock to a raw material (e.g., receive purchase)."
)
def add_stock(
    raw_material_id: str,
    request: StockAdjustmentRequest,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RawMaterialRead:
    """Add stock to a raw material.
    
    Args:
        raw_material_id: ID of the raw material
        request: StockAdjustmentRequest with quantity and optional reason
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RawMaterialRead: Updated raw material
        
    Raises:
        HTTPException: 400 if validation fails, 404 if not found
    """
    service = RawMaterialService(db)
    try:
        result = service.add_stock(
            tenant_id,
            raw_material_id,
            request.quantity,
            request.reason
        )
        if not result:
            raise HTTPException(status_code=404, detail="Raw material not found")
        db.commit()
        return result
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add stock")


@router.post(
    "/{raw_material_id}/remove-stock",
    response_model=RawMaterialRead,
    summary="Remove stock",
    description="Remove stock from a raw material (e.g., deduct for sale or recipe)."
)
def remove_stock(
    raw_material_id: str,
    request: StockAdjustmentRequest,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> RawMaterialRead:
    """Remove stock from a raw material.
    
    Args:
        raw_material_id: ID of the raw material
        request: StockAdjustmentRequest with quantity and optional reason
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        RawMaterialRead: Updated raw material
        
    Raises:
        HTTPException: 400 if validation fails (quantity invalid or insufficient stock), 404 if not found
    """
    service = RawMaterialService(db)
    try:
        result = service.remove_stock(
            tenant_id,
            raw_material_id,
            request.quantity,
            request.reason
        )
        if not result:
            raise HTTPException(status_code=404, detail="Raw material not found")
        db.commit()
        return result
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to remove stock")


@router.get(
    "/{raw_material_id}/stock",
    response_model=StockLevel,
    summary="Get stock level",
    description="Retrieve only the current stock level of a raw material."
)
def get_stock_level(
    raw_material_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> StockLevel:
    """Get the current stock level.
    
    Args:
        raw_material_id: ID of the raw material
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        StockLevel: Current stock level
        
    Raises:
        HTTPException: 404 if not found
    """
    service = RawMaterialService(db)
    stock = service.get_stock(tenant_id, raw_material_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="Raw material not found")
    
    return StockLevel(id=raw_material_id, current_stock=stock)
