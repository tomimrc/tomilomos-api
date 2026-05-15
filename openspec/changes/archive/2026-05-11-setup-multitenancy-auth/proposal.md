## Why

TomiLomos is a SaaS platform for gastronomic business management. Without foundational authentication and multi-tenant isolation, no other feature can be deployed securely. This change establishes the core infrastructure: PostgreSQL database models, JWT authentication with bcrypt password hashing, and tenant isolation to ensure data privacy across multiple independent users/businesses.

## What Changes

- **Tenant Model**: SQLAlchemy model representing independent business units. Each has its own data namespace.
- **User Model**: Represents users within a tenant. Authentication via email + bcrypt-hashed passwords (cost ≥ 12).
- **JWT Token Generation & Validation**: Secure stateless authentication. Tokens encode `user_id` and `tenant_id`.
- **Database Migrations**: Alembic migrations to create Tenant and User tables with proper constraints.
- **Dependency Injection**: Request-level middleware to extract and validate `tenant_id` from JWT token.
- **Password Hashing**: bcrypt integration (cost factor ≥ 12) for secure password storage.
- **Unit Tests**: Comprehensive tests for auth flows, token generation, and tenant isolation.

## Capabilities

### New Capabilities

- `tenant-management`: Tenant creation, retrieval. Each tenant is an isolated business entity.
- `user-authentication`: User creation, login with JWT token generation. Passwords hashed with bcrypt (cost ≥ 12).
- `jwt-token-generation`: Issue stateless JWT tokens encoding `user_id`, `tenant_id`, and expiration.
- `jwt-token-validation`: Middleware to validate JWT tokens on incoming requests. Extract `tenant_id` for request context.
- `multi-tenant-isolation`: Dependency injection ensuring all queries are scoped to the authenticated user's tenant.
- `password-security`: bcrypt password hashing with configurable cost factor (minimum 12).

### Modified Capabilities

(None - this is the foundational layer)

## Impact

- **Database**: Creates PostgreSQL schema (Tenant, User tables with proper relationships).
- **API**: All subsequent API endpoints must enforce multi-tenant isolation via dependency injection.
- **Dependencies**: Adds `python-jose[cryptography]`, `bcrypt`, `SQLAlchemy`, `alembic`, `python-multipart`.
- **Architecture**: Establishes the foundational layer for all business logic modules (Raw Materials, Products, Recipes, Sales).
- **Security**: Password handling and JWT secrets must be managed via environment variables (.env).
