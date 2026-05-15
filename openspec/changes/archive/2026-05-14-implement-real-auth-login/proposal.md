## Why

The authentication infrastructure exists in `app/` (AuthService, JWT handler, security module, dependencies) but is completely disconnected from the running application. The login endpoint returns HTTP 501 (stubbed), all 5 business routers use `get_tenant_id_placeholder()` that always fails with 401, and the auth router is never registered in `main.py`. **No user can log in and no endpoint can be used.** This change wires up the real auth system so the entire application becomes functional end-to-end.

## What Changes

- **Login endpoint becomes functional**: `POST /api/v1/auth/login` validates credentials against the database and returns a real JWT token (was: always returns 501)
- **JWT validation middleware replaces placeholder**: All routers use `Depends(get_current_tenant_id)` that extracts `tenant_id` from the JWT Authorization header (was: `get_tenant_id_placeholder()` that always raises 401)
- **Auth router registered in main.py**: The `app/api/auth_router.py` is connected to the FastAPI app
- **Dependency injection wired end-to-end**: The existing `app/core/dependencies.py` is connected to all routers so tenant context flows from JWT → router → service → repository
- **Unified import path**: All auth-related imports resolve consistently (eliminating `app.` vs root-level ambiguity for auth modules)

## Capabilities

### New Capabilities
- `auth-login-endpoint`: Functional login endpoint that authenticates users against the database and returns JWT tokens. Replaces the 501 stub.

### Modified Capabilities
- `jwt-token-validation`: Token validation now runs as real middleware on all protected endpoints instead of being bypassed by the placeholder function.
- `multi-tenant-isolation`: Tenant context is extracted from the validated JWT token via dependency injection, replacing `get_tenant_id_placeholder()` in all 5 business routers (34 occurrences).
- `user-authentication`: Login flow is now complete — credentials are verified against stored bcrypt hashes and JWT tokens are issued on success.

## Impact

- **5 router files modified**: `raw_materials_router.py`, `products_router.py`, `recipes_router.py`, `product_cost_router.py`, `sales_router.py` — replace placeholder with real dependency
- **main.py modified**: Register auth router
- **app/api/auth_router.py modified**: Remove 501 stub, connect to AuthService
- **No database schema changes**: Models already exist (Tenant, User)
- **No frontend changes**: Frontend already expects JWT auth flow
- **Breaking**: None — the placeholder was already blocking all usage, so this unblocks rather than breaks
