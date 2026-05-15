## MODIFIED Requirements

### Requirement: Retrieve cost per unit for calculation
The system SHALL expose the cost_per_unit field in API responses so that other modules (recipes, products) can retrieve and use it for cost calculations. This requirement is extended to support recipe context queries.

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
