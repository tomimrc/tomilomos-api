## ADDED Requirements

### Requirement: Complete requirements.txt
The system SHALL have a requirements.txt file with all necessary Python dependencies pinned to specific versions.

#### Scenario: requirements.txt exists
- **WHEN** the project is initialized
- **THEN** requirements.txt is present in the project root

#### Scenario: FastAPI is in requirements
- **WHEN** examining requirements.txt
- **THEN** fastapi (version ≥ 0.100.0) is listed

#### Scenario: SQLAlchemy is in requirements
- **WHEN** examining requirements.txt
- **THEN** sqlalchemy (version ≥ 2.0) is listed

#### Scenario: Alembic is in requirements
- **WHEN** examining requirements.txt
- **THEN** alembic (version ≥ 1.13) is listed

#### Scenario: pytest is in requirements
- **WHEN** examining requirements.txt
- **THEN** pytest and pytest-cov are listed

#### Scenario: Authentication libraries are in requirements
- **WHEN** examining requirements.txt
- **THEN** python-jose[cryptography], bcrypt, python-dotenv are listed

#### Scenario: All dependencies can be installed
- **WHEN** running `pip install -r requirements.txt`
- **THEN** all packages install without errors

#### Scenario: Versions are pinned exactly
- **WHEN** examining requirements.txt
- **THEN** all packages have specific version numbers (e.g., fastapi==0.104.1, not fastapi>=0.100.0)

### Requirement: Development vs. Production Separation
The system SHALL allow distinguishing between development and production dependencies (future support for requirements-dev.txt).

#### Scenario: Core dependencies are in requirements.txt
- **WHEN** installing for production
- **THEN** only requirements.txt is needed

#### Scenario: Documentation includes dependency management
- **WHEN** reading README.md
- **THEN** instructions show how to install dependencies for development vs. production
