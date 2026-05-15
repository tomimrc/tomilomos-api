## ADDED Requirements

### Requirement: Product List Display
The system SHALL display a paginated list of products belonging to the authenticated user's tenant.

#### Scenario: Products load successfully
- **WHEN** the user navigates to the products page and the API returns products
- **THEN** the system displays a table with columns: Name, Sale Price (formatted as currency), Cost Price, Status (active/inactive badge), and Actions
- **AND** the table supports pagination (previous/next or infinite scroll)

#### Scenario: No products exist
- **WHEN** the user navigates to the products page and the tenant has zero products
- **THEN** the system displays an empty state with a message "No products yet" and a CTA button "Create your first product"

#### Scenario: Products fail to load
- **WHEN** the API returns an error (network, 500, etc.)
- **THEN** the system displays an error state with a "Retry" button that refetches the products

#### Scenario: Loading state
- **WHEN** the products page mounts and the API request is in flight
- **THEN** the system displays a loading skeleton that mimics the table structure (rows with pulsing placeholders)

### Requirement: Create Product
The system SHALL allow creating a new product with name, sale price, optional recipe link, and active status.

#### Scenario: Successful product creation
- **WHEN** the user fills in all required fields (name, sale price) with valid values and submits
- **THEN** the system creates the product via POST /api/v1/products
- **AND** displays a success toast "Product created successfully"
- **AND** navigates to the product list where the new product appears

#### Scenario: Invalid sale price
- **WHEN** the user enters a sale price of 0, negative, or with more than 2 decimal places
- **THEN** the system displays an inline validation error "Price must be greater than 0 with up to 2 decimal places"
- **AND** the form is not submitted

#### Scenario: Name too long
- **WHEN** the user enters a product name exceeding 255 characters
- **THEN** the system displays an inline validation error "Name must be 255 characters or less"
- **AND** the form is not submitted

#### Scenario: Recipe-linked product creation
- **WHEN** the user selects a recipe from the dropdown and submits the form
- **THEN** the system sends `recipe_id` in the request body
- **AND** the created product appears linked to that recipe

### Requirement: Edit Product
The system SHALL allow editing an existing product's name, sale price, recipe link, and active status.

#### Scenario: Successful product update
- **WHEN** the user modifies fields in the edit form and submits
- **THEN** the system updates the product via PUT /api/v1/products/{id}
- **AND** displays a success toast "Product updated successfully"
- **AND** navigates back to the product detail or list

#### Scenario: Edit form pre-populated
- **WHEN** the user navigates to edit a product
- **THEN** the edit form SHALL be pre-populated with the product's current values (name, sale price, recipe, status)

#### Scenario: Unlink recipe from product
- **WHEN** the user clears the recipe selection (sets to "None") and submits
- **THEN** the system sends `recipe_id: null` in the PUT request
- **AND** the product no longer has a linked recipe

### Requirement: Delete Product
The system SHALL allow deleting a product with confirmation.

#### Scenario: Successful product deletion
- **WHEN** the user clicks "Delete" on a product and confirms in the modal
- **THEN** the system deletes the product via DELETE /api/v1/products/{id}
- **AND** removes the product from the list with an exit animation (Framer Motion)
- **AND** displays a success toast "Product deleted"

#### Scenario: Deletion cancelled
- **WHEN** the user clicks "Delete" on a product but cancels in the confirmation modal
- **THEN** no request is sent and the product remains in the list

### Requirement: Product Detail View
The system SHALL display a detailed view of a single product including its cost information.

#### Scenario: Product with recipe shows cost
- **WHEN** the user views a product that has a linked recipe
- **THEN** the system displays the product name, sale price, cost price (calculated from recipe), linked recipe name, and status
- **AND** the cost price is fetched from GET /api/v1/products/{id}/cost

#### Scenario: Product without recipe shows manual mode
- **WHEN** the user views a product that has no linked recipe
- **THEN** the system displays cost source as "Manual" with cost price showing as "—" or $0.00

#### Scenario: Cost calculation fails
- **WHEN** the cost endpoint returns a 424 error (missing raw material prices)
- **THEN** the system displays a warning "Cost cannot be calculated — some ingredients have no price set"
- **AND** the product still shows all other information correctly

#### Scenario: Product not found
- **WHEN** the user navigates to a product ID that does not exist
- **THEN** the system displays a 404 state "Product not found" with a link back to the product list
