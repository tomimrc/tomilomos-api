## Context

The TomiLomos API has a **dual-structure problem**: auth infrastructure lives in `app/` (with its own models, session, schemas) while business modules live at root level (`api/`, `services/`, `repositories/`, `db/`). These two structures use **different model definitions** for the same tables:

```
app/db/models.py          ← Auth uses these (UUID PKs, singular table names)
├── Tenant (table="tenant", id=UUID)
├── User (table="user", id=UUID, password_hash)
├── RawMaterial (table="raw_materials", id=UUID)
├── Product (table="products", id=UUID)
├── Recipe (table="recipes", id=UUID)
└── RecipeIngredient (table="recipe_ingredients", id=UUID)

db/models.py              ← Business routers use these (String(50) PKs, plural table names)
├── Tenant (table="tenants", id=String(50))
├── User (table="users", id=String(50), hashed_password)
├── RawMaterial (table="raw_materials", id=String(50))
├── Product (table="products", id=String(50))
├── Recipe (table="recipes", id=String(50))
├── RecipeIngredient (table="recipe_ingredients", id=String(50))
└── Sale (table="sales", id=String(50))
```

The auth router (`app/api/auth_router.py`) returns 501 (stubbed). All 5 business routers use `get_tenant_id_placeholder()` which always raises 401. The auth router is never registered in `main.py`.

**What already works** (no changes needed):
- `app/core/jwt_handler.py` — JWT creation/validation with python-jose ✅
- `app/core/security.py` — bcrypt password hashing ✅
- `app/core/dependencies.py` — `get_current_user()`, `get_tenant_id()`, `get_user_id()` ✅
- `app/services/auth_service.py` — AuthService with authenticate_user ✅

## Goals / Non-Goals

**Goals:**
- Login endpoint returns real JWT tokens (not 501)
- All routers extract tenant_id from JWT via dependency injection (not placeholder)
- Single source of truth for database models
- Auth router registered and functional in main.py

**Non-Goals:**
- Full project structure consolidation (separate change: `consolidate-project-structure`)
- User registration endpoint (separate change: `add-user-registration`)
- Token refresh / password reset flows
- RBAC or role-based permissions

## Decisions

### Decision 1: Consolidate models into `db/models.py` as single source of truth

**Choice**: Add User model to `db/models.py` (the file business routers already use). Update auth imports to reference `db/models.py` instead of `app/db/models.py`.

**Why**:
- Business routers already depend on `db/models.py` — it's the de facto canonical location
- Having two model files for the same tables causes SQLAlchemy conflicts and confusion
- User model is needed by auth service; it must exist in the same file as other models
- Minimal disruption: only auth imports change, business code stays untouched

**Alternatives considered**:
- Keep both files: causes duplicate table definitions and import confusion
- Move everything to `app/db/models.py`: breaks all 5 business routers and their imports
- Create a shared models package: over-engineering for current scope

**Implementation**:
1. Add `User` model to `db/models.py` with matching conventions (String(50) PK, table="users", `hashed_password` column)
2. Add `relationship` on Tenant for users (if not present)
3. Update `app/services/auth_service.py` imports: `app.db.models` → `db.models`
4. Update `app/core/dependencies.py` imports: `app.db.session` → `db.session`
5. Update `app/api/auth_router.py` imports to use root-level paths

### Decision 2: Auth router uses root-level import paths

**Choice**: The auth router at `app/api/auth_router.py` imports from root-level modules (`db.models`, `services.auth_service`, `core.exceptions`) rather than `app.*` paths.

**Why**:
- The auth service, security module, and JWT handler are the real implementations
- Root-level `core/` already has `config.py` and `exceptions.py` that the app uses
- Avoids creating a parallel `app.services.auth_service` that duplicates logic

**Import mapping**:
```python
# Before (broken)
from app.db.models import Tenant, User
from app.services.auth_service import AuthService
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_access_token

# After (working)
from db.models import Tenant, User
from app.services.auth_service import AuthService  # Keep this — it's the real service
from core.security import hash_password, verify_password  # Or keep app.core.security
from app.core.jwt_handler import create_access_token  # Keep this — it's the real JWT handler
```

Note: `app/core/security.py` and `app/core/jwt_handler.py` remain as-is since they're the canonical implementations. Only model and session imports change.

