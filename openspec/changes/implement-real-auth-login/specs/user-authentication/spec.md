## ADDED Requirements

### Requirement: Login endpoint is connected to the running application
The auth router SHALL be registered in main.py so that `POST /api/v1/auth/login` is a functional endpoint (not returning 501).

#### Scenario: Login returns JWT token for valid credentials
- **WHEN** a user sends `POST /api/v1/auth/login` with email "admin@test.com" and correct password
- **THEN** the system returns HTTP 200 with `{ "access_token": "...", "token_type": "bearer", "expires_in": 86400 }`

#### Scenario: Login returns 401 for wrong password
- **WHEN** a user sends `POST /api/v1/auth/login` with correct email but wrong password
- **THEN** the system returns HTTP 401 (not 501)

#### Scenario: Login returns 401 for non-existent email
- **WHEN** a user sends `POST /api/v1/auth/login` with an email that doesn't exist
- **THEN** the system returns HTTP 401 (not 501)

#### Scenario: Login returns 422 for missing fields
- **WHEN** a user sends `POST /api/v1/auth/login` with empty body
- **THEN** the system returns HTTP 422 with validation errors

### Requirement: Auth service uses consolidated model imports
AuthService SHALL import User and Tenant from `db.models` (canonical location) instead of `app.db.models`.

#### Scenario: AuthService can query users table
- **WHEN** AuthService.authenticate_user() is called
- **THEN** it successfully queries the users table via the consolidated model
