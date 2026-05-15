"""Tests for the configuration module."""

import os
import pytest
from pydantic import ValidationError


def test_config_loads_from_env():
    """Test that config loads from environment variables."""
    from core.config import Settings
    
    # Create instance with environment variables
    config = Settings()
    
    assert config.database_url
    assert config.jwt_secret
    assert config.jwt_algorithm == "HS256"
    assert config.bcrypt_cost == 10  # Test env set to 10


def test_config_database_url_required():
    """Test that config raises error if DATABASE_URL is missing."""
    # Temporarily clear DATABASE_URL
    old_db_url = os.environ.get("DATABASE_URL")
    if "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]
    
    try:
        from importlib import reload
        import core.config
        reload(core.config)
        
        with pytest.raises(ValidationError):
            from core.config import Settings
            Settings()
    finally:
        # Restore
        if old_db_url:
            os.environ["DATABASE_URL"] = old_db_url


def test_config_jwt_secret_required():
    """Test that config raises error if JWT_SECRET is missing."""
    old_jwt_secret = os.environ.get("JWT_SECRET")
    if "JWT_SECRET" in os.environ:
        del os.environ["JWT_SECRET"]
    
    try:
        from importlib import reload
        import core.config
        reload(core.config)
        
        with pytest.raises(ValidationError):
            from core.config import Settings
            Settings()
    finally:
        # Restore
        if old_jwt_secret:
            os.environ["JWT_SECRET"] = old_jwt_secret


def test_config_bcrypt_cost_validation():
    """Test that BCRYPT_COST must be between 10 and 31."""
    # Test valid value (already set to 10)
    from core.config import settings
    assert 10 <= settings.bcrypt_cost <= 31
    
    # Test invalid values using direct Settings
    from core.config import Settings
    with pytest.raises(ValidationError):
        Settings(
            database_url="postgresql://test",
            jwt_secret="test_secret",
            bcrypt_cost=5,  # Too low
        )
    
    with pytest.raises(ValidationError):
        Settings(
            database_url="postgresql://test",
            jwt_secret="test_secret",
            bcrypt_cost=32,  # Too high
        )
