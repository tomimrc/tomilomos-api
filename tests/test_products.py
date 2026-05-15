"""Tests for products module.

Includes unit tests for service/repository and integration tests for API endpoints.
"""

import pytest
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base
from db.models import Tenant, User, Product
from services.products_service import ProductService
from repositories.products_repository import ProductRepository
from schemas.products import (
    ProductCreate,
    ProductUpdate,
)


# Test database setup
@pytest.fixture
def db_engine():
    """Create an in-memory SQLite engine for testing (fresh per test)."""
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
    """Create a test tenant with unique email per test."""
    import uuid
    tenant = Tenant(
        id=f"tenant-{uuid.uuid4()}",
        name="Test Restaurant",
        email=f"test-{uuid.uuid4()}@example.com"
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

class TestProductRepository:
    """Tests for ProductRepository."""
    
    def test_create_product(self, db_session, tenant):
        """Test creating a product."""
        repo = ProductRepository(db_session)
        
        product = repo.create(
            tenant_id=tenant.id,
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True,
            product_id="prod-1"
        )
        db_session.commit()
        
        assert product.id == "prod-1"
        assert product.name == "Lomito Completo"
        assert product.tenant_id == tenant.id
        assert product.sale_price == Decimal("45.99")
        assert product.is_active == True
    
    def test_get_by_id(self, db_session, tenant):
        """Test getting a product by ID."""
        repo = ProductRepository(db_session)
        
        product = repo.create(
            tenant_id=tenant.id,
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True,
            product_id="prod-1"
        )
        db_session.commit()
        
        found = repo.get_by_id(tenant.id, "prod-1")
        assert found is not None
        assert found.name == "Lomito Completo"
        assert found.sale_price == Decimal("45.99")
    
    def test_get_by_id_enforces_tenant_isolation(self, db_session, tenant):
        """Test that get_by_id enforces tenant isolation."""
        repo = ProductRepository(db_session)
        
        product = repo.create(
            tenant_id=tenant.id,
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True,
            product_id="prod-1"
        )
        db_session.commit()
        
        # Try to access with different tenant ID
        found = repo.get_by_id("other-tenant", "prod-1")
        assert found is None
    
    def test_list_by_tenant(self, db_session, tenant):
        """Test listing products by tenant."""
        repo = ProductRepository(db_session)
        
        repo.create(
            tenant_id=tenant.id,
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True,
            product_id="prod-1"
        )
        repo.create(
            tenant_id=tenant.id,
            name="Papas",
            sale_price=Decimal("12.50"),
            is_active=True,
            product_id="prod-2"
        )
        db_session.commit()
        
        products = repo.list_by_tenant(tenant.id)
        assert len(products) == 2
    
    def test_list_by_tenant_with_pagination(self, db_session, tenant):
        """Test listing products with pagination."""
        repo = ProductRepository(db_session)
        
        for i in range(5):
            repo.create(
                tenant_id=tenant.id,
                name=f"Product {i}",
                sale_price=Decimal("10.00"),
                is_active=True,
                product_id=f"prod-{i}"
            )
        db_session.commit()
        
        page1 = repo.list_by_tenant(tenant.id, skip=0, limit=2)
        page2 = repo.list_by_tenant(tenant.id, skip=2, limit=2)
        
        assert len(page1) == 2
        assert len(page2) == 2
    
    def test_update_product(self, db_session, tenant):
        """Test updating a product."""
        repo = ProductRepository(db_session)
        
        product = repo.create(
            tenant_id=tenant.id,
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True,
            product_id="prod-1"
        )
        db_session.commit()
        
        updated = repo.update(
            tenant_id=tenant.id,
            product_id="prod-1",
            name="Lomito Premium",
            sale_price=Decimal("49.99")
        )
        db_session.commit()
        
        assert updated is not None
        assert updated.name == "Lomito Premium"
        assert updated.sale_price == Decimal("49.99")
    
    def test_delete_product(self, db_session, tenant):
        """Test deleting a product."""
        repo = ProductRepository(db_session)
        
        repo.create(
            tenant_id=tenant.id,
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True,
            product_id="prod-1"
        )
        db_session.commit()
        
        deleted = repo.delete(tenant.id, "prod-1")
        db_session.commit()
        
        assert deleted == True
        found = repo.get_by_id(tenant.id, "prod-1")
        assert found is None


# Service Tests

class TestProductService:
    """Tests for ProductService."""
    
    def test_create_product(self, db_session, tenant):
        """Test creating a product via service."""
        service = ProductService(db_session)
        
        data = ProductCreate(
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True
        )
        result = service.create_product(tenant.id, data)
        db_session.commit()
        
        assert result.name == "Lomito Completo"
        assert result.sale_price == Decimal("45.99")
        assert result.is_active == True
        assert result.id is not None
    
    def test_get_product(self, db_session, tenant):
        """Test getting a product via service."""
        service = ProductService(db_session)
        
        data = ProductCreate(
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True
        )
        created = service.create_product(tenant.id, data)
        db_session.commit()
        
        found = service.get_product(tenant.id, created.id)
        assert found is not None
        assert found.name == "Lomito Completo"
    
    def test_list_products(self, db_session, tenant):
        """Test listing products via service."""
        service = ProductService(db_session)
        
        for i in range(3):
            data = ProductCreate(
                name=f"Product {i}",
                sale_price=Decimal("25.00"),
                is_active=True
            )
            service.create_product(tenant.id, data)
        db_session.commit()
        
        products = service.list_products(tenant.id)
        assert len(products) == 3
    
    def test_update_product(self, db_session, tenant):
        """Test updating a product via service."""
        service = ProductService(db_session)
        
        data = ProductCreate(
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True
        )
        created = service.create_product(tenant.id, data)
        db_session.commit()
        
        update_data = ProductUpdate(
            name="Lomito Premium",
            sale_price=Decimal("49.99")
        )
        updated = service.update_product(tenant.id, created.id, update_data)
        db_session.commit()
        
        assert updated is not None
        assert updated.name == "Lomito Premium"
        assert updated.sale_price == Decimal("49.99")
    
    def test_delete_product(self, db_session, tenant):
        """Test deleting a product via service."""
        service = ProductService(db_session)
        
        data = ProductCreate(
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True
        )
        created = service.create_product(tenant.id, data)
        db_session.commit()
        
        deleted = service.delete_product(tenant.id, created.id)
        db_session.commit()
        
        assert deleted == True
        found = service.get_product(tenant.id, created.id)
        assert found is None


# Integration Tests

class TestProductValidation:
    """Tests for product validation."""
    
    def test_validate_sale_price_required(self):
        """Test that sale_price is required."""
        with pytest.raises(ValueError):
            ProductCreate(name="Test", sale_price=None)
    
    def test_validate_sale_price_positive(self):
        """Test that sale_price must be positive."""
        with pytest.raises(ValueError):
            ProductCreate(name="Test", sale_price=Decimal("0"))
        
        with pytest.raises(ValueError):
            ProductCreate(name="Test", sale_price=Decimal("-10.00"))
    
    def test_validate_sale_price_decimal_precision(self):
        """Test that decimal precision is maintained."""
        data = ProductCreate(
            name="Test",
            sale_price=Decimal("45.99"),
            is_active=True
        )
        assert data.sale_price == Decimal("45.99")
    
    def test_validate_name_required(self):
        """Test that name is required and not empty."""
        with pytest.raises(ValueError):
            ProductCreate(name="", sale_price=Decimal("10.00"))
    
    def test_validate_is_active_defaults_to_true(self):
        """Test that is_active defaults to true."""
        data = ProductCreate(name="Test", sale_price=Decimal("10.00"))
        assert data.is_active == True


class TestMultiTenantIsolation:
    """Tests for multi-tenant isolation."""
    
    def test_product_not_accessible_across_tenants(self, db_session):
        """Test that a product is not accessible to another tenant."""
        tenant1 = Tenant(id="tenant-1", name="Restaurant 1", email="r1@example.com")
        tenant2 = Tenant(id="tenant-2", name="Restaurant 2", email="r2@example.com")
        db_session.add(tenant1)
        db_session.add(tenant2)
        db_session.commit()
        
        repo = ProductRepository(db_session)
        repo.create(
            tenant_id=tenant1.id,
            name="Lomito Completo",
            sale_price=Decimal("45.99"),
            is_active=True,
            product_id="prod-1"
        )
        db_session.commit()
        
        # Tenant 1 should see the product
        found1 = repo.get_by_id(tenant1.id, "prod-1")
        assert found1 is not None
        
        # Tenant 2 should NOT see the product
        found2 = repo.get_by_id(tenant2.id, "prod-1")
        assert found2 is None
