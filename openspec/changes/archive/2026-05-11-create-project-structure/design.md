## Context

TomiLomos API is a FastAPI-based backend for gastronomic business management. The project must follow Clean Architecture principles as defined in AGENTS.md: Router → Service → Repository → Model. Currently, the project has basic documentation and a change map but no actual code structure.

Constraints:
- Must follow Clean Architecture (separation of concerns)
- Python 3.10+ and FastAPI 0.100+
- All configuration via environment variables
- pytest for testing
- Alembic for database migrations

## Goals / Non-Goals

**Goals:**
- Create a scalable directory structure that supports parallel feature development
- Establish clear separation of concerns (API handlers, business logic, data access)
- Provide a base FastAPI application ready for route registration
- Set up testing infrastructure (fixtures, database setup)
- Create a configuration system that reads and validates environment variables
- Document the project structure for onboarding new developers

**Non-Goals:**
- Implement authentication (handled in change 1.1: setup-multitenancy-auth)
- Create actual feature modules (Raw Materials, Products, etc.)
- Set up CI/CD pipelines (future)
- Docker containerization (future)

## Decisions

### Decision 1: Directory Structure Following Clean Architecture

**Choice**: Organize code into `api/`, `services/`, `repositories/`, `db/`, `schemas/`, and `core/` directories

**Why**:
- Clear separation of concerns: each layer has a single responsibility
- Easy to locate code: know where business logic vs. data access belongs
- Scales well: can add new features without merging directory conflicts
- Matches industry standards (Django, NestJS, Spring Boot)

**Structure**:
```
tomilomos_api/
├── api/                    # Routes/endpoints (Router layer)
│   ├── __init__.py
│   ├── auth_router.py
│   ├── health_router.py
│   └── (more routers for future features)
├── services/               # Business logic (Service layer)
│   ├── __init__.py
│   ├── auth_service.py
│   └── (more services for future features)
├── repositories/           # Data access (Repository layer)
│   ├── __init__.py
│   ├── user_repository.py
│   └── (more repos for future features)
├── db/                     # Database models and setup
│   ├── __init__.py
│   ├── models.py
│   ├── base.py
│   ├── session.py
│   └── migrations/         # Alembic migrations
├── schemas/                # Pydantic models (validation)
│   ├── __init__.py
│   ├── auth.py
│   └── (more schemas for future features)
├── core/                   # Configuration and utilities
│   ├── __init__.py
│   ├── config.py           # Environment variables
│   ├── logging.py          # Logging setup
│   ├── exceptions.py       # Custom exceptions
│   └── (more utilities)
├── tests/                  # Unit and integration tests
│   ├── __init__.py
│   ├── conftest.py
│   └── (test modules)
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
└── README.md               # Setup instructions
```

---

### Decision 2: Configuration Management via core/config.py

**Choice**: Single configuration module that reads and validates environment variables at startup

**Why**:
- Centralized: all config in one place
- Type-safe: Pydantic models validate types and ranges
- Early failure: invalid config detected at startup, not at runtime
- Secure: no secrets hardcoded

**Implementation**:
- `core/config.py`: Uses Pydantic BaseSettings
- Reads from `.env` file (via python-dotenv)
- Validates DATABASE_URL, JWT_SECRET, BCRYPT_COST, etc.
- Raises error if required variables missing

---

### Decision 3: Testing Infrastructure with pytest

**Choice**: Use pytest as the test runner with fixtures and database isolation

**Why**:
- Industry standard
- Excellent plugin ecosystem (pytest-cov for coverage, pytest-async for async tests)
- Simple syntax (fixtures > mocking)
- Works well with SQLAlchemy (in-memory SQLite for tests)

**Implementation**:
- `tests/conftest.py`: Defines fixtures (db session, test tenant, test user, test JWT token)
- In-memory SQLite for test database (no network I/O, fast)
- Each test gets a clean database (rollback after test)
- Fixtures provide ready-to-use test data

---

### Decision 4: FastAPI Application Structure

**Choice**: Main FastAPI app in `main.py` that registers all routers and exception handlers

**Why**:
- Single entry point for the application
- Clear where to add middleware, exception handlers, startup/shutdown events
- Easy to extend (add more routers, add CORS, etc.)

**Implementation**:
- `main.py` creates FastAPI() app
- Registers routers from `api/` package
- Adds exception handlers for custom exceptions
- Adds CORS middleware (configurable via environment)
- Adds request logging middleware

---

### Decision 5: Logging Setup

**Choice**: Create `core/logging.py` with structured logging configuration

**Why**:
- Consistent log format across the app
- Can be configured via environment (log level, format)
- Secrets (passwords, tokens) never logged

**Implementation**:
- Use Python's `logging` module
- Set up JSON-formatted logs (for structured parsing)
- Different handlers for console (dev) vs. file (production)
- Never log sensitive fields

## Risks / Trade-offs

### Risk: Over-engineering for Phase 1
**Problem**: Creating too much structure for features that don't exist yet  
**Mitigation**: Stick to the 5 core directories (api, services, repositories, db, schemas, core). Don't create placeholder modules.

---

### Risk: Test Database Performance
**Problem**: In-memory SQLite might behave differently than PostgreSQL  
**Mitigation**: Use PostgreSQL for integration tests in Phase 2. Phase 1 tests use SQLite for speed.

---

### Risk: Configuration Complexity
**Problem**: Too many environment variables → hard to manage  
**Mitigation**: Provide sensible defaults for non-critical variables. Document all variables in .env.example.

---

### Trade-off: Type Safety vs. Simplicity
**Problem**: Pydantic validation adds overhead; simpler to use plain dicts  
**Mitigation**: Pydantic's benefits (auto-docs, validation, IDE support) outweigh overhead. Use it everywhere.

## Migration Plan

### Phase 1 (Initial Setup)

1. **Create directory structure**
   - Create api/, services/, repositories/, db/, schemas/, core/, tests/ directories
   - Create __init__.py files in each

2. **Create main configuration files**
   - main.py (FastAPI app)
   - requirements.txt (dependencies)
   - .env.example (environment template)

3. **Set up testing infrastructure**
   - tests/conftest.py with fixtures
   - Run pytest to verify setup

4. **Verify imports and structure**
   - Ensure all imports resolve correctly
   - Run `python -m api` or `uvicorn main:app` to verify app starts

### Phase 2 (Expansion)
- As new features are added, follow this structure
- Create new routers in api/, services in services/, etc.

### Rollback
- If structure is wrong, simply rename/move directories and update imports
- No database schema involved, so no migrations to rollback

## Open Questions

1. **Should we include Makefile or just pytest/uvicorn commands?**
   - Current assumption: Use pytest and uvicorn directly. Add Makefile in Phase 2 if needed.

2. **Should tests/ be inside project folder or alongside?**
   - Current assumption: `tests/` folder at project root (not inside tomilomos_api/).

3. **Should we have api_v1/ subfolder to support future /api/v2?**
   - Current assumption: No. Start with flat api/ folder. Refactor in Phase 2 if multiple versions needed.

4. **Should we add pre-commit hooks (black, flake8, isort)?**
   - Current assumption: Not in Phase 1. Add in Phase 2 for code quality checks.
