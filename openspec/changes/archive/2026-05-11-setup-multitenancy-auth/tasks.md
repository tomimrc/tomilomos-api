## 1. Project Structure & Dependencies

- [x] 1.1 Create core/ directory for security utilities (core/security.py, core/jwt_handler.py, core/exceptions.py, core/dependencies.py)
- [x] 1.2 Create db/ directory for database models and migrations (db/models.py, db/base.py, db/session.py)
- [x] 1.3 Create schemas/ directory for Pydantic models (schemas/auth.py, schemas/user.py)
- [x] 1.4 Update requirements.txt with dependencies: SQLAlchemy, alembic, python-jose[cryptography], bcrypt, python-multipart
- [x] 1.5 Create .env.example with: DATABASE_URL, JWT_SECRET, BCRYPT_COST, JWT_ALGORITHM, JWT_EXPIRATION_HOURS

## 2. Database Models & Migrations

- [x] 2.1 Create db/models.py with Tenant model (id UUID, name String, created_at DateTime)
- [x] 2.2 Create db/models.py with User model (id UUID, tenant_id FK, email String, password_hash String, created_at DateTime)
- [x] 2.3 Add database constraints: email unique per (tenant_id, email), ON DELETE CASCADE for user → tenant
- [x] 2.4 Create db/base.py with SQLAlchemy declarative_base and engine setup
- [x] 2.5 Create db/session.py with SessionLocal and get_db() dependency function
- [x] 2.6 Initialize Alembic: alembic init db/migrations
- [x] 2.7 Create initial migration: alembic revision --autogenerate -m "create_tenant_user_tables"
- [x] 2.8 Create migration functions: env.py configured to read DATABASE_URL from environment

## 3. Security Layer - Password Hashing

- [x] 3.1 Create core/security.py with hash_password(password: str) → bcrypt hash with cost from BCRYPT_COST env var (default 12)
- [x] 3.2 Create core/security.py with verify_password(password: str, hash: str) → bool using constant-time bcrypt comparison
- [x] 3.3 Add validation: bcrypt cost must be between 10 and 31 (raise ValueError if not)
- [x] 3.4 Test: hash_password produces different hashes for same input (salt uniqueness)
- [x] 3.5 Test: verify_password returns True for correct password, False for incorrect

## 4. JWT Token Generation & Validation

- [x] 4.1 Create core/jwt_handler.py with create_access_token(user_id: str, tenant_id: str) → JWT token
- [x] 4.2 Token payload includes: sub (user_id), tenant_id, exp (now + JWT_EXPIRATION_HOURS), iat, jti (unique ID)
- [x] 4.3 Token is signed with HS256 algorithm using JWT_SECRET from environment
- [x] 4.4 Create core/jwt_handler.py with validate_token(token: str) → dict with decoded claims
- [x] 4.5 Validate token: check signature (raise InvalidTokenError if invalid)
- [x] 4.6 Validate token: check expiration (raise ExpiredTokenError if exp < now)
- [x] 4.7 Handle JWT errors: InvalidTokenError, ExpiredTokenError → proper exception classes
- [x] 4.8 Test: create_access_token generates valid JWT with correct payload
- [x] 4.9 Test: validate_token rejects invalid signatures
- [x] 4.10 Test: validate_token rejects expired tokens

## 5. Custom Exceptions & Error Handling

- [x] 5.1 Create core/exceptions.py with InvalidCredentialsError (401)
- [x] 5.2 Create core/exceptions.py with TenantNotFoundError (404)
- [x] 5.3 Create core/exceptions.py with UserNotFoundError (404)
- [x] 5.4 Create core/exceptions.py with InvalidTokenError (401)
- [x] 5.5 Create core/exceptions.py with ExpiredTokenError (401)
- [x] 5.6 Create core/exceptions.py with DuplicateEmailError (409)
- [x] 5.7 All exceptions inherit from base exception class with http_status_code property

## 6. Dependency Injection & Middleware

