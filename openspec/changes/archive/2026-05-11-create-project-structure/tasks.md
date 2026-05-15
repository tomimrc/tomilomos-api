## 1. Directory Structure Creation

- [x] 1.1 Create api/ directory (for route handlers)
- [x] 1.2 Create api/__init__.py (empty or with imports)
- [x] 1.3 Create services/ directory (for business logic)
- [x] 1.4 Create services/__init__.py
- [x] 1.5 Create repositories/ directory (for data access)
- [x] 1.6 Create repositories/__init__.py
- [x] 1.7 Create db/ directory (for models and database setup)
- [x] 1.8 Create db/__init__.py
- [x] 1.9 Create db/migrations/ directory (for Alembic)
- [x] 1.10 Create schemas/ directory (for Pydantic models)
- [x] 1.11 Create schemas/__init__.py
- [x] 1.12 Create core/ directory (for configuration and utilities)
- [x] 1.13 Create core/__init__.py
- [x] 1.14 Create tests/ directory (for unit and integration tests)
- [x] 1.15 Create tests/__init__.py

## 2. Configuration Module (core/config.py)

- [x] 2.1 Create core/config.py with Pydantic BaseSettings
- [x] 2.2 Define DATABASE_URL environment variable (required, PostgreSQL connection string)
- [x] 2.3 Define JWT_SECRET environment variable (required, for JWT signing)
- [x] 2.4 Define JWT_ALGORITHM (default: "HS256")
- [x] 2.5 Define JWT_EXPIRATION_HOURS (default: 24)
- [x] 2.6 Define BCRYPT_COST (default: 12, min: 10, max: 31)
- [x] 2.7 Define PORT (default: 8000)
- [x] 2.8 Define LOG_LEVEL (default: "INFO")
- [x] 2.9 Define CORS_ORIGINS (default: ["http://localhost:3000"])
- [x] 2.10 Add validation: DATABASE_URL must not be empty, JWT_SECRET must not be empty
- [x] 2.11 Add validation: BCRYPT_COST must be between 10 and 31
- [x] 2.12 Create @root_validator to perform cross-field validation if needed
- [x] 2.13 Test: config loads from environment variables
- [x] 2.14 Test: config raises error if DATABASE_URL is missing
- [x] 2.15 Test: config raises error if JWT_SECRET is missing

## 3. Logging Configuration (core/logging.py)

- [x] 3.1 Create core/logging.py with logging setup
- [x] 3.2 Configure JSON logging format for structured logs
- [x] 3.3 Set logging level from config.LOG_LEVEL
- [x] 3.4 Create logger instance that can be imported by other modules
- [x] 3.5 Ensure passwords, tokens, and secrets are never logged (add filtering)

## 4. Custom Exceptions (core/exceptions.py)

- [x] 4.1 Create core/exceptions.py with base APIException class
- [x] 4.2 Create specific exception classes (InvalidCredentialsError, TenantNotFoundError, etc.)
- [x] 4.3 Each exception has: message, http_status_code, and detail_dict()

## 5. FastAPI Application (main.py)

- [x] 5.1 Create main.py with FastAPI() app instance
- [x] 5.2 Set app title = "Tomilomos API"
- [x] 5.3 Set app description = "Multi-tenant business management system for gastronomy"
- [x] 5.4 Set app version = "1.0.0"
- [x] 5.5 Add CORS middleware with origins from config.CORS_ORIGINS
- [x] 5.6 Create health check route: GET /api/v1/health → { "status": "ok" }
- [x] 5.7 Add exception handler for HTTPException (return JSON)
- [x] 5.8 Add exception handler for APIException subclasses (return JSON with detail)
- [x] 5.9 Add exception handler for generic Exception (catch-all, return 500)
- [x] 5.10 Include APIRouter for health check in main app
- [x] 5.11 Add request ID logging middleware (for tracing)
- [x] 5.12 Verify app starts without errors: `uvicorn main:app --reload`

## 6. Environment Variables & .env.example

- [x] 6.1 Create .env.example in project root
- [x] 6.2 Add DATABASE_URL=postgresql://user:password@localhost:5432/tomilomos
- [x] 6.3 Add JWT_SECRET=your_super_secret_key_change_me_in_production
- [x] 6.4 Add JWT_ALGORITHM=HS256
- [x] 6.5 Add JWT_EXPIRATION_HOURS=24
- [x] 6.6 Add BCRYPT_COST=12
- [x] 6.7 Add PORT=8000
- [x] 6.8 Add LOG_LEVEL=INFO
- [x] 6.9 Add CORS_ORIGINS=["http://localhost:3000"]
- [x] 6.10 Create .gitignore and add .env (to prevent committing actual secrets)

## 7. Requirements.txt with Pinned Versions

