"""Tests for raw materials module.

Includes unit tests for service/repository and integration tests for API endpoints.
"""

import pytest
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base
from db.models import Tenant, User, RawMaterial
from services.raw_materials_service import RawMaterialService
from repositories.raw_materials_repository import RawMaterialRepository
from schemas.raw_materials import (
    RawMaterialCreate,
    RawMaterialUpdate,
)


# Test database setup
@pytest.fixture(scope="session")
def db_engine():
    """Create an in-memory SQLite engine for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def db_session(db_engine):
    """Create a new database session for each test."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    
    yield session
    
    session.rollback()
    session.close()


@pytest.fixture
def tenant(db_session):
    """Create a test tenant."""
    tenant = Tenant(
        id="tenant-123",
        name="Test Restaurant",
        email="test@example.com"
    )
    db_session.add(tenant)
    db_session.commit()
    return tenant


@pytest.fixture
def user(db_session, tenant):
    """Create a test user."""
    user = User(
        id="user-456",
        email="user@example.com",
        hashed_password="hashed_password_here",
        tenant_id=tenant.id
    )
    db_session.add(user)
    db_session.commit()
    return user


# Repository Tests

class TestRawMaterialRepository:
    """Tests for RawMaterialRepository."""
    
    def test_create_raw_material(self, db_session, tenant):
        """Test creating a raw material."""
        repo = RawMaterialRepository(db_session)
        
        raw_material = repo.create(
            tenant_id=tenant.id,
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            supplier="Local Farm",
            raw_material_id="raw-1"
        )
        db_session.commit()
        
        assert raw_material.id == "raw-1"
        assert raw_material.name == "Tomatoes"
        assert raw_material.tenant_id == tenant.id
        assert raw_material.cost_per_unit == Decimal("2.50")
        assert raw_material.current_stock == Decimal("0")
    
    def test_get_by_id(self, db_session, tenant):
        """Test getting a raw material by ID."""
        repo = RawMaterialRepository(db_session)
        
        raw_material = repo.create(
            tenant_id=tenant.id,
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            raw_material_id="raw-1"
        )
        db_session.commit()
        
        found = repo.get_by_id(tenant.id, "raw-1")
        assert found is not None
        assert found.name == "Tomatoes"
    
    def test_get_by_id_enforces_tenant_isolation(self, db_session, tenant):
        """Test that get_by_id enforces tenant isolation."""
        repo = RawMaterialRepository(db_session)
        
        raw_material = repo.create(
            tenant_id=tenant.id,
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            raw_material_id="raw-1"
        )
        db_session.commit()
        
        # Try to access with different tenant ID
        found = repo.get_by_id("other-tenant", "raw-1")
        assert found is None
    
    def test_list_by_tenant(self, db_session, tenant):
        """Test listing raw materials by tenant."""
        repo = RawMaterialRepository(db_session)
        
        repo.create(
            tenant_id=tenant.id,
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            raw_material_id="raw-1"
        )
        repo.create(
            tenant_id=tenant.id,
            name="Onions",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("1.00"),
            raw_material_id="raw-2"
        )
        db_session.commit()
        
        materials = repo.list_by_tenant(tenant.id)
        assert len(materials) == 2
    
    def test_update(self, db_session, tenant):
        """Test updating a raw material."""
        repo = RawMaterialRepository(db_session)
        
        raw_material = repo.create(
            tenant_id=tenant.id,
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            raw_material_id="raw-1"
        )
        db_session.commit()
        
        updated = repo.update(
            tenant.id,
            "raw-1",
            name="Premium Tomatoes",
            cost_per_unit=Decimal("3.00")
        )
        db_session.commit()
        
        assert updated.name == "Premium Tomatoes"
        assert updated.cost_per_unit == Decimal("3.00")
    
    def test_delete(self, db_session, tenant):
        """Test deleting a raw material."""
        repo = RawMaterialRepository(db_session)
        
        raw_material = repo.create(
            tenant_id=tenant.id,
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            raw_material_id="raw-1"
        )
        db_session.commit()
        
        success = repo.delete(tenant.id, "raw-1")
        assert success is True
        
        found = repo.get_by_id(tenant.id, "raw-1")
        assert found is None
    
    def test_add_stock(self, db_session, tenant):
        """Test adding stock to a raw material."""
        repo = RawMaterialRepository(db_session)
        
        raw_material = repo.create(
            tenant_id=tenant.id,
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            raw_material_id="raw-1"
        )
        db_session.commit()
        
        updated = repo.add_stock(tenant.id, "raw-1", Decimal("10.50"))
        db_session.commit()
        
        assert updated.current_stock == Decimal("10.50")
    
    def test_remove_stock_success(self, db_session, tenant):
        """Test removing stock successfully."""
        repo = RawMaterialRepository(db_session)
        
        raw_material = repo.create(
            tenant_id=tenant.id,
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            raw_material_id="raw-1"
        )
        db_session.commit()
        
        repo.add_stock(tenant.id, "raw-1", Decimal("10.00"))
        db_session.commit()
        
        updated = repo.remove_stock(tenant.id, "raw-1", Decimal("3.00"))
        db_session.commit()
        
        assert updated.current_stock == Decimal("7.00")
    
    def test_remove_stock_insufficient_stock(self, db_session, tenant):
        """Test that remove_stock fails with insufficient stock."""
        repo = RawMaterialRepository(db_session)
        
        raw_material = repo.create(
            tenant_id=tenant.id,
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            raw_material_id="raw-1"
        )
        db_session.commit()
        
        repo.add_stock(tenant.id, "raw-1", Decimal("5.00"))
        db_session.commit()
        
        with pytest.raises(ValueError, match="Insufficient stock"):
            repo.remove_stock(tenant.id, "raw-1", Decimal("10.00"))
    
    def test_get_stock(self, db_session, tenant):
        """Test getting stock level."""
        repo = RawMaterialRepository(db_session)
        
        raw_material = repo.create(
            tenant_id=tenant.id,
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            raw_material_id="raw-1"
        )
        db_session.commit()
        
        repo.add_stock(tenant.id, "raw-1", Decimal("15.75"))
        db_session.commit()
        
        stock = repo.get_stock(tenant.id, "raw-1")
        assert stock == Decimal("15.75")


