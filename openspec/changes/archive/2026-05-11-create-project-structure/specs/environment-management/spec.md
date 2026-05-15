## ADDED Requirements

### Requirement: Environment Variable Management
The system SHALL read all configuration from environment variables via a centralized core/config.py module.

#### Scenario: core/config.py provides typed configuration
- **WHEN** importing from core.config
- **THEN** all environment variables are available with correct types (str, int, bool, etc.)

#### Scenario: Missing required variables raise error
- **WHEN** required environment variables are not set
- **THEN** the application fails to start with a clear error message

#### Scenario: Configuration is read from .env file
- **WHEN** a .env file exists in the project root
- **THEN** environment variables are read from it (via python-dotenv)

#### Scenario: Environment variables override .env file
- **WHEN** an environment variable is set AND a .env file contains the same variable
- **THEN** the environment variable takes precedence

### Requirement: .env.example Template
The system SHALL provide a .env.example file documenting all required environment variables.

#### Scenario: .env.example exists
- **WHEN** cloning the project
- **THEN** .env.example is present and shows all required variables with example values

#### Scenario: .env.example is not gitignored
- **WHEN** committing to git
- **THEN** .env.example is committed (safe, contains no secrets)

#### Scenario: .env is gitignored
- **WHEN** creating a .env file locally
- **THEN** .env is in .gitignore and not committed

### Requirement: Configuration Validation
The system SHALL validate configuration values at startup.

#### Scenario: DATABASE_URL is validated
- **WHEN** the application starts with invalid DATABASE_URL
- **THEN** an error is raised (e.g., "DATABASE_URL must be a valid PostgreSQL connection string")

#### Scenario: PORT is an integer
- **WHEN** PORT is set in environment
- **THEN** it is parsed as an integer; non-integer values raise an error
