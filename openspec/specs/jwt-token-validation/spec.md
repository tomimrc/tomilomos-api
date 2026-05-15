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
