## ADDED Requirements

### Requirement: Create a new product
The system SHALL allow authenticated users to create a new product record within their tenant, with fields for name, sale price, and active status.

#### Scenario: Create product successfully
- **WHEN** an authenticated user sends a POST request to `/api/v1/products` with valid name and sale_price
- **THEN** the system creates a new Product record scoped to the user's tenant and returns HTTP 201 with the created product data including id and timestamps

#### Scenario: Name is required
- **WHEN** attempting to create a product without a name
- **THEN** the system returns HTTP 400 Bad Request with validation error indicating name is required

#### Scenario: Sale price is required
- **WHEN** attempting to create a product without sale_price
- **THEN** the system returns HTTP 400 Bad Request with validation error indicating sale_price is required

#### Scenario: Sale price must be positive
- **WHEN** attempting to create a product with sale_price ≤ 0
- **THEN** the system returns HTTP 400 Bad Request with validation error indicating price must be greater than 0

#### Scenario: is_active defaults to true
- **WHEN** creating a product without specifying is_active
- **THEN** the system creates the record successfully with is_active set to true

#### Scenario: Multi-tenant isolation on create
- **WHEN** user A creates a product in tenant A
- **THEN** the product is only accessible within tenant A and not visible to users in other tenants

### Requirement: Retrieve all products for a tenant
The system SHALL allow authenticated users to retrieve a list of all products for their tenant with pagination and optional filtering.

#### Scenario: List products successfully
- **WHEN** an authenticated user sends a GET request to `/api/v1/products`
- **THEN** the system returns HTTP 200 with a paginated list of all products in the user's tenant, including id, name, sale_price, is_active, created_at, and updated_at

#### Scenario: List returns empty when no products exist
- **WHEN** an authenticated user in a new tenant sends a GET request to `/api/v1/products`
- **THEN** the system returns HTTP 200 with an empty list

#### Scenario: List respects pagination
- **WHEN** an authenticated user sends a GET request to `/api/v1/products?skip=0&limit=10`
- **THEN** the system returns no more than 10 products in the response

#### Scenario: List is filtered by tenant
- **WHEN** user A in tenant A retrieves products
- **THEN** only products created by users in tenant A are returned

### Requirement: Retrieve a specific product
The system SHALL allow authenticated users to retrieve a single product by its ID if it belongs to their tenant.

#### Scenario: Get product successfully
- **WHEN** an authenticated user sends a GET request to `/api/v1/products/{id}` for a product in their tenant
- **THEN** the system returns HTTP 200 with the product data

#### Scenario: Product not found
- **WHEN** an authenticated user sends a GET request to `/api/v1/products/{id}` for a non-existent product
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Cannot access product from different tenant
- **WHEN** user A from tenant A attempts to GET a product that belongs to tenant B
- **THEN** the system returns HTTP 404 Not Found (not 403 Forbidden, to avoid leaking that the resource exists)

### Requirement: Update a product
The system SHALL allow authenticated users to update fields of a product record (name, sale_price, is_active) if it belongs to their tenant.

#### Scenario: Update product successfully
- **WHEN** an authenticated user sends a PUT request to `/api/v1/products/{id}` with updated fields
- **THEN** the system updates the Product record and returns HTTP 200 with the updated data

#### Scenario: Update sale price to negative value fails
- **WHEN** attempting to update a product with sale_price ≤ 0
- **THEN** the system returns HTTP 400 Bad Request with validation error

#### Scenario: Cannot update product from different tenant
- **WHEN** user A from tenant A attempts to UPDATE a product that belongs to tenant B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Partial updates are allowed
- **WHEN** sending a PUT request with only some fields populated (e.g., only is_active)
- **THEN** the system updates only the provided fields and leaves others unchanged

#### Scenario: Update timestamp is recorded
- **WHEN** a product is successfully updated
- **THEN** the updated_at timestamp is set to the current time

### Requirement: Delete a product
The system SHALL allow authenticated users to delete a product record from their tenant. Deletion is permanent.

#### Scenario: Delete product successfully
- **WHEN** an authenticated user sends a DELETE request to `/api/v1/products/{id}` for a product in their tenant
- **THEN** the system deletes the Product record and returns HTTP 204 No Content

#### Scenario: Delete non-existent product
- **WHEN** an authenticated user sends a DELETE request to `/api/v1/products/{id}` for a non-existent product
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Cannot delete product from different tenant
- **WHEN** user A from tenant A attempts to DELETE a product that belongs to tenant B
- **THEN** the system returns HTTP 404 Not Found
