## Requirements

### Requirement: Store cost per unit for raw materials
The system SHALL store the cost per unit of each raw material using precise DECIMAL(10,2) representation to enable accurate product profitability calculations without floating-point rounding errors.

#### Scenario: Cost per unit is required on creation
- **WHEN** attempting to create a raw material without cost_per_unit
- **THEN** the system returns HTTP 400 Bad Request with validation error

#### Scenario: Cost per unit is stored with precision
- **WHEN** creating a raw material with cost_per_unit = 12.99
- **THEN** the system stores the value as exactly 12.99 and returns it in API responses without any rounding

#### Scenario: Cost per unit uses two decimal places
- **WHEN** retrieving a raw material with cost_per_unit
- **THEN** the response always shows exactly two decimal places (e.g., 12.50, not 12.5)

#### Scenario: Very small cost values are supported
- **WHEN** creating a raw material with cost_per_unit = 0.01 (e.g., salt, very cheap ingredient)
- **THEN** the system stores and returns the value accurately

#### Scenario: High cost values are supported
- **WHEN** creating a raw material with cost_per_unit = 99999999.99 (e.g., expensive spice)
- **THEN** the system accepts and stores the value successfully

### Requirement: Retrieve cost per unit for calculation
The system SHALL expose the cost_per_unit field in API responses so that other modules (recipes, products) can retrieve and use it for cost calculations.

#### Scenario: Cost per unit is included in GET responses
- **WHEN** an authenticated user sends a GET request to `/api/v1/raw-materials/{id}`
- **THEN** the response includes cost_per_unit field with the current cost

#### Scenario: Cost per unit is included in list responses
- **WHEN** an authenticated user sends a GET request to `/api/v1/raw-materials`
- **THEN** each raw material in the list includes the cost_per_unit field

#### Scenario: Cost retrieval respects multi-tenancy
- **WHEN** user A from tenant A retrieves cost_per_unit for their raw material
- **THEN** the value is returned successfully
- **WHEN** user A from tenant A attempts to retrieve cost_per_unit for a raw material in tenant B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Recipes can query raw material cost in batch
- **WHEN** a recipe service needs to calculate costs for multiple ingredients
- **THEN** the system provides an efficient way to retrieve cost_per_unit for multiple raw_material_ids in a single operation

#### Scenario: Recipe cost queries respect tenant isolation
- **WHEN** calculating a recipe's cost in tenant A
- **THEN** only raw materials belonging to tenant A can be used in ingredient lookups

### Requirement: Update cost per unit
The system SHALL allow authenticated users to update the cost_per_unit of a raw material. Updated cost applies to future products/recipes; existing products retain their historical cost.

#### Scenario: Update cost per unit successfully
- **WHEN** an authenticated user sends a PUT request to `/api/v1/raw-materials/{id}` with a new cost_per_unit value
- **THEN** the system updates the cost and returns HTTP 200 with updated data

#### Scenario: Updated cost must be positive
- **WHEN** attempting to update cost_per_unit to a value ≤ 0
- **THEN** the system returns HTTP 400 Bad Request with validation error

#### Scenario: Cost update is precise
- **WHEN** updating cost_per_unit from 12.99 to 13.50
- **THEN** the system stores the new value as exactly 13.50 and applies it to future calculations

#### Scenario: Updated cost affects product cost calculation
- **WHEN** a product was created linked to a recipe with raw material A at cost_per_unit = 10.00, then cost_per_unit is updated to 12.00
- **THEN** subsequent product cost calculation queries (`/api/v1/products/{id}/cost`) use the updated cost of 12.00

#### Scenario: Cannot update cost for raw material from different tenant
- **WHEN** user A from tenant A attempts to update cost for a raw material in tenant B
- **THEN** the system returns HTTP 404 Not Found

### Requirement: Calculate cost from quantity and unit
The system SHALL enable calculations of total cost based on raw material quantity and unit of measurement. Formula: cost_total = quantity * cost_per_unit.

#### Scenario: Calculate total cost for a quantity
- **WHEN** a raw material has cost_per_unit = 5.00 and a quantity of 2.50 units is needed
- **THEN** the calculated total cost is 2.50 * 5.00 = 12.50

#### Scenario: Cost calculation supports fractional quantities
- **WHEN** a raw material with cost_per_unit = 10.00 is used in quantity 0.33 units
- **THEN** the calculated total cost is 0.33 * 10.00 = 3.30 (precise to two decimals)

#### Scenario: Cost calculation maintains precision
- **WHEN** calculating cost for multiple quantities (e.g., 1.33 * 7.99)
- **THEN** the result is exact without floating-point rounding (e.g., 10.6267 rounded to 10.63 using half-up rounding)

### Requirement: Cost per unit is used in product costing
The system SHALL provide cost_per_unit so that the recipe/product costing module can calculate ingredient costs for products via the product cost endpoint.

#### Scenario: Recipe module can access raw material costs
- **WHEN** a recipe is created with ingredient references to raw materials
- **THEN** the recipe costing module can retrieve cost_per_unit for each ingredient to calculate recipe cost

#### Scenario: Product cost endpoint uses raw material costs
- **WHEN** a product is linked to a recipe and the product cost endpoint is called
- **THEN** the system retrieves current cost_per_unit for all recipe ingredients and calculates product cost accurately

#### Scenario: Cost information is queryable
- **WHEN** a system component needs to calculate product profitability
- **THEN** it can query raw materials API and access cost_per_unit for all required ingredients

#### Scenario: Cost data is consistent across API calls
- **WHEN** retrieving the same raw material multiple times
- **THEN** cost_per_unit remains consistent across calls (unless explicitly updated)

### Requirement: Cost history is not tracked at raw material level
The system SHALL NOT maintain historical versions of cost_per_unit at the raw material level. Cost changes apply prospectively to new products.

#### Scenario: Cost update is final
- **WHEN** cost_per_unit is updated
- **THEN** there is no automatic history or rollback of previous costs at the raw material level

#### Scenario: Historical costing is the responsibility of products
- **WHEN** a product needs to know the cost at the time of creation
- **THEN** the product stores its own cost snapshot; it does not reference the raw material's current cost

#### Scenario: Note about future audit trail
- **WHEN** cost changes occur
- **THEN** currently no audit log is created (future enhancement; can be added via middleware or change events)
