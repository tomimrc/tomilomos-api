"""Health check endpoint for monitoring.

This router provides a health check endpoint that can be used for:
- Kubernetes/container orchestration probes
- Load balancer health checks
- Monitoring systems
"""

from datetime import datetime
from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for monitoring.
    
    This endpoint requires no authentication and returns the current API status.
    
    Returns:
        Dict with status, timestamp, and version
        
    Example:
        GET /api/v1/health
        
        Response:
        {
            "status": "ok",
            "timestamp": "2024-01-15T10:30:45.123456",
            "version": "1.0.0"
        }
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }
