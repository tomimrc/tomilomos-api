"""User repository for database operations."""

from typing import Optional
from sqlalchemy.orm import Session

from db.models import User


class UserRepository:
    """Repository for user database operations."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session.
        
        Args:
            db: SQLAlchemy session
        """
        self.db = db
    
    def get_user_by_email(self, email: str, tenant_id: str) -> Optional[User]:
        """Get user by email within a specific tenant.
        
        Args:
            email: User email
            tenant_id: Tenant UUID
            
        Returns:
            User: User object if found, None otherwise
        """
        return self.db.query(User).filter(
            User.email == email,
            User.tenant_id == tenant_id,
        ).first()
    
    def create_user(self, email: str, password_hash: str, tenant_id: str) -> User:
        """Create a new user.
        
        Args:
            email: User email
            password_hash: Bcrypt password hash
            tenant_id: Tenant UUID
            
        Returns:
            User: Created user object
        """
        user = User(
            email=email,
            password_hash=password_hash,
            tenant_id=tenant_id,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
