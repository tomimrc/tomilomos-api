"""Tenant management API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.tenant import TenantCreate, TenantResponse
from app.services.auth_service import AuthService
from app.db.session import get_db

router = APIRouter(prefix="/api/v1/tenants", tags=["tenants"])


@router.post("", response_model=TenantResponse)
def create_tenant(
    request: TenantCreate,
    db: Session = Depends(get_db),
) -> TenantResponse:
    """Create a new tenant.
    
    Args:
        request: TenantCreate with name
        db: Database session
        
    Returns:
        TenantResponse: Created tenant
    """
    auth_service = AuthService(db)
    tenant = auth_service.create_tenant(request.name)
    return TenantResponse(
        id=str(tenant.id),
        name=tenant.name,
        created_at=tenant.created_at,
    )
