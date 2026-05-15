## ADDED Requirements

### Requirement: Tenant Creation
The system SHALL allow creation of a new independent tenant (business entity) with a unique identifier and name.

#### Scenario: Create tenant successfully
- **WHEN** an admin creates a new tenant with name "Restaurant ABC"
- **THEN** the system creates a Tenant record with unique UUID, stores the name, and returns the tenant_id

#### Scenario: Tenant name is required
- **WHEN** an attempt is made to create a tenant without a name
- **THEN** the system returns a validation error (400 Bad Request)

### Requirement: Tenant Retrieval
The system SHALL allow retrieval of tenant information by tenant_id.

#### Scenario: Get existing tenant
- **WHEN** requesting tenant information by valid tenant_id
- **THEN** the system returns tenant details (id, name, created_at)

#### Scenario: Get non-existent tenant
- **WHEN** requesting tenant information by non-existent tenant_id
- **THEN** the system returns a 404 Not Found error

### Requirement: Multi-Tenant Data Isolation
The system SHALL ensure that all subsequent queries/operations automatically scope to the authenticated user's tenant.

#### Scenario: User can only see their tenant's data
- **WHEN** a user from Tenant A performs any operation
- **THEN** the system only returns/modifies data belonging to Tenant A, never Tenant B

#### Scenario: Tenant_id from JWT is enforced
- **WHEN** a request includes a JWT token with tenant_id
- **THEN** the system uses that tenant_id for all database queries in that request
