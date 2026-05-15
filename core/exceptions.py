"""Custom exception classes for TomiLomos API.

All custom exceptions inherit from APIException and include an HTTP status code.
Exception handlers in main.py convert these to proper JSON responses.
"""

from typing import Any, Dict, Optional


class APIException(Exception):
    """Base exception class for all API errors.
    
    Attributes:
        message: Human-readable error message
        http_status_code: HTTP status code to return
        detail: Additional error details or context
    """

    def __init__(
        self,
        message: str,
        http_status_code: int = 500,
        detail: Optional[Dict[str, Any]] = None,
    ):
        """Initialize APIException.
        
        Args:
            message: Error message
            http_status_code: HTTP status code (default: 500)
            detail: Additional error details
        """
        self.message = message
        self.http_status_code = http_status_code
        self.detail = detail or {}
        super().__init__(self.message)

    def detail_dict(self) -> Dict[str, Any]:
        """Return error details as a dictionary.
        
        Returns:
            Dict with error information
        """
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "status_code": self.http_status_code,
            **self.detail,
        }


class InvalidCredentialsError(APIException):
    """Raised when login credentials are invalid."""

    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(
            message=message,
            http_status_code=401,
            detail={"error_type": "invalid_credentials"},
        )


class TenantNotFoundError(APIException):
    """Raised when a tenant is not found."""

    def __init__(self, tenant_id: str):
        super().__init__(
            message=f"Tenant '{tenant_id}' not found",
            http_status_code=404,
            detail={"error_type": "tenant_not_found", "tenant_id": tenant_id},
        )


class UserNotFoundError(APIException):
    """Raised when a user is not found."""

    def __init__(self, user_id: str):
        super().__init__(
            message=f"User '{user_id}' not found",
            http_status_code=404,
            detail={"error_type": "user_not_found", "user_id": user_id},
        )


class UnauthorizedError(APIException):
    """Raised when a request is unauthorized."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            http_status_code=401,
            detail={"error_type": "unauthorized"},
        )


class ForbiddenError(APIException):
    """Raised when a request is forbidden."""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message,
            http_status_code=403,
            detail={"error_type": "forbidden"},
        )


class ValidationError(APIException):
    """Raised when request validation fails."""

    def __init__(self, message: str, fields: Optional[Dict[str, str]] = None):
        super().__init__(
            message=message,
            http_status_code=422,
            detail={"error_type": "validation_error", "fields": fields or {}},
        )


class ConflictError(APIException):
    """Raised when a resource already exists (conflict)."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            http_status_code=409,
            detail={"error_type": "conflict"},
        )


class InternalServerError(APIException):
    """Raised for unexpected server errors."""

    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            message=message,
            http_status_code=500,
            detail={"error_type": "internal_server_error"},
        )


class ProductNotFoundError(APIException):
    """Raised when a product is not found."""

    def __init__(self, message: str = "Product not found"):
        super().__init__(
            message=message,
            http_status_code=404,
            detail={"error_type": "product_not_found"},
        )


class RecipeNotFoundError(APIException):
    """Raised when a recipe is not found or is unavailable for costing."""

    def __init__(self, message: str = "Recipe not found or unavailable"):
        super().__init__(
            message=message,
            http_status_code=424,
            detail={"error_type": "recipe_not_found"},
        )


class RawMaterialNotFoundError(APIException):
    """Raised when a raw material referenced in a recipe is not found."""

    def __init__(self, message: str = "Raw material not found"):
        super().__init__(
            message=message,
            http_status_code=424,
            detail={"error_type": "raw_material_not_found"},
        )


class DuplicateEmailError(APIException):
    """Raised when attempting to create a user with duplicate email."""

    def __init__(self, message: str = "Email already exists"):
        super().__init__(
            message=message,
            http_status_code=409,
            detail={"error_type": "duplicate_email"},
        )
