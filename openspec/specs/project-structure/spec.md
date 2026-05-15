## ADDED Requirements

### Requirement: Project Directory Structure
The system SHALL organize code into Clean Architecture layers: api/, services/, repositories/, db/, schemas/, core/, and tests/.

#### Scenario: Directory structure is created
- **WHEN** the project is initialized
- **THEN** the following directories exist: api/, services/, repositories/, db/, schemas/, core/, tests/

#### Scenario: Each directory has __init__.py
- **WHEN** examining the project structure
- **THEN** each layer directory contains __init__.py (empty or with imports)

#### Scenario: db/migrations exists for Alembic
- **WHEN** setting up database migrations
- **THEN** db/migrations/ directory exists and is ready for Alembic

### Requirement: Separation of Concerns
The system SHALL enforce separation between routing layer (api/), business logic (services/), and data access (repositories/).

#### Scenario: API handlers are in api/ folder
- **WHEN** implementing a route
- **THEN** the route handler is placed in api/<feature>_router.py, not in services or repositories

#### Scenario: Business logic is in services/ folder
- **WHEN** implementing business logic (validation, calculations, etc.)
- **THEN** the logic is placed in services/<feature>_service.py, not in routers or repositories

#### Scenario: Data access is in repositories/ folder
- **WHEN** implementing database queries
- **THEN** queries are placed in repositories/<entity>_repository.py, not in services or routers

### Requirement: Configuration Module
The system SHALL have a centralized configuration module (core/config.py) that reads and validates environment variables.

#### Scenario: core/config.py exists
- **WHEN** the project starts
- **THEN** core/config.py can be imported and provides access to environment variables

#### Scenario: Configuration validates environment variables
- **WHEN** required environment variables are missing
- **THEN** the application raises an error during startup (not at runtime)

#### Scenario: Secrets never appear in logs
- **WHEN** logging configuration or environment state
- **THEN** passwords, JWT secrets, and database URLs are never written to logs
