## 1. Fix broken test imports and infrastructure

- [ ] 1.1 Update `tests/conftest.py`: replace placeholder auth fixtures with real JWT token generation and authenticated test client
- [ ] 1.2 Update `tests/test_auth_flow.py`: fix imports to use `app.core.jwt_handler`, `app.core.security`, `db.models`
- [ ] 1.3 Update `tests/test_auth_service.py`: fix imports to use `app.services.auth_service`, `db.models`
- [ ] 1.4 Update `tests/test_jwt_handler.py`: fix imports to use `app.core.jwt_handler`
- [ ] 1.5 Update `tests/test_security.py`: fix imports to use `app.core.security`
- [ ] 1.6 Update `tests/test_protected_endpoints.py`: rewrite to use real JWT auth instead of placeholder mocks

## 2. Fix CRUD test imports

- [ ] 2.1 Update `tests/test_raw_materials.py`: fix imports, replace placeholder tenant fixtures with real JWT auth
- [ ] 2.2 Update `tests/test_products.py`: fix imports, replace placeholder tenant fixtures with real JWT auth
- [ ] 2.3 Update `tests/test_recipes.py`: fix imports, replace placeholder tenant fixtures with real JWT auth
- [ ] 2.4 Update `tests/test_product_cost.py`: fix imports, replace placeholder tenant fixtures with real JWT auth
- [ ] 2.5 Update `tests/test_health.py` and `tests/test_config.py`: verify they still work (no auth dependency)

## 3. Add test fixtures and seed data

- [ ] 3.1 Create `conftest.py` fixture: `test_db_session` — isolated SQLite/PostgreSQL session per test
- [ ] 3.2 Create `conftest.py` fixture: `test_tenant` — pre-seeded tenant in test database
- [ ] 3.3 Create `conftest.py` fixture: `test_user` — pre-seeded user with known password in test tenant
- [ ] 3.4 Create `conftest.py` fixture: `auth_token` — valid JWT token for test user
- [ ] 3.5 Create `conftest.py` fixture: `authenticated_client` — httpx TestClient with Bearer token
- [ ] 3.6 Create `conftest.py` fixture: `seeded_raw_material` — pre-seeded raw material for testing
- [ ] 3.7 Create `conftest.py` fixture: `seeded_product` — pre-seeded product for testing
- [ ] 3.8 Create `conftest.py` fixture: `seeded_recipe` — pre-seeded recipe with ingredients for testing

## 4. Write unit tests

- [ ] 4.1 Write AuthService unit tests: login, authenticate_user, create_user, create_tenant, generate_tokens
- [ ] 4.2 Write RawMaterialService unit tests: create, list, get, update, delete, add_stock, remove_stock
- [ ] 4.3 Write ProductService unit tests: create, list, get, update, delete
- [ ] 4.4 Write RecipeService unit tests: create, list, get, update, delete, add_ingredient, calculate_cost
- [ ] 4.5 Write SaleService unit tests: create_sale with stock deduction, list_sales
- [ ] 4.6 Write UserRepository unit tests: get_user_by_email, create_user
- [ ] 4.7 Write TenantRepository unit tests: create_tenant, get_tenant_by_id

## 5. Write integration tests

- [ ] 5.1 Write auth flow integration test: login → get token → access protected endpoint
- [ ] 5.2 Write multi-tenant isolation test: Tenant A cannot see Tenant B's data
- [ ] 5.3 Write raw materials CRUD integration test with real auth
- [ ] 5.4 Write products CRUD integration test with real auth
- [ ] 5.5 Write recipes CRUD integration test with real auth
- [ ] 5.6 Write sales integration test: create sale → verify stock deduction
- [ ] 5.7 Write product cost integration test: verify cost calculation via API

## 6. Verify and measure coverage

- [ ] 6.1 Run full test suite: `pytest tests/ -v` — all tests pass
- [ ] 6.2 Run coverage report: `pytest tests/ --cov=. --cov-report=term-missing`
- [ ] 6.3 Verify ≥80% coverage on critical paths: auth, stock deduction, multi-tenant isolation
- [ ] 6.4 Fix any failing tests or coverage gaps
