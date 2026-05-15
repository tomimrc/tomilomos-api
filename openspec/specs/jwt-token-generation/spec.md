## ADDED Requirements

### Requirement: JWT Token Creation
The system SHALL generate a signed JWT token upon successful user login, encoding user and tenant identifiers.

#### Scenario: Token includes required claims
- **WHEN** a user successfully logs in
- **THEN** the system generates a JWT token containing: sub (user_id), tenant_id, exp (expiration), iat (issued_at), and jti (unique token ID)

#### Scenario: Token is cryptographically signed
- **WHEN** generating a JWT token
- **THEN** the token is signed using HS256 algorithm with a SECRET_KEY from environment variables

#### Scenario: Token expires after 24 hours
- **WHEN** a JWT token is generated
- **THEN** the token's exp claim is set to current time + 24 hours

#### Scenario: Token is returned in response
- **WHEN** login succeeds
- **THEN** the system returns JSON: { "access_token": "eyJ...", "token_type": "bearer", "expires_in": 86400 }

### Requirement: Token Secret Management
The system SHALL use environment variables to manage the JWT signing secret.

#### Scenario: Secret is read from environment
- **WHEN** the application starts
- **THEN** the system reads JWT_SECRET from environment variables (or raises an error if missing)

#### Scenario: Secret is never logged
- **WHEN** the application logs events
- **THEN** JWT_SECRET is never written to logs or error messages
