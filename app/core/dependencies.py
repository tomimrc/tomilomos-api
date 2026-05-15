"""Dependency injection for FastAPI endpoints."""

from typing import Dict, Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredential
from sqlalchemy.orm import Session

from db.session import get_db
from app.core.jwt_handler import validate_token, InvalidTokenError, ExpiredTokenError
from app.core.exceptions import InvalidTokenError as InvalidTokenAppError, ExpiredTokenError as ExpiredTokenAppError


http_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthCredential = Depends(http_bearer),
) -> Dict[str, Any]:
    """Validate JWT token and extract user information.
    
    Args:
        credentials: HTTP Bearer token from request headers
        
    Returns:
        Dict: Decoded token payload with user_id, tenant_id, etc.
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    
    try:
        payload = validate_token(token)
        return payload
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ExpiredTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except InvalidTokenAppError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ExpiredTokenAppError as e:
        raise HTTPException(status_code=401, detail=str(e))


def get_tenant_id(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> str:
    """Extract tenant_id from current user context.
    
    Args:
        current_user: Current user decoded from JWT token
        
    Returns:
        str: Tenant UUID
        
    Raises:
        HTTPException: If tenant_id is not in token
    """
    tenant_id = current_user.get("tenant_id")
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Tenant ID not found in token")
    return tenant_id


def get_user_id(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> str:
    """Extract user_id from current user context.
    
    Args:
        current_user: Current user decoded from JWT token
        
    Returns:
        str: User UUID
        
    Raises:
        HTTPException: If user_id (sub) is not in token
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    return user_id


# Re-export get_db for consistency
__all__ = ["get_db", "get_current_user", "get_tenant_id", "get_user_id"]
