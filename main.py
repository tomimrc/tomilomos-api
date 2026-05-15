"""TomiLomos API - FastAPI application entry point.

This module creates the FastAPI application instance, configures middleware,
exception handlers, and registers all API routers.

The app is production-ready with:
- CORS middleware
- Request logging
- Exception handling
- Health check endpoint
"""

from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid

from core.config import settings
from core.logging import logger
from core.exceptions import APIException
from api import health_router
from api import raw_materials_router
from api import products_router
from api import product_cost_router
from api import sales_router
from api.recipes_router import router as recipes_router
from app.api import auth_router



# Middleware to add request ID for tracing
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup/shutdown events."""
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="Tomilomos API",
        description="Multi-tenant business management system for gastronomy",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.include_router(recipes_router, prefix="/api/v1/recipes", tags=["Recipes"])
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request ID Middleware for tracing
    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        """Add unique request ID to each request for tracing."""
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        logger.info(
            f"HTTP {request.method} {request.url.path}",
            extra={"request_id": request_id, "status_code": response.status_code},
        )
        return response

    # Exception Handlers
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        """Handle custom APIException and return JSON response."""
        return JSONResponse(
            status_code=exc.http_status_code,
            content=exc.detail_dict(),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Catch-all exception handler for unexpected errors."""
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "status_code": 500,
            },
        )

    # Register routers
    app.include_router(health_router.router)
    app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth"])
    app.include_router(raw_materials_router.router)
    app.include_router(products_router.router)
    app.include_router(product_cost_router.router)
    app.include_router(sales_router.router)

    return app


# Create app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True,
    )
