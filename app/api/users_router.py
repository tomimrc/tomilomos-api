"""User management API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.db.session import get_db
from app.core.exceptions import DuplicateEmailError

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("", response_model=UserResponse)
def create_user(
    request: UserCreate,
    tenant_id: str,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Create a new user in a tenant.
    
    Args:
        request: UserCreate with email and password
        tenant_id: Tenant UUID (should come from auth context in Phase 2)
        db: Database session
        
    Returns:
        UserResponse: Created user
        
    Raises:
        HTTPException: 409 if email already exists in tenant
    """
    auth_service = AuthService(db)
    
    try:
        user = auth_service.create_user(request.email, request.password, tenant_id)
        return UserResponse(
            id=str(user.id),
            email=user.email,
            created_at=user.created_at,
        )
    except DuplicateEmailError as e:
        raise HTTPException(status_code=409, detail=str(e))
