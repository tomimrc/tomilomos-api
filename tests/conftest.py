"""Pytest configuration and fixtures for TomiLomos API tests.

This module provides common fixtures for testing:
- test_db: In-memory SQLite database
- test_tenant: Test tenant instance
- test_user: Test user instance
- test_jwt_token: Valid JWT token
- test_client: FastAPI TestClient
"""

import os
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from jose import jwt

# Set test environment variables before importing app
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("JWT_SECRET", "test_secret_key_do_not_use_in_production")
os.environ.setdefault("BCRYPT_COST", "10")  # Lower for test speed

from main import app, create_app
from core.config import settings
from app.db.base import Base
import app.db.models  # Ensure models are registered with Base
from db.session import SessionLocal, get_db


# ============================================================================
# DATABASE SETUP
# ============================================================================

@pytest.fixture(scope="function")
def test_db():
    """Create an in-memory SQLite database for testing.
    
    Returns a SQLAlchemy session that is rolled back after each test.
    """
    # Create in-memory SQLite engine
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    
    # Enable UUID support in SQLite by mapping UUID columns to VARCHAR(36)
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID
    from sqlalchemy.dialects.sqlite.base import SQLiteTypeCompiler
    
    def _visit_UUID(self, type_, **kw):
        return "VARCHAR(36)"
    
    SQLiteTypeCompiler.visit_UUID = _visit_UUID
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create session
    db = SessionLocal()
    
    yield db
    
    # Rollback after test
    db.rollback()
    db.close()


# ============================================================================
# TEST CLIENT
# ============================================================================

@pytest.fixture(scope="function")
def test_client(test_db: Session):
    """Create a FastAPI TestClient with dependency override for test database.
    
    Returns:
        TestClient: FastAPI test client with test database
    """
    # Override get_db dependency to use test database
    def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    client = TestClient(app)
    
    yield client
    
    # Clean up
    app.dependency_overrides.clear()


# ============================================================================
# TEST DATA FIXTURES
# ============================================================================

@pytest.fixture
def test_tenant(test_db: Session):
    """Create a test tenant.
    
    Returns:
        Tenant model instance
    """
    from app.db.models import Tenant
    
    tenant = Tenant(
        name="Test Restaurant",
    )
    test_db.add(tenant)
    test_db.commit()
    test_db.refresh(tenant)
    
    return tenant


@pytest.fixture
def test_user(test_db: Session, test_tenant):
    """Create a test user.
    
    Returns:
        User model instance
    """
    from app.db.models import User
    from bcrypt import hashpw, gensalt
    
    hashed_password = hashpw(b"testpassword123", gensalt(rounds=10))
    
    user = User(
        email="testuser@example.com",
        password_hash=hashed_password,
        tenant_id=test_tenant.id,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    return user


@pytest.fixture
def test_jwt_token(test_user):
    """Create a valid JWT token for testing.
    
    Returns:
        str: JWT token string
    """
    payload = {
        "sub": test_user.id,
        "tenant_id": test_user.tenant_id,
        "email": test_user.email,
        "exp": datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours),
        "iat": datetime.utcnow(),
    }
    
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    
    return token


@pytest.fixture
def test_expired_jwt_token(test_user):
    """Create an expired JWT token for testing.
    
    Returns:
        str: Expired JWT token string
    """
    payload = {
        "sub": test_user.id,
        "tenant_id": test_user.tenant_id,
        "email": test_user.email,
        "exp": datetime.utcnow() - timedelta(hours=1),  # Expired 1 hour ago
        "iat": datetime.utcnow() - timedelta(hours=2),
    }
    
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    
    return token


# ============================================================================
# HELPER FIXTURES
# ============================================================================

@pytest.fixture
def create_test_user(test_db: Session, test_tenant):
    """Factory fixture for creating test users with custom data.
    
    Returns:
        Callable: Function to create users
    """
    from app.db.models import User
    from bcrypt import hashpw, gensalt
    
    def _create_user(
        email: str = "user@example.com",
        password: str = "password123",
        tenant_id: str = None,
    ):
        if tenant_id is None:
            tenant_id = test_tenant.id
        
        hashed_password = hashpw(password.encode(), gensalt(rounds=10))
        
        user = User(
            email=email,
            password_hash=hashed_password,
            tenant_id=tenant_id,
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        return user
    
    return _create_user


@pytest.fixture
def create_test_tenant(test_db: Session):
    """Factory fixture for creating test tenants with custom data.
    
    Returns:
        Callable: Function to create tenants
    """
    from app.db.models import Tenant
    
    def _create_tenant(
        name: str = "Test Tenant",
    ):
        tenant = Tenant(
            name=name,
        )
        test_db.add(tenant)
        test_db.commit()
        test_db.refresh(tenant)
        return tenant
    
    return _create_tenant
