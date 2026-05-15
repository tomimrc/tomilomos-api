"""Service layer for sales business logic.

This layer orchestrates sale creation with automatic stock deduction
from raw materials based on the product's recipe ingredients.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, List
import uuid

from sqlalchemy.orm import Session

from repositories.sales_repository import SaleRepository
from repositories.products_repository import ProductRepository
from schemas.sales import SaleCreate, SaleRead
from db.models import Sale


class SaleService:
    """Service for sales business logic."""
    
    def __init__(self, session: Session):
        """Initialize the service with a database session.
        
        Args:
            session: SQLAlchemy session for database operations
        """
        self.repository = SaleRepository(session)
        self.product_repository = ProductRepository(session)
        self.session = session
    
    def _deduct_recipe_stock(
        self,
        tenant_id: str,
        recipe_id: str,
        quantity: int,
        sale_id: str,
    ) -> Decimal:
        """Deduct raw material stock for each ingredient in the recipe.
        
        Args:
            tenant_id: ID of the tenant
            recipe_id: ID of the recipe
            quantity: Sale quantity (multiplier for ingredient amounts)
            sale_id: Sale ID for the deduction reason
            
        Returns:
            Total cost of the recipe (cost per unit × quantity)
            
        Raises:
            ValueError: If a raw material has insufficient stock
        """
        # Lazy imports to avoid circular dependencies
        from services.recipe_service import RecipeService
        from services.raw_materials_service import RawMaterialService
        
        recipe_service = RecipeService(self.session)
        raw_material_service = RawMaterialService(self.session)
        
        # Calculate recipe cost and get ingredient list
        cost_response = recipe_service.calculate_recipe_cost(tenant_id, recipe_id)
        
        # Deduct stock for each ingredient proportionally
        for ingredient in cost_response.ingredients:
            deduction_quantity = (ingredient.quantity * quantity).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            
            reason = f"Sale: {sale_id}"
            
            try:
                raw_material_service.remove_stock(
                    tenant_id=tenant_id,
                    raw_material_id=ingredient.raw_material_id,
                    quantity=deduction_quantity,
                    reason=reason,
                )
            except ValueError as e:
                # Enrich error with raw material name for the API response
                raise ValueError(
                    f"Insufficient stock for {ingredient.raw_material_name}: "
                    f"need {deduction_quantity}, have (see current_stock)"
                ) from e
        
        return cost_response.total_cost
    
    def create_sale(
        self,
        tenant_id: str,
        data: SaleCreate,
    ) -> SaleRead:
        """Create a new sale with automatic stock deduction.
        
        Args:
            tenant_id: ID of the tenant
            data: SaleCreate schema with product_id and quantity
            
        Returns:
            SaleRead schema with created data
            
        Raises:
            ValueError: If product not found, not active, or stock insufficient
        """
        # 1. Validate product exists and is active
        product = self.product_repository.get_by_id(tenant_id, data.product_id)
        if not product:
            raise ValueError("Product not found")
        if not product.is_active:
            raise ValueError("Product not found or inactive")
        
        # 2. Freeze pricing at time of sale
        unit_price = product.sale_price
        total_price = (unit_price * data.quantity).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        # 3. Generate sale ID
        sale_id = str(uuid.uuid4())
        
        # 4. Calculate cost and deduct stock if recipe exists
        total_cost: Optional[Decimal] = None
        margin: Optional[Decimal] = None
        
        if product.recipe_id:
            # Deduct stock and get recipe cost
            recipe_unit_cost = self._deduct_recipe_stock(
                tenant_id=tenant_id,
                recipe_id=product.recipe_id,
                quantity=data.quantity,
                sale_id=sale_id,
            )
            total_cost = (recipe_unit_cost * data.quantity).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            margin = (total_price - total_cost).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        
        # 5. Create sale record
        sale = self.repository.create(
            tenant_id=tenant_id,
            product_id=data.product_id,
            quantity=data.quantity,
            unit_price=unit_price,
            total_price=total_price,
            total_cost=total_cost,
            margin=margin,
            sale_id=sale_id,
        )
        
        # 6. Build response with product_name
        return SaleRead(
            id=sale.id,
            tenant_id=sale.tenant_id,
            product_id=sale.product_id,
            product_name=product.name,
            quantity=sale.quantity,
            unit_price=sale.unit_price,
            total_price=sale.total_price,
            total_cost=sale.total_cost,
            margin=sale.margin,
            created_at=sale.created_at,
        )
    
    def get_sale(
        self,
        tenant_id: str,
        sale_id: str,
    ) -> Optional[SaleRead]:
        """Get a sale by ID with product name.
        
        Args:
            tenant_id: ID of the tenant
            sale_id: ID of the sale
            
        Returns:
            SaleRead schema or None if not found
        """
        sale = self.repository.get_by_id(tenant_id, sale_id)
        if not sale:
            return None
        
        product = self.product_repository.get_by_id(tenant_id, sale.product_id)
        
        return SaleRead(
            id=sale.id,
            tenant_id=sale.tenant_id,
            product_id=sale.product_id,
            product_name=product.name if product else "Unknown",
            quantity=sale.quantity,
            unit_price=sale.unit_price,
            total_price=sale.total_price,
            total_cost=sale.total_cost,
            margin=sale.margin,
            created_at=sale.created_at,
        )
    
    def list_sales(
        self,
        tenant_id: str,
        skip: int = 0,
        limit: int = 50,
    ) -> List[SaleRead]:
        """List sales for a tenant with pagination.
        
        Args:
            tenant_id: ID of the tenant
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of SaleRead schemas, newest first
        """
        sales = self.repository.list_by_tenant(tenant_id, skip, limit)
        
        # Batch-fetch products for names
        product_ids = {s.product_id for s in sales}
        products = {}
        for pid in product_ids:
            p = self.product_repository.get_by_id(tenant_id, pid)
            if p:
                products[pid] = p.name
        
        return [
            SaleRead(
                id=s.id,
                tenant_id=s.tenant_id,
                product_id=s.product_id,
                product_name=products.get(s.product_id, "Unknown"),
                quantity=s.quantity,
                unit_price=s.unit_price,
                total_price=s.total_price,
                total_cost=s.total_cost,
                margin=s.margin,
                created_at=s.created_at,
            )
            for s in sales
        ]
