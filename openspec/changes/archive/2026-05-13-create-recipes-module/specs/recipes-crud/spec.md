## ADDED Requirements

### Requirement: Create a new recipe
The system SHALL allow authenticated users to create a new recipe record within their tenant with fields for name and optional description.

#### Scenario: Create recipe successfully
- **WHEN** an authenticated user sends a POST request to `/api/v1/recipes` with a valid name
- **THEN** the system creates a new Recipe record scoped to the user's tenant and returns HTTP 201 with the created recipe data including id, name, description, and timestamps

#### Scenario: Recipe name is required
- **WHEN** attempting to create a recipe without a name
- **THEN** the system returns HTTP 400 Bad Request with validation error indicating name is required

#### Scenario: Recipe name must be unique within tenant
- **WHEN** attempting to create a recipe with a name that already exists in the user's tenant
- **THEN** the system returns HTTP 409 Conflict with validation error indicating the recipe name is already in use

#### Scenario: Description is optional
- **WHEN** creating a recipe without specifying description
- **THEN** the system creates the record successfully with description as empty string or null

#### Scenario: Multi-tenant isolation on create
- **WHEN** user A creates a recipe in tenant A
- **THEN** the recipe is only accessible within tenant A and not visible to users in other tenants

### Requirement: Retrieve all recipes for a tenant
The system SHALL allow authenticated users to retrieve a list of all recipes for their tenant with pagination.

#### Scenario: List recipes successfully
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes`
- **THEN** the system returns HTTP 200 with a paginated list of all recipes in the user's tenant, including id, name, description, created_at, and updated_at

#### Scenario: List returns empty when no recipes exist
- **WHEN** an authenticated user in a new tenant sends a GET request to `/api/v1/recipes`
- **THEN** the system returns HTTP 200 with an empty list

#### Scenario: List respects pagination
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes?skip=0&limit=10`
- **THEN** the system returns no more than 10 recipes in the response

#### Scenario: List is filtered by tenant
- **WHEN** user A in tenant A retrieves recipes
- **THEN** only recipes created in tenant A are returned

### Requirement: Retrieve a specific recipe
The system SHALL allow authenticated users to retrieve a single recipe by its ID if it belongs to their tenant.

#### Scenario: Get recipe successfully
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes/{id}` for a recipe in their tenant
- **THEN** the system returns HTTP 200 with the recipe data including id, name, description, created_at, and updated_at

#### Scenario: Recipe not found
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes/{id}` for a non-existent recipe
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Cannot access recipe from different tenant
- **WHEN** user A sends a GET request to `/api/v1/recipes/{id}` for a recipe belonging to user B in a different tenant
- **THEN** the system returns HTTP 404 Not Found (recipe appears not to exist)

### Requirement: Update an existing recipe
The system SHALL allow authenticated users to update a recipe's name and description if they own the recipe.

#### Scenario: Update recipe successfully
- **WHEN** an authenticated user sends a PUT request to `/api/v1/recipes/{id}` with updated name or description
- **THEN** the system updates the recipe record and returns HTTP 200 with the updated recipe data

#### Scenario: Updated recipe name must be unique within tenant
- **WHEN** attempting to update a recipe name to one that already exists in the user's tenant
- **THEN** the system returns HTTP 409 Conflict with validation error

#### Scenario: Cannot update recipe from different tenant
- **WHEN** user A sends a PUT request to `/api/v1/recipes/{id}` for a recipe belonging to user B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Recipe not found for update
- **WHEN** an authenticated user sends a PUT request to `/api/v1/recipes/{id}` for a non-existent recipe
- **THEN** the system returns HTTP 404 Not Found

### Requirement: Delete a recipe
The system SHALL allow authenticated users to delete a recipe they own.

#### Scenario: Delete recipe successfully
- **WHEN** an authenticated user sends a DELETE request to `/api/v1/recipes/{id}` for a recipe they own
- **THEN** the system deletes the recipe record and all associated ingredients, returning HTTP 204 No Content

#### Scenario: Cannot delete recipe from different tenant
- **WHEN** user A sends a DELETE request to `/api/v1/recipes/{id}` for a recipe belonging to user B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Recipe not found for deletion
- **WHEN** an authenticated user sends a DELETE request to `/api/v1/recipes/{id}` for a non-existent recipe
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Deleting recipe clears product associations
- **WHEN** a recipe is deleted and one or more products reference it
- **THEN** the recipe_id field in associated products is set to NULL, allowing products to remain valid