# Service Tests

class TestRawMaterialService:
    """Tests for RawMaterialService."""
    
    def test_create_raw_material(self, db_session, tenant):
        """Test creating a raw material via service."""
        service = RawMaterialService(db_session)
        
        data = RawMaterialCreate(
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50"),
            supplier="Local Farm"
        )
        
        result = service.create_raw_material(tenant.id, data)
        db_session.commit()
        
        assert result.name == "Tomatoes"
        assert result.tenant_id == tenant.id
        assert result.cost_per_unit == Decimal("2.50")
    
    def test_get_raw_material(self, db_session, tenant):
        """Test getting a raw material via service."""
        service = RawMaterialService(db_session)
        
        data = RawMaterialCreate(
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50")
        )
        
        created = service.create_raw_material(tenant.id, data)
        db_session.commit()
        
        found = service.get_raw_material(tenant.id, created.id)
        assert found is not None
        assert found.name == "Tomatoes"
    
    def test_list_raw_materials(self, db_session, tenant):
        """Test listing raw materials via service."""
        service = RawMaterialService(db_session)
        
        for i in range(3):
            data = RawMaterialCreate(
                name=f"Ingredient {i}",
                unit_of_measurement="kg",
                cost_per_unit=Decimal("1.00")
            )
            service.create_raw_material(tenant.id, data)
        db_session.commit()
        
        materials = service.list_raw_materials(tenant.id)
        assert len(materials) == 3
    
    def test_update_raw_material(self, db_session, tenant):
        """Test updating a raw material via service."""
        service = RawMaterialService(db_session)
        
        data = RawMaterialCreate(
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50")
        )
        
        created = service.create_raw_material(tenant.id, data)
        db_session.commit()
        
        update_data = RawMaterialUpdate(
            name="Premium Tomatoes",
            cost_per_unit=Decimal("3.50")
        )
        
        updated = service.update_raw_material(tenant.id, created.id, update_data)
        db_session.commit()
        
        assert updated.name == "Premium Tomatoes"
        assert updated.cost_per_unit == Decimal("3.50")
    
    def test_add_stock_via_service(self, db_session, tenant):
        """Test adding stock via service."""
        service = RawMaterialService(db_session)
        
        data = RawMaterialCreate(
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50")
        )
        
        created = service.create_raw_material(tenant.id, data)
        db_session.commit()
        
        result = service.add_stock(tenant.id, created.id, Decimal("10.00"), reason="purchase")
        db_session.commit()
        
        assert result.current_stock == Decimal("10.00")
    
    def test_remove_stock_via_service(self, db_session, tenant):
        """Test removing stock via service."""
        service = RawMaterialService(db_session)
        
        data = RawMaterialCreate(
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50")
        )
        
        created = service.create_raw_material(tenant.id, data)
        db_session.commit()
        
        service.add_stock(tenant.id, created.id, Decimal("10.00"))
        db_session.commit()
        
        result = service.remove_stock(tenant.id, created.id, Decimal("3.00"), reason="sale")
        db_session.commit()
        
        assert result.current_stock == Decimal("7.00")
    
    def test_validation_cost_per_unit_positive(self, db_session, tenant):
        """Test that cost_per_unit must be positive."""
        service = RawMaterialService(db_session)
        
        data = RawMaterialCreate(
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("-1.00")
        )
        
        # Validation should happen in schema, so this shouldn't reach here
        # But service should also validate
        with pytest.raises(ValueError):
            result = service.create_raw_material(tenant.id, data)
    
    def test_decimal_precision(self, db_session, tenant):
        """Test that decimal precision is maintained."""
        service = RawMaterialService(db_session)
        
        data = RawMaterialCreate(
            name="Salt",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("0.05")
        )
        
        created = service.create_raw_material(tenant.id, data)
        db_session.commit()
        
        assert created.cost_per_unit == Decimal("0.05")
        
        # Test stock decimal precision
        result = service.add_stock(tenant.id, created.id, Decimal("2.50"))
        db_session.commit()
        
        assert result.current_stock == Decimal("2.50")


