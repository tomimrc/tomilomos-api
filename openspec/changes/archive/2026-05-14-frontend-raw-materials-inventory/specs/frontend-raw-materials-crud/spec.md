## ADDED Requirements

### Requirement: Raw Material List Display
The system SHALL display a paginated, filterable list of raw materials belonging to the authenticated user's tenant.

#### Scenario: Materials load successfully
- **WHEN** the user navigates to the raw materials page and the API returns materials
- **THEN** the system displays a table with columns: Name, Unit, Cost per Unit (currency), Current Stock (with stock level badge), Supplier, and Actions
- **AND** the table supports sorting by any column (default: name ascending)

#### Scenario: No materials exist
- **WHEN** the tenant has zero raw materials
- **THEN** the system displays an empty state with message "No raw materials yet" and CTA "Create your first raw material"

#### Scenario: Materials fail to load
- **WHEN** the API returns an error
- **THEN** the system displays an error state with a "Retry" button

#### Scenario: Search by name
- **WHEN** the user types in the search/filter input
- **THEN** the table filters to show only materials whose name contains the search text (case-insensitive client-side filter)

### Requirement: Create Raw Material
The system SHALL allow creating a new raw material with name, unit of measurement, cost per unit, and optional supplier.

#### Scenario: Successful creation
- **WHEN** the user fills in name, selects a valid unit, enters a cost > 0, and submits
- **THEN** the system creates the material via POST /api/v1/raw-materials
- **AND** displays a success toast "Raw material created"
- **AND** navigates to the raw materials list

#### Scenario: Invalid cost
- **WHEN** the user enters a cost of 0 or negative
- **THEN** the system displays an inline validation error "Cost must be greater than 0"
- **AND** the form is not submitted

#### Scenario: Name too long
- **WHEN** the user enters a name exceeding 255 characters
- **THEN** the system displays an inline validation error "Name must be 255 characters or less"

#### Scenario: Unit not selected
- **WHEN** the user submits without selecting a unit of measurement
- **THEN** the system displays an inline validation error "Unit is required"

### Requirement: Edit Raw Material
The system SHALL allow editing an existing raw material's name, unit, cost, and supplier.

#### Scenario: Successful update
- **WHEN** the user modifies fields and submits
- **THEN** the system updates via PUT /api/v1/raw-materials/{id}
- **AND** displays a success toast "Raw material updated"
- **AND** navigates to the material detail page

#### Scenario: Edit form pre-populated
- **WHEN** the user navigates to edit a material
- **THEN** the form SHALL be pre-populated with the current values (name, unit, cost, supplier)

#### Scenario: Cost update triggers recipe cost refresh
- **WHEN** a material's cost is updated
- **THEN** the system invalidates recipe cost queries (React Query invalidation) so linked recipes reflect new costs

### Requirement: Delete Raw Material
The system SHALL allow deleting a raw material with confirmation.

#### Scenario: Successful deletion
- **WHEN** the user confirms deletion in the dialog
- **THEN** the system deletes via DELETE /api/v1/raw-materials/{id}
- **AND** displays a success toast "Raw material deleted"
- **AND** removes the material from the list with exit animation

#### Scenario: Deletion blocked by recipe usage
- **WHEN** the material is used in one or more recipes and the backend returns an error (409 or FK constraint)
- **THEN** the system displays an error toast "Cannot delete — this material is used in recipes"

### Requirement: Raw Material Detail View
The system SHALL display detailed information about a single raw material including its stock level.

#### Scenario: Detail page loads
- **WHEN** the user views a raw material detail
- **THEN** the system displays: name, unit of measurement, cost per unit (currency), supplier (or "—"), current stock with stock level badge, created/updated dates
- **AND** action buttons: Edit, Delete, Add Stock, Remove Stock

#### Scenario: Material not found
- **WHEN** the user navigates to an ID that does not exist
- **THEN** the system displays a 404 state "Raw material not found" with a link back to the list
