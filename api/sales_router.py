"""API Router for sales endpoints.

This router handles sale registration with automatic stock deduction,
sale listing with pagination, and individual sale retrieval.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.session import get_db
from services.sales_service import SaleService
from schemas.sales import SaleCreate, SaleRead
from app.core.dependencies import get_tenant_id


router = APIRouter(prefix="/api/v1/sales", tags=["Sales"])


@router.post(
    "",
    response_model=SaleRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new sale",
    description="Register a sale and automatically deduct raw material stock via recipe ingredients."
)
def create_sale(
    data: SaleCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> SaleRead:
    """Register a new sale.
    
    Args:
        data: SaleCreate schema with product_id and quantity
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        SaleRead: Created sale with pricing, cost, and margin
        
    Raises:
        HTTPException: 400 if product not found, inactive, or stock insufficient
                      401 if unauthorized
                      500 if unexpected error
    """
    service = SaleService(db)
    try:
        result = service.create_sale(tenant_id, data)
        db.commit()
        return result
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to register sale")


@router.get(
    "",
    response_model=List[SaleRead],
    summary="List sales",
    description="Retrieve all sales for the tenant with pagination, newest first."
)
def list_sales(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> List[SaleRead]:
    """List sales for the tenant.
    
    Args:
        skip: Pagination offset
        limit: Pagination limit
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        List[SaleRead]: List of sales, newest first
    """
    service = SaleService(db)
    return service.list_sales(tenant_id, skip, limit)


@router.get(
    "/{sale_id}",
    response_model=SaleRead,
    summary="Get a sale",
    description="Retrieve a specific sale by ID."
)
def get_sale(
    sale_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Depends(get_tenant_id),
) -> SaleRead:
    """Get a single sale by ID.
    
    Args:
        sale_id: ID of the sale
        db: Database session
        tenant_id: Tenant ID from JWT token
        
    Returns:
        SaleRead: Sale data with product name
        
    Raises:
        HTTPException: 404 if not found
    """
    service = SaleService(db)
    result = service.get_sale(tenant_id, sale_id)
    if not result:
        raise HTTPException(status_code=404, detail="Sale not found")
    return result
