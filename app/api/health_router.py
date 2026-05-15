"""Health check endpoint (no authentication required)."""

from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str


router = APIRouter(tags=["health"])


@router.get("/api/v1/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Health check endpoint.
    
    Returns:
        HealthResponse: Service health status
    """
    return HealthResponse(status="ok")
