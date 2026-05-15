"""JWT token generation and validation using python-jose."""

import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any

from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError


class JWTConfig:
    """JWT configuration from environment."""
    
    SECRET_KEY = os.getenv("JWT_SECRET")
    ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    @classmethod
    def validate(cls) -> None:
        """Validate required JWT configuration."""
        if not cls.SECRET_KEY:
            raise ValueError("JWT_SECRET environment variable is required")
        if not cls.SECRET_KEY or len(cls.SECRET_KEY) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters")


def create_access_token(user_id: str, tenant_id: str) -> str:
    """Create a JWT access token.
    
    Args:
        user_id: User UUID
        tenant_id: Tenant UUID
        
    Returns:
        str: JWT token signed with HS256
        
    Token payload includes:
        - sub: user_id
        - tenant_id: tenant UUID
        - exp: expiration (24 hours from now)
        - iat: issued at
        - jti: unique token ID
    """
    JWTConfig.validate()
    
    now = datetime.utcnow()
    expiration = now + timedelta(hours=JWTConfig.EXPIRATION_HOURS)
    
    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "exp": expiration,
        "iat": now,
        "jti": str(uuid.uuid4()),  # Unique token ID
    }
    
    token = jwt.encode(
        payload,
        JWTConfig.SECRET_KEY,
        algorithm=JWTConfig.ALGORITHM,
    )
    
    return token


def validate_token(token: str) -> Dict[str, Any]:
    """Validate and decode a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Dict: Decoded token payload
        
    Raises:
        InvalidTokenError: If token signature is invalid
        ExpiredTokenError: If token has expired
    """
    JWTConfig.validate()
    
    try:
        payload = jwt.decode(
            token,
            JWTConfig.SECRET_KEY,
            algorithms=[JWTConfig.ALGORITHM],
        )
        return payload
    except ExpiredSignatureError:
        raise ExpiredTokenError("Token has expired")
    except JWTError as e:
        raise InvalidTokenError(f"Invalid token: {str(e)}")


class InvalidTokenError(Exception):
    """Raised when token signature is invalid."""
    pass


class ExpiredTokenError(Exception):
    """Raised when token has expired."""
    pass
