## Requirements

### Requirement: Sale price uses precise decimal representation
The system SHALL store and return sale_price using DECIMAL(10,2) precision to ensure accurate revenue calculations without floating-point rounding errors.

#### Scenario: Price with two decimal places is preserved
- **WHEN** creating a product with sale_price = 45.99
- **THEN** the system stores and returns the value as exactly 45.99 without floating-point rounding

#### Scenario: Price calculation maintains precision
- **WHEN** retrieving a product with sale_price = 0.50
- **THEN** the value is returned as exactly 0.50, not 0.500000001 or similar

#### Scenario: Price maximum value
- **WHEN** creating a product with sale_price = 99999999.99
- **THEN** the system accepts and stores the value successfully

#### Scenario: Price minimum value (just above zero)
- **WHEN** creating a product with sale_price = 0.01
- **THEN** the system accepts and stores the value successfully

### Requirement: Product pricing supports revenue calculations
The system SHALL allow retrieval of product pricing information for use in revenue and profitability calculations.

#### Scenario: Price is included in product retrieval
- **WHEN** an authenticated user retrieves a product via GET /api/v1/products/{id}
- **THEN** the response includes the sale_price field with full DECIMAL(10,2) precision

#### Scenario: Price is included in product list
- **WHEN** an authenticated user retrieves a list of products via GET /api/v1/products
- **THEN** each product in the response includes the sale_price field with full DECIMAL(10,2) precision

#### Scenario: Price can be updated independently
- **WHEN** an authenticated user updates only the sale_price field via PUT /api/v1/products/{id}
- **THEN** the system updates only the price while preserving other fields like name and is_active

### Requirement: Product pricing supports revenue and profitability calculations with recipe-based costing
The system SHALL allow retrieval of product pricing information and support recipe-based cost calculations for profitability analysis.

#### Scenario: Price is included in product retrieval
- **WHEN** an authenticated user retrieves a product via GET /api/v1/products/{id}
- **THEN** the response includes the sale_price field with full DECIMAL(10,2) precision

#### Scenario: Price is included in product list
- **WHEN** an authenticated user retrieves a list of products via GET /api/v1/products
- **THEN** each product in the response includes the sale_price field with full DECIMAL(10,2) precision

#### Scenario: Price can be updated independently
- **WHEN** an authenticated user updates only the sale_price field via PUT /api/v1/products/{id}
- **THEN** the system updates only the price while preserving other fields like name and is_active

#### Scenario: Product can optionally reference a recipe
- **WHEN** an authenticated user creates or updates a product with recipe_id field
- **THEN** the system associates the product with the specified recipe (or NULL for manual pricing)

#### Scenario: Recipe reference respects multi-tenancy
- **WHEN** an authenticated user attempts to set recipe_id to a recipe from a different tenant
- **THEN** the system returns HTTP 404 Not Found for the recipe

### Requirement: Link product to recipe for cost accuracy
The system SHALL allow products to optionally link to a recipe, enabling automatic cost calculations based on ingredient costs.

#### Scenario: Link product to recipe successfully
- **WHEN** an authenticated user sends a PUT request to `/api/v1/products/{id}` with a valid recipe_id
- **THEN** the system links the product to the recipe and returns HTTP 200 with updated product data including recipe_id

#### Scenario: Cannot link product to non-existent recipe
- **WHEN** attempting to link a product to a non-existent recipe_id
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Recipe link is optional
- **WHEN** creating a product without specifying recipe_id
- **THEN** the system creates the product successfully with recipe_id as NULL

#### Scenario: Remove recipe link by setting to NULL
- **WHEN** an authenticated user sends a PUT request to `/api/v1/products/{id}` with recipe_id set to NULL
- **THEN** the system removes the recipe association and the product reverts to manual pricing mode

### Requirement: Product cost is available via dedicated endpoint
The system SHALL provide a `/api/v1/products/{id}/cost` endpoint to retrieve the calculated cost of a product based on its pricing mode.

#### Scenario: Cost endpoint is accessible for products with recipes
- **WHEN** an authenticated user sends a GET request to `/api/v1/products/{id}/cost` for a product with recipe_id set
- **THEN** the system returns HTTP 200 with cost calculated from the recipe's current ingredient costs

#### Scenario: Cost endpoint is accessible for products without recipes
- **WHEN** an authenticated user sends a GET request to `/api/v1/products/{id}/cost` for a product without recipe_id
- **THEN** the system returns HTTP 200 with cost_source indicating manual pricing mode

#### Scenario: Cost endpoint respects multi-tenancy
- **WHEN** user A attempts to access `/api/v1/products/{id}/cost` for a product belonging to user B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Cost calculation handles missing dependencies gracefully
- **WHEN** calculating cost for a product linked to a recipe with missing ingredients or raw materials
- **THEN** the system returns HTTP 424 Failed Dependency with descriptive error message
