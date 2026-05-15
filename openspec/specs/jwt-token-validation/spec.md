## ADDED Requirements

### Requirement: JWT Token Validation
The system SHALL validate JWT tokens on incoming requests and extract tenant_id and user_id for request context.

#### Scenario: Valid token is accepted
- **WHEN** a request includes a valid JWT token in the Authorization header (Bearer <token>)
- **THEN** the system validates the signature, expiration, and returns the decoded token claims

#### Scenario: Invalid signature is rejected
- **WHEN** a request includes a JWT token with an invalid signature
- **THEN** the system returns a 401 Unauthorized error

#### Scenario: Expired token is rejected
- **WHEN** a request includes a JWT token with exp < current_time
- **THEN** the system returns a 401 Unauthorized error ("Token expired")

#### Scenario: Missing token returns 401
- **WHEN** a protected endpoint is called without an Authorization header
- **THEN** the system returns a 401 Unauthorized error

#### Scenario: Malformed token is rejected
- **WHEN** a request includes an Authorization header that is not "Bearer <token>"
- **THEN** the system returns a 401 Unauthorized error

### Requirement: Tenant ID Extraction from Token
The system SHALL extract and use tenant_id from the JWT token for all subsequent request processing.

#### Scenario: Tenant_id is available in request context
- **WHEN** a valid token is validated
- **THEN** the tenant_id claim is extracted and available as a dependency for the request handler

#### Scenario: All queries use extracted tenant_id
- **WHEN** processing a request
- **THEN** all database queries filter results by the extracted tenant_id

### Requirement: Token Validation Middleware
The system SHALL validate all requests to protected endpoints via middleware or dependency injection.

#### Scenario: Middleware runs on protected endpoints
- **WHEN** a request reaches a protected endpoint
- **THEN** the middleware validates the JWT token before the handler executes

#### Scenario: Unprotected endpoints bypass validation
- **WHEN** a request reaches an unprotected endpoint (e.g., /health, /login)
- **THEN** the middleware skips token validation

## ADDED Requirements

### Requirement: JWT validation dependency is wired in all protected routers
All protected routers SHALL use `Depends(get_tenant_id)` from `app.core.dependencies` to extract tenant context from the JWT Authorization header, replacing `get_tenant_id_placeholder()`.

#### Scenario: Valid JWT token grants access to raw materials endpoints
- **WHEN** a request to `GET /api/v1/raw-materials` includes a valid Bearer token
- **THEN** the `get_tenant_id` dependency extracts tenant_id from the token and the handler executes

#### Scenario: Valid JWT token grants access to products endpoints
- **WHEN** a request to `GET /api/v1/products` includes a valid Bearer token
- **THEN** the `get_tenant_id` dependency extracts tenant_id from the token and the handler executes

#### Scenario: Valid JWT token grants access to recipes endpoints
- **WHEN** a request to `GET /api/v1/recipes` includes a valid Bearer token
- **THEN** the `get_tenant_id` dependency extracts tenant_id from the token and the handler executes

#### Scenario: Valid JWT token grants access to sales endpoints
- **WHEN** a request to `GET /api/v1/sales` includes a valid Bearer token
- **THEN** the `get_tenant_id` dependency extracts tenant_id from the token and the handler executes

#### Scenario: Valid JWT token grants access to product cost endpoints
- **WHEN** a request to `GET /api/v1/products/{id}/cost` includes a valid Bearer token
- **THEN** the `get_tenant_id` dependency extracts tenant_id from the token and the handler executes

### Requirement: Missing or invalid JWT token is rejected on all protected endpoints
All protected routers SHALL return 401 when the Authorization header is missing, malformed, or contains an invalid token.

#### Scenario: Missing Authorization header returns 401
- **WHEN** a request to any protected endpoint omits the Authorization header
- **THEN** the system returns HTTP 401 with "Not authenticated" or similar error

#### Scenario: Expired JWT token returns 401
- **WHEN** a request includes a JWT token with `exp` in the past
- **THEN** the system returns HTTP 401 with "Token has expired"

#### Scenario: Invalid signature returns 401
- **WHEN** a request includes a JWT token signed with a different secret
- **THEN** the system returns HTTP 401 with "Invalid token"
