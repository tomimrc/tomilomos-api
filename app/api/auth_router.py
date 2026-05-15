"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.core.exceptions import InvalidCredentialsError, UserNotFoundError

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Login user and return JWT token.
    
    Args:
        request: LoginRequest with email and password
        db: Database session
        
    Returns:
        TokenResponse: JWT access token
        
    Raises:
        HTTPException: 401 if credentials invalid or user not found
    """
    auth_service = AuthService(db)
    
    try:
        _, token_response = auth_service.login(request.email, request.password)
        return token_response
    except (UserNotFoundError, InvalidCredentialsError):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
