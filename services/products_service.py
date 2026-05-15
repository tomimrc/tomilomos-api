"""Service layer for products business logic.

This layer contains all business logic for products operations.
Repositories handle persistence; services handle validation and orchestration.
"""

from decimal import Decimal
from typing import Optional, List
import uuid

from sqlalchemy.orm import Session

from repositories.products_repository import ProductRepository
from schemas.products import (
    ProductCreate,
    ProductUpdate,
    ProductRead,
)
from db.models import Product


class ProductService:
    """Service for products business logic."""
    
    def __init__(self, session: Session):
        """Initialize the service with a database session.
        
        Args:
            session: SQLAlchemy session for database operations
        """
        self.repository = ProductRepository(session)
        self.session = session
    
    def _calculate_product_cost_price(
        self,
        tenant_id: str,
        recipe_id: Optional[str]
    ) -> Optional[Decimal]:
        """Calculate cost_price for a product based on its recipe.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe (if any)
            
        Returns:
            Decimal cost_price or None if no recipe_id
            
        Raises:
            Exception: If recipe calculation fails
        """
        if not recipe_id:
            return None
        
        # Import here to avoid circular imports
        from services.recipe_service import RecipeService
        
        recipe_service = RecipeService(self.session)
        try:
            cost_response = recipe_service.calculate_recipe_cost(tenant_id, recipe_id)
            return cost_response.total_cost
        except Exception as e:
            # If recipe doesn't exist or calculation fails, return None
            # (cost_price is optional in the response)
            return None
    
    def _enrich_product_with_cost(
        self,
        product: Product,
        tenant_id: str
    ) -> ProductRead:
        """Convert Product to ProductRead, calculating cost_price if recipe_id is set.
        
        Args:
            product: Product ORM model
            tenant_id: Tenant ID for cost calculations
            
        Returns:
            ProductRead schema with calculated cost_price if applicable
        """
        product_read = ProductRead.from_orm(product)
        
        # Calculate cost_price if recipe_id is set
        if product.recipe_id:
            try:
                cost_price = self._calculate_product_cost_price(tenant_id, product.recipe_id)
                product_read.cost_price = cost_price
            except Exception:
                # If cost calculation fails, leave cost_price as None
                # (non-critical, product data is still valid)
                pass
        
        return product_read
    
    def create_product(
        self,
        tenant_id: str,
        data: ProductCreate
    ) -> ProductRead:
        """Create a new product with validation.
        
        Args:
            tenant_id: ID of the tenant
            data: ProductCreate schema with validated data
            
        Returns:
            ProductRead schema with created data
            
        Raises:
            ValueError: If validation fails
        """
        # Generate UUID for product
        product_id = str(uuid.uuid4())
        
        # Create via repository
        product = self.repository.create(
            tenant_id=tenant_id,
            name=data.name,
            sale_price=data.sale_price,
            is_active=data.is_active,
            product_id=product_id,
            recipe_id=data.recipe_id
        )
        
        return self._enrich_product_with_cost(product, tenant_id)
    
    def get_product(
        self,
        tenant_id: str,
        product_id: str
    ) -> Optional[ProductRead]:
        """Get a product by ID.
        
        Args:
            tenant_id: ID of the tenant
            product_id: ID of the product
            
        Returns:
            ProductRead schema or None if not found
        """
        product = self.repository.get_by_id(tenant_id, product_id)
        if not product:
            return None
        return self._enrich_product_with_cost(product, tenant_id)
    
    def list_products(
        self,
        tenant_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductRead]:
        """List products for a tenant with pagination.
        
        Args:
            tenant_id: ID of the tenant
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of ProductRead schemas
        """
        products = self.repository.list_by_tenant(tenant_id, skip, limit)
        return [self._enrich_product_with_cost(p, tenant_id) for p in products]
    
    def update_product(
        self,
        tenant_id: str,
        product_id: str,
        data: ProductUpdate
    ) -> Optional[ProductRead]:
        """Update a product with validation.
        
        Args:
            tenant_id: ID of the tenant
            product_id: ID of the product
            data: ProductUpdate schema with validated data
            
        Returns:
            ProductRead schema or None if not found
            
        Raises:
            ValueError: If validation fails
        """
        # Prepare updates dictionary (exclude None values)
        updates = {}
        if data.name is not None:
            updates['name'] = data.name
        if data.sale_price is not None:
            updates['sale_price'] = data.sale_price
        if data.is_active is not None:
            updates['is_active'] = data.is_active
        if data.recipe_id is not None:
            updates['recipe_id'] = data.recipe_id
        
        if not updates:
            # If no updates provided, just return current state
            return self.get_product(tenant_id, product_id)
        
        product = self.repository.update(tenant_id, product_id, **updates)
        if not product:
            return None
        return self._enrich_product_with_cost(product, tenant_id)
    
    def delete_product(self, tenant_id: str, product_id: str) -> bool:
        """Delete a product.
        
        Args:
            tenant_id: ID of the tenant
            product_id: ID of the product
            
        Returns:
            True if deleted, False if not found
        """
        return self.repository.delete(tenant_id, product_id)
