## ADDED Requirements

### Requirement: JWT validation dependency is wired in all protected routers
All protected routers SHALL use `Depends(get_tenant_id)` from `app.core.dependencies` to extract tenant context from the JWT Authorization header, replacing `get_tenant_id_placeholder()`.

#### Scenario: Valid JWT token grants access to raw materials endpoints
- **WHEN** a request to `GET /api/v1/raw-materials` includes a valid Bearer token
- **THEN** the `get_tenant_id` dependency extracts tenant_id from the token and the handler executes

#### Scenario: Valid JWT token grants access to products endpoints
- **WHEN** a request to `GET /api/v1/products` includes a valid Bearer token
- **THEN** the `get_tenant_id` dependency extracts tenant_id from the token and the handler executes

#### Scenario: Valid JWT token grants access to recipes endpoints
- **WHEN** a request to `GET /api/v1/recipes` includes a valid Bearer token
- **THEN** the `get_tenant_id` dependency extracts tenant_id from the token and the handler executes

#### Scenario: Valid JWT token grants access to sales endpoints
- **WHEN** a request to `GET /api/v1/sales` includes a valid Bearer token
- **THEN** the `get_tenant_id` dependency extracts tenant_id from the token and the handler executes

#### Scenario: Valid JWT token grants access to product cost endpoints
- **WHEN** a request to `GET /api/v1/products/{id}/cost` includes a valid Bearer token
- **THEN** the `get_tenant_id` dependency extracts tenant_id from the token and the handler executes

### Requirement: Missing or invalid JWT token is rejected on all protected endpoints
All protected routers SHALL return 401 when the Authorization header is missing, malformed, or contains an invalid token.

#### Scenario: Missing Authorization header returns 401
- **WHEN** a request to any protected endpoint omits the Authorization header
- **THEN** the system returns HTTP 401 with "Not authenticated" or similar error

#### Scenario: Expired JWT token returns 401
- **WHEN** a request includes a JWT token with `exp` in the past
- **THEN** the system returns HTTP 401 with "Token has expired"

#### Scenario: Invalid signature returns 401
- **WHEN** a request includes a JWT token signed with a different secret
- **THEN** the system returns HTTP 401 with "Invalid token"
