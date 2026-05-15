## ADDED Requirements

### Requirement: Profitability Table Display
The system SHALL display a sortable, filterable table with profitability metrics for every product.

#### Scenario: Table loads with all products
- **WHEN** the dashboard loads and profitability data is available
- **THEN** the system displays a table with columns: Product Name (clickable link), Sale Price, Cost Price, Gross Margin ($), Margin (%), and a visual indicator
- **AND** the table is sorted by Margin (%) descending by default
- **AND** each column header is clickable to toggle sort direction

#### Scenario: Product with cost unavailable
- **WHEN** a product's cost endpoint returns 424 or the product has no recipe and manual pricing
- **THEN** the Gross Margin and Margin (%) columns display "—" for that product
- **AND** the row shows a warning icon with tooltip "Cost unavailable"

#### Scenario: Negative margin product
- **WHEN** a product's cost exceeds its sale price (negative margin)
- **THEN** the Margin (%) cell displays the percentage in red text
- **AND** the visual indicator shows a red downward arrow

#### Scenario: Positive margin product
- **WHEN** a product's sale price exceeds its cost
- **THEN** the Margin (%) cell displays the percentage in green text
- **AND** the visual indicator shows a green upward arrow

#### Scenario: Zero margin product
- **WHEN** a product's cost equals its sale price
- **THEN** the Margin (%) cell displays "0.00%" in neutral gray
- **AND** the visual indicator shows a gray dash

### Requirement: Profitability Filters
The system SHALL allow filtering the profitability table by margin type.

#### Scenario: Filter by all products
- **WHEN** the "All" filter is selected (default)
- **THEN** all products are displayed regardless of margin

#### Scenario: Filter by profitable only
- **WHEN** the user selects the "Profitable" filter
- **THEN** only products with margin > 0 are displayed
- **AND** products with unavailable costs are excluded

#### Scenario: Filter by unprofitable only
- **WHEN** the user selects the "Unprofitable" filter
- **THEN** only products with margin < 0 are displayed

#### Scenario: Filter with no results
- **WHEN** the selected filter yields zero products
- **THEN** the system displays an empty state message "No products match this filter"

### Requirement: Profitability Table Sorting
The system SHALL support sorting by any numeric or text column.

#### Scenario: Sort by margin percentage
- **WHEN** the user clicks the "Margin (%)" column header
- **THEN** the table toggles between ascending and descending order by margin percentage

#### Scenario: Sort by product name
- **WHEN** the user clicks the "Product Name" column header
- **THEN** the table sorts alphabetically by product name

#### Scenario: Sort by gross margin
- **WHEN** the user clicks the "Gross Margin" column header
- **THEN** the table sorts by the dollar amount of margin

### Requirement: Margin Calculation Accuracy
The system SHALL calculate profit margins using the backend-provided sale price and cost price with proper handling of edge cases.

#### Scenario: Recipe-based product margin
- **WHEN** a product has sale_price "50.00" and cost_price "32.50"
- **THEN** the gross margin displayed is "$17.50"
- **AND** the margin percentage displayed is "35.00%"

#### Scenario: Manual pricing product
- **WHEN** a product has sale_price "25.00" and cost_source "manual" (cost = 0)
- **THEN** the gross margin displayed is "$25.00"
- **AND** the margin percentage displayed is "100.00%"

#### Scenario: Product with zero sale price
- **WHEN** a product has sale_price "0.00" (edge case)
- **THEN** the margin percentage displayed is "—" (cannot divide by zero)
- **AND** the gross margin is the negative of cost_price

### Requirement: Product Name Navigation from Table
The system SHALL make product names in the profitability table clickable links to the product detail page.

#### Scenario: Click product name
- **WHEN** the user clicks a product name in the profitability table
- **THEN** the system navigates to `/app/products/{product_id}`
- **AND** the browser back button returns to the dashboard with filters preserved
