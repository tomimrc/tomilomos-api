## ADDED Requirements

### Requirement: Login endpoint is registered in the FastAPI application
The auth router SHALL be registered in main.py with prefix `/api/v1/auth` so that `POST /api/v1/auth/login` is a reachable endpoint.

#### Scenario: Login endpoint is reachable
- **WHEN** a client sends `POST /api/v1/auth/login` with valid JSON body
- **THEN** the request reaches the login handler (not a 404)

#### Scenario: Login endpoint returns 200 on success
- **WHEN** a client sends `POST /api/v1/auth/login` with valid email and password for an existing user
- **THEN** the system returns HTTP 200 with a JSON body containing `access_token`, `token_type`, and `expires_in`

#### Scenario: Login endpoint returns 401 on invalid credentials
- **WHEN** a client sends `POST /api/v1/auth/login` with incorrect email or password
- **THEN** the system returns HTTP 401 with an error message

#### Scenario: Login endpoint returns 422 on invalid request body
- **WHEN** a client sends `POST /api/v1/auth/login` with missing or malformed fields
- **THEN** the system returns HTTP 422 with validation errors

### Requirement: Login handler delegates to AuthService
The login endpoint SHALL use the existing `AuthService.authenticate_user()` to validate credentials and `AuthService.generate_tokens()` to issue JWT tokens.

#### Scenario: Credentials verified against database
- **WHEN** a user logs in with email "admin@restaurant.com" and correct password
- **THEN** AuthService queries the users table, finds the user, and verifies the bcrypt password hash

#### Scenario: JWT token contains user_id and tenant_id claims
- **WHEN** login succeeds
- **THEN** the returned JWT token decodes to include `sub` (user_id) and `tenant_id` claims

### Requirement: Auth router uses consolidated model imports
The auth router and auth service SHALL import models from `db.models` (the canonical location) instead of `app.db.models`.

#### Scenario: No duplicate model definitions at runtime
- **WHEN** the application starts
- **THEN** only one set of SQLAlchemy model definitions is loaded (from `db.models`)

#### Scenario: AuthService can access User and Tenant models
- **WHEN** AuthService.authenticate_user() is called
- **THEN** it queries User and Tenant from the same model registry used by business routers
