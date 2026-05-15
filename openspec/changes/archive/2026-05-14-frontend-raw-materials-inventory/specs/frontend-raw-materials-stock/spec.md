## ADDED Requirements

### Requirement: Stock Level Display with Visual Indicator
The system SHALL display the current stock level of each raw material with a color-coded badge.

#### Scenario: Normal stock level
- **WHEN** a raw material has current_stock > 10
- **THEN** the stock badge displays the quantity in green with a check or box icon

#### Scenario: Low stock level
- **WHEN** a raw material has current_stock > 0 and ≤ 10
- **THEN** the stock badge displays the quantity in amber/yellow with a warning icon
- **AND** the badge text includes "Low stock" as a label

#### Scenario: Out of stock
- **WHEN** a raw material has current_stock = 0
- **THEN** the stock badge displays "0" in red with an alert icon
- **AND** the badge text includes "Out of stock" as a label

#### Scenario: Stock badge on list page
- **WHEN** viewing the raw materials list
- **THEN** each row SHALL display the stock badge in the Current Stock column
- **AND** the table can be sorted by stock quantity

### Requirement: Add Stock
The system SHALL allow adding stock to a raw material via a modal dialog.

#### Scenario: Successful stock addition
- **WHEN** the user opens "Add Stock" on a material detail page, enters a quantity > 0, and submits
- **THEN** the system calls POST /api/v1/raw-materials/{id}/add-stock
- **AND** displays a success toast "Stock added successfully"
- **AND** the stock level updates immediately on the detail page

#### Scenario: Quantity validation
- **WHEN** the user enters a quantity of 0, negative, or non-numeric
- **THEN** the system displays an inline validation error "Quantity must be greater than 0"
- **AND** the submit button is disabled

#### Scenario: Reason is optional
- **WHEN** the user adds stock without entering a reason
- **THEN** the system sends the request with `reason: null` and the operation succeeds

#### Scenario: Reason provided
- **WHEN** the user enters a reason (e.g., "Weekly purchase")
- **THEN** the system sends the reason in the request body

### Requirement: Remove Stock
The system SHALL allow removing stock from a raw material via a modal dialog, with validation for insufficient stock.

#### Scenario: Successful stock removal
- **WHEN** the user opens "Remove Stock", enters a quantity ≤ current stock, and submits
- **THEN** the system calls POST /api/v1/raw-materials/{id}/remove-stock
- **AND** displays a success toast "Stock removed successfully"
- **AND** the stock level updates immediately

#### Scenario: Insufficient stock
- **WHEN** the user enters a quantity greater than current_stock and submits
- **THEN** the backend returns a 400 error "Insufficient stock"
- **AND** the system displays an error toast with the backend's error message
- **AND** the stock level does NOT change

#### Scenario: Current stock shown in modal
- **WHEN** the "Remove Stock" modal opens
- **THEN** the modal displays the current stock level as reference text (e.g., "Available: 25.50 kg")

### Requirement: Stock Adjustment Modal
The system SHALL provide a reusable modal component for both add and remove stock operations.

#### Scenario: Add stock mode
- **WHEN** the user opens the stock modal in "add" mode
- **THEN** the modal title reads "Add Stock — [Material Name]"
- **AND** the action button reads "Add Stock" in green/primary color
- **AND** the quantity input has no maximum limit

#### Scenario: Remove stock mode
- **WHEN** the user opens the stock modal in "remove" mode
- **THEN** the modal title reads "Remove Stock — [Material Name]"
- **AND** the action button reads "Remove Stock" in red/danger color
- **AND** the current available stock is displayed as reference

#### Scenario: Modal loading state
- **WHEN** the stock adjustment request is in flight
- **THEN** the action button shows a loading spinner and is disabled
- **AND** the cancel button is also disabled

#### Scenario: Modal closes on success
- **WHEN** the stock adjustment succeeds
- **THEN** the modal closes automatically
- **AND** the detail page refreshes the stock data

### Requirement: Stock Data Freshness
The system SHALL keep stock data up to date after any adjustment.

#### Scenario: Stock updated after add
- **WHEN** stock is added successfully
- **THEN** the system invalidates the raw material query and refetches current stock
- **AND** the list page also reflects the updated stock when the user navigates back

#### Scenario: Stock updated after remove
- **WHEN** stock is removed successfully
- **THEN** the system invalidates and refetches the stock data
- **AND** the stock badge color updates if the level crossed a threshold

### Requirement: Cost Update Propagation
The system SHALL trigger cost recalculation in dependent features when a raw material's cost changes.

#### Scenario: Cost updated
- **WHEN** a raw material's cost_per_unit is updated via the edit form
- **THEN** the system invalidates recipe cost queries and product cost queries
- **AND** navigating to a recipe or product detail shows the updated costs

#### Scenario: Cost update on list page
- **WHEN** viewing the raw materials list after a cost update
- **THEN** the cost column reflects the new value immediately (via query invalidation)
