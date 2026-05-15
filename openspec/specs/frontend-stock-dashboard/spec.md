## ADDED Requirements

### Requirement: Stock Level Dashboard Display
The system SHALL display a dashboard view of all raw material stock levels for quick monitoring.

#### Scenario: Dashboard loads
- **WHEN** the user navigates to /app/stock
- **THEN** the system displays a table with columns: Material Name, Unit, Current Stock (with color-coded StockLevelBadge), Supplier, Cost per Unit
- **AND** the table is sorted by stock level ascending by default (low stock first)

#### Scenario: No materials exist
- **WHEN** the tenant has no raw materials
- **THEN** the system displays an empty state "No raw materials to monitor" with link to create materials

#### Scenario: Stock fails to load
- **WHEN** the API returns an error
- **THEN** the system displays an error state with a "Retry" button

#### Scenario: Quick stock adjustment access
- **WHEN** the user clicks on a raw material name in the stock dashboard
- **THEN** the system navigates to the raw material detail page (/app/raw-materials/:id) where stock can be adjusted

### Requirement: Stock Dashboard Filtering and Sorting
The system SHALL allow filtering and sorting the stock dashboard.

#### Scenario: Search by name
- **WHEN** the user types in the search input
- **THEN** the table filters to show only materials whose name contains the search text (case-insensitive)

#### Scenario: Sort by stock level
- **WHEN** the user clicks the stock column header
- **THEN** the table sorts by stock quantity ascending/descending

#### Scenario: Highlight low stock
- **WHEN** materials have stock ≤ 10
- **THEN** they SHALL appear with amber/red badges to draw attention
- **AND** they SHALL appear at the top when sorted by stock ascending

### Requirement: Stock Dashboard Page Layout
The system SHALL present the stock dashboard with clear, actionable information.

#### Scenario: Page header
- **WHEN** viewing the stock dashboard
- **THEN** the header displays "Stock Monitor" with subtitle "Track raw material levels and identify what needs restocking"
- **AND** a summary shows count of materials with low stock (≤ 10) and out of stock (0)

#### Scenario: Page transition
- **WHEN** navigating to or from the stock dashboard
- **THEN** the page SHALL have a Framer Motion transition (opacity + y)

#### Scenario: Refresh stock data
- **WHEN** the user clicks a refresh button or navigates back from a stock adjustment
- **THEN** the stock data SHALL be refetched to show the latest levels
