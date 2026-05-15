## Why

The backend has zero passing tests. All 13 test files in `tests/` were written against the placeholder auth system (`get_tenant_id_placeholder`) and `app.*` import paths that no longer exist after `implement-real-auth-login`. Without tests, we have no safety net for refactoring, no regression protection, and no confidence that the auth flow works correctly.

## What Changes

- **Fix all broken imports** in existing test files to match the consolidated project structure
- **Add test fixtures** for real JWT tokens, authenticated test client, and seeded test data (tenant + user)
- **Write unit tests** for AuthService, all services, and all repositories
- **Write integration tests** for the full auth flow: register → login → protected endpoint
- **Add conftest.py fixtures** that work with a real PostgreSQL or test SQLite database
- **Achieve ≥80% coverage** on critical paths: auth, stock deduction, multi-tenant isolation

## Capabilities

### New Capabilities
- `test-fixtures-and-seeding`: Pytest fixtures for authenticated client, JWT tokens, test tenant/user, and database isolation
- `backend-unit-tests`: Unit tests for AuthService, services (raw_materials, products, recipes, sales), and repositories
- `backend-integration-tests`: End-to-end tests for auth flow, CRUD operations with real JWT, and multi-tenant isolation verification

### Modified Capabilities
- `testing-infrastructure`: Update existing test infrastructure to work with real auth instead of placeholders

## Impact

- **All test files updated**: imports, fixtures, test client setup
- **conftest.py rewritten**: auth-aware fixtures replacing placeholder mocks
- **New test files**: auth integration tests, service unit tests
- **Dependencies**: `pytest`, `pytest-asyncio`, `httpx` (for TestClient), `pytest-cov`
- **No production code changes**: this change only affects `tests/`
