"""Repository layer for sales.

This layer handles all database operations for sales.
"""

from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session

from db.models import Sale


class SaleRepository:
    """Repository for sale database operations."""
    
    def __init__(self, session: Session):
        """Initialize the repository with a database session.
        
        Args:
            session: SQLAlchemy session for database operations
        """
        self.session = session
    
    def create(
        self,
        tenant_id: str,
        product_id: str,
        quantity: int,
        unit_price: Decimal,
        total_price: Decimal,
        total_cost: Optional[Decimal],
        margin: Optional[Decimal],
        sale_id: str,
    ) -> Sale:
        """Create a new sale record.
        
        Args:
            tenant_id: ID of the tenant
            product_id: ID of the product sold
            quantity: Number of units sold
            unit_price: Sale price per unit at time of sale
            total_price: unit_price × quantity
            total_cost: Recipe cost × quantity, or None
            margin: total_price - total_cost, or None
            sale_id: UUID for the sale
            
        Returns:
            Created Sale instance
        """
        sale = Sale(
            id=sale_id,
            tenant_id=tenant_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            total_cost=total_cost,
            margin=margin,
        )
        self.session.add(sale)
        self.session.flush()
        return sale
    
    def get_by_id(self, tenant_id: str, sale_id: str) -> Optional[Sale]:
        """Get a sale by ID, enforcing tenant isolation.
        
        Args:
            tenant_id: ID of the tenant
            sale_id: ID of the sale
            
        Returns:
            Sale instance or None if not found
        """
        return self.session.query(Sale).filter(
            Sale.id == sale_id,
            Sale.tenant_id == tenant_id,
        ).first()
    
    def list_by_tenant(
        self,
        tenant_id: str,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Sale]:
        """List sales for a tenant with pagination, newest first.
        
        Args:
            tenant_id: ID of the tenant
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of Sale instances ordered by created_at DESC
        """
        return (
            self.session.query(Sale)
            .filter(Sale.tenant_id == tenant_id)
            .order_by(Sale.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
