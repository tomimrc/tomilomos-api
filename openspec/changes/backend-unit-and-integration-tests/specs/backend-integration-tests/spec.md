## ADDED Requirements

### Requirement: Full auth flow integration test
The test suite SHALL verify the complete auth flow from login to accessing protected resources.

#### Scenario: Login → get token → access protected endpoint
- **WHEN** a test logs in, extracts the JWT token, and calls `GET /api/v1/raw-materials` with it
- **THEN** the request succeeds with HTTP 200

#### Scenario: Invalid token is rejected on protected endpoint
- **WHEN** a test calls `GET /api/v1/raw-materials` with a forged JWT token
- **THEN** the system returns HTTP 401

### Requirement: Multi-tenant isolation integration test
The test suite SHALL verify that tenants cannot access each other's data.

#### Scenario: Tenant A cannot see Tenant B's raw materials
- **WHEN** a test creates data for Tenant A and Tenant B, then queries raw materials with Tenant A's token
- **THEN** only Tenant A's raw materials are returned

#### Scenario: Tenant A cannot create sales for Tenant B's products
- **WHEN** a test attempts to create a sale for Tenant B's product using Tenant A's token
- **THEN** the system returns HTTP 404

### Requirement: CRUD integration tests with real auth
The test suite SHALL verify all CRUD endpoints work with real JWT authentication.

#### Scenario: Full raw materials CRUD with auth
- **WHEN** a test creates, reads, updates, and deletes a raw material using an authenticated client
- **THEN** all operations succeed with correct HTTP status codes

#### Scenario: Full products CRUD with auth
- **WHEN** a test creates, reads, updates, and deletes a product using an authenticated client
- **THEN** all operations succeed with correct HTTP status codes

#### Scenario: Full recipes CRUD with auth
- **WHEN** a test creates, reads, updates, and deletes a recipe with ingredients using an authenticated client
- **THEN** all operations succeed with correct HTTP status codes

#### Scenario: Sales creation with stock deduction
- **WHEN** a test creates a sale for a product linked to a recipe
- **THEN** the sale is created and raw material stock is reduced
