## ADDED Requirements

### Requirement: Add ingredient to recipe
The system SHALL allow authenticated users to add raw material ingredients to a recipe with quantity and unit information.

#### Scenario: Add ingredient successfully
- **WHEN** an authenticated user sends a POST request to `/api/v1/recipes/{id}/ingredients` with a valid raw_material_id and quantity
- **THEN** the system creates a new RecipeIngredient record and returns HTTP 201 with the ingredient data including id, raw_material_id, quantity, unit, and timestamps

#### Scenario: Raw material ID is required
- **WHEN** attempting to add an ingredient without a raw_material_id
- **THEN** the system returns HTTP 400 Bad Request with validation error

#### Scenario: Quantity is required and must be positive
- **WHEN** attempting to add an ingredient without quantity or with quantity ≤ 0
- **THEN** the system returns HTTP 400 Bad Request with validation error

#### Scenario: Unit is required
- **WHEN** attempting to add an ingredient without a unit
- **THEN** the system returns HTTP 400 Bad Request with validation error

#### Scenario: Raw material must exist and belong to same tenant
- **WHEN** attempting to add an ingredient with a raw_material_id from a different tenant
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Cannot add ingredient to recipe from different tenant
- **WHEN** user A sends a POST request to `/api/v1/recipes/{id}/ingredients` for a recipe belonging to user B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Recipe not found when adding ingredient
- **WHEN** an authenticated user sends a POST request to `/api/v1/recipes/{id}/ingredients` for a non-existent recipe
- **THEN** the system returns HTTP 404 Not Found

### Requirement: List ingredients in a recipe
The system SHALL allow authenticated users to retrieve all ingredients for a recipe they own.

#### Scenario: List ingredients successfully
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes/{id}/ingredients`
- **THEN** the system returns HTTP 200 with a list of all ingredients for the recipe, including raw_material_id, quantity, unit, and timestamps

#### Scenario: Recipe ingredients endpoint works for recipe without ingredients
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes/{id}/ingredients` for a recipe with no ingredients
- **THEN** the system returns HTTP 200 with an empty list

#### Scenario: Cannot list ingredients from recipe in different tenant
- **WHEN** user A sends a GET request to `/api/v1/recipes/{id}/ingredients` for a recipe belonging to user B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Recipe not found when listing ingredients
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes/{id}/ingredients` for a non-existent recipe
- **THEN** the system returns HTTP 404 Not Found

### Requirement: Retrieve a specific ingredient
The system SHALL allow authenticated users to retrieve a single ingredient within a recipe.

#### Scenario: Get ingredient successfully
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}` for an ingredient in their recipe
- **THEN** the system returns HTTP 200 with the ingredient data

#### Scenario: Ingredient not found
- **WHEN** an authenticated user sends a GET request to `/api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}` for a non-existent ingredient
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Cannot access ingredient from recipe in different tenant
- **WHEN** user A sends a GET request to `/api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}` for an ingredient in a recipe belonging to user B
- **THEN** the system returns HTTP 404 Not Found

### Requirement: Update an ingredient in a recipe
The system SHALL allow authenticated users to update ingredient quantity and unit.

#### Scenario: Update ingredient successfully
- **WHEN** an authenticated user sends a PUT request to `/api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}` with updated quantity or unit
- **THEN** the system updates the ingredient record and returns HTTP 200 with the updated ingredient data

#### Scenario: Updated quantity must be positive
- **WHEN** attempting to update an ingredient with quantity ≤ 0
- **THEN** the system returns HTTP 400 Bad Request with validation error

#### Scenario: Cannot update ingredient in recipe from different tenant
- **WHEN** user A sends a PUT request to `/api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}` for an ingredient in a recipe belonging to user B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Ingredient not found for update
- **WHEN** an authenticated user sends a PUT request to `/api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}` for a non-existent ingredient
- **THEN** the system returns HTTP 404 Not Found

### Requirement: Remove an ingredient from a recipe
The system SHALL allow authenticated users to delete ingredients from a recipe.

#### Scenario: Delete ingredient successfully
- **WHEN** an authenticated user sends a DELETE request to `/api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}` for an ingredient they own
- **THEN** the system deletes the ingredient record and returns HTTP 204 No Content

#### Scenario: Cannot delete ingredient from recipe in different tenant
- **WHEN** user A sends a DELETE request to `/api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}` for an ingredient in a recipe belonging to user B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Ingredient not found for deletion
- **WHEN** an authenticated user sends a DELETE request to `/api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}` for a non-existent ingredient
- **THEN** the system returns HTTP 404 Not Found
