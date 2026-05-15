"""FastAPI application entry point."""

import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import auth_router, tenants_router, users_router, health_router
from app.core.exceptions import ApplicationException
from app.db.base import Base, engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Tomilomos API",
    description="Multi-tenant SaaS API for gastronomic business management",
    version="0.1.0",
)

# Configure CORS
if os.getenv("ENVIRONMENT") != "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(auth_router.router)
app.include_router(tenants_router.router)
app.include_router(users_router.router)
app.include_router(health_router.router)


# Exception handlers
@app.exception_handler(ApplicationException)
async def application_exception_handler(request, exc: ApplicationException):
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.http_status_code,
        content={"detail": exc.message},
    )


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Tomilomos API - Multi-tenant Authentication System"}


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Tomilomos API starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Tomilomos API shutting down")


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENVIRONMENT") != "production",
    )
