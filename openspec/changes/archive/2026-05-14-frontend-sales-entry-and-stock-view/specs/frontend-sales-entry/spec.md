## ADDED Requirements

### Requirement: Product Selector for Sales
The system SHALL provide a searchable product selector to choose which product is being sold.

#### Scenario: Products load successfully
- **WHEN** the user opens the sales entry page
- **THEN** the product selector displays all active products (is_active = true) with name and sale price
- **AND** the selector supports search/filter by product name

#### Scenario: Products fail to load
- **WHEN** the products API returns an error
- **THEN** the product selector displays "Failed to load products" and a retry button

#### Scenario: No active products
- **WHEN** the tenant has no active products
- **THEN** the product selector displays "No products available" and a link to create products

#### Scenario: Product selected
- **WHEN** the user selects a product from the dropdown
- **THEN** the selected product's name and sale price are displayed
- **AND** the quantity input becomes enabled

### Requirement: Sale Quantity Input
The system SHALL allow entering the quantity of units sold.

#### Scenario: Quantity entered
- **WHEN** the user enters a valid positive integer quantity
- **THEN** the system calculates and displays the total (unit_price × quantity) in currency format

#### Scenario: Invalid quantity
- **WHEN** the user enters 0, negative, or non-numeric quantity
- **THEN** the system displays an inline validation error "Quantity must be greater than 0"
- **AND** the confirm button is disabled

#### Scenario: Subtotal updates in real-time
- **WHEN** the user changes quantity after selecting a product
- **THEN** the displayed total updates immediately to reflect unit_price × quantity

### Requirement: Sale Confirmation Modal
The system SHALL show a confirmation modal with a summary before registering the sale.

#### Scenario: Confirmation modal opens
- **WHEN** the user clicks "Review Sale" after selecting a product and entering quantity
- **THEN** a modal displays: product name, quantity, unit price (currency), total price (currency)
- **AND** if the product has a cost_price, the modal shows estimated cost and estimated margin
- **AND** the modal shows "Cancel" and "Confirm Sale" buttons

#### Scenario: Sale confirmed successfully
- **WHEN** the user confirms the sale in the modal
- **THEN** the system calls POST /api/v1/sales with product_id and quantity
- **AND** displays a success toast "Sale registered successfully"
- **AND** the form resets to initial state (no product selected, quantity cleared)
- **AND** the modal closes

#### Scenario: Sale fails
- **WHEN** the backend returns an error (e.g., insufficient stock, product not found)
- **THEN** the system displays an error toast with the backend's error message
- **AND** the form retains the entered values so the user can retry
- **AND** the modal closes on error to allow correction

### Requirement: Sales Entry Page Layout
The system SHALL present the sales entry form in a clean, focused layout.

#### Scenario: Page loads
- **WHEN** the user navigates to /app/sales
- **THEN** the page displays: title "New Sale", product selector, quantity input, calculated total display, and "Review Sale" button
- **AND** the page has a Framer Motion page transition

#### Scenario: Form initial state
- **WHEN** the page first loads
- **THEN** the product selector shows placeholder "Select a product..."
- **AND** the quantity input is disabled until a product is selected
- **AND** the "Review Sale" button is disabled until both product and valid quantity are provided
