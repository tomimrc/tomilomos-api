## Context

TomiLomos API is a FastAPI-based SaaS backend for gastronomic business management. The system must support multiple independent businesses (tenants) with strict data isolation. Authentication is the critical path dependency for all subsequent business logic modules (Raw Materials, Products, Recipes, Sales).

Current state: Project initialized with AGENTS.md defining Clean Architecture (Router → Service → Repository → Model). No database schema or authentication layer exists yet.

Constraints:
- Must follow Clean Architecture (Router → Service → Repository)
- PostgreSQL as primary database
- JWT for stateless authentication
- Multi-tenant isolation required (each tenant sees only their own data)
- Passwords must be hashed with bcrypt (cost ≥ 12)
- All secrets managed via environment variables

## Goals / Non-Goals

**Goals:**
- Establish PostgreSQL database schema with Tenant and User models
- Implement JWT authentication with token generation and validation
- Create dependency injection layer for multi-tenant request context
- Provide secure password hashing via bcrypt
- Create comprehensive unit tests for auth flows and tenant isolation
- Enable all subsequent modules to build atop this foundation

**Non-Goals:**
- OAuth/SSO integration (future enhancement)
- User registration endpoint (out of scope; handled externally)
- Token refresh endpoints (initial implementation uses single-use tokens)
- Role-based access control (RBAC) - only tenant isolation in Phase 1
- Email verification or 2FA

## Decisions

### Decision 1: JWT + bcrypt for Authentication

**Choice**: Use JWT tokens (stateless) with bcrypt-hashed passwords

**Why**: 
- **JWT**: Stateless tokens allow horizontal scaling without session storage
- **bcrypt**: Industry standard, resistant to GPU/ASIC attacks. Cost factor ≥ 12 provides future-proof security

**Alternatives considered**:
- Sessions (stateful): Requires Redis/database; doesn't scale as easily for SaaS
- OAuth2: Adds complexity for Phase 1; can be added later as a layer

**Implementation**:
- `core/security.py`: Contains `hash_password()` and `verify_password()` using bcrypt
- `core/jwt_handler.py`: Contains `create_access_token()` and `validate_token()` using `python-jose`
- Tokens encode: `{"sub": user_id, "tenant_id": tenant_id, "exp": expiration}`

---

### Decision 2: Multi-Tenant Isolation via Dependency Injection

**Choice**: Use FastAPI dependency injection to extract `tenant_id` from JWT and pass to all service/repository layers

**Why**:
- Type-safe, automatic at route level
- Clear, auditable data access patterns (every query explicitly scoped)
- Prevents accidental cross-tenant data leaks

**Alternatives considered**:
- Row-level security (RLS) in PostgreSQL: Powerful but complex; adds database dependency
- Manual filtering in each repository method: Verbose, error-prone

**Implementation**:
- `core/dependencies.py`: Contains `get_current_user()` and `get_tenant_id()` dependencies
- All routers use `tenant_id: str = Depends(get_tenant_id)` to extract from request
- All repositories receive `tenant_id` as parameter; queries filter by `Tenant.id == tenant_id`
- Middleware validates JWT signature and expiration

---

### Decision 3: Database Models - Tenant & User Relationship

**Choice**: One-to-many relationship (Tenant → User). All other models will have `tenant_id` foreign key.

**Why**:
- Clean separation: each user belongs to exactly one tenant
- Scalable: future models simply add `tenant_id` FK and filter on it
- Prevents accidental sharing of resources across tenants

**Schema**:
```sql
Tenant:
  id (UUID, PK)
  name (String)
  created_at (DateTime)

User:
  id (UUID, PK)
  tenant_id (UUID, FK → Tenant.id)
  email (String, unique per tenant)
  password_hash (String, bcrypt)
  created_at (DateTime)
```

---

### Decision 4: Alembic Migrations for Schema Evolution

**Choice**: Use Alembic to manage all database migrations

