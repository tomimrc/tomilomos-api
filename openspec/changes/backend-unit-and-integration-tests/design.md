## Context

The project has 13 test files in `tests/` that were written against a placeholder auth system. After `implement-real-auth-login`, all imports are broken and the test fixtures use mocked authentication that doesn't match the real JWT flow. The test infrastructure needs a complete overhaul to work with real auth.

Current test files:
- `test_auth_flow.py`, `test_auth_service.py`, `test_jwt_handler.py`, `test_security.py` — auth tests (need real JWT)
- `test_protected_endpoints.py` — tests placeholder auth (needs complete rewrite)
- `test_raw_materials.py`, `test_products.py`, `test_recipes.py`, `test_product_cost.py` — CRUD tests (need auth fixtures)
- `test_config.py`, `test_health.py` — infrastructure tests (likely still work)

## Goals / Non-Goals

**Goals:**
- All tests pass with real JWT authentication
- Test fixtures provide authenticated test client, seeded tenant/user, and isolated database
- ≥80% coverage on critical paths (auth, stock, multi-tenant isolation)
- Tests run against both SQLite (fast, local) and PostgreSQL (CI, production-like)

**Non-Goals:**
- Frontend tests (separate change)
- Load/performance testing
- Mocking external services (no external dependencies yet)

## Decisions

### Decision 1: Use httpx TestClient with real JWT middleware

**Choice**: Use `httpx.TestClient` (FastAPI's recommended test client) with the real `create_app()` from `main.py`, including full JWT validation middleware.

**Why**: Tests the real auth stack end-to-end. No mocking of authentication means tests catch real integration bugs.

**Alternatives considered**:
- Mock the auth dependency: faster tests but doesn't catch integration issues
- Skip auth in tests: defeats the purpose of testing protected endpoints

### Decision 2: SQLite for unit tests, PostgreSQL for integration tests

**Choice**: Use in-memory SQLite for fast unit tests (services, repositories). Use PostgreSQL (via Docker or env var) for integration tests that need full DB features.

**Why**: SQLite is fast and doesn't require external setup. Some PostgreSQL-specific features (UUID, specific types) may not work in SQLite, so integration tests need real PostgreSQL.

### Decision 3: Seed test data via fixtures, not migration scripts

**Choice**: Create test tenant, user, raw materials, products, and recipes in `conftest.py` fixtures that run before each test session.

**Why**: Fixtures are isolated per test run, don't pollute the database, and are easy to reason about. Migration scripts are for production schema evolution, not test data.

## Risks / Trade-offs

### Risk: SQLite doesn't support all PostgreSQL types
**Mitigation**: Use String(50) instead of UUID in models (already done). Skip integration tests that need PostgreSQL-specific features when running with SQLite.

### Risk: Tests are slow with real JWT + database
**Mitigation**: Separate unit tests (fast, SQLite) from integration tests (slower, PostgreSQL). Run unit tests on every commit, integration tests on PR.
