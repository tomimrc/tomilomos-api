## ADDED Requirements

### Requirement: KPI Summary Cards Display
The system SHALL display summary KPI cards at the top of the profitability dashboard showing key metrics calculated from all products.

#### Scenario: All products have valid costs
- **WHEN** the dashboard loads and all products have calculable costs
- **THEN** the system displays four cards: Average Margin (%), Most Profitable Product (name + margin), Least Profitable Product (name + margin), and Active Products (count)
- **AND** each card shows a trend icon (Lucide) and the calculated value

#### Scenario: Some products have missing costs
- **WHEN** some products return 424 or have manual pricing (cost = 0)
- **THEN** the Average Margin card SHALL exclude products with unavailable costs from the calculation
- **AND** the count of excluded products is shown as a footnote ("X products excluded — cost unavailable")

#### Scenario: No products exist
- **WHEN** the tenant has zero products
- **THEN** the summary cards display zeros or "—" for all metrics
- **AND** the Most/Least Profitable cards show "No products"

#### Scenario: Single product
- **WHEN** the tenant has exactly one product
- **THEN** the Most and Least Profitable cards SHALL both show the same product
- **AND** the Average Margin card shows that single product's margin

### Requirement: Average Margin Calculation
The system SHALL calculate the average profit margin percentage across all products with available costs.

#### Scenario: Average margin with mixed costs
- **WHEN** 3 products have margins of 50%, 30%, and 20%
- **THEN** the average margin displayed is 33.33% (rounded to 2 decimals)

#### Scenario: Product with zero sale price excluded
- **WHEN** a product has sale_price = 0
- **THEN** that product SHALL be excluded from the average margin calculation
- **AND** counted in the excluded products footnote

### Requirement: Most and Least Profitable Product Identification
The system SHALL identify and display the product with the highest and lowest profit margin.

#### Scenario: Clear winner and loser
- **WHEN** products have varying margins
- **THEN** the Most Profitable card shows the product with the highest margin (%) and its margin value
- **AND** the Least Profitable card shows the product with the lowest margin (could be negative) and its margin value
- **AND** product names are clickable links to their detail pages

#### Scenario: Tie in margins
- **WHEN** two products share the same highest margin
- **THEN** the Most Profitable card shows the first one alphabetically by name

### Requirement: Active Products Count
The system SHALL display the count of active products in the tenant.

#### Scenario: Mixed active and inactive products
- **WHEN** the tenant has 10 products, 7 active and 3 inactive
- **THEN** the Active Products card shows "7"
- **AND** includes a subtitle "out of 10 total"

#### Scenario: All products inactive
- **WHEN** all products are inactive
- **THEN** the Active Products card shows "0"
- **AND** displays "out of N total"
