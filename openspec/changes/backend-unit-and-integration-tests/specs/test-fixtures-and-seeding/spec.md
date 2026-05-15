## ADDED Requirements

### Requirement: Test database isolation
Each test SHALL run against an isolated database that is created before the test and destroyed after.

#### Scenario: Tests do not share database state
- **WHEN** test A creates a tenant and test B runs
- **THEN** test B does not see test A's tenant

### Requirement: Authenticated test client
The test suite SHALL provide an `authenticated_client` fixture that includes a valid JWT token in the Authorization header.

#### Scenario: Authenticated client can access protected endpoints
- **WHEN** a test uses `authenticated_client` to call `GET /api/v1/raw-materials`
- **THEN** the request succeeds with HTTP 200 (not 401)

### Requirement: Seeded test tenant and user
The test suite SHALL provide fixtures for a pre-created tenant and user with known credentials.

#### Scenario: Test user can log in
- **WHEN** a test logs in with the seeded user's email and password
- **THEN** the system returns a valid JWT token

### Requirement: JWT token generation in tests
The test suite SHALL provide a utility to generate valid JWT tokens for any user_id and tenant_id.

#### Scenario: Generated token is accepted by the app
- **WHEN** a test generates a JWT token and includes it in a request
- **THEN** the app's JWT validation middleware accepts the token
