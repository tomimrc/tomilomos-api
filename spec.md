## ADDED Requirements

### Requirement: User Creation
The system SHALL allow creation of a new user within a specific tenant with email and password.

#### Scenario: Create user successfully
- **WHEN** an admin creates a new user with email "alice@example.com" and password "SecurePass123" in Tenant A
- **THEN** the system creates a User record, hashes the password with bcrypt (cost ≥ 12), and returns the user_id

#### Scenario: Email must be unique per tenant
- **WHEN** attempting to create a second user with the same email in the same tenant
- **THEN** the system returns a 409 Conflict error (duplicate email)

#### Scenario: Email is required
- **WHEN** attempting to create a user without an email
- **THEN** the system returns a 400 Bad Request validation error

#### Scenario: Password is required
- **WHEN** attempting to create a user without a password
- **THEN** the system returns a 400 Bad Request validation error

### Requirement: User Login
The system SHALL authenticate a user by email and password, returning a JWT token on success.

#### Scenario: Login with correct credentials
- **WHEN** a user logs in with correct email and password
- **THEN** the system validates the credentials, generates a JWT token, and returns it with HTTP 200

#### Scenario: Login with incorrect password
- **WHEN** a user logs in with correct email but incorrect password
- **THEN** the system returns an "Invalid credentials" error (401 Unauthorized)

#### Scenario: Login with non-existent email
- **WHEN** a user attempts to log in with an email that doesn't exist
- **THEN** the system returns an "Invalid credentials" error (401 Unauthorized)

#### Scenario: Password comparison is time-constant
- **WHEN** comparing passwords during login
- **THEN** the system uses bcrypt's constant-time comparison to prevent timing attacks

### Requirement: Password Hashing Security
The system SHALL hash all passwords using bcrypt with a cost factor of at least 12.

#### Scenario: Password stored as bcrypt hash
- **WHEN** a user is created with a password
- **THEN** the password is hashed with bcrypt (cost ≥ 12) and stored as a hash, never as plaintext

#### Scenario: Password hash is non-reversible
- **WHEN** inspecting the database directly
- **THEN** passwords appear as bcrypt hashes (e.g., $2b$12$...) and cannot be reversed to plaintext
