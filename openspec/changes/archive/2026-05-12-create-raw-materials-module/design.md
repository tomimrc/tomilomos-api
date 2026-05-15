## Context

TomiLomos is a multi-tenant SaaS for restaurant management built on Clean Architecture. The system needs a Raw Materials module to track ingredients as the foundation for recipe costing and inventory management.

**Current State:**
- Multi-tenancy model exists (Tenant and User models in db/models.py)
- Clean Architecture pattern established: Router → Service → Repository → ORM Model
- Database session management and dependency injection framework in place
- Project structure defines clear separation between API, services, repositories, and database layers

**Constraints:**
- MUST use DECIMAL(10,2) for cost-per-unit to ensure monetary precision
- MUST enforce multi-tenant isolation via tenant_id on all records
- MUST NOT commit database transactions within the service layer
- Stock operations MUST be atomic to prevent inventory inconsistencies
- All passwords and sensitive data managed via environment variables

**Stakeholders:**
- Backend API developers implementing business logic
- Frontend team building raw materials inventory UI
- Recipe and product costing modules (downstream dependencies)
- System administrators managing tenants

## Goals / Non-Goals

**Goals:**
- Establish the foundational raw materials inventory model with multi-tenant isolation
- Create CRUD APIs following Clean Architecture (Router → Service → Repository)
- Support diverse units of measurement (kg, L, units, pieces, etc.)
- Enable cost tracking (cost per unit) for product profitability calculations
- Provide full inventory lifecycle management (create, read, update, delete)
- Ensure atomic stock operations to maintain data consistency

**Non-Goals:**
- Recipe creation or ingredient-to-recipe binding (future module: create-recipes-module)
- Supplier management or purchase order integration (future enhancement)
- Stock reorder alerts or forecasting (future analytics module)
- Barcode scanning or external integrations
- Historical cost tracking or audit trails for price changes

## Decisions

### Decision 1: Data Model Structure
**Choice:** Add `RawMaterial` ORM model with `tenant_id` foreign key

**Rationale:**
- Maintains multi-tenant isolation at the database level
- Follows the existing Tenant/User relationship pattern
- Ensures queries are naturally scoped to a single tenant

**Alternatives Considered:**
- Row-level security policies in PostgreSQL: More complex, requires database-specific configuration
- Application-level filtering only: Risk of leaking data across tenants; less secure

**Fields included:**
- `id`: Primary key (String, generated UUID)
- `tenant_id`: Foreign key to Tenant (enforces isolation)
- `name`: Ingredient name (String, not null)
- `unit_of_measurement`: Unit type (String, e.g., "kg", "L", "units")
- `cost_per_unit`: Cost in home currency (DECIMAL(10,2), not null)
- `supplier`: Optional supplier name or reference (String, nullable)
- `current_stock`: Current quantity in inventory (DECIMAL(10,2), default 0)
- `created_at`, `updated_at`: Timestamps for audit trail

### Decision 2: API Layer Organization
**Choice:** Single router file (`raw_materials_router.py`) handling all CRUD operations

**Rationale:**
- Follows the existing health_router.py pattern
- All raw materials endpoints grouped logically
- Easy to mount in main.py as a sub-router
- Minimal cognitive overhead

**Endpoints:**
```
POST   /api/v1/raw-materials              - Create
GET    /api/v1/raw-materials              - List (with pagination/filtering)
GET    /api/v1/raw-materials/{id}         - Get by ID
PUT    /api/v1/raw-materials/{id}         - Update
DELETE /api/v1/raw-materials/{id}         - Delete
```

### Decision 3: Service Layer Business Logic
**Choice:** Raw materials service handles validation, data transformation, and business rules; repository handles persistence

**Rationale:**
- Aligns with Clean Architecture: services contain business logic, repositories are data access only
- Services validate inputs (e.g., cost_per_unit > 0, unit_of_measurement valid)
- Repositories execute only queries and CRUD operations
- Makes testing easier: mock repositories, test business logic independently

