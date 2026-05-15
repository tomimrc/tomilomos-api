## 1. Database Setup

- [x] 1.1 Add RawMaterial ORM model to db/models.py with fields: id, tenant_id, name, unit_of_measurement, cost_per_unit, supplier, current_stock, created_at, updated_at
- [x] 1.2 Create Alembic migration to add raw_materials table with appropriate constraints and indexes
- [x] 1.3 Run migration against test database to verify schema

## 2. Schema Layer (Pydantic)

- [x] 2.1 Create schemas/raw_materials.py with RawMaterialCreate schema (name, unit_of_measurement, cost_per_unit, supplier optional)
- [x] 2.2 Create RawMaterialUpdate schema for PUT requests (all fields optional)
- [x] 2.3 Create RawMaterialRead schema for API responses (includes id, tenant_id, current_stock, timestamps)
- [x] 2.4 Add validation to schemas: cost_per_unit > 0, unit_of_measurement in valid list, name not empty

## 3. Repository Layer

- [x] 3.1 Create repositories/raw_materials_repository.py with class RawMaterialRepository
- [x] 3.2 Implement create(tenant_id, name, unit_of_measurement, cost_per_unit, supplier) method
- [x] 3.3 Implement get_by_id(tenant_id, raw_material_id) method
- [x] 3.4 Implement list_by_tenant(tenant_id, skip, limit) method for pagination
- [x] 3.5 Implement update(tenant_id, raw_material_id, **updates) method
- [x] 3.6 Implement delete(tenant_id, raw_material_id) method
- [x] 3.7 Implement add_stock(tenant_id, raw_material_id, quantity) method
- [x] 3.8 Implement remove_stock(tenant_id, raw_material_id, quantity) method - with validation for insufficient stock
- [x] 3.9 Implement get_stock(tenant_id, raw_material_id) method
- [x] 3.10 Ensure all queries enforce tenant_id isolation in WHERE clauses

## 4. Service Layer

- [x] 4.1 Create services/raw_materials_service.py with class RawMaterialService
- [x] 4.2 Implement create_raw_material(tenant_id, name, unit_of_measurement, cost_per_unit, supplier) - validate inputs, call repository
- [x] 4.3 Implement get_raw_material(tenant_id, raw_material_id) - call repository, handle not found
- [x] 4.4 Implement list_raw_materials(tenant_id, skip, limit) - call repository
- [x] 4.5 Implement update_raw_material(tenant_id, raw_material_id, **updates) - validate updates, call repository
- [x] 4.6 Implement delete_raw_material(tenant_id, raw_material_id) - call repository
- [x] 4.7 Implement add_stock(tenant_id, raw_material_id, quantity, reason) - validate quantity > 0, call repository
- [x] 4.8 Implement remove_stock(tenant_id, raw_material_id, quantity, reason) - validate quantity > 0 and stock available, call repository
- [x] 4.9 Implement get_stock(tenant_id, raw_material_id) - call repository
- [x] 4.10 Add error handling: 404 for missing raw materials, 400 for invalid inputs

## 5. API Router Layer

- [x] 5.1 Create api/raw_materials_router.py with APIRouter
- [x] 5.2 Implement POST /api/v1/raw-materials - create endpoint, extract tenant from JWT, return 201
- [x] 5.3 Implement GET /api/v1/raw-materials - list endpoint with pagination (skip, limit query params)
- [x] 5.4 Implement GET /api/v1/raw-materials/{id} - get single endpoint
- [x] 5.5 Implement PUT /api/v1/raw-materials/{id} - update endpoint
- [x] 5.6 Implement DELETE /api/v1/raw-materials/{id} - delete endpoint, return 204
- [x] 5.7 Implement POST /api/v1/raw-materials/{id}/add-stock - add stock endpoint with quantity and reason
- [x] 5.8 Implement POST /api/v1/raw-materials/{id}/remove-stock - remove stock endpoint with quantity and reason
- [x] 5.9 Implement GET /api/v1/raw-materials/{id}/stock - get stock level endpoint
- [x] 5.10 Add @router.get and @router.post decorators with proper status codes and responses
- [x] 5.11 All endpoints require authentication (Depends on JWT dependency)

## 6. Integration and Dependencies

- [x] 6.1 Import and mount raw_materials_router in main.py (app.include_router)
- [x] 6.2 Create or update the database session dependency for use in router
- [x] 6.3 Ensure FastAPI dependency injection is configured (DBSession, current_user)
- [x] 6.4 Verify imports: RawMaterial model, RawMaterialRepository, RawMaterialService, schemas

## 7. Testing

- [x] 7.1 Create tests/test_raw_materials.py with test fixtures
- [x] 7.2 Write unit tests for RawMaterialService (create, get, list, update, delete, add_stock, remove_stock)
- [x] 7.3 Write unit tests for RawMaterialRepository (same operations)
- [x] 7.4 Write integration tests for API endpoints (POST, GET, PUT, DELETE, stock operations)
- [x] 7.5 Test multi-tenant isolation: verify user from tenant A cannot access raw materials from tenant B
- [x] 7.6 Test validation: name required, cost_per_unit > 0, unit_of_measurement valid
- [x] 7.7 Test stock operations: add stock, remove stock, insufficient stock error
- [x] 7.8 Test decimal precision: cost_per_unit and current_stock maintain DECIMAL(10,2) precision
- [x] 7.9 Run all tests and ensure 100% pass

## 8. Documentation and Cleanup

- [x] 8.1 Update README.md to document raw materials module endpoints and usage
- [x] 8.2 Add docstrings to all public methods in service and repository
- [x] 8.3 Verify no hardcoded secrets or sensitive data in code
- [x] 8.4 Run code style checks (if applicable)
- [x] 8.5 Verify all imports are correct and no circular dependencies
- [x] 8.6 Create or update openapi.yaml spec with raw materials endpoints

## 9. Verification

- [x] 9.1 Run full test suite to confirm all tests pass
- [x] 9.2 Start application and verify health check works
- [x] 9.3 Test endpoints manually with curl or Postman
- [x] 9.4 Verify multi-tenant isolation with two different tenants
- [x] 9.5 Verify API documentation in /docs endpoint shows all raw materials endpoints
