## ADDED Requirements

### Requirement: Create a new raw material (ingredient)
The system SHALL allow authenticated users to create a new raw material (ingredient) record within their tenant, with fields for name, unit of measurement, cost per unit, and optional supplier information.

#### Scenario: Create raw material successfully
- **WHEN** an authenticated user sends a POST request to `/api/v1/raw-materials` with valid name, unit_of_measurement, and cost_per_unit
- **THEN** the system creates a new RawMaterial record scoped to the user's tenant and returns HTTP 201 with the created raw material data including id and timestamps

#### Scenario: Name is required
- **WHEN** attempting to create a raw material without a name
- **THEN** the system returns HTTP 400 Bad Request with validation error indicating name is required

#### Scenario: Cost per unit is required
- **WHEN** attempting to create a raw material without cost_per_unit
- **THEN** the system returns HTTP 400 Bad Request with validation error indicating cost_per_unit is required

#### Scenario: Cost per unit must be positive
- **WHEN** attempting to create a raw material with cost_per_unit ≤ 0
- **THEN** the system returns HTTP 400 Bad Request with validation error indicating cost must be greater than 0

#### Scenario: Unit of measurement is required
- **WHEN** attempting to create a raw material without unit_of_measurement
- **THEN** the system returns HTTP 400 Bad Request with validation error indicating unit is required

#### Scenario: Unit of measurement must be valid
- **WHEN** attempting to create a raw material with an invalid unit_of_measurement (not in: kg, g, L, mL, units, pieces, boxes)
- **THEN** the system returns HTTP 400 Bad Request with validation error indicating invalid unit

#### Scenario: Supplier is optional
- **WHEN** creating a raw material without providing a supplier
- **THEN** the system creates the record successfully with supplier set to null

#### Scenario: Multi-tenant isolation on create
- **WHEN** user A creates a raw material in tenant A
- **THEN** the raw material is only accessible within tenant A and not visible to users in other tenants

### Requirement: Retrieve all raw materials for a tenant
The system SHALL allow authenticated users to retrieve a list of all raw materials for their tenant with pagination and optional filtering.

#### Scenario: List raw materials successfully
- **WHEN** an authenticated user sends a GET request to `/api/v1/raw-materials`
- **THEN** the system returns HTTP 200 with a paginated list of all raw materials in the user's tenant, including id, name, unit_of_measurement, cost_per_unit, supplier, current_stock, created_at, and updated_at

#### Scenario: List returns empty when no raw materials exist
- **WHEN** an authenticated user in a new tenant sends a GET request to `/api/v1/raw-materials`
- **THEN** the system returns HTTP 200 with an empty list

#### Scenario: List respects pagination
- **WHEN** an authenticated user sends a GET request to `/api/v1/raw-materials?skip=0&limit=10`
- **THEN** the system returns no more than 10 raw materials in the response

#### Scenario: List is filtered by tenant
- **WHEN** user A in tenant A retrieves raw materials
- **THEN** only raw materials created by users in tenant A are returned

### Requirement: Retrieve a specific raw material
The system SHALL allow authenticated users to retrieve a single raw material by its ID if it belongs to their tenant.

#### Scenario: Get raw material successfully
- **WHEN** an authenticated user sends a GET request to `/api/v1/raw-materials/{id}` for a raw material in their tenant
- **THEN** the system returns HTTP 200 with the raw material data

#### Scenario: Raw material not found
- **WHEN** an authenticated user sends a GET request to `/api/v1/raw-materials/{id}` for a non-existent raw material
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Cannot access raw material from different tenant
- **WHEN** user A from tenant A attempts to GET a raw material that belongs to tenant B
- **THEN** the system returns HTTP 404 Not Found (not 403 Forbidden, to avoid leaking that the resource exists)

### Requirement: Update a raw material
The system SHALL allow authenticated users to update fields of a raw material record (name, unit_of_measurement, cost_per_unit, supplier, current_stock) if it belongs to their tenant.

#### Scenario: Update raw material successfully
- **WHEN** an authenticated user sends a PUT request to `/api/v1/raw-materials/{id}` with updated fields
- **THEN** the system updates the RawMaterial record and returns HTTP 200 with the updated data

#### Scenario: Update cost per unit to negative value fails
- **WHEN** attempting to update a raw material with cost_per_unit ≤ 0
- **THEN** the system returns HTTP 400 Bad Request with validation error

#### Scenario: Cannot update raw material from different tenant
- **WHEN** user A from tenant A attempts to UPDATE a raw material that belongs to tenant B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Partial updates are allowed
- **WHEN** sending a PUT request with only some fields populated (e.g., only name)
- **THEN** the system updates only the provided fields and leaves others unchanged

#### Scenario: Update timestamp is recorded
- **WHEN** a raw material is successfully updated
- **THEN** the updated_at timestamp is set to the current time

### Requirement: Delete a raw material
The system SHALL allow authenticated users to delete a raw material record from their tenant. Deletion is permanent.

#### Scenario: Delete raw material successfully
- **WHEN** an authenticated user sends a DELETE request to `/api/v1/raw-materials/{id}` for a raw material in their tenant
- **THEN** the system deletes the RawMaterial record and returns HTTP 204 No Content

#### Scenario: Delete non-existent raw material
- **WHEN** an authenticated user sends a DELETE request to `/api/v1/raw-materials/{id}` for a non-existent raw material
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Cannot delete raw material from different tenant
- **WHEN** user A from tenant A attempts to DELETE a raw material that belongs to tenant B
- **THEN** the system returns HTTP 404 Not Found

### Requirement: Cost per unit uses precise decimal representation
The system SHALL store and return cost_per_unit using DECIMAL(10,2) precision to ensure accurate monetary calculations without floating-point rounding errors.

#### Scenario: Cost with two decimal places is preserved
- **WHEN** creating a raw material with cost_per_unit = 12.99
- **THEN** the system stores and returns the value as exactly 12.99 without floating-point rounding

#### Scenario: Cost calculation maintains precision
- **WHEN** retrieving a raw material with cost_per_unit = 0.05
- **THEN** the value is returned as exactly 0.05, not 0.050000001 or similar

#### Scenario: Cost maximum value
- **WHEN** creating a raw material with cost_per_unit = 99999999.99
- **THEN** the system accepts and stores the value successfully
