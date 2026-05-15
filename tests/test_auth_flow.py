"""Integration tests for authentication flows."""

import pytest
import uuid
from app.services.auth_service import AuthService


class TestAuthFlow:
    """Test end-to-end authentication flows."""
    
    def test_full_login_flow(self, db):
        """Test complete flow: create tenant → create user → login."""
        auth_service = AuthService(db)
        
        # Create tenant
        tenant = auth_service.create_tenant("Test Restaurant")
        
        # Create user
        email = "chef@restaurant.com"
        password = "SecurePassword123!"
        user = auth_service.create_user(email, password, str(tenant.id))
        
        # Login
        authenticated_user = auth_service.authenticate_user(email, password, str(tenant.id))
        
        assert authenticated_user.id == user.id
        
        # Generate token
        token_response = auth_service.generate_tokens(authenticated_user)
        assert token_response.access_token is not None
    
    def test_multi_tenant_isolation(self, db):
        """Test multi-tenant isolation: same email in different tenants."""
        auth_service = AuthService(db)
        
        # Create two tenants
        tenant1 = auth_service.create_tenant("Restaurant A")
        tenant2 = auth_service.create_tenant("Restaurant B")
        
        # Create users with same email in different tenants
        email = "owner@business.com"
        password1 = "Password1234!"
        password2 = "Password5678!"
        
        user1 = auth_service.create_user(email, password1, str(tenant1.id))
        user2 = auth_service.create_user(email, password2, str(tenant2.id))
        
        # Verify they are different users
        assert user1.id != user2.id
        assert user1.tenant_id != user2.tenant_id
    
    def test_login_with_wrong_tenant(self, db):
        """Test user cannot login with wrong tenant context."""
        auth_service = AuthService(db)
        
        # Create tenant and user
        tenant = auth_service.create_tenant("Restaurant")
        email = "user@restaurant.com"
        password = "Password123!"
        user = auth_service.create_user(email, password, str(tenant.id))
        
        # Try to login with wrong tenant ID
        from app.core.exceptions import UserNotFoundError
        
        wrong_tenant_id = str(uuid.uuid4())
        with pytest.raises(UserNotFoundError):
            auth_service.authenticate_user(email, password, wrong_tenant_id)