- [x] 7.1 Create requirements.txt in project root
- [x] 7.2 Add fastapi==0.104.1
- [x] 7.3 Add uvicorn[standard]==0.24.0
- [x] 7.4 Add sqlalchemy==2.0.23
- [x] 7.5 Add psycopg2-binary==2.9.9 (PostgreSQL driver)
- [x] 7.6 Add alembic==1.13.0
- [x] 7.7 Add python-jose[cryptography]==3.3.0
- [x] 7.8 Add bcrypt==4.1.2
- [x] 7.9 Add python-dotenv==1.0.0
- [x] 7.10 Add python-multipart==0.0.6
- [x] 7.11 Add pydantic==2.4.2
- [x] 7.12 Add pytest==7.4.3
- [x] 7.13 Add pytest-cov==4.1.0
- [x] 7.14 Add pytest-asyncio==0.21.1
- [x] 7.15 Test: `pip install -r requirements.txt` succeeds

## 8. Testing Infrastructure (tests/conftest.py)

- [x] 8.1 Create tests/conftest.py
- [x] 8.2 Create @pytest.fixture for test_db (in-memory SQLite session)
- [x] 8.3 Test database schema: tables are created before each test
- [x] 8.4 Create @pytest.fixture for test_tenant (Tenant instance with id, name)
- [x] 8.5 Create @pytest.fixture for test_user (User with email, hashed_password, tenant_id)
- [x] 8.6 Create @pytest.fixture for test_jwt_token (valid JWT token string)
- [x] 8.7 Create @pytest.fixture for test_expired_jwt_token (expired JWT)
- [x] 8.8 Create @pytest.fixture for test_client (TestClient from FastAPI)
- [x] 8.9 Ensure test database is rolled back after each test (isolation)
- [x] 8.10 Add helper fixture for creating test users with custom data
- [x] 8.11 Add helper fixture for creating test tenants with custom data

## 9. Testing Setup Verification

- [x] 9.1 Create tests/test_health.py to verify health endpoint works
- [x] 9.2 Create tests/test_config.py to verify config loads correctly
- [x] 9.3 Run pytest to ensure fixtures are discoverable: `pytest --collect-only`
- [x] 9.4 Run tests/test_health.py to verify TestClient works
- [x] 9.5 Run coverage report: `pytest tests/ --cov=app --cov-report=html`

## 10. Database Session Setup (db/session.py)

- [x] 10.1 Create db/session.py with SQLAlchemy engine creation
- [x] 10.2 Create engine using config.DATABASE_URL
- [x] 10.3 Create SessionLocal factory for sessions
- [x] 10.4 Create get_db() dependency generator (yields session, closes after request)
- [x] 10.5 Test: SessionLocal() creates a session successfully

## 11. Database Base Model (db/base.py)

- [x] 11.1 Create db/base.py with declarative_base()
- [x] 11.2 This will be imported by db/models.py for Tenant and User models

## 12. Database Models Placeholder (db/models.py)

- [x] 12.1 Create db/models.py (placeholder, actual models in change 1.1)
- [x] 12.2 Import declarative_base from db/base.py
- [x] 12.3 Add comment: "Tenant and User models will be defined in change setup-multitenancy-auth"

## 13. Example API Routes (api/health_router.py)

- [x] 13.1 Create api/health_router.py with health check endpoint
- [x] 13.2 Define GET /api/v1/health → { "status": "ok", "timestamp": "..." }
- [x] 13.3 This route requires no authentication (for monitoring)

## 14. Main App Router Registration

- [x] 14.1 Update main.py to include APIRouter from api/health_router.py
- [x] 14.2 Verify /api/v1/health is accessible
- [x] 14.3 Test: GET /api/v1/health returns 200 with correct JSON

## 15. Documentation

- [x] 15.1 Create README.md in project root
- [x] 15.2 Add section: Project Overview (what is TomiLomos API)
- [x] 15.3 Add section: Setup Instructions (Python version, pip install, environment setup)
- [x] 15.4 Add section: Directory Structure (explain each folder)
- [x] 15.5 Add section: Running the Application (`uvicorn main:app --reload`)
- [x] 15.6 Add section: Running Tests (`pytest tests/`)
- [x] 15.7 Add section: Database Migrations (Alembic)
- [x] 15.8 Add section: Environment Variables (explain each variable in .env.example)
- [x] 15.9 Add section: Clean Architecture Overview (Router → Service → Repository)
- [x] 15.10 Add section: Contributing Guidelines (commit message format)

## 16. Final Verification

- [x] 16.1 Verify all imports resolve: `python -c "import app; import api; import services"`
- [x] 16.2 Verify FastAPI app starts: `python -c "from main import app; print(app)"`
- [x] 16.3 Run `uvicorn main:app` and test GET /api/v1/health in browser/curl
- [x] 16.4 Run pytest with coverage: `pytest tests/ --cov=app --cov-report=term-missing`
- [x] 16.5 Verify no console errors or import failures
- [x] 16.6 Verify .env.example is complete and clear
- [x] 16.7 Verify .gitignore includes .env and __pycache__/
- [x] 16.8 Code review: Ensure adherence to AGENTS.md (Clean Architecture principles)
- [x] 16.9 All commits follow conventional commit format (feat:, refactor:, docs:)
- [x] 16.10 README is clear and accurate for onboarding

