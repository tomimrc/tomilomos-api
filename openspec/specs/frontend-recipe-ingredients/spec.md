## ADDED Requirements

### Requirement: View Recipe Ingredients
The system SHALL display all ingredients of a recipe with their details on the recipe detail page.

#### Scenario: Ingredients list displays correctly
- **WHEN** the user views a recipe that has ingredients
- **THEN** the system displays a list where each ingredient shows: raw material name, quantity, unit (kg, g, L, mL, units, pieces, boxes), unit cost, and total ingredient cost
- **AND** the list is fetched from GET /api/v1/recipes/{recipe_id}/ingredients and GET /api/v1/recipes/{recipe_id}/cost

#### Scenario: Empty ingredient list
- **WHEN** the recipe has no ingredients
- **THEN** the system displays an empty state "No ingredients yet" with an "Add first ingredient" button

#### Scenario: Ingredient list loading
- **WHEN** the recipe detail page mounts and ingredients are being fetched
- **THEN** the system displays loading spinners or skeleton placeholders for the ingredient rows

### Requirement: Add Ingredient to Recipe
The system SHALL allow adding an ingredient (raw material) to a recipe with quantity and unit.

#### Scenario: Successful ingredient addition
- **WHEN** the user selects a raw material, enters a valid quantity, selects a unit, and submits
- **THEN** the system creates the ingredient via POST /api/v1/recipes/{recipe_id}/ingredients
- **AND** displays a success toast "Ingredient added"
- **AND** the new ingredient appears in the list with an enter animation (Framer Motion)
- **AND** the recipe cost updates to reflect the new ingredient

#### Scenario: Quantity must be positive
- **WHEN** the user enters a quantity of 0 or negative
- **THEN** the system displays an inline validation error "Quantity must be greater than 0"
- **AND** the form is not submitted

#### Scenario: Unit must be selected
- **WHEN** the user submits without selecting a unit
- **THEN** the system displays an inline validation error "Unit is required"
- **AND** the form is not submitted

#### Scenario: Raw material must be selected
- **WHEN** the user submits without selecting a raw material
- **THEN** the system displays an inline validation error "Raw material is required"
- **AND** the form is not submitted

#### Scenario: Duplicate raw material
- **WHEN** the user tries to add a raw material that already exists in the recipe
- **THEN** the API returns a conflict error and the system displays an error toast "This raw material is already in the recipe"
- **AND** the ingredient is not added

### Requirement: Edit Ingredient in Recipe
The system SHALL allow modifying the quantity and unit of an existing ingredient in a recipe.

#### Scenario: Successful ingredient update
- **WHEN** the user modifies the quantity or unit of an existing ingredient and confirms
- **THEN** the system updates via PUT /api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}
- **AND** displays a success toast "Ingredient updated"
- **AND** the recipe cost updates

#### Scenario: Inline edit mode
- **WHEN** the user clicks "Edit" on an ingredient row
- **THEN** the quantity and unit fields become editable inline (no modal or separate page)
- **AND** "Save" and "Cancel" buttons appear next to the row

### Requirement: Remove Ingredient from Recipe
The system SHALL allow removing an ingredient from a recipe with confirmation.

#### Scenario: Successful ingredient removal
- **WHEN** the user clicks "Remove" on an ingredient and confirms
- **THEN** the system deletes via DELETE /api/v1/recipes/{recipe_id}/ingredients/{ingredient_id}
- **AND** the ingredient row disappears with an exit animation
- **AND** displays a success toast "Ingredient removed"
- **AND** the recipe cost updates

#### Scenario: Removal cancelled
- **WHEN** the user clicks "Remove" but cancels the confirmation
- **THEN** the ingredient remains in the list

### Requirement: Recipe Cost Display
The system SHALL display the total calculated cost of a recipe based on its ingredients and current raw material prices.

#### Scenario: Recipe cost with all prices available
- **WHEN** all ingredients have raw materials with defined prices
- **THEN** the system displays the total recipe cost prominently (e.g., "Total Cost: $45.99")
- **AND** each ingredient row shows its individual contribution to the total cost

#### Scenario: Recipe cost with missing prices
- **WHEN** some ingredients have raw materials without prices (API returns 424 or partial data)
- **THEN** the system displays a warning "Cost may be incomplete — some ingredients have no price"
- **AND** ingredients with missing prices are visually distinguished (e.g., muted row with warning icon)

#### Scenario: Ingredient with zero cost
- **WHEN** a raw material has a price of $0.00
- **THEN** the ingredient row shows "$0.00" as the total cost for that ingredient
- **AND** the system does NOT show a warning (zero is a valid price, distinct from missing)

### Requirement: Raw Material Selector
The system SHALL provide a searchable dropdown to select raw materials when adding ingredients.

#### Scenario: Raw material search and selection
- **WHEN** the user opens the raw material selector in the ingredient form
- **THEN** the system fetches and displays the tenant's raw materials via GET /api/v1/raw-materials
- **AND** the user can type to filter/search by name
- **AND** selecting a raw material populates the field

#### Scenario: No raw materials available
- **WHEN** the tenant has no raw materials
- **THEN** the selector displays "No raw materials available — create one first"
- **AND** the Add button is disabled
