## ADDED Requirements

### Requirement: Sale price uses precise decimal representation
The system SHALL store and return sale_price using DECIMAL(10,2) precision to ensure accurate revenue calculations without floating-point rounding errors.

#### Scenario: Price with two decimal places is preserved
- **WHEN** creating a product with sale_price = 45.99
- **THEN** the system stores and returns the value as exactly 45.99 without floating-point rounding

#### Scenario: Price calculation maintains precision
- **WHEN** retrieving a product with sale_price = 0.50
- **THEN** the value is returned as exactly 0.50, not 0.500000001 or similar

#### Scenario: Price maximum value
- **WHEN** creating a product with sale_price = 99999999.99
- **THEN** the system accepts and stores the value successfully

#### Scenario: Price minimum value (just above zero)
- **WHEN** creating a product with sale_price = 0.01
- **THEN** the system accepts and stores the value successfully

### Requirement: Product pricing supports revenue calculations
The system SHALL allow retrieval of product pricing information for use in revenue and profitability calculations.

#### Scenario: Price is included in product retrieval
- **WHEN** an authenticated user retrieves a product via GET /api/v1/products/{id}
- **THEN** the response includes the sale_price field with full DECIMAL(10,2) precision

#### Scenario: Price is included in product list
- **WHEN** an authenticated user retrieves a list of products via GET /api/v1/products
- **THEN** each product in the response includes the sale_price field with full DECIMAL(10,2) precision

#### Scenario: Price can be updated independently
- **WHEN** an authenticated user updates only the sale_price field via PUT /api/v1/products/{id}
- **THEN** the system updates only the price while preserving other fields like name and is_active
