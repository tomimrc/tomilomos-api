"""Tests for authentication service."""

import pytest
import uuid
from app.services.auth_service import AuthService
from app.core.exceptions import (
    UserNotFoundError,
    InvalidCredentialsError,
    DuplicateEmailError,
)


class TestAuthenticateUser:
    """Test user authentication."""
    
    def test_authenticate_user_success(self, db, test_user, test_user_password):
        """Test successful user authentication."""
        auth_service = AuthService(db)
        
        user = auth_service.authenticate_user(
            test_user.email,
            test_user_password,
            str(test_user.tenant_id),
        )
        
        assert user.id == test_user.id
        assert user.email == test_user.email
    
    def test_authenticate_user_invalid_password(self, db, test_user):
        """Test authentication fails with wrong password."""
        auth_service = AuthService(db)
        
        with pytest.raises(InvalidCredentialsError):
            auth_service.authenticate_user(
                test_user.email,
                "WrongPassword123!",
                str(test_user.tenant_id),
            )
    
    def test_authenticate_user_not_found(self, db, test_user):
        """Test authentication fails when user not found."""
        auth_service = AuthService(db)
        
        with pytest.raises(UserNotFoundError):
            auth_service.authenticate_user(
                "nonexistent@example.com",
                "AnyPassword123!",
                str(test_user.tenant_id),
            )


class TestCreateTenant:
    """Test tenant creation."""
    
    def test_create_tenant(self, db):
        """Test successful tenant creation."""
        auth_service = AuthService(db)
        
        tenant = auth_service.create_tenant("New Tenant")
        
        assert tenant.id is not None
        assert tenant.name == "New Tenant"
        assert tenant.created_at is not None


class TestCreateUser:
    """Test user creation."""
    
    def test_create_user(self, db, test_tenant):
        """Test successful user creation."""
        auth_service = AuthService(db)
        
        email = "newuser@example.com"
        password = "NewPassword123!"
        
        user = auth_service.create_user(email, password, str(test_tenant.id))
        
        assert user.id is not None
        assert user.email == email
        assert user.tenant_id == test_tenant.id
        # Password should be hashed, not plaintext
        assert user.password_hash != password
        assert user.password_hash.startswith("$2b$")
    
    def test_create_user_duplicate_email_same_tenant(self, db, test_user):
        """Test creating user with duplicate email in same tenant fails."""
        auth_service = AuthService(db)
        
        with pytest.raises(DuplicateEmailError):
            auth_service.create_user(
                test_user.email,
                "AnotherPassword123!",
                str(test_user.tenant_id),
            )
    
    def test_create_user_same_email_different_tenant_allowed(self, db, test_user):
        """Test same email allowed in different tenants."""
        auth_service = AuthService(db)
        
        # Create new tenant
        new_tenant = auth_service.create_tenant("Another Tenant")
        
        # Create user with same email in different tenant
        user = auth_service.create_user(
            test_user.email,  # Same email
            "DifferentPassword123!",
            str(new_tenant.id),  # Different tenant
        )
        
        assert user.id != test_user.id
        assert user.email == test_user.email
        assert user.tenant_id != test_user.tenant_id


class TestGenerateTokens:
    """Test token generation."""
    
    def test_generate_tokens(self, db, test_user):
        """Test token generation for user."""
        auth_service = AuthService(db)
        
        response = auth_service.generate_tokens(test_user)
        
        assert response.access_token is not None
        assert response.token_type == "bearer"
        assert response.expires_in == 24 * 60 * 60  # 24 hours
