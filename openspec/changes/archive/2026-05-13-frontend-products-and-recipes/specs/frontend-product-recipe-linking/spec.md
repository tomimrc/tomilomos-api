## ADDED Requirements

### Requirement: Link Recipe to Product During Creation
The system SHALL allow selecting a recipe when creating a new product.

#### Scenario: Recipe selected during product creation
- **WHEN** the user creates a product and selects a recipe from the dropdown
- **THEN** the system sends `recipe_id` in the POST /api/v1/products request
- **AND** the created product is linked to that recipe

#### Scenario: No recipe selected (manual pricing)
- **WHEN** the user creates a product without selecting a recipe
- **THEN** the system sends the request without a `recipe_id` field (or with null)
- **AND** the product uses manual pricing mode

#### Scenario: Recipe selector loads tenant's recipes
- **WHEN** the product form mounts
- **THEN** the recipe dropdown fetches and displays the tenant's recipes via GET /api/v1/recipes
- **AND** the dropdown includes a "None" option to leave the product unlinked

### Requirement: Link Recipe to Product During Edit
The system SHALL allow changing or removing the recipe linked to an existing product.

#### Scenario: Recipe changed during edit
- **WHEN** the user edits a product and selects a different recipe
- **THEN** the system updates the product with the new `recipe_id`
- **AND** displays a success toast

#### Scenario: Recipe unlinked during edit
- **WHEN** the user edits a product and selects "None" for recipe
- **THEN** the system sends `recipe_id: null` in the PUT request
- **AND** the product switches to manual pricing mode
- **AND** the product detail page no longer shows recipe information

### Requirement: Display Linked Recipe on Product Detail
The system SHALL show which recipe (if any) is linked to a product on the product detail page.

#### Scenario: Product with linked recipe
- **WHEN** viewing a product that has a linked recipe
- **THEN** the system displays the recipe name as a clickable link to the recipe detail page
- **AND** shows the recipe description (if available)

#### Scenario: Product without linked recipe
- **WHEN** viewing a product without a linked recipe
- **THEN** the system displays "No recipe linked — manual pricing" or similar indicator
- **AND** offers an "Assign recipe" button that navigates to the edit form

### Requirement: Display Product Cost from Recipe
The system SHALL display the calculated cost of a product based on its linked recipe on the product detail page.

#### Scenario: Recipe-based product cost displayed
- **WHEN** viewing a product that has a linked recipe with ingredients
- **THEN** the system fetches and displays the total cost from GET /api/v1/products/{id}/cost
- **AND** labels the cost source as "Based on recipe: [Recipe Name]"

#### Scenario: Product cost updates after recipe ingredients change
- **WHEN** an ingredient is added, modified, or removed from the linked recipe
- **THEN** the product cost SHALL be refetched (React Query invalidation) and updated on the product detail page

#### Scenario: Product cost shows manual mode
- **WHEN** viewing a product without a linked recipe
- **THEN** the cost section displays "Manual pricing — no recipe linked"
- **AND** the cost amount is not shown or shows as "$0.00"

#### Scenario: Cost calculation unavailable
- **WHEN** the cost endpoint returns 424 (missing raw material prices)
- **THEN** the system displays a warning "Cost cannot be fully calculated — some ingredients lack pricing"
- **AND** the product still shows the linked recipe name

### Requirement: Recipe Selector Component
The system SHALL provide a reusable recipe selector dropdown component for product forms.

#### Scenario: Recipe selector shows all recipes
- **WHEN** the recipe selector mounts
- **THEN** the system fetches the tenant's recipes
- **AND** displays them in a searchable dropdown with recipe names

#### Scenario: Recipe selector loading state
- **WHEN** recipes are being fetched
- **THEN** the dropdown shows a loading spinner and is disabled

#### Scenario: Recipe selector error state
- **WHEN** recipes fail to load
- **THEN** the dropdown shows "Failed to load recipes" and a "Retry" button
- **AND** the user can still submit the product form without a recipe

### Requirement: Cross-Navigation Between Products and Recipes
The system SHALL allow navigating between a product and its linked recipe seamlessly.

#### Scenario: Navigate from product to linked recipe
- **WHEN** the user clicks the linked recipe name on a product detail page
- **THEN** the system navigates to `/app/recipes/{recipe_id}`
- **AND** the recipe detail page loads showing ingredients and cost

#### Scenario: Back navigation from recipe to product
- **WHEN** the user navigates to a recipe from a product and clicks the browser back button
- **THEN** the system returns to the previous product detail page with state preserved
