"""Custom application exceptions with HTTP status codes."""

from typing import Optional


class ApplicationException(Exception):
    """Base exception for all application errors."""
    
    http_status_code: int = 500
    message: str = "Internal server error"
    
    def __init__(self, message: Optional[str] = None):
        """Initialize exception with optional message override."""
        if message:
            self.message = message
        super().__init__(self.message)


class InvalidCredentialsError(ApplicationException):
    """Raised when login credentials are invalid (email/password mismatch)."""
    
    http_status_code = 401
    message = "Invalid credentials"


class TenantNotFoundError(ApplicationException):
    """Raised when tenant is not found."""
    
    http_status_code = 404
    message = "Tenant not found"


class UserNotFoundError(ApplicationException):
    """Raised when user is not found."""
    
    http_status_code = 404
    message = "User not found"


class InvalidTokenError(ApplicationException):
    """Raised when JWT token signature is invalid."""
    
    http_status_code = 401
    message = "Invalid token"


class ExpiredTokenError(ApplicationException):
    """Raised when JWT token has expired."""
    
    http_status_code = 401
    message = "Token has expired"


class DuplicateEmailError(ApplicationException):
    """Raised when email already exists in tenant."""
    
    http_status_code = 409
    message = "Email already exists"


class AuthenticationError(ApplicationException):
    """Raised when authentication fails (missing/invalid token)."""
    
    http_status_code = 401
    message = "Authentication required"


class AuthorizationError(ApplicationException):
    """Raised when user lacks permissions."""
    
    http_status_code = 403
    message = "Insufficient permissions"


class ProductNotFoundError(ApplicationException):
    """Raised when a product is not found in the tenant."""
    
    http_status_code = 404
    message = "Product not found"


class RecipeNotFoundError(ApplicationException):
    """Raised when a recipe is not found or is unavailable for costing."""
    
    http_status_code = 424
    message = "Recipe not found or unavailable"


class RawMaterialNotFoundError(ApplicationException):
    """Raised when a raw material referenced in a recipe is not found."""
    
    http_status_code = 424
    message = "Raw material not found"
