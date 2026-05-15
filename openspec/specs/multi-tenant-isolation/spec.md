## ADDED Requirements

### Requirement: Dependency Injection for Tenant Context
The system SHALL use FastAPI dependency injection to provide tenant_id to all request handlers and service layers.

#### Scenario: get_tenant_id dependency is available
- **WHEN** a request handler uses `tenant_id: str = Depends(get_tenant_id)`
- **THEN** the dependency function extracts tenant_id from the JWT token and injects it into the handler

#### Scenario: Service layer receives tenant_id parameter
- **WHEN** a service method is called
- **THEN** it receives tenant_id as an explicit parameter (never inferred)

#### Scenario: Repository layer receives tenant_id parameter
- **WHEN** a repository method is called
- **THEN** it receives tenant_id and filters all queries by it

### Requirement: Cross-Tenant Data Protection
The system SHALL prevent any data access across tenant boundaries.

#### Scenario: User A cannot access User B's data
- **WHEN** User A (Tenant A) attempts to query resources from Tenant B
- **THEN** the system returns an empty result or 403 Forbidden (no cross-tenant leakage)

#### Scenario: Raw queries that bypass tenant_id filter fail
- **WHEN** a developer writes a query without filtering by tenant_id
- **THEN** the linter/tests flag this as a violation (enforced via code review)

### Requirement: Audit Trail for Authorization
The system SHALL log all tenant_id context for debugging and security auditing.

#### Scenario: Failed cross-tenant access attempt is logged
- **WHEN** a request attempts to access a resource from a different tenant
- **THEN** the system logs the attempt with user_id, attempted tenant_id, and actual tenant_id

#### Scenario: Logs do not expose sensitive data
- **WHEN** authorization events are logged
- **THEN** passwords and tokens are never included in logs

## ADDED Requirements

### Requirement: All business routers use real tenant extraction from JWT
All business routers (raw_materials, products, recipes, product_cost, sales) SHALL use `Depends(get_tenant_id)` instead of `get_tenant_id_placeholder()`. The placeholder function SHALL be removed from all router files.

#### Scenario: Raw materials router uses real tenant context
- **WHEN** a request hits any raw materials endpoint
- **THEN** tenant_id is extracted from the JWT token via `get_tenant_id` dependency (not placeholder)

#### Scenario: Products router uses real tenant context
- **WHEN** a request hits any products endpoint
- **THEN** tenant_id is extracted from the JWT token via `get_tenant_id` dependency (not placeholder)

#### Scenario: Recipes router uses real tenant context
- **WHEN** a request hits any recipes endpoint
- **THEN** tenant_id is extracted from the JWT token via `get_tenant_id` dependency (not placeholder)

#### Scenario: Sales router uses real tenant context
- **WHEN** a request hits any sales endpoint
- **THEN** tenant_id is extracted from the JWT token via `get_tenant_id` dependency (not placeholder)

#### Scenario: Product cost router uses real tenant context
- **WHEN** a request hits any product cost endpoint
- **THEN** tenant_id is extracted from the JWT token via `get_tenant_id` dependency (not placeholder)

### Requirement: Zero occurrences of get_tenant_id_placeholder remain in router files
After this change, no router file SHALL contain the string `get_tenant_id_placeholder`.

#### Scenario: Grep finds zero placeholder references
- **WHEN** searching all files in `api/` for `get_tenant_id_placeholder`
- **THEN** zero matches are found
