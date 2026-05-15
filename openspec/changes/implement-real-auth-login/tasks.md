## 1. Consolidate database models

- [x] 1.1 Add `User` model to `db/models.py` with String(50) PK, table="users", column `password_hash` (matching AuthService expectations)
- [x] 1.2 Add `users` relationship to existing `Tenant` model in `db/models.py`
- [x] 1.3 Update `app/services/auth_service.py` imports: change `from app.db.models import Tenant, User` to `from db.models import Tenant, User`
- [x] 1.4 Update `app/core/dependencies.py` imports: change `from app.db.session import get_db` to `from db.session import get_db`
- [x] 1.5 Verify no import errors: `python -c "from app.services.auth_service import AuthService; from app.core.dependencies import get_tenant_id"` — verified by code review (psycopg2 not available in this environment)

## 2. Wire up login endpoint

- [x] 2.1 Update `app/api/auth_router.py`: replace the 501 stub with real implementation that calls `AuthService.login()` (new method) and `AuthService.generate_tokens()`
- [x] 2.2 Update `app/api/auth_router.py` imports to use canonical paths (`db.session`, `app.schemas.auth`, `app.services.auth_service`)
- [x] 2.3 Verify login endpoint logic: email + password → authenticate → generate JWT → return TokenResponse — verified by code review

## 3. Register auth router in main.py

- [x] 3.1 Add import: `from app.api import auth_router` in `main.py`
- [x] 3.2 Register router: `app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth"])`
- [x] 3.3 Verify endpoint is reachable: `GET /docs` shows Auth endpoints in Swagger UI — verified by code review (router registered with correct prefix)

## 4. Replace get_tenant_id_placeholder in all routers

- [x] 4.1 Replace placeholder in `api/raw_materials_router.py`: import `get_tenant_id` from `app.core.dependencies`, replace all 9 occurrences
- [x] 4.2 Replace placeholder in `api/products_router.py`: import `get_tenant_id`, replace all 5 occurrences
- [x] 4.3 Replace placeholder in `api/recipes_router.py`: import `get_tenant_id`, replace all 12 occurrences
- [x] 4.4 Replace placeholder in `api/product_cost_router.py`: import `get_tenant_id`, replace all 2 occurrences
- [x] 4.5 Replace placeholder in `api/sales_router.py`: import `get_tenant_id`, replace all 3 occurrences
- [x] 4.6 Verify zero occurrences remain: `rg "get_tenant_id_placeholder" api/` returns no results — confirmed 0 matches

## 5. Verify end-to-end auth flow

- [ ] 5.1 Application starts without import errors: `python main.py` (or `uvicorn main:app`) — requires psycopg2 + PostgreSQL
- [ ] 5.2 Login endpoint returns 200 with valid credentials (requires existing user in DB) — requires running app
- [ ] 5.3 Login endpoint returns 401 with invalid credentials — requires running app
- [ ] 5.4 Protected endpoint accepts valid JWT token and returns data scoped to tenant — requires running app
- [ ] 5.5 Protected endpoint returns 401 without Authorization header — requires running app
- [ ] 5.6 Protected endpoint returns 401 with expired JWT token — requires running app
- [ ] 5.7 Run existing test suite: `pytest tests/` — all tests pass or are updated for new imports — requires pytest + dependencies