**Why**:
- Version-controlled schema changes
- Easy rollback if needed
- Consistent with industry practices (Rails, Django)

**Alternatives considered**:
- Manual SQL scripts: Fragile, hard to track
- Direct SQLAlchemy `create_all()`: Doesn't support schema versioning

**Implementation**:
- `db/migrations/` directory with numbered migration files
- Each change creates a new migration file
- Run migrations before tests and in production

---

### Decision 5: Error Handling & Validation

**Choice**: Use Pydantic schemas at route level; Custom exceptions in service layer

**Why**:
- Pydantic auto-validates input types and constraints
- Custom exceptions provide clarity on business logic errors (e.g., `InvalidCredentials`, `TenantNotFound`)
- Consistent error responses across all endpoints

**Implementation**:
- `schemas/auth.py`: Pydantic models for LoginRequest, TokenResponse, etc.
- `core/exceptions.py`: Custom exception classes with appropriate HTTP status codes
- Exception handlers in main.py to return standardized error responses

## Risks / Trade-offs

### Risk: Token Expiration Management
**Problem**: If tokens expire too quickly, poor UX; if too long, security risk  
**Mitigation**: Set token TTL to 24 hours initially. Phase 2 will add refresh token endpoint for seamless UX.

---

### Risk: Password Complexity Not Enforced
**Problem**: Users could set weak passwords  
**Mitigation**: Phase 2 will add password strength validation (min length, character diversity). Phase 1 focuses on secure storage (bcrypt cost ≥ 12).

---

### Risk: Database Connection Pooling
**Problem**: Naive SQLAlchemy setup could exhaust connections under load  
**Mitigation**: Use `sqlalchemy.pool.QueuePool` with configurable pool_size and max_overflow. Set via environment variables.

---

### Risk: Tenant ID Injection / Spoofing
**Problem**: User could try to modify JWT token to access another tenant's data  
**Mitigation**: 
- JWT tokens are cryptographically signed with SECRET_KEY (environment variable)
- Modify token → signature invalid → request rejected
- All repository queries filter by `tenant_id` from token (defense in depth)

---

### Trade-off: Stateless JWT vs. Token Revocation
**Problem**: JWT tokens can't be revoked until they expire  
**Mitigation**: Acceptable for Phase 1. If critical, Phase 2 can add token blacklist (Redis/database).

## Migration Plan

### Phase 1 (Initial Deployment)

1. **Create database schema**
   - Run Alembic migration to create `tenant` and `user` tables
   - Create indexes on `user.tenant_id` and `user.email`

2. **Deploy API changes**
   - Deploy auth routes (login, create_tenant, create_user)
   - All other routes now require JWT token

3. **Verification**
   - Run unit tests (80%+ coverage for auth module)
   - Manual integration test: login → token → access protected resource

### Phase 2 (Future)
- Add token refresh endpoint
- Add password reset flow
- Add role-based access control (RBAC)

### Rollback Strategy
- If critical issue in auth layer: Keep previous version of `db/migrations/` and routes. Run `alembic downgrade -1` to rollback schema.
- If token generation broken: Revert `core/jwt_handler.py` and redeploy.

## Open Questions

1. **User Registration Endpoint**: Should Phase 1 include a self-registration endpoint, or is user creation handled externally (CLI, admin panel)?
   - **Current assumption**: User creation handled externally (CLI seed script). Phase 2 adds public registration.

2. **Email as Unique Identifier**: Should emails be globally unique or unique per tenant?
   - **Current assumption**: Unique per tenant (alice@example.com in Tenant A ≠ alice@example.com in Tenant B). Revisit if needed.

3. **Audit Logging**: Should we log all login attempts / token validations?
   - **Current assumption**: Log only failed auth attempts initially. Phase 2 adds full audit trail.

4. **Token Secret Rotation**: How often should JWT_SECRET be rotated?
   - **Current assumption**: Manual via environment variable update. Phase 2 considers automated rotation.
