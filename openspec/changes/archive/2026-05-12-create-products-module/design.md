## Context

TomiLomos is a multi-tenant SaaS for restaurant management built on Clean Architecture. The system needs a Products module to track sellable items (final products like "Lomito Completo", "Papas", etc.) as the foundation for recipes, sales registration, and profitability calculations.

**Current State:**
- Multi-tenancy model exists (Tenant and User models in db/models.py)
- Raw Materials module is complete and deployed (ingredients with cost tracking)
- Clean Architecture pattern established: Router → Service → Repository → ORM Model
- Database session management and dependency injection framework in place
- Project structure defines clear separation between API, services, repositories, and database layers

**Constraints:**
- MUST use DECIMAL(10,2) for sale_price to ensure monetary precision
- MUST enforce multi-tenant isolation via tenant_id on all records
- MUST NOT commit database transactions within the service layer
- All passwords and sensitive data managed via environment variables
- Products are simple containers for sale prices; stock is managed at raw material level (via recipes)

**Stakeholders:**
- Backend API developers implementing business logic
- Frontend team building product management UI
- Recipes module (downstream dependency) which will link products to raw materials
- Sales module which will register sales against products
- System administrators managing tenants

## Goals / Non-Goals

**Goals:**
- Establish the foundational products (sellable items) model with multi-tenant isolation
- Create CRUD APIs following Clean Architecture (Router → Service → Repository)
- Support price tracking with DECIMAL(10,2) precision for accurate revenue calculations
- Provide full product lifecycle management (create, read, update, delete) with is_active flag
- Enable product availability control (is_active for toggling availability without deletion)
- Ensure clean separation between products (output) and raw materials (input) domains

**Non-Goals:**
- Recipe creation or product-to-raw-material binding (future module: create-recipes-module)
- Sales registration (future module: register-sales-with-stock-deduction)
- Product categorization or hierarchies (future enhancement)
- Image/media management (future enhancement)
- Stock tracking at product level (stock is managed via recipes and raw materials)
- Product descriptions or rich metadata (future enhancement)
- Price history or versioning (future enhancement)
- Bulk operations or CSV import (future enhancement)

## Decisions

### Decision 1: Data Model Structure
**Choice:** Add `Product` ORM model with `tenant_id` foreign key

**Rationale:**
- Maintains multi-tenant isolation at the database level
- Follows the existing Tenant/User relationship pattern used in raw materials
- Ensures queries are naturally scoped to a single tenant
- Simple model (no inheritance or complex relationships at this stage)

**Alternatives Considered:**
- Row-level security policies in PostgreSQL: More complex, requires database-specific configuration
- Application-level filtering only: Risk of leaking data across tenants; less secure

**Fields included:**
- `id`: Primary key (String, generated UUID)
- `tenant_id`: Foreign key to Tenant (enforces isolation)
- `name`: Product name (String, not null, e.g., "Lomito Completo")
- `sale_price`: Selling price (DECIMAL(10,2), not null, must be > 0)
- `is_active`: Availability flag (Boolean, default true; allows soft lifecycle without deletion)
- `created_at`, `updated_at`: Timestamps for audit trail

### Decision 2: API Layer Organization
**Choice:** Single router file (`products_router.py`) handling all CRUD operations

**Rationale:**
- Follows the existing raw_materials_router.py pattern and health_router.py pattern
- All products endpoints grouped logically
- Easy to mount in main.py as a sub-router
- Minimal cognitive overhead

**Endpoints:**
```
POST   /api/v1/products              - Create
GET    /api/v1/products              - List (with pagination/filtering)
GET    /api/v1/products/{id}         - Get by ID
PUT    /api/v1/products/{id}         - Update
DELETE /api/v1/products/{id}         - Delete
```

### Decision 3: Service Layer Business Logic
**Choice:** Products service handles validation, data transformation, and business rules; repository handles persistence

**Rationale:**
- Aligns with Clean Architecture: services contain business logic, repositories are data access only
- Services validate inputs (e.g., sale_price > 0, name not empty)
- Repositories execute only queries and CRUD operations
- Makes testing easier: mock repositories, test business logic independently

**Service Responsibilities:**
- Validate input schemas
- Enforce business rules (e.g., price must be positive, name required)
- Transform data for storage/retrieval
- Handle errors gracefully

**Repository Responsibilities:**
- Execute database queries
- Manage product records
- Enforce tenant isolation at the query level

