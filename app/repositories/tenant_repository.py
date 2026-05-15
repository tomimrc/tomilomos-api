"""Tenant repository for database operations."""

from typing import Optional
from sqlalchemy.orm import Session

from db.models import Tenant


class TenantRepository:
    """Repository for tenant database operations."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session.
        
        Args:
            db: SQLAlchemy session
        """
        self.db = db
    
    def create_tenant(self, name: str) -> Tenant:
        """Create a new tenant.
        
        Args:
            name: Tenant name
            
        Returns:
            Tenant: Created tenant object
        """
        tenant = Tenant(name=name)
        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)
        return tenant
    
    def get_tenant_by_id(self, tenant_id: str) -> Optional[Tenant]:
        """Get tenant by ID.
        
        Args:
            tenant_id: Tenant UUID
            
        Returns:
            Tenant: Tenant object if found, None otherwise
        """
        return self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