### Decision 3: Replace `get_tenant_id_placeholder()` with `Depends(get_tenant_id)` from auth dependencies

**Choice**: All 5 business routers replace the placeholder function with the real `get_tenant_id` dependency from `app/core/dependencies.py`.

**Why**:
- `get_tenant_id` already exists and is properly implemented (validates JWT, extracts tenant_id)
- `get_current_user` chains JWT validation → returns decoded payload
- `get_tenant_id` chains `get_current_user` → extracts tenant_id claim
- This is the pattern the original auth design intended

**Implementation per router**:
```python
# Before
from fastapi import Depends, HTTPException

async def get_tenant_id_placeholder() -> str:
    raise HTTPException(status_code=401, detail="Authentication required")

@router.post("/...", ...)
async def create_item(..., tenant_id: str = Depends(get_tenant_id_placeholder)):
    ...

# After
from fastapi import Depends
from app.core.dependencies import get_tenant_id

@router.post("/...", ...)
async def create_item(..., tenant_id: str = Depends(get_tenant_id)):
    ...
```

This change affects 34 occurrences across 5 files.

### Decision 4: Register auth router in main.py under `/api/v1/auth` prefix

**Choice**: Import `app.api.auth_router` and register it with prefix `/api/v1/auth` and tag `["Auth"]`.

**Why**:
- Consistent with existing router registration pattern in main.py
- Frontend already calls `POST /api/v1/auth/login`
- Matches the OpenAPI contract

**Implementation**:
```python
from app.api import auth_router

app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth"])
```

## Risks / Trade-offs

### Risk: Model column name mismatch (`hashed_password` vs `password_hash`)

**Problem**: `app/db/models.py` uses `password_hash`, `db/models.py` uses `hashed_password`. AuthService references `user.password_hash`.

**Mitigation**: When adding User to `db/models.py`, use `password_hash` as the column name to match AuthService expectations. Or update AuthService to use `hashed_password`. Decision: use `password_hash` in the consolidated model since AuthService is the only consumer.

### Risk: Table name conflict if both model files are imported

**Problem**: If `app/db/models.py` and `db/models.py` are both imported, SQLAlchemy sees duplicate table definitions.

**Mitigation**: After consolidation, `app/db/models.py` should either be deleted or reduced to a re-export file. During this change, ensure `main.py` only imports from `db/models.py`.

### Risk: `app/db/session.py` vs `db/session.py` — two session factories

**Problem**: Auth dependencies import `get_db` from `app.db.session`, but business code uses `db.session.get_db`. Two different session factories could cause transaction isolation issues.

**Mitigation**: Update `app/core/dependencies.py` to import `get_db` from `db.session` (the canonical one used by main.py).

### Risk: Breaking existing tests

**Problem**: Tests in `tests/` may import from `app.*` paths that change.

**Mitigation**: Run full test suite after changes. Update any broken imports.

## Migration Plan

1. **Add User model to `db/models.py`** — single source of truth
2. **Update auth imports** — `app.core.dependencies` uses `db.session.get_db`, `app.services.auth_service` uses `db.models`
3. **Wire up login endpoint** — replace 501 stub with AuthService call
4. **Register auth router in main.py**
5. **Replace placeholder in all 5 routers** — 34 occurrences
6. **Run tests** — verify auth flow end-to-end
7. **Manual verification** — login → get token → call protected endpoint

### Rollback Strategy

- Keep a copy of original router files before modifications
- If auth breaks, revert router changes and re-register placeholder (system returns to previous "blocked but stable" state)
- No database migration needed (models already exist in DB from previous changes)

## Open Questions

1. **Should we delete `app/db/models.py` after consolidation?** — Yes, but as part of `consolidate-project-structure` to keep this change focused. For now, leave it but ensure it's not imported.

2. **Should `app/core/security.py` and `app/core/jwt_handler.py` move to root `core/`?** — Eventually yes, but not in this change. The auth service depends on them at their current paths. Moving them is part of the consolidation change.

3. **Does the database already have the `users` table?** — The models exist but Alembic migrations may not have been run. If the table doesn't exist, a seed script or manual table creation will be needed before login works. This is addressed in the `seed-data-and-fixtures` change.
