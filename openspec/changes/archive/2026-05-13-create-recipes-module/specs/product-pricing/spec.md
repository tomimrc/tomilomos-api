## MODIFIED Requirements

### Requirement: Product pricing supports revenue calculations
The system SHALL allow retrieval of product pricing information for use in revenue and profitability calculations. This requirement is extended to support recipe-based cost calculations where applicable.

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

#### Scenario: Product with recipe displays cost
- **WHEN** retrieving a product that has recipe_id set
- **THEN** the response includes a cost_price field calculated from the recipe's current cost

#### Scenario: Product without recipe has no automatic cost
- **WHEN** retrieving a product that does not have recipe_id set
- **THEN** the response does not include a recipe-derived cost_price field (only sale_price)

#### Scenario: Recipe reference respects multi-tenancy
- **WHEN** an authenticated user attempts to set recipe_id to a recipe from a different tenant
- **THEN** the system returns HTTP 404 Not Found for the recipe

## ADDED Requirements

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
