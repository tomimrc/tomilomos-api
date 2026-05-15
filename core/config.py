"""Configuration module for TomiLomos API.

This module reads and validates environment variables at startup using Pydantic BaseSettings.
All environment-specific settings (DATABASE_URL, JWT_SECRET, etc.) must be defined here.

Raises:
    ValueError: If required environment variables are missing or invalid.
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator, model_validator


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Database
    database_url: str
    """PostgreSQL connection string. Required. Format: postgresql://user:password@host:port/dbname"""

    # JWT
    jwt_secret: str
    """Secret key for JWT signing. Required. Must be a strong random string."""
    jwt_algorithm: str = "HS256"
    """JWT algorithm. Default: HS256"""
    jwt_expiration_hours: int = 24
    """JWT token expiration time in hours. Default: 24"""

    # Security
    bcrypt_cost: int = 12
    """bcrypt hashing cost factor. Default: 12. Must be between 10 and 31."""

    # Server
    port: int = 8000
    """Server port. Default: 8000"""
    log_level: str = "INFO"
    """Logging level. Default: INFO. Options: DEBUG, INFO, WARNING, ERROR, CRITICAL"""

    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]
    """Allowed CORS origins. Default: [\"http://localhost:3000\"]"""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate DATABASE_URL is not empty."""
        if not v or not v.strip():
            raise ValueError("DATABASE_URL environment variable is required and must not be empty")
        return v

    @field_validator("jwt_secret")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """Validate JWT_SECRET is not empty."""
        if not v or not v.strip():
            raise ValueError("JWT_SECRET environment variable is required and must not be empty")
        return v

    @field_validator("bcrypt_cost")
    @classmethod
    def validate_bcrypt_cost(cls, v: int) -> int:
        """Validate BCRYPT_COST is within valid range [10, 31]."""
        if not (10 <= v <= 31):
            raise ValueError(f"BCRYPT_COST must be between 10 and 31, got {v}")
        return v

    @model_validator(mode="after")
    def validate_settings(self) -> "Settings":
        """Cross-field validation if needed."""
        # Add any cross-field validation logic here
        return self


# Global settings instance
settings = Settings()