- [x] 6.1 Create core/dependencies.py with get_current_user(token: str = Depends(HTTPBearer())) → dict
- [x] 6.2 get_current_user: validate token, extract user_id and tenant_id, return decoded token
- [x] 6.3 Create core/dependencies.py with get_tenant_id(current_user: dict = Depends(get_current_user)) → str
- [x] 6.4 get_tenant_id: extract tenant_id from current_user, return it for use in handlers
- [x] 6.5 Create core/dependencies.py with get_db() → Session generator for database access
- [x] 6.6 All dependencies raise HTTPException with appropriate status codes if validation fails

## 7. Pydantic Schemas

- [x] 7.1 Create schemas/auth.py with LoginRequest (email: str, password: str)
- [x] 7.2 Create schemas/auth.py with TokenResponse (access_token: str, token_type: str, expires_in: int)
- [x] 7.3 Create schemas/user.py with UserCreate (email: str, password: str)
- [x] 7.4 Create schemas/user.py with UserResponse (id: str, email: str, created_at: datetime)
- [x] 7.5 Create schemas/tenant.py with TenantCreate (name: str)
- [x] 7.6 Create schemas/tenant.py with TenantResponse (id: str, name: str, created_at: datetime)

## 8. Service Layer - Authentication

- [x] 8.1 Create services/auth_service.py with authenticate_user(email: str, password: str, tenant_id: str, db: Session) → User
- [x] 8.2 Query user by email and tenant_id; if not found raise UserNotFoundError
- [x] 8.3 Verify password using verify_password(); if incorrect raise InvalidCredentialsError
- [x] 8.4 Create services/auth_service.py with create_tenant(name: str, db: Session) → Tenant
- [x] 8.5 Create services/auth_service.py with create_user(email: str, password: str, tenant_id: str, db: Session) → User
- [x] 8.6 Hash password using hash_password() before storing
- [x] 8.7 Check email uniqueness within tenant; raise DuplicateEmailError if exists

## 9. Service Layer - Token Generation

- [x] 9.1 Create services/auth_service.py with generate_tokens(user: User) → TokenResponse
- [x] 9.2 Call create_access_token(user.id, user.tenant_id) to generate token
- [x] 9.3 Return TokenResponse with access_token, token_type="bearer", expires_in (in seconds)

## 10. Repository Layer

- [x] 10.1 Create repositories/user_repository.py with get_user_by_email(email: str, tenant_id: str, db: Session) → User | None
- [x] 10.2 Create repositories/user_repository.py with create_user(email: str, password_hash: str, tenant_id: str, db: Session) → User
- [x] 10.3 Create repositories/tenant_repository.py with create_tenant(name: str, db: Session) → Tenant
- [x] 10.4 Create repositories/tenant_repository.py with get_tenant_by_id(tenant_id: str, db: Session) → Tenant | None
- [x] 10.5 All repository methods accept tenant_id parameter and filter by it (where applicable)

## 11. API Routes

- [x] 11.1 Create api/auth_router.py with POST /api/v1/auth/login (LoginRequest) → TokenResponse
- [x] 11.2 Login endpoint: extract email/password, call authenticate_user(), generate tokens, return response
- [x] 11.3 Create api/tenants_router.py with POST /api/v1/tenants (TenantCreate) → TenantResponse
- [x] 11.4 Create api/users_router.py with POST /api/v1/users (UserCreate) → UserResponse
- [x] 11.5 Create api/health_router.py with GET /api/v1/health → { "status": "ok" } (no auth required)

## 12. FastAPI Application Setup

- [x] 12.1 Create main.py with FastAPI() app initialization
- [x] 12.2 Include routers: auth_router, tenants_router, users_router, health_router
- [x] 12.3 Add exception handlers for custom exceptions (InvalidCredentialsError, TenantNotFoundError, etc.)
- [x] 12.4 Add CORS middleware if needed for frontend
- [x] 12.5 Add logging configuration (log errors, not secrets)
- [x] 12.6 Initialize database on startup: run Alembic migrations

## 13. Unit Tests - Security

- [x] 13.1 Create tests/test_security.py with test_hash_password_produces_unique_hashes()
- [x] 13.2 Create tests/test_security.py with test_verify_password_correct()
- [x] 13.3 Create tests/test_security.py with test_verify_password_incorrect()
- [x] 13.4 Create tests/test_security.py with test_bcrypt_cost_validation()
- [x] 13.5 All security tests use fixtures for test passwords and bcrypt costs

