## ADDED Requirements

### Requirement: Recipe List Display
The system SHALL display a list of recipes belonging to the authenticated user's tenant.

#### Scenario: Recipes load successfully
- **WHEN** the user navigates to the recipes page and the API returns recipes
- **THEN** the system displays a list or table with columns: Name, Description (truncated if long), Ingredient Count, and Actions

#### Scenario: No recipes exist
- **WHEN** the user navigates to the recipes page and the tenant has zero recipes
- **THEN** the system displays an empty state with a message "No recipes yet" and a CTA button "Create your first recipe"

#### Scenario: Recipes fail to load
- **WHEN** the API returns an error
- **THEN** the system displays an error state with a "Retry" button

#### Scenario: Loading state
- **WHEN** the recipes page mounts and the API request is in flight
- **THEN** the system displays a loading skeleton with pulsing placeholder cards

### Requirement: Create Recipe
The system SHALL allow creating a new recipe with a name and optional description.

#### Scenario: Successful recipe creation
- **WHEN** the user fills in the recipe name (and optionally description) and submits
- **THEN** the system creates the recipe via POST /api/v1/recipes
- **AND** displays a success toast "Recipe created successfully"
- **AND** navigates to the recipe detail page where ingredients can be added

#### Scenario: Empty name validation
- **WHEN** the user submits the form with an empty name
- **THEN** the system displays an inline validation error "Name is required"
- **AND** the form is not submitted

#### Scenario: Duplicate recipe name
- **WHEN** the user submits a name that already exists within the tenant and the API returns 409 Conflict
- **THEN** the system displays an error toast "A recipe with this name already exists"

#### Scenario: Name exceeds maximum length
- **WHEN** the user enters a recipe name exceeding 255 characters
- **THEN** the system displays an inline validation error "Name must be 255 characters or less"

### Requirement: Edit Recipe
The system SHALL allow editing an existing recipe's name and description.

#### Scenario: Successful recipe update
- **WHEN** the user modifies the name or description and submits
- **THEN** the system updates the recipe via PUT /api/v1/recipes/{id}
- **AND** displays a success toast "Recipe updated"

#### Scenario: Edit form pre-populated
- **WHEN** the user navigates to edit a recipe
- **THEN** the edit form SHALL be pre-populated with the recipe's current name and description

#### Scenario: Name conflict on update
- **WHEN** the user changes the name to one that already exists and the API returns 409
- **THEN** the system displays an error toast "A recipe with this name already exists"
- **AND** the form remains open so the user can adjust

### Requirement: Delete Recipe
The system SHALL allow deleting a recipe with confirmation, understanding that linked products will have their recipe_id set to null.

#### Scenario: Successful recipe deletion
- **WHEN** the user clicks "Delete" on a recipe and confirms in the modal
- **THEN** the system deletes the recipe via DELETE /api/v1/recipes/{id}
- **AND** removes the recipe from the list with an exit animation
- **AND** displays a success toast "Recipe deleted"

#### Scenario: Deletion cancelled
- **WHEN** the user clicks "Delete" on a recipe but cancels in the confirmation modal
- **THEN** no request is sent and the recipe remains in the list

### Requirement: Recipe Detail View
The system SHALL display a detailed view of a single recipe including its description, ingredient list, and total cost.

#### Scenario: Recipe detail loads with ingredients and cost
- **WHEN** the user views a recipe that has ingredients
- **THEN** the system displays: recipe name, description, list of ingredients (each showing raw material name, quantity, unit), and the total calculated cost from GET /api/v1/recipes/{id}/cost

#### Scenario: Recipe with no ingredients
- **WHEN** the user views a recipe that has zero ingredients
- **THEN** the system displays an empty state within the ingredient section: "No ingredients yet — add your first ingredient"
- **AND** the cost section shows "$0.00" or "No cost calculated"

#### Scenario: Cost calculation fails (missing raw material prices)
- **WHEN** the cost endpoint returns 424
- **THEN** the system displays a warning banner "Some ingredients have no price set — cost is incomplete" above the ingredient list

### Requirement: Navigation Between Products and Recipes
The system SHALL provide clear navigation between the Products and Recipes sections.

#### Scenario: Sidebar navigation
- **WHEN** the user is authenticated and viewing any page within the app
- **THEN** the sidebar displays "Products" and "Recipes" as navigation links
- **AND** the active link is visually highlighted

#### Scenario: Recipe name link from product detail
- **WHEN** the user views a product that has a linked recipe
- **THEN** the recipe name SHALL be a clickable link that navigates to that recipe's detail page
