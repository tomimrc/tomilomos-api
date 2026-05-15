"""SQLAlchemy ORM models for TomiLomos API.

This is a placeholder file. Actual models (Tenant, User, Product, etc.) will be
defined in the change 'setup-multitenancy-auth' which includes comprehensive
multi-tenancy architecture and authentication models.

For now, we define minimal Tenant and User models required for the testing infrastructure.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Numeric, Boolean, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class Tenant(Base):
    """Tenant model representing a business/restaurant.
    
    Attributes:
        id: Unique tenant identifier
        name: Business name
        email: Business email
        created_at: Timestamp when tenant was created
    """
    __tablename__ = "tenants"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    users = relationship("User", back_populates="tenant")


class User(Base):
    """User model representing a person with access to the system.
    
    Attributes:
        id: Unique user identifier
        email: User email (unique per tenant)
        password_hash: Bcrypt-hashed password
        tenant_id: Foreign key to Tenant
        created_at: Timestamp when user was created
    """
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    tenant_id = Column(String(50), ForeignKey("tenants.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    tenant = relationship("Tenant", back_populates="users")


class RawMaterial(Base):
    """RawMaterial model representing an ingredient/raw ingredient in the inventory.
    
    Attributes:
        id: Unique raw material identifier (UUID)
        tenant_id: Foreign key to Tenant (multi-tenant isolation)
        name: Name of the raw material/ingredient
        unit_of_measurement: Unit type (kg, g, L, mL, units, pieces, boxes, etc.)
        cost_per_unit: Cost in home currency (DECIMAL(10,2) for precise monetary calculation)
        supplier: Optional supplier name or reference
        current_stock: Current quantity in inventory (DECIMAL(10,2), default 0)
        created_at: Timestamp when raw material was created
        updated_at: Timestamp when raw material was last updated
    """
    __tablename__ = "raw_materials"
    
    id = Column(String(50), primary_key=True, index=True)
    tenant_id = Column(String(50), ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    unit_of_measurement = Column(String(50), nullable=False)
    cost_per_unit = Column(Numeric(10, 2), nullable=False)
    supplier = Column(String(255), nullable=True)
    current_stock = Column(Numeric(10, 2), nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tenant = relationship("Tenant")


class Product(Base):
    """Product model representing a sellable item (final product).
    
    Attributes:
        id: Unique product identifier (UUID)
        tenant_id: Foreign key to Tenant (multi-tenant isolation)
        name: Product name (e.g., "Lomito Completo", "Papas")
        sale_price: Selling price (DECIMAL(10,2) for precise monetary calculation)
        is_active: Availability flag (True = active, False = inactive/hidden)
        recipe_id: Optional foreign key to Recipe (nullable for backward compatibility)
        created_at: Timestamp when product was created
        updated_at: Timestamp when product was last updated
    """
    __tablename__ = "products"
    
    id = Column(String(50), primary_key=True, index=True)
    tenant_id = Column(String(50), ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    sale_price = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    recipe_id = Column(String(50), ForeignKey("recipes.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tenant = relationship("Tenant")
    recipe = relationship("Recipe", back_populates="products")
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, recipe_id={self.recipe_id})>"


class Recipe(Base):
    """Recipe model representing a formula for combining raw materials into products.
    
    Attributes:
        id: Unique recipe identifier
        tenant_id: Foreign key to Tenant (multi-tenant isolation)
        name: Recipe name (unique within tenant)
        description: Optional recipe description
        created_at: Timestamp when recipe was created
        updated_at: Timestamp when recipe was last updated
    """
    __tablename__ = "recipes"
    
    id = Column(String(50), primary_key=True, index=True)
    tenant_id = Column(String(50), ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tenant = relationship("Tenant")
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="recipe")
    
    def __repr__(self) -> str:
        return f"<Recipe(id={self.id}, name={self.name}, tenant_id={self.tenant_id})>"


class RecipeIngredient(Base):
    """RecipeIngredient model representing a line item in a recipe.
    
    Attributes:
        id: Unique ingredient identifier
        recipe_id: Foreign key to Recipe (cascade delete)
        raw_material_id: Foreign key to RawMaterial
        quantity: Amount of raw material needed (DECIMAL(10,2))
        unit: Unit of measurement (inherited from raw material context)
        created_at: Timestamp when ingredient was added
        updated_at: Timestamp when ingredient was last updated
    """
    __tablename__ = "recipe_ingredients"
    
    id = Column(String(50), primary_key=True, index=True)
    recipe_id = Column(String(50), ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False, index=True)
    raw_material_id = Column(String(50), ForeignKey("raw_materials.id"), nullable=False, index=True)
    quantity = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    recipe = relationship("Recipe", back_populates="ingredients")
    raw_material = relationship("RawMaterial")
    
    def __repr__(self) -> str:
        return f"<RecipeIngredient(id={self.id}, recipe_id={self.recipe_id}, raw_material_id={self.raw_material_id})>"


class Sale(Base):
    """Sale model representing a registered sale transaction.
    
    When a sale is created for a product with a recipe, raw material stock
    is automatically deducted based on the recipe's ingredients.
    
    Prices and costs are frozen at the time of sale (snapshot) to maintain
    accurate financial history even if product prices change later.
    
    Attributes:
        id: Unique sale identifier (UUID)
        tenant_id: Foreign key to Tenant (multi-tenant isolation)
        product_id: Foreign key to Product sold
        quantity: Number of units sold (integer)
        unit_price: Sale price per unit at time of sale (DECIMAL 10,2 snapshot)
        total_price: unit_price × quantity (DECIMAL 10,2)
        total_cost: Recipe cost × quantity, or None if product has no recipe
        margin: total_price - total_cost, or None if no cost
        created_at: Timestamp when sale was registered
    """
    __tablename__ = "sales"

    id = Column(String(50), primary_key=True, index=True)
    tenant_id = Column(String(50), ForeignKey("tenants.id"), nullable=False, index=True)
    product_id = Column(String(50), ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    total_cost = Column(Numeric(10, 2), nullable=True)
    margin = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    tenant = relationship("Tenant")
    product = relationship("Product")

    def __repr__(self) -> str:
        return f"<Sale(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