**Service Responsibilities:**
- Validate input schemas
- Enforce business rules (e.g., cost must be positive)
- Transform data for storage/retrieval
- Handle errors gracefully

**Repository Responsibilities:**
- Execute database queries
- Manage raw material records
- Enforce tenant isolation at the query level

### Decision 4: Stock Management Strategy
**Choice:** Store `current_stock` in the RawMaterial record; updates are handled via service layer with explicit stock adjustment methods

**Rationale:**
- Simple, queryable stock levels for dashboard/reporting
- Service layer can implement business logic for stock adjustments (e.g., check minimum stock, prevent negative stock)
- Supports atomic operations through database constraints and session management
- Ready for future: purchase orders, stock movement auditing

**Stock Operations:**
- Add stock: `adjust_stock(raw_material_id, +quantity)`
- Remove stock: `adjust_stock(raw_material_id, -quantity)` (used by sales, recipes)
- Check stock: `get_current_stock(raw_material_id)`

### Decision 5: Unit of Measurement Handling
**Choice:** Store as flexible string field with validation; no separate enum table

**Rationale:**
- Simplifies initial implementation
- Allows tenants flexibility in units (different regions, industries)
- Can add strict enum/validation later without migration
- Avoids unnecessary foreign key relationships

**Validation Rule:** Unit must be one of: kg, g, L, mL, units, pieces, boxes, etc.

## Risks / Trade-offs

**[Risk 1] Stock Consistency with Concurrent Updates**
→ *Mitigation:* Use database-level locking and transactional updates via SQLAlchemy. Service layer manages adjustments atomically. Future: implement event sourcing if audit trail becomes critical.

**[Risk 2] Cost Changes and Historical Tracking**
→ *Mitigation:* For now, cost_per_unit is current only. Products/recipes using this cost reference it at creation time. Document that cost changes affect new products only. Future: implement versioned costing or historical audit.

**[Risk 3] Unlimited Stock Quantities**
→ *Mitigation:* DECIMAL(10,2) supports up to 99,999,999.99 units; sufficient for most restaurants. Add alert if stock reaches unrealistic values in future.

**[Risk 4] Supplier Management Underspecified**
→ *Mitigation:* Supplier is a simple string field for now. Can evolve to a separate Supplier model with foreign key later without breaking existing data.

**Trade-off 1: Simplicity vs. Feature Completeness**
→ Prioritizing simplicity now (no historical cost tracking, no advanced stock forecasting). Enables faster initial delivery. Features can be added in future sprints.

**Trade-off 2: Tenant Isolation Strategy**
→ Using application-level filtering + foreign key constraint (vs. database policies). Slightly more work in queries, but more portable and easier to test.

## Migration Plan

**Phase 1: Database**
1. Add `RawMaterial` model to `db/models.py`
2. Generate and run Alembic migration to create `raw_materials` table

**Phase 2: API Layer**
1. Create `schemas/raw_materials.py` with Pydantic schemas (RawMaterialCreate, RawMaterialRead, etc.)
2. Create `services/raw_materials_service.py` with business logic
3. Create `repositories/raw_materials_repository.py` with database queries
4. Create `api/raw_materials_router.py` with endpoints
5. Mount router in `main.py`

**Phase 3: Testing & Documentation**
1. Write unit tests for service layer
2. Write integration tests for API endpoints
3. Update API documentation in README

**Deployment:**
- Backward compatible: no breaking changes to existing APIs
- Rollback: drop `raw_materials` table (no data dependencies yet)

## Open Questions

1. **Should we implement role-based permissions (admin-only for create/delete)?** → Defer to auth module; assume all authenticated users can manage raw materials for now.
2. **Should we support bulk operations (create/update multiple at once)?** → Start with single operations; add batch endpoints if needed.
3. **Do we need audit logging (who created/modified each raw material)?** → Not for MVP; can be added via middleware later.
4. **Should stock adjustments trigger events/webhooks?** → Out of scope for this module; can be added as a separate pubsub system later.
