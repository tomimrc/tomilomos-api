## MODIFIED Requirements

### Requirement: Calculate recipe cost
The system SHALL allow authenticated users to calculate the total cost of a recipe based on current raw material prices and ingredient quantities.

#### Scenario: Calculate recipe cost successfully
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes/{id}/cost` for a recipe with ingredients
- **THEN** the system returns HTTP 200 with the calculated total cost, including itemized costs per ingredient and sum

#### Scenario: Recipe cost includes all ingredients
- **WHEN** calculating recipe cost for a recipe with multiple ingredients
- **THEN** the system multiplies each ingredient quantity by its corresponding raw material unit cost and sums all costs

#### Scenario: Recipe cost uses current raw material prices
- **WHEN** calculating recipe cost and raw material prices have changed since recipe creation
- **THEN** the system uses the CURRENT unit cost of each raw material, not historical prices

#### Scenario: Recipe cost calculation fails gracefully for missing ingredients
- **WHEN** calculating recipe cost and one ingredient references a raw material that has been deleted
- **THEN** the system returns HTTP 424 Failed Dependency with an error message indicating which raw material is missing

#### Scenario: Recipe cost is zero for recipe with no ingredients
- **WHEN** calculating cost for a recipe with no ingredients
- **THEN** the system returns HTTP 200 with total cost of 0.00

#### Scenario: Cannot calculate cost for recipe from different tenant
- **WHEN** user A sends a GET request to `/api/v1/recipes/{id}/cost` for a recipe belonging to user B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Recipe not found for cost calculation
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes/{id}/cost` for a non-existent recipe
- **THEN** the system returns HTTP 404 Not Found

### Requirement: Recipe cost response format
The system SHALL return recipe cost in a structured format that includes itemized ingredient costs.

#### Scenario: Cost response includes detail
- **WHEN** calculating recipe cost
- **THEN** the system returns HTTP 200 with response body containing:
  - total_cost (Decimal, 2 decimal places)
  - currency (e.g., "USD")
  - ingredients array with:
    - raw_material_id
    - raw_material_name
    - quantity
    - unit
    - unit_cost (current price)
    - ingredient_total_cost (quantity × unit_cost)
  - calculated_at (ISO 8601 timestamp)

#### Scenario: Cost values use correct decimal precision
- **WHEN** calculating recipe cost with ingredient costs having fractional cents
- **THEN** all cost values in response are rounded to 2 decimal places using standard rounding (half-up)

### Requirement: Integrate recipe cost with product pricing
The system SHALL allow products to optionally use recipe-based costing for accurate cost tracking through the product cost endpoint.

#### Scenario: Product with recipe uses recipe cost
- **WHEN** a product is associated with a recipe_id and a request to `/api/v1/products/{id}/cost` is made
- **THEN** the system uses the recipe's calculated cost as the product cost with cost_source = "recipe"

#### Scenario: Product without recipe uses manual pricing mode
- **WHEN** a product does not have a recipe_id set and a request to `/api/v1/products/{id}/cost` is made
- **THEN** the system returns cost_source = "manual" without recipe-derived costs

#### Scenario: Recipe cost changes propagate to product
- **WHEN** an ingredient is added to or modified in a recipe linked to a product
- **THEN** subsequent product cost queries via `/api/v1/products/{id}/cost` reflect the updated recipe cost without requiring product update

### Requirement: Recipe cost supports service-layer integration
The system SHALL provide recipe cost calculation as a service method for use by other components like product cost calculation.

#### Scenario: Service method returns cost data
- **WHEN** a service calls an internal method to calculate recipe cost (not via HTTP)
- **THEN** the system returns structured cost data (total_cost, ingredients itemization, timestamp) suitable for composition

#### Scenario: Service method respects multi-tenancy
- **WHEN** a service method is called to calculate cost for a recipe
- **THEN** the method enforces tenant_id isolation to prevent cross-tenant data leakage

#### Scenario: Service method reuses HTTP endpoint logic
- **WHEN** calculating recipe cost via service method
- **THEN** the cost calculation logic is identical to that used by the HTTP endpoint to ensure consistency