### Decision 4: Price Handling and Validation
**Choice:** Store `sale_price` as DECIMAL(10,2); validate in service layer that price > 0

**Rationale:**
- DECIMAL(10,2) prevents floating-point rounding errors in monetary calculations
- Consistent with raw materials cost_per_unit handling
- Supports prices up to 99,999,999.99 (sufficient for restaurant industry)
- Service-layer validation ensures business rule consistency

**Validation Rules:**
- price must be > 0 (no zero or negative prices)
- price must not exceed 99,999,999.99 (DECIMAL(10,2) max)
- price must be a valid decimal value

### Decision 5: Product Lifecycle via is_active Flag
**Choice:** Use `is_active` boolean flag; soft delete (no hard deletion from database)

**Rationale:**
- Allows toggling product availability without data loss
- Supports business case: temporarily hide products without destroying historical data
- Can be extended later with soft delete logic if needed
- Prevents accidental data loss

**Behavior:**
- `is_active=true` (default): Product is visible and available for recipes/sales
- `is_active=false`: Product is hidden; can be reactivated later
- DELETE endpoint can either hard-delete or set is_active=false (decision deferred to implementation)

### Decision 6: Multi-Tenant Isolation Implementation
**Choice:** Application-level filtering + database foreign key constraint on tenant_id

**Rationale:**
- Same approach as raw materials module (consistency)
- More portable than database policies
- Easier to test
- Less dependency on database-specific features

**Query Pattern:**
- All list/get/update/delete queries filter by `tenant_id` from authenticated user context
- Foreign key constraint ensures data integrity
- Repository layer enforces isolation on every query

## Risks / Trade-offs

**[Risk 1] Simple Data Model**
→ *Mitigation:* Design allows extending with descriptions, categories, images later without breaking changes. Non-Goals section explicit about deferrals.

**[Risk 2] No Price History**
→ *Mitigation:* For now, sale_price is current only. Recipes and sales reference this price at creation time. Document that price changes affect new recipes only. Future: implement versioned pricing if audit trail becomes critical.

**[Risk 3] Stock Not Managed at Product Level**
→ *Mitigation:* Stock is managed at raw materials level and derived from recipes. Products are simple price containers. This separation keeps concerns clean and prevents confusion.

**[Risk 4] Concurrent Updates on is_active**
→ *Mitigation:* Use database-level locking and transactional updates via SQLAlchemy. is_active is a simple boolean toggle, not a complex state machine. Future: implement event sourcing if audit trail becomes critical.

**Trade-off 1: Simplicity vs. Feature Completeness**
→ Prioritizing simplicity now (no categories, no descriptions, no media). Enables faster initial delivery. Features can be added in future sprints without breaking existing data.

**Trade-off 2: Hard Delete vs. Soft Delete**
→ Allowing both semantics (implementation choice during apply phase). Hard delete matches raw materials pattern; soft delete can be added later if needed.

## Migration Plan

**Phase 1: Database**
1. Add `Product` model to `db/models.py`
2. Generate and run Alembic migration to create `products` table

**Phase 2: API Layer**
1. Create `schemas/products.py` with Pydantic schemas (ProductCreate, ProductRead, ProductUpdate)
2. Create `services/products_service.py` with business logic
3. Create `repositories/products_repository.py` with database queries
4. Create `api/products_router.py` with endpoints
5. Mount router in `main.py`

**Phase 3: Testing & Documentation**
1. Write unit tests for service layer
2. Write integration tests for API endpoints
3. Update API documentation in openapi.yaml

**Deployment:**
- Backward compatible: no breaking changes to existing APIs
- Rollback: drop `products` table (no data dependencies yet; recipes module will add dependency later)

## Open Questions

1. **Should we implement role-based permissions (admin-only for create/delete)?** → Defer to auth module; assume all authenticated users can manage products for their tenant for now.
2. **Should we support bulk operations (create/update multiple at once)?** → Start with single operations; add batch endpoints if needed.
3. **Do we need audit logging (who created/modified each product)?** → Not for MVP; can be added via middleware later.
4. **Should DELETE be hard delete or soft delete (set is_active=false)?** → Default to hard delete to match raw materials; can revisit based on business needs.
5. **Should we add product descriptions or additional metadata now?** → No; keep it minimal for MVP. Can be added as extension without breaking existing records.
