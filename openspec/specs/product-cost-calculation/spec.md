## Requirements

### Requirement: Calculate product cost with API endpoint
The system SHALL provide an API endpoint to calculate the cost of a product based on its pricing mode (recipe-based or manual).

#### Scenario: Calculate cost for product with recipe
- **WHEN** an authenticated user sends a GET request to `/api/v1/products/{id}/cost` for a product linked to a recipe
- **THEN** the system returns HTTP 200 with total cost calculated from the recipe's current ingredient costs and cost_source set to "recipe"

#### Scenario: Calculate cost for product without recipe
- **WHEN** an authenticated user sends a GET request to `/api/v1/products/{id}/cost` for a product without a recipe link
- **THEN** the system returns HTTP 200 with a message indicating manual pricing mode (cost_source: "manual")

#### Scenario: Product not found returns 404
- **WHEN** an authenticated user sends a GET request to `/api/v1/products/{id}/cost` for a non-existent product
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Respects multi-tenancy in cost queries
- **WHEN** user A sends a GET request to `/api/v1/products/{id}/cost` for a product belonging to user B
- **THEN** the system returns HTTP 404 Not Found

### Requirement: Cost response includes detailed breakdown
The system SHALL return cost information in a structured format with itemization for recipe-based costs.

#### Scenario: Cost response structure includes metadata
- **WHEN** calculating product cost
- **THEN** the response includes:
  - product_id (UUID)
  - total_cost (Decimal with 2 decimal places)
  - currency (e.g., "USD")
  - cost_source ("recipe" or "manual")
  - calculated_at (ISO 8601 timestamp)

#### Scenario: Recipe-based cost includes ingredients breakdown
- **WHEN** calculating cost for a product linked to a recipe with ingredients
- **THEN** the response includes an "ingredients" array with:
  - raw_material_id
  - raw_material_name
  - quantity
  - unit
  - unit_cost (current price)
  - ingredient_total_cost (quantity × unit_cost)

#### Scenario: Manual pricing mode has no ingredients breakdown
- **WHEN** calculating cost for a product without a recipe link
- **THEN** the response does not include an "ingredients" array, only total_cost and cost_source

### Requirement: Handle incomplete or missing dependencies
The system SHALL fail gracefully when recipes or raw materials are incomplete or missing.

#### Scenario: Missing recipe returns 424
- **WHEN** calculating cost for a product linked to a recipe that no longer exists
- **THEN** the system returns HTTP 424 Failed Dependency with an error message indicating the recipe is missing

#### Scenario: Missing raw material in recipe returns 424
- **WHEN** calculating cost for a product linked to a recipe containing an ingredient referencing a deleted raw material
- **THEN** the system returns HTTP 424 Failed Dependency with an error message indicating which raw material is missing

#### Scenario: Recipe with no ingredients returns zero cost
- **WHEN** calculating cost for a product linked to a recipe with no ingredients
- **THEN** the system returns HTTP 200 with total_cost = 0.00

### Requirement: Cost calculations use precise decimal representation
The system SHALL calculate and return all costs using DECIMAL(10,2) precision with half-up rounding.

#### Scenario: Cost values have exactly 2 decimal places
- **WHEN** calculating product cost with ingredient costs that have fractional cents
- **THEN** all cost values in the response are rounded to 2 decimal places using half-up rounding (e.g., 45.995 → 46.00)

#### Scenario: Total cost is sum of ingredient costs
- **WHEN** calculating recipe cost for a recipe with multiple ingredients
- **THEN** total_cost equals the sum of all ingredient_total_cost values, with final sum rounded to 2 decimal places

#### Scenario: Zero costs are preserved
- **WHEN** calculating cost for any product
- **THEN** zero values are returned as 0.00, not omitted or null
