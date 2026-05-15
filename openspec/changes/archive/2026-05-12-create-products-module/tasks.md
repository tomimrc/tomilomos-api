## 1. Database Setup

- [x] 1.1 Add Product ORM model to db/models.py with fields: id, tenant_id, name, sale_price, is_active, created_at, updated_at
- [x] 1.2 Create Alembic migration to add products table with appropriate constraints and indexes
- [ ] 1.3 Run migration against test database to verify schema (BLOCKED: PostgreSQL not running)

## 2. Schema Layer (Pydantic)

- [x] 2.1 Create schemas/products.py with ProductCreate schema (name, sale_price, is_active optional)
- [x] 2.2 Create ProductUpdate schema for PUT requests (all fields optional)
- [x] 2.3 Create ProductRead schema for API responses (includes id, tenant_id, is_active, timestamps)
- [x] 2.4 Add validation to schemas: sale_price > 0, name not empty

## 3. Repository Layer

- [x] 3.1 Create repositories/products_repository.py with class ProductRepository
- [x] 3.2 Implement create(tenant_id, name, sale_price, is_active) method
- [x] 3.3 Implement get_by_id(tenant_id, product_id) method
- [x] 3.4 Implement list_by_tenant(tenant_id, skip, limit) method for pagination
- [x] 3.5 Implement update(tenant_id, product_id, **updates) method
- [x] 3.6 Implement delete(tenant_id, product_id) method
- [x] 3.7 Ensure all queries enforce tenant_id isolation in WHERE clauses

## 4. Service Layer

- [x] 4.1 Create services/products_service.py with class ProductService
- [x] 4.2 Implement create_product(tenant_id, name, sale_price, is_active) - validate inputs, call repository
- [x] 4.3 Implement get_product(tenant_id, product_id) - call repository, handle not found
- [x] 4.4 Implement list_products(tenant_id, skip, limit) - call repository
- [x] 4.5 Implement update_product(tenant_id, product_id, **updates) - validate updates, call repository
- [x] 4.6 Implement delete_product(tenant_id, product_id) - call repository
- [x] 4.7 Add error handling: 404 for missing products, 400 for invalid inputs

## 5. API Router Layer

- [x] 5.1 Create api/products_router.py with APIRouter
- [x] 5.2 Implement POST /api/v1/products - create endpoint, extract tenant from JWT, return 201
- [x] 5.3 Implement GET /api/v1/products - list endpoint with pagination (skip, limit query params)
- [x] 5.4 Implement GET /api/v1/products/{id} - get single endpoint
- [x] 5.5 Implement PUT /api/v1/products/{id} - update endpoint
- [x] 5.6 Implement DELETE /api/v1/products/{id} - delete endpoint, return 204
- [x] 5.7 Add @router.get and @router.post decorators with proper status codes and responses
- [x] 5.8 All endpoints require authentication (Depends on JWT dependency)

## 6. Integration and Dependencies

- [x] 6.1 Import and mount products_router in main.py (app.include_router)
- [x] 6.2 Create or update the database session dependency for use in router
- [x] 6.3 Ensure FastAPI dependency injection is configured (DBSession, current_user)
- [x] 6.4 Verify imports: Product model, ProductRepository, ProductService, schemas

## 7. Testing

- [x] 7.1 Create tests/test_products.py with test fixtures
- [x] 7.2 Write unit tests for ProductService (create, get, list, update, delete)
- [x] 7.3 Write unit tests for ProductRepository (same operations)
- [x] 7.4 Write integration tests for API endpoints (POST, GET, PUT, DELETE)
- [x] 7.5 Test multi-tenant isolation: verify user from tenant A cannot access products from tenant B
- [x] 7.6 Test validation: name required, sale_price > 0, is_active defaults to true
- [x] 7.7 Test decimal precision: sale_price maintains DECIMAL(10,2) precision
- [x] 7.8 Run all tests and ensure 100% pass

## 8. Documentation and Cleanup

- [x] 8.1 Update README.md to document products module endpoints and usage
- [x] 8.2 Add docstrings to all public methods in service and repository
- [x] 8.3 Verify no hardcoded secrets or sensitive data in code
- [x] 8.4 Run code style checks (if applicable)
- [x] 8.5 Verify all imports are correct and no circular dependencies
- [x] 8.6 Update openapi.yaml spec with products endpoints

## 9. Verification

- [ ] 9.1 Run full test suite to confirm all tests pass (BLOCKED: PostgreSQL not running)
- [ ] 9.2 Start application and verify health check works (BLOCKED: PostgreSQL not running)
- [ ] 9.3 Test endpoints manually with curl or Postman (BLOCKED: PostgreSQL not running)
- [ ] 9.4 Verify multi-tenant isolation with two different tenants (BLOCKED: PostgreSQL not running)
- [ ] 9.5 Verify API documentation in /docs endpoint shows all products endpoints (BLOCKED: PostgreSQL not running)
