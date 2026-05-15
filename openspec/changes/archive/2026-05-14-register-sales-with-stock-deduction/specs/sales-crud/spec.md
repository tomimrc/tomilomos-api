## ADDED Requirements

### Requirement: Sale Model
The system SHALL store sales with product reference, quantity, pricing snapshot, and cost data.

#### Scenario: Sale record created
- **WHEN** a sale is registered
- **THEN** the system stores: id (UUID), tenant_id, product_id (FK), quantity (integer > 0), unit_price (Decimal snapshot of product.sale_price), total_price (unit_price × quantity), total_cost (nullable Decimal, from recipe × quantity), margin (total_price - total_cost, nullable), and created_at (UTC timestamp)

### Requirement: Create Sale Endpoint
The system SHALL expose an endpoint to register a new sale with automatic stock deduction.

#### Scenario: Successful sale with recipe
- **WHEN** a POST to /api/v1/sales with valid product_id and quantity is made
- **THEN** the system creates the sale record with frozen prices and calculated costs
- **AND** returns 201 with the SaleRead response including product_name, unit_price, total_price, total_cost, margin, and created_at

#### Scenario: Sale of product without recipe
- **WHEN** the product has no recipe_id
- **THEN** the total_cost and margin fields SHALL be null in the response
- **AND** no stock deduction is performed
- **AND** the sale is still created successfully (201)

#### Scenario: Product not found
- **WHEN** the product_id does not exist or is inactive
- **THEN** the system returns 400 "Product not found or inactive"

#### Scenario: Invalid quantity
- **WHEN** quantity is 0, negative, or non-integer
- **THEN** the system returns 422 (Pydantic validation error)

### Requirement: List Sales Endpoint
The system SHALL expose an endpoint to list sales with pagination.

#### Scenario: Sales list with pagination
- **WHEN** a GET to /api/v1/sales?skip=0&limit=50 is made
- **THEN** the system returns a list of SaleRead objects ordered by created_at descending
- **AND** each sale includes product_name

#### Scenario: No sales exist
- **WHEN** the tenant has no recorded sales
- **THEN** the system returns an empty list (200)

### Requirement: Get Sale Endpoint
The system SHALL expose an endpoint to retrieve a single sale by ID.

#### Scenario: Sale found
- **WHEN** a GET to /api/v1/sales/{id} is made with a valid sale ID
- **THEN** the system returns the SaleRead object with all fields

#### Scenario: Sale not found
- **WHEN** the sale ID does not exist or belongs to another tenant
- **THEN** the system returns 404 "Sale not found"

### Requirement: Multi-Tenant Isolation
The system SHALL enforce tenant isolation on all sale operations.

#### Scenario: Sale creation with tenant context
- **WHEN** a sale is created
- **THEN** the tenant_id is extracted from the JWT token and set on the sale record
- **AND** the product lookup SHALL be scoped to the authenticated tenant

#### Scenario: Cross-tenant access prevented
- **WHEN** a user requests a sale from another tenant
- **THEN** the system returns 404 (not 403) to avoid leaking existence information
