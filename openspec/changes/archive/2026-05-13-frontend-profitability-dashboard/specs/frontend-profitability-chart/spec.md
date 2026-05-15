## ADDED Requirements

### Requirement: Profitability Bar Chart
The system SHALL display a horizontal bar chart comparing profit margins of the top products.

#### Scenario: Chart renders with sufficient products
- **WHEN** the dashboard loads and 10 or more products have valid margins
- **THEN** the system displays a horizontal bar chart showing the top 10 products by margin percentage
- **AND** each bar is labeled with the product name on the left and margin percentage on the right
- **AND** bars are color-coded: green for positive margins, red for negative margins

#### Scenario: Chart with fewer than 10 products
- **WHEN** the tenant has fewer than 10 products with valid margins
- **THEN** the chart displays all available products
- **AND** the chart title shows "Top N Products" where N is the actual count

#### Scenario: Chart with no valid margins
- **WHEN** no products have calculable margins (all cost unavailable or 0 products)
- **THEN** the chart area displays an empty state "No margin data available"
- **AND** the chart container retains its size to avoid layout shift

#### Scenario: Chart loading state
- **WHEN** product costs are still being fetched
- **THEN** the chart area displays a loading skeleton (pulsing placeholder bars)

### Requirement: Chart Interactivity
The system SHALL support basic interactivity on the bar chart.

#### Scenario: Hover tooltip
- **WHEN** the user hovers over a bar
- **THEN** a tooltip appears showing: product name, sale price, cost price, gross margin ($), and margin (%)

#### Scenario: Click bar to navigate
- **WHEN** the user clicks on a bar
- **THEN** the system navigates to that product's detail page at `/app/products/{product_id}`

### Requirement: Chart Responsiveness
The system SHALL render the chart responsively to fit different screen sizes.

#### Scenario: Desktop view
- **WHEN** viewed on a screen wider than 1024px
- **THEN** the chart occupies approximately 50-60% of the dashboard width
- **AND** is positioned alongside the summary cards or below them

#### Scenario: Mobile view
- **WHEN** viewed on a screen narrower than 768px
- **THEN** the chart spans full width
- **AND** bars remain readable with truncated product names if needed

### Requirement: Chart Data Consistency
The system SHALL keep the chart data consistent with the table filters.

#### Scenario: Filter applied to table
- **WHEN** the user filters the table to show only "Profitable" products
- **THEN** the chart SHALL also update to show only profitable products
- **AND** the chart title updates to reflect the active filter (e.g., "Top Profitable Products")

#### Scenario: Reset filter
- **WHEN** the user switches back to "All" filter
- **THEN** the chart returns to showing all products with valid margins

### Requirement: Axis and Label Formatting
The system SHALL format chart axes and labels clearly for financial data.

#### Scenario: Percentage axis
- **WHEN** the chart renders
- **THEN** the X-axis (bottom) shows percentage values with "%" suffix
- **AND** the axis starts at 0% or the minimum margin if negative margins exist
- **AND** includes grid lines for readability

#### Scenario: Product name labels
- **WHEN** product names exceed 20 characters
- **THEN** the Y-axis labels SHALL truncate the name with ellipsis
- **AND** the full name is visible in the hover tooltip