## 14. Unit Tests - JWT

- [x] 14.1 Create tests/test_jwt_handler.py with test_create_access_token()
- [x] 14.2 Verify token structure: sub, tenant_id, exp, iat, jti present
- [x] 14.3 Create tests/test_jwt_handler.py with test_validate_token_valid()
- [x] 14.4 Create tests/test_jwt_handler.py with test_validate_token_invalid_signature()
- [x] 14.5 Create tests/test_jwt_handler.py with test_validate_token_expired()
- [x] 14.6 Create tests/test_jwt_handler.py with test_token_expiration_is_24_hours()

## 15. Unit Tests - Authentication Service

- [x] 15.1 Create tests/test_auth_service.py with test_authenticate_user_success()
- [x] 15.2 Create tests/test_auth_service.py with test_authenticate_user_invalid_password()
- [x] 15.3 Create tests/test_auth_service.py with test_authenticate_user_not_found()
- [x] 15.4 Create tests/test_auth_service.py with test_create_user()
- [x] 15.5 Create tests/test_auth_service.py with test_create_user_duplicate_email_same_tenant()
- [x] 15.6 Create tests/test_auth_service.py with test_create_user_same_email_different_tenant_allowed()
- [x] 15.7 Create tests/test_auth_service.py with test_create_tenant()

## 16. Integration Tests - Auth Flow

- [x] 16.1 Create tests/test_auth_flow.py with test_full_login_flow() (create tenant → create user → login)
- [x] 16.2 Verify JWT token is returned and contains correct tenant_id
- [x] 16.3 Create tests/test_auth_flow.py with test_multi_tenant_isolation() (two tenants, same email allowed in different tenants)
- [x] 16.4 Create tests/test_auth_flow.py with test_login_with_wrong_tenant() (user from Tenant A cannot claim they're from Tenant B)

## 17. Integration Tests - Protected Endpoints

- [x] 17.1 Create tests/test_protected_endpoints.py with test_endpoint_without_token_returns_401()
- [x] 17.2 Create tests/test_protected_endpoints.py with test_endpoint_with_expired_token_returns_401()
- [x] 17.3 Create tests/test_protected_endpoints.py with test_endpoint_with_invalid_token_returns_401()
- [x] 17.4 Create tests/test_protected_endpoints.py with test_protected_endpoint_with_valid_token()

## 18. Test Fixtures & Conftest

- [x] 18.1 Create tests/conftest.py with database fixture (in-memory SQLite for tests)
- [x] 18.2 Create fixture for test tenant (id, name)
- [x] 18.3 Create fixture for test user (email, password, hashed_password, tenant_id)
- [x] 18.4 Create fixture for valid JWT token (with specific user_id, tenant_id)
- [x] 18.5 Create fixture for expired JWT token
- [x] 18.6 Create fixture for invalid JWT token (bad signature)

## 19. Documentation

- [x] 19.1 Create API documentation in main.py: title="Tomilomos API", description="Multi-tenant authentication"
- [x] 19.2 Document each endpoint in docstrings (what it does, what it returns)
- [x] 19.3 Update README.md with: Setup instructions, Environment variables, Running tests, Database migrations

## 20. Final Verification

- [x] 20.1 Run all unit tests: pytest tests/ --cov=app --cov-report=html
- [x] 20.2 Verify test coverage ≥ 80% for auth module
- [x] 20.3 Run Alembic migrations: alembic upgrade head
- [x] 20.4 Verify database schema matches models (Tenant, User tables with correct columns)
- [x] 20.5 Manual test: Create tenant, create user, login, receive JWT token
- [x] 20.6 Manual test: Use token to access protected endpoint
- [x] 20.7 Manual test: Multi-tenant isolation (two users from different tenants)
- [x] 20.8 Verify no passwords or secrets in logs
- [x] 20.9 Code review for compliance with AGENTS.md (Router → Service → Repository pattern)
- [x] 20.10 All commit messages follow conventional commits (feat:, fix:, etc.)


