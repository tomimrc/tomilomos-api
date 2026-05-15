"""Service layer for raw materials business logic.

This layer contains all business logic for raw materials operations.
Repositories handle persistence; services handle validation and orchestration.
"""

from decimal import Decimal
from typing import Optional, List
import uuid

from sqlalchemy.orm import Session

from repositories.raw_materials_repository import RawMaterialRepository
from schemas.raw_materials import (
    RawMaterialCreate,
    RawMaterialUpdate,
    RawMaterialRead,
)
from db.models import RawMaterial


class RawMaterialService:
    """Service for raw materials business logic."""
    
    def __init__(self, session: Session):
        """Initialize the service with a database session.
        
        Args:
            session: SQLAlchemy session for database operations
        """
        self.repository = RawMaterialRepository(session)
    
    def create_raw_material(
        self,
        tenant_id: str,
        data: RawMaterialCreate
    ) -> RawMaterialRead:
        """Create a new raw material with validation.
        
        Args:
            tenant_id: ID of the tenant
            data: RawMaterialCreate schema with validated data
            
        Returns:
            RawMaterialRead schema with created data
            
        Raises:
            ValueError: If validation fails
        """
        # Generate UUID for raw material
        raw_material_id = str(uuid.uuid4())
        
        # Create via repository
        raw_material = self.repository.create(
            tenant_id=tenant_id,
            name=data.name,
            unit_of_measurement=data.unit_of_measurement,
            cost_per_unit=data.cost_per_unit,
            supplier=data.supplier,
            raw_material_id=raw_material_id
        )
        
        return RawMaterialRead.from_orm(raw_material)
    
    def get_raw_material(
        self,
        tenant_id: str,
        raw_material_id: str
    ) -> Optional[RawMaterialRead]:
        """Get a raw material by ID.
        
        Args:
            tenant_id: ID of the tenant
            raw_material_id: ID of the raw material
            
        Returns:
            RawMaterialRead schema or None if not found
        """
        raw_material = self.repository.get_by_id(tenant_id, raw_material_id)
        if not raw_material:
            return None
        return RawMaterialRead.from_orm(raw_material)
    
    def list_raw_materials(
        self,
        tenant_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[RawMaterialRead]:
        """List raw materials for a tenant with pagination.
        
        Args:
            tenant_id: ID of the tenant
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of RawMaterialRead schemas
        """
        raw_materials = self.repository.list_by_tenant(tenant_id, skip, limit)
        return [RawMaterialRead.from_orm(rm) for rm in raw_materials]
    
    def update_raw_material(
        self,
        tenant_id: str,
        raw_material_id: str,
        data: RawMaterialUpdate
    ) -> Optional[RawMaterialRead]:
        """Update a raw material with validation.
        
        Args:
            tenant_id: ID of the tenant
            raw_material_id: ID of the raw material
            data: RawMaterialUpdate schema with validated data
            
        Returns:
            RawMaterialRead schema or None if not found
            
        Raises:
            ValueError: If validation fails
        """
        # Prepare updates dictionary (exclude None values)
        updates = {}
        if data.name is not None:
            updates['name'] = data.name
        if data.unit_of_measurement is not None:
            updates['unit_of_measurement'] = data.unit_of_measurement
        if data.cost_per_unit is not None:
            updates['cost_per_unit'] = data.cost_per_unit
        if data.supplier is not None:
            updates['supplier'] = data.supplier
        # Note: current_stock should NOT be updated via direct update;
        # stock changes must go through add_stock or remove_stock
        
        if not updates:
            # If no updates provided, just return current state
            return self.get_raw_material(tenant_id, raw_material_id)
        
        raw_material = self.repository.update(tenant_id, raw_material_id, **updates)
        if not raw_material:
            return None
        return RawMaterialRead.from_orm(raw_material)
    
    def delete_raw_material(self, tenant_id: str, raw_material_id: str) -> bool:
        """Delete a raw material.
        
        Args:
            tenant_id: ID of the tenant
            raw_material_id: ID of the raw material
            
        Returns:
            True if deleted, False if not found
        """
        return self.repository.delete(tenant_id, raw_material_id)
    
    def add_stock(
        self,
        tenant_id: str,
        raw_material_id: str,
        quantity: Decimal,
        reason: Optional[str] = None
    ) -> Optional[RawMaterialRead]:
        """Add stock to a raw material.
        
        Args:
            tenant_id: ID of the tenant
            raw_material_id: ID of the raw material
            quantity: Quantity to add (must be positive)
            reason: Optional reason for adjustment (e.g., "purchase", "restock")
            
        Returns:
            RawMaterialRead schema or None if not found
            
        Raises:
            ValueError: If quantity is not positive
        """
        if quantity <= 0:
            raise ValueError("Quantity to add must be greater than 0")
        
        # TODO: Log reason to audit trail when implemented
        
        raw_material = self.repository.add_stock(tenant_id, raw_material_id, quantity)
        if not raw_material:
            return None
        return RawMaterialRead.from_orm(raw_material)
    
    def remove_stock(
        self,
        tenant_id: str,
        raw_material_id: str,
        quantity: Decimal,
        reason: Optional[str] = None
    ) -> Optional[RawMaterialRead]:
        """Remove stock from a raw material with validation.
        
        Args:
            tenant_id: ID of the tenant
            raw_material_id: ID of the raw material
            quantity: Quantity to remove (must be positive)
            reason: Optional reason for adjustment (e.g., "sale", "recipe", "waste")
            
        Returns:
            RawMaterialRead schema or None if not found
            
        Raises:
            ValueError: If quantity is not positive or would result in negative stock
        """
        if quantity <= 0:
            raise ValueError("Quantity to remove must be greater than 0")
        
        # TODO: Log reason to audit trail when implemented
        
        try:
            raw_material = self.repository.remove_stock(tenant_id, raw_material_id, quantity)
            if not raw_material:
                return None
            return RawMaterialRead.from_orm(raw_material)
        except ValueError as e:
            raise ValueError(str(e))
    
    def get_stock(self, tenant_id: str, raw_material_id: str) -> Optional[Decimal]:
        """Get the current stock level of a raw material.
        
        Args:
            tenant_id: ID of the tenant
            raw_material_id: ID of the raw material
            
        Returns:
            Current stock level or None if not found
        """
        return self.repository.get_stock(tenant_id, raw_material_id)
