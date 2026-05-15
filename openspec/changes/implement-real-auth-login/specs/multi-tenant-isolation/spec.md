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
