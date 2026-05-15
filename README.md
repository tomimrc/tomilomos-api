# TomiLomos API

**Multi-tenant business management system for gastronomy**

A modern FastAPI-based backend for restaurants and food businesses, enabling inventory management, recipe costing, staff management, and comprehensive financial reporting.

---

## Project Overview

TomiLomos API is built on **Clean Architecture** principles with clear separation of concerns:

- **Router Layer** (`api/`): HTTP endpoints and request validation
- **Service Layer** (`services/`): Business logic and rules
- **Repository Layer** (`repositories/`): Database queries and persistence
- **Database Layer** (`db/`): ORM models and migrations

The system is designed for **multi-tenancy**, allowing multiple restaurants to use the platform simultaneously with complete data isolation.

---

## Setup Instructions

### Prerequisites

- **Python 3.10+**
- **PostgreSQL 12+** (or SQLite for development)
- **pip** (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tomilomos-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your local database URL and secrets
   ```

5. **Initialize database** (when migrations are set up)
   ```bash
   alembic upgrade head
   ```

---

## Directory Structure

```
tomilomos-api/
├── api/                         # API routers and endpoints
│   ├── __init__.py
│   ├── health_router.py         # Health check endpoint
│   └── (future: auth_router, products_router, etc.)
│
├── services/                    # Business logic layer
│   ├── __init__.py
│   └── (future: auth_service, inventory_service, etc.)
│
├── repositories/                # Data access layer
│   ├── __init__.py
│   └── (future: user_repository, product_repository, etc.)
│
├── db/                          # Database configuration
│   ├── __init__.py
│   ├── base.py                  # SQLAlchemy declarative base
│   ├── models.py                # ORM models (Tenant, User, etc.)
│   ├── session.py               # Engine and session factory
│   └── migrations/              # Alembic migration scripts
│
├── schemas/                     # Pydantic request/response models
│   ├── __init__.py
│   └── (future: auth.py, product.py, etc.)
│
├── core/                        # Core configuration and utilities
│   ├── __init__.py
│   ├── config.py                # Environment configuration
│   ├── logging.py               # Structured logging setup
│   └── exceptions.py            # Custom exception classes
│
├── tests/                       # Unit and integration tests
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures and configuration
│   ├── test_health.py           # Health endpoint tests
│   └── (future: test_auth.py, test_products.py, etc.)
│
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template (DO NOT COMMIT .env)
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

---

## Running the Application

### Development

Start the development server with auto-reload:

```bash
uvicorn main:app --reload
```

The API will be available at:
- **Base URL**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc` (ReDoc)
- **Health Check**: `http://localhost:8000/api/v1/health`

### Production

Use a production ASGI server (e.g., Gunicorn):

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## Running Tests

Execute all tests with coverage:

```bash
pytest tests/
```

With coverage report:

```bash
pytest tests/ --cov=app --cov-report=html
```

View coverage in browser: `htmlcov/index.html`

### Test-Specific Commands

```bash
# Run specific test file
pytest tests/test_health.py

# Run specific test
pytest tests/test_health.py::test_health_check_status_ok

# Run with verbose output
pytest -v

# Run with print statements visible
pytest -s
```

---

## Database Migrations (Alembic)

[Documentation will be added when migrations are set up]

### Quick Commands

```bash
# Create new migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

---

## Environment Variables

All environment variables must be defined in `.env`. Copy `.env.example` and fill in your values:

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `DATABASE_URL` | string | **Yes** | — | PostgreSQL connection string: `postgresql://user:password@host:port/db` |
| `JWT_SECRET` | string | **Yes** | — | Secret key for JWT signing (generate with `secrets.token_urlsafe(32)`) |
| `JWT_ALGORITHM` | string | No | HS256 | JWT signing algorithm |
| `JWT_EXPIRATION_HOURS` | int | No | 24 | Token expiration time in hours |
| `BCRYPT_COST` | int | No | 12 | Bcrypt hashing cost factor (10-31; higher = slower but more secure) |
| `PORT` | int | No | 8000 | Server port |
| `LOG_LEVEL` | string | No | INFO | Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `CORS_ORIGINS` | array | No | `["http://localhost:3000"]` | Allowed CORS origins (JSON array format) |

### Example .env

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/tomilomos
JWT_SECRET=your_super_secret_key_from_secrets_module
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
BCRYPT_COST=12
PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

---

## Clean Architecture Overview

### Data Flow: Request → Response

```
Request
   ↓
[API Router]              ← Input validation, HTTP headers
   ↓
[Service Layer]           ← Business logic, rules, decisions
   ↓
[Repository Layer]        ← Query building, database access
   ↓
[Database]                ← Persistence, transactions
   ↓
[Repository Layer]        ← Result mapping
   ↓
[Service Layer]           ← Result transformation
   ↓
[API Router]              ← Response formatting, status codes
   ↓
Response (JSON)
```

### Example: Get User by ID

```python
# API Router (api/users_router.py)
@router.get("/users/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = await user_service.get_user(user_id, db)  # ← Call service
    return UserResponse.from_orm(user)

# Service (services/user_service.py)
async def get_user(user_id: str, db: Session) -> User:
    user = await user_repository.get_by_id(user_id, db)  # ← Call repository
    if not user:
        raise UserNotFoundError(user_id)
    return user

# Repository (repositories/user_repository.py)
async def get_by_id(user_id: str, db: Session) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()  # ← Query DB
```

### Benefits

- **Testability**: Easy to mock each layer independently
- **Maintainability**: Clear responsibility in each layer
- **Scalability**: Can scale layers independently (add caching, queuing, etc.)
- **Flexibility**: Can change database or external service without affecting business logic

---

## Contributing Guidelines

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
type(scope): description

[optional body]
[optional footer]
```

**Types**:
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring (no feature change)
- `test:` Adding or updating tests
- `docs:` Documentation changes
- `chore:` Build, dependencies, or tooling

**Examples**:
```bash
git commit -m "feat(auth): add JWT token validation"
git commit -m "fix(config): validate bcrypt cost range"
git commit -m "test(health): add health endpoint tests"
git commit -m "docs(readme): update setup instructions"
```

### Code Style

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **Naming**: Use descriptive names in English
- **Type Hints**: Always use type hints for functions and variables
- **Docstrings**: Use docstrings for modules, classes, and public methods

### Before Committing

1. Run tests: `pytest tests/`
2. Check types: `mypy app/` (if installed)
3. Format code: `black .` (if installed)

---

## Troubleshooting

### ModuleNotFoundError on startup

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Database connection error

**Problem**: `psycopg2.OperationalError: could not connect to server`

**Solution**: Check `DATABASE_URL` in `.env`:
```bash
# Verify PostgreSQL is running and accessible
psql -U postgres -h localhost
```

### Port already in use

**Problem**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Use a different port
uvicorn main:app --port 8001
```

Or set in `.env`:
```env
PORT=8001
```

---

## Raw Materials API

The Raw Materials module provides foundational inventory management for TomiLomos. It enables tracking of ingredients/raw materials with multi-tenant isolation, cost management, and stock control.

### Features

- **CRUD Operations**: Create, read, update, delete raw materials
- **Stock Management**: Add and remove stock with decimal precision
- **Cost Tracking**: Store cost-per-unit for profitability calculations
- **Multi-Tenant Isolation**: Each tenant has isolated inventory
- **Decimal Precision**: DECIMAL(10,2) for accurate monetary values
- **Unit of Measurement**: Support for kg, g, L, mL, units, pieces, boxes

### Endpoints

All endpoints require JWT authentication.

#### Create a Raw Material
```
POST /api/v1/raw-materials
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "name": "Tomatoes",
    "unit_of_measurement": "kg",
    "cost_per_unit": "2.50",
    "supplier": "Local Farm"
}

Response: 201 Created
{
    "id": "raw-mat-123",
    "tenant_id": "tenant-456",
    "name": "Tomatoes",
    "unit_of_measurement": "kg",
    "cost_per_unit": "2.50",
    "supplier": "Local Farm",
    "current_stock": "0.00",
    "created_at": "2026-05-11T10:00:00",
    "updated_at": "2026-05-11T10:00:00"
}
```

#### List Raw Materials
```
GET /api/v1/raw-materials?skip=0&limit=100
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
[
    { ... raw material objects ... }
]
```

#### Get a Specific Raw Material
```
GET /api/v1/raw-materials/{id}
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
{ ... raw material object ... }
```

#### Update a Raw Material
```
PUT /api/v1/raw-materials/{id}
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "name": "Premium Tomatoes",
    "cost_per_unit": "3.50"
}

Response: 200 OK
{ ... updated raw material object ... }
```

#### Delete a Raw Material
```
DELETE /api/v1/raw-materials/{id}
Authorization: Bearer <JWT_TOKEN>

Response: 204 No Content
```

#### Add Stock
```
POST /api/v1/raw-materials/{id}/add-stock
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "quantity": "10.50",
    "reason": "purchase"
}

Response: 200 OK
{ ... updated raw material with new current_stock ... }
```

#### Remove Stock
```
POST /api/v1/raw-materials/{id}/remove-stock
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "quantity": "2.00",
    "reason": "sale"
}

Response: 200 OK
{ ... updated raw material with adjusted current_stock ... }
```

#### Get Stock Level
```
GET /api/v1/raw-materials/{id}/stock
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
{
    "id": "raw-mat-123",
    "current_stock": "8.50"
}
```

### Validation Rules

- **name**: Required, non-empty string (max 255 characters)
- **unit_of_measurement**: Required, must be one of: kg, g, L, mL, units, pieces, boxes
- **cost_per_unit**: Required, must be positive (DECIMAL(10,2))
- **supplier**: Optional, max 255 characters
- **quantity** (for stock adjustments): Must be positive

### Error Responses

- `400 Bad Request`: Validation failed
- `401 Unauthorized`: Invalid or missing JWT token
- `404 Not Found`: Resource not found or tenant isolation violation
- `500 Internal Server Error`: Server error

### Multi-Tenant Isolation

All raw materials are isolated by tenant. Users can only access materials from their own tenant:

```bash
# User from tenant-A cannot access materials from tenant-B
GET /api/v1/raw-materials/raw-mat-B
# Returns 404 Not Found
```

---

## Products API

The Products module provides management of sellable items for TomiLomos. Products are the final items customers purchase, each with a sale price tracked with decimal precision for accurate revenue calculations.

### Features

- **CRUD Operations**: Create, read, update, delete products
- **Decimal Precision**: DECIMAL(10,2) for accurate pricing (no floating-point errors)
- **Product Lifecycle**: is_active flag for toggling availability
- **Multi-Tenant Isolation**: Each tenant has isolated product catalog
- **Pagination**: List products with skip/limit parameters

### Endpoints

All endpoints require JWT authentication.

#### Create a Product
```
POST /api/v1/products
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "name": "Lomito Completo",
    "sale_price": "45.99",
    "is_active": true
}

Response: 201 Created
{
    "id": "prod-123",
    "tenant_id": "tenant-456",
    "name": "Lomito Completo",
    "sale_price": "45.99",
    "is_active": true,
    "created_at": "2026-05-12T10:00:00",
    "updated_at": "2026-05-12T10:00:00"
}
```

#### List Products
```
GET /api/v1/products?skip=0&limit=100
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
[
    { ... product objects ... }
]
```

#### Get a Specific Product
```
GET /api/v1/products/{id}
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
{ ... product object ... }
```

#### Update a Product
```
PUT /api/v1/products/{id}
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "name": "Lomito Premium",
    "sale_price": "49.99",
    "is_active": true
}

Response: 200 OK
{ ... updated product object ... }
```

#### Delete a Product
```
DELETE /api/v1/products/{id}
Authorization: Bearer <JWT_TOKEN>

Response: 204 No Content
```

### Validation Rules

- **name**: Required, non-empty string (max 255 characters)
- **sale_price**: Required, must be positive, DECIMAL(10,2) format (e.g., 45.99)
- **is_active**: Optional, defaults to true (can be true or false)

### Error Responses

- `400 Bad Request`: Validation failed (e.g., sale_price ≤ 0, name empty)
- `401 Unauthorized`: Invalid or missing JWT token
- `404 Not Found`: Product not found or tenant isolation violation
- `500 Internal Server Error`: Server error

### Multi-Tenant Isolation

All products are isolated by tenant. Users can only access products from their own tenant:

```bash
# User from tenant-A cannot access products from tenant-B
GET /api/v1/products/prod-B
# Returns 404 Not Found
```

---

---

## Recipes API

The Recipes module provides foundational recipe management and automatic cost calculation based on ingredient costs. Recipes enable restaurants to define how raw materials combine to create products, automatically calculating costs from current ingredient prices.

### Features

- **CRUD Operations**: Create, read, update, delete recipes
- **Recipe Ingredients**: Manage ingredient line items (quantity, unit, cost)
- **Automatic Cost Calculation**: Calculate recipe cost in real-time based on current raw material prices
- **Product Linking**: Optionally link products to recipes for automatic cost pricing
- **Multi-Tenant Isolation**: Each tenant has isolated recipes
- **Decimal Precision**: DECIMAL(10,2) for accurate cost calculations (no floats)
- **Tenant-Scoped Ingredients**: Cannot link cross-tenant raw materials to recipes

### Endpoints

All endpoints require JWT authentication.

#### Create a Recipe
```
POST /api/v1/recipes
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "name": "Lomito Completo",
    "description": "Tenderloin with chimichurri and sides"
}

Response: 201 Created
{
    "id": "recipe-123",
    "tenant_id": "tenant-456",
    "name": "Lomito Completo",
    "description": "Tenderloin with chimichurri and sides",
    "created_at": "2026-05-12T10:00:00",
    "updated_at": "2026-05-12T10:00:00"
}
```

#### List Recipes
```
GET /api/v1/recipes?skip=0&limit=100
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
[
    { ... recipe objects ... }
]
```

#### Get a Specific Recipe
```
GET /api/v1/recipes/{id}
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
{ ... recipe object ... }
```

#### Update a Recipe
```
PUT /api/v1/recipes/{id}
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "name": "Lomito Premium",
    "description": "Premium tenderloin with special chimichurri"
}

Response: 200 OK
{ ... updated recipe object ... }
```

#### Delete a Recipe
```
DELETE /api/v1/recipes/{id}
Authorization: Bearer <JWT_TOKEN>

Response: 204 No Content
```

### Recipe Ingredients

#### Add Ingredient to Recipe
```
POST /api/v1/recipes/{recipe_id}/ingredients
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "raw_material_id": "raw-mat-beef",
    "quantity": "0.5",
    "unit": "kg"
}

Response: 201 Created
{
    "id": "ingredient-123",
    "recipe_id": "recipe-123",
    "raw_material_id": "raw-mat-beef",
    "quantity": "0.5",
    "unit": "kg",
    "created_at": "2026-05-12T10:00:00"
}
```

#### List Recipe Ingredients
```
GET /api/v1/recipes/{recipe_id}/ingredients
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
[
    { ... ingredient objects ... }
]
```

#### Get Specific Ingredient
```
GET /api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
{ ... ingredient object ... }
```

#### Update Ingredient
```
PUT /api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "quantity": "0.75",
    "unit": "kg"
}

Response: 200 OK
{ ... updated ingredient object ... }
```

#### Remove Ingredient
```
DELETE /api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}
Authorization: Bearer <JWT_TOKEN>

Response: 204 No Content
```

### Recipe Costing

#### Calculate Recipe Cost
```
GET /api/v1/recipes/{recipe_id}/cost
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
{
    "total_cost": "28.50",
    "currency": "USD",
    "calculated_at": "2026-05-12T10:00:00",
    "ingredients": [
        {
            "raw_material_id": "raw-mat-beef",
            "raw_material_name": "Beef",
            "quantity": "0.5",
            "unit": "kg",
            "unit_cost": "20.00",
            "ingredient_total_cost": "10.00"
        },
        {
            "raw_material_id": "raw-mat-chimichurri",
            "raw_material_name": "Chimichurri",
            "quantity": "0.1",
            "unit": "L",
            "unit_cost": "5.00",
            "ingredient_total_cost": "0.50"
        }
    ]
}
```

### Linking Recipes to Products

#### Create Product with Recipe
```
POST /api/v1/products
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "name": "Lomito Completo",
    "sale_price": "45.99",
    "recipe_id": "recipe-123",
    "is_active": true
}

Response: 201 Created
{
    "id": "prod-123",
    "tenant_id": "tenant-456",
    "name": "Lomito Completo",
    "sale_price": "45.99",
    "recipe_id": "recipe-123",
    "cost_price": "28.50",
    "is_active": true,
    "created_at": "2026-05-12T10:00:00",
    "updated_at": "2026-05-12T10:00:00"
}
```

#### Get Product with Calculated Cost
```
GET /api/v1/products/{product_id}
Authorization: Bearer <JWT_TOKEN>

Response: 200 OK
{
    "id": "prod-123",
    "tenant_id": "tenant-456",
    "name": "Lomito Completo",
    "sale_price": "45.99",
    "recipe_id": "recipe-123",
    "cost_price": "28.50",
    "is_active": true,
    "created_at": "2026-05-12T10:00:00",
    "updated_at": "2026-05-12T10:00:00"
}
```

#### Link Recipe to Existing Product
```
PUT /api/v1/products/{product_id}
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "recipe_id": "recipe-123"
}

Response: 200 OK
{ ... updated product with cost_price calculated ... }
```

#### Remove Recipe Link from Product
```
PUT /api/v1/products/{product_id}
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "recipe_id": null
}

Response: 200 OK
{ ... updated product without cost_price ... }
```

### Validation Rules

- **Recipe name**: Required, non-empty string (max 255 characters), unique per tenant
- **Recipe description**: Optional
- **Ingredient quantity**: Required, must be > 0 (DECIMAL format)
- **Ingredient unit**: Required, non-empty string (e.g., "kg", "L", "units")
- **Raw material**: Must exist in same tenant as recipe

### Cost Calculation Precision

- All costs use **DECIMAL(10,2)** format (2 decimal places)
- Rounding: **ROUND_HALF_UP** (banker's rounding not used)
- Cost is **calculated in real-time** based on current raw material prices
- Empty recipes return cost of 0.00
- If a raw material is deleted, cost calculation fails gracefully with HTTP 424

### Error Responses

- `400 Bad Request`: Validation failed (e.g., quantity ≤ 0, name empty)
- `401 Unauthorized`: Invalid or missing JWT token
- `404 Not Found`: Recipe not found or tenant isolation violation
- `409 Conflict`: Recipe name already exists in tenant
- `424 Failed Dependency`: Raw material referenced in recipe is no longer available
- `500 Internal Server Error`: Server error

### Multi-Tenant Isolation

All recipes and ingredients are isolated by tenant:

```bash
# User from tenant-A cannot access recipes from tenant-B
GET /api/v1/recipes/recipe-B
# Returns 404 Not Found

# Cannot link raw materials from another tenant
POST /api/v1/recipes/recipe-A/ingredients
{
    "raw_material_id": "raw-mat-B",  # from tenant-B
    "quantity": "1.0",
    "unit": "kg"
}
# Returns error - raw material not found in tenant-A
```

### Business Rules

1. **Recipe Name Uniqueness**: Recipe names must be unique within each tenant
2. **Ingredient Validation**: Cannot add ingredients using raw materials from another tenant
3. **Cost Calculation**: Automatically calculated from current raw material costs; not stored
4. **Product Linking**: Optional; products can have recipes or manual pricing
5. **Cascade Deletion**: Deleting a recipe sets recipe_id to NULL in linked products (doesn't delete products)
6. **Stock Tracking**: Recipes do NOT consume stock; they define composition for costing purposes

---

## Performance Tips

1. **Database**: Use indexes on frequently queried columns
2. **Caching**: Implement Redis caching for read-heavy endpoints
3. **Async**: Use `async`/`await` for I/O-bound operations
4. **Batching**: Fetch related data in bulk (avoid N+1 queries)
5. **Monitoring**: Set up APM (Application Performance Monitoring)
6. **Recipe Costing**: Cache recipe costs if recalculated frequently (prices don't change often)

---

## Next Steps

- Implement authentication (JWT-based multi-tenancy)
- Deploy to production (Docker, Kubernetes, or cloud platform)
- Set up comprehensive monitoring and logging
- Add recipe templates and scaling features
- Implement recipe versioning and audit trails

---

## License

[Add license information here]

## Support

For questions or issues, please:
- Open an issue on GitHub
- Contact the development team
- Check existing documentation

---

**Built with ❤️ for gastronomy professionals**
