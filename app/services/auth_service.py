"""Authentication business logic."""

from sqlalchemy.orm import Session

from db.models import Tenant, User
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_access_token
from app.schemas.auth import TokenResponse
from app.core.exceptions import (
    UserNotFoundError,
    InvalidCredentialsError,
    DuplicateEmailError,
)
from app.repositories.user_repository import UserRepository
from app.repositories.tenant_repository import TenantRepository


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: Session):
        """Initialize service with database session.
        
        Args:
            db: SQLAlchemy session
        """
        self.db = db
        self.user_repo = UserRepository(db)
        self.tenant_repo = TenantRepository(db)
    
    def login(self, email: str, password: str) -> tuple[User, TokenResponse]:
        """Authenticate user by email and password, return user and JWT token.
        
        Looks up user by email (assumed globally unique), verifies password,
        and generates a JWT token.
        
        Args:
            email: User email
            password: Plaintext password
            
        Returns:
            tuple[User, TokenResponse]: Authenticated user and JWT token
            
        Raises:
            UserNotFoundError: If user doesn't exist
            InvalidCredentialsError: If password is incorrect
        """
        # Query user by email alone
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise UserNotFoundError(f"User not found: {email}")
        
        # Verify password using constant-time comparison
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        
        # Generate token
        token_response = self.generate_tokens(user)
        return user, token_response
    
    def authenticate_user(self, email: str, password: str, tenant_id: str) -> User:
        """Authenticate user by email and password.
        
        Args:
            email: User email
            password: Plaintext password
            tenant_id: Tenant UUID
            
        Returns:
            User: Authenticated user object
            
        Raises:
            UserNotFoundError: If user doesn't exist
            InvalidCredentialsError: If password is incorrect
        """
        # Query user by email and tenant_id
        user = self.user_repo.get_user_by_email(email, tenant_id)
        if not user:
            raise UserNotFoundError(f"User not found: {email}")
        
        # Verify password using constant-time comparison
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        
        return user
    
    def create_tenant(self, name: str) -> Tenant:
        """Create a new tenant.
        
        Args:
            name: Tenant name
            
        Returns:
            Tenant: Created tenant object
        """
        return self.tenant_repo.create_tenant(name)
    
    def create_user(self, email: str, password: str, tenant_id: str) -> User:
        """Create a new user in a tenant.
        
        Args:
            email: User email
            password: Plaintext password
            tenant_id: Tenant UUID
            
        Returns:
            User: Created user object
            
        Raises:
            DuplicateEmailError: If email already exists in tenant
        """
        # Check email uniqueness within tenant
        existing_user = self.user_repo.get_user_by_email(email, tenant_id)
        if existing_user:
            raise DuplicateEmailError(f"Email already exists in tenant: {email}")
        
        # Hash password with bcrypt
        password_hash = hash_password(password)
        
        # Create user in repository
        return self.user_repo.create_user(email, password_hash, tenant_id)
    
    def generate_tokens(self, user: User) -> TokenResponse:
        """Generate JWT token for user.
        
        Args:
            user: User object
            
        Returns:
            TokenResponse: JWT token and metadata
        """
        token = create_access_token(str(user.id), str(user.tenant_id))
        
        # 24 hours = 86400 seconds
        expires_in = 24 * 60 * 60
        
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=expires_in,
        )