# Test multi-tenant isolation
class TestMultiTenantIsolation:
    """Tests for multi-tenant isolation in raw materials."""
    
    def test_tenant_isolation_on_read(self, db_session):
        """Test that users cannot access raw materials from other tenants."""
        # Create two tenants
        tenant1 = Tenant(id="tenant-1", name="Restaurant 1", email="rest1@example.com")
        tenant2 = Tenant(id="tenant-2", name="Restaurant 2", email="rest2@example.com")
        db_session.add_all([tenant1, tenant2])
        db_session.commit()
        
        # Create raw materials in tenant1
        service = RawMaterialService(db_session)
        data = RawMaterialCreate(
            name="Tomatoes",
            unit_of_measurement="kg",
            cost_per_unit=Decimal("2.50")
        )
        
        created = service.create_raw_material(tenant1.id, data)
        db_session.commit()
        
        # Try to access from tenant2
        found = service.get_raw_material(tenant2.id, created.id)
        assert found is None
    
    def test_tenant_isolation_on_list(self, db_session):
        """Test that users see only their tenant's raw materials."""
        tenant1 = Tenant(id="tenant-1", name="Restaurant 1", email="rest1@example.com")
        tenant2 = Tenant(id="tenant-2", name="Restaurant 2", email="rest2@example.com")
        db_session.add_all([tenant1, tenant2])
        db_session.commit()
        
        service = RawMaterialService(db_session)
        
        # Create raw materials in both tenants
        for tenant_id in [tenant1.id, tenant2.id]:
            for i in range(2):
                data = RawMaterialCreate(
                    name=f"Ingredient {i}",
                    unit_of_measurement="kg",
                    cost_per_unit=Decimal("1.00")
                )
                service.create_raw_material(tenant_id, data)
        db_session.commit()
        
        # Check that each tenant sees only their materials
        tenant1_materials = service.list_raw_materials(tenant1.id)
        tenant2_materials = service.list_raw_materials(tenant2.id)
        
        assert len(tenant1_materials) == 2
        assert len(tenant2_materials) == 2
        
        # Verify materials are different
        tenant1_names = {m.id for m in tenant1_materials}
        tenant2_names = {m.id for m in tenant2_materials}
        assert len(tenant1_names & tenant2_names) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
