## 1. Data Model

- [x] 1.1 Add `Sale` class to `db/models.py` — SQLAlchemy model with table `sales`, columns: id (String(50) PK), tenant_id (FK→tenants), product_id (FK→products), quantity (Integer), unit_price (Numeric 10,2), total_price (Numeric 10,2), total_cost (Numeric 10,2 nullable), margin (Numeric 10,2 nullable), created_at (DateTime). Relationships to Tenant and Product.

## 2. Schemas

- [x] 2.1 Create `schemas/sales.py` — `SaleCreate` (product_id: str, quantity: int with validator > 0), `SaleRead` (id, tenant_id, product_id, product_name, quantity, unit_price, total_price, total_cost, margin, created_at). Config from_attributes on SaleRead.

## 3. Repository

- [x] 3.1 Create `repositories/sales_repository.py` — `SaleRepository` class with:
  - `create(tenant_id, product_id, quantity, unit_price, total_price, total_cost, margin, sale_id)` — creates Sale, returns ORM instance
  - `get_by_id(tenant_id, sale_id)` — get sale scoped to tenant
  - `list_by_tenant(tenant_id, skip, limit)` — paginated list ordered by created_at DESC
  - All methods use `session.flush()` only

## 4. Service

- [x] 4.1 Create `services/sales_service.py` — `SaleService` class with:
  - `create_sale(tenant_id, data: SaleCreate)` — full flow:
    a. Validate product exists and is_active via ProductRepository
    b. Freeze unit_price = product.sale_price, total_price = unit_price × quantity
    c. If product has recipe_id: call RecipeService.calculate_recipe_cost(), set total_cost = cost × quantity, margin = total_price - total_cost, iterate recipe ingredients and call RawMaterialService.remove_stock() for each
    d. If product has no recipe: total_cost = None, margin = None
    e. Create Sale via repository
    f. Return SaleRead with product_name
  - `get_sale(tenant_id, sale_id)` — get sale, enrich with product_name
  - `list_sales(tenant_id, skip, limit)` — list sales, enrich each with product_name
  - Use lazy imports for RecipeService and RawMaterialService to avoid circular imports
  - Generate UUID for sale_id
- [x] 4.2 Handle stock deduction edge cases: insufficient stock raises ValueError with descriptive message identifying the raw material

## 5. Router

- [x] 5.1 Create `api/sales_router.py` — FastAPI APIRouter with:
  - `POST /api/v1/sales` — accepts SaleCreate, returns SaleRead (201). Validates quantity > 0. Handles ValueError → 400, product not found → 400, Exception → 500. Calls db.commit() on success, db.rollback() on error.
  - `GET /api/v1/sales` — accepts ?skip=0&limit=50, returns List[SaleRead]
  - `GET /api/v1/sales/{sale_id}` — returns SaleRead or 404
  - Uses `get_tenant_id_placeholder` dependency (same pattern as existing routers)

## 6. Integration

- [x] 6.1 Register sales router in `main.py` — add `from api import sales_router` and `app.include_router(sales_router.router)`

## 7. Migration

- [x] 7.1 Generate Alembic migration for sales table — `alembic revision --autogenerate -m "add sales table"` and verify the migration file
