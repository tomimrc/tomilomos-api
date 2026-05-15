"""Database models for multi-tenant SaaS application."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, Boolean, Numeric, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Tenant(Base):
    """Represents an independent business unit in the SaaS application."""

    __tablename__ = "tenant"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Tenant id={self.id} name={self.name}>"


class User(Base):
    """Represents a user within a tenant."""

    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    tenant = relationship("Tenant", back_populates="users")

    # Constraints: email must be unique per (tenant_id, email)
    __table_args__ = (
        UniqueConstraint("tenant_id", "email", name="uq_tenant_email"),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} tenant_id={self.tenant_id}>"


class RawMaterial(Base):
    """Represents a raw material (ingredient) in the inventory."""

    __tablename__ = "raw_materials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    unit_of_measurement = Column(String(50), nullable=False)
    cost_per_unit = Column(Numeric(10, 2), nullable=False)
    supplier = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recipe_ingredients = relationship("RecipeIngredient", back_populates="raw_material", cascade="all, delete-orphan")

    # Constraints: name must be unique per tenant
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_tenant_raw_material_name"),
    )

    def __repr__(self) -> str:
        return f"<RawMaterial id={self.id} name={self.name} tenant_id={self.tenant_id}>"


class Recipe(Base):
    """Represents a recipe (formula for a product)."""

    __tablename__ = "recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="recipe")

    # Constraints: name must be unique per tenant
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_tenant_recipe_name"),
    )

    def __repr__(self) -> str:
        return f"<Recipe id={self.id} name={self.name} tenant_id={self.tenant_id}>"


class RecipeIngredient(Base):
    """Represents an ingredient in a recipe (many-to-many with quantity/unit)."""

    __tablename__ = "recipe_ingredients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    raw_material_id = Column(UUID(as_uuid=True), ForeignKey("raw_materials.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Numeric(10, 3), nullable=False)  # 3 decimal places for fractional quantities
    unit = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recipe = relationship("Recipe", back_populates="ingredients")
    raw_material = relationship("RawMaterial", back_populates="recipe_ingredients")

    # Constraints: raw_material must be unique per recipe
    __table_args__ = (
        UniqueConstraint("recipe_id", "raw_material_id", name="uq_recipe_raw_material"),
    )

    def __repr__(self) -> str:
        return f"<RecipeIngredient recipe_id={self.recipe_id} raw_material_id={self.raw_material_id} quantity={self.quantity}>"


class Product(Base):
    """Represents a sellable product (with optional recipe-based costing)."""

    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    sale_price = Column(Numeric(10, 2), nullable=False)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id", ondelete="SET NULL"), nullable=True, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recipe = relationship("Recipe", back_populates="products")

    # Constraints: name must be unique per tenant
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_tenant_product_name"),
        Index("ix_products_tenant_recipe", "tenant_id", "recipe_id"),  # Composite index for product cost queries
    )

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name} tenant_id={self.tenant_id}>"
