## ADDED Requirements

### Requirement: Sales History List
The system SHALL display a paginated list of past sales ordered by date descending.

#### Scenario: Sales load successfully
- **WHEN** the user navigates to the sales history page and the API returns sales
- **THEN** the system displays a table with columns: Date, Product, Quantity, Unit Price (currency), Total (currency), Cost (currency or "—"), Margin (currency or "—")
- **AND** sales are sorted by date descending (most recent first)

#### Scenario: No sales exist
- **WHEN** the tenant has zero recorded sales
- **THEN** the system displays an empty state with message "No sales recorded yet" and CTA "Register your first sale"

#### Scenario: Sales fail to load
- **WHEN** the API returns an error
- **THEN** the system displays an error state with a "Retry" button

#### Scenario: Search by product name
- **WHEN** the user types in the search input
- **THEN** the table filters to show only sales whose product name contains the search text (case-insensitive client-side filter)

### Requirement: Sales History Table Formatting
The system SHALL format sales data consistently.

#### Scenario: Currency formatting
- **WHEN** displaying monetary values (unit price, total, cost, margin)
- **THEN** they SHALL be formatted as currency (e.g., $15.00) with 2 decimal places

#### Scenario: Missing cost display
- **WHEN** a sale has no cost data (total_cost is null)
- **THEN** the cost and margin columns display "—"

#### Scenario: Date formatting
- **WHEN** displaying sale dates
- **THEN** they SHALL be formatted as readable date strings (e.g., "May 14, 2026, 03:30 PM")

### Requirement: Sales History Page Navigation
The system SHALL provide navigation to and from the sales history page.

#### Scenario: Navigate from sales entry
- **WHEN** the user is on the sales entry page and clicks "Sales History"
- **THEN** the system navigates to /app/sales/history

#### Scenario: Navigate back to sales entry
- **WHEN** the user is on the sales history page and clicks "New Sale"
- **THEN** the system navigates to /app/sales
