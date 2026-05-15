## ADDED Requirements

### Requirement: Bcrypt Password Hashing
The system SHALL hash all passwords using bcrypt with a minimum cost factor of 12.

#### Scenario: Password hashed with bcrypt cost 12
- **WHEN** a user password is hashed during user creation
- **THEN** bcrypt is used with cost_factor = 12 (or higher if configured)

#### Scenario: Bcrypt hash output is stored
- **WHEN** a user password is created
- **THEN** the bcrypt hash (e.g., $2b$12$...) is stored in the database, not the plaintext password

#### Scenario: Bcrypt hash is salted
- **WHEN** bcrypt hashes a password
- **THEN** each hash includes a unique salt, so identical passwords produce different hashes

### Requirement: Secure Password Comparison
The system SHALL compare passwords using constant-time comparison to prevent timing attacks.

#### Scenario: Password verification uses constant-time comparison
- **WHEN** during login, the system compares the provided password against the stored hash
- **THEN** bcrypt's `verify()` method is used, which performs constant-time comparison

#### Scenario: Timing attack resistance
- **WHEN** an attacker tries to guess a password by timing request responses
- **THEN** the system takes the same time regardless of whether the password is correct or incorrect

### Requirement: Environment-Configured Bcrypt Cost
The system SHALL allow the bcrypt cost factor to be configurable via environment variables.

#### Scenario: Default bcrypt cost is 12
- **WHEN** the application starts
- **THEN** the bcrypt cost factor defaults to 12 if not explicitly configured

#### Scenario: Cost can be increased via environment variable
- **WHEN** BCRYPT_COST environment variable is set to 13 or higher
- **THEN** the system uses that cost factor for all password hashing operations

#### Scenario: Invalid cost is rejected
- **WHEN** BCRYPT_COST is set to less than 10 or greater than 31
- **THEN** the system raises a configuration error on startup
