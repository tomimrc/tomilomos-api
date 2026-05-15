"""Tests for JWT token generation and validation."""

import pytest
import os
import uuid
import time
from datetime import datetime, timedelta

# Set environment variables before importing
os.environ["JWT_SECRET"] = "test-secret-key-at-least-32-characters-long-xxxx"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_EXPIRATION_HOURS"] = "24"

from app.core.jwt_handler import (
    create_access_token,
    validate_token,
    InvalidTokenError,
    ExpiredTokenError,
    JWTConfig,
)


class TestTokenCreation:
    """Test JWT token creation."""
    
    def test_create_access_token(self):
        """Test create_access_token generates valid JWT."""
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        
        token = create_access_token(user_id, tenant_id)
        
        assert token is not None
        assert isinstance(token, str)
        # JWT has 3 parts: header.payload.signature
        parts = token.split(".")
        assert len(parts) == 3
    
    def test_token_payload_contains_required_claims(self):
        """Test token includes required claims: sub, tenant_id, exp, iat, jti."""
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        
        token = create_access_token(user_id, tenant_id)
        payload = validate_token(token)
        
        assert "sub" in payload
        assert payload["sub"] == user_id
        assert "tenant_id" in payload
        assert payload["tenant_id"] == tenant_id
        assert "exp" in payload
        assert "iat" in payload
        assert "jti" in payload
    
    def test_token_expiration_is_24_hours(self):
        """Test token expires in 24 hours."""
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        
        token = create_access_token(user_id, tenant_id)
        payload = validate_token(token)
        
        # Calculate expiration window (24 hours = 86400 seconds)
        exp_time = datetime.utcfromtimestamp(payload["exp"])
        iat_time = datetime.utcfromtimestamp(payload["iat"])
        
        duration = exp_time - iat_time
        # Allow 1 minute grace period
        assert 23 * 60 * 60 <= duration.total_seconds() <= 24 * 60 * 60 + 60


class TestTokenValidation:
    """Test JWT token validation."""
    
    def test_validate_token_valid(self):
        """Test validate_token accepts valid token."""
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        
        token = create_access_token(user_id, tenant_id)
        payload = validate_token(token)
        
        assert payload["sub"] == user_id
        assert payload["tenant_id"] == tenant_id
    
    def test_validate_token_invalid_signature(self):
        """Test validate_token rejects invalid signature."""
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        
        token = create_access_token(user_id, tenant_id)
        
        # Modify token to invalidate signature
        invalid_token = token[:-10] + "0123456789"
        
        with pytest.raises(InvalidTokenError):
            validate_token(invalid_token)
    
    def test_validate_token_malformed(self):
        """Test validate_token rejects malformed token."""
        malformed_token = "not.a.valid.jwt.token"
        
        with pytest.raises(InvalidTokenError):
            validate_token(malformed_token)


class TestJWTConfig:
    """Test JWT configuration."""
    
    def test_jwt_config_validate_requires_secret(self):
        """Test JWT_SECRET is required."""
        original_secret = os.environ.get("JWT_SECRET")
        del os.environ["JWT_SECRET"]
        
        with pytest.raises(ValueError, match="JWT_SECRET"):
            JWTConfig.validate()
        
        # Restore
        if original_secret:
            os.environ["JWT_SECRET"] = original_secret
    
    def test_jwt_config_validate_secret_length(self):
        """Test JWT_SECRET must be at least 32 characters."""
        os.environ["JWT_SECRET"] = "short"
        
        with pytest.raises(ValueError, match="at least 32 characters"):
            JWTConfig.validate()
        
        # Restore
        os.environ["JWT_SECRET"] = "test-secret-key-at-least-32-characters-long-xxxx"
