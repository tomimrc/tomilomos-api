## ADDED Requirements

### Requirement: Track current stock quantity for a raw material
The system SHALL maintain and track the current quantity of each raw material in inventory, supporting decimal quantities to accommodate various units (kg can be 2.5, liters can be 0.75, etc.).

#### Scenario: New raw material starts with zero stock
- **WHEN** a new raw material is created
- **THEN** the system initializes current_stock to 0.00

#### Scenario: Current stock is retrievable
- **WHEN** an authenticated user sends a GET request to `/api/v1/raw-materials/{id}`
- **THEN** the response includes the current_stock field with the current quantity

#### Scenario: Stock quantity supports decimals
- **WHEN** a raw material has current_stock = 2.50 kg or 0.75 L
- **THEN** the system stores and returns the decimal quantity accurately without rounding

### Requirement: Add stock to a raw material (receipt/purchase)
The system SHALL allow authenticated users to increase the stock quantity of a raw material, typically when receiving a purchase or restocking.

#### Scenario: Add stock successfully
- **WHEN** an authenticated user sends a POST request to `/api/v1/raw-materials/{id}/add-stock` with quantity (positive number) and optional reason
- **THEN** the system increases current_stock by the provided quantity and returns HTTP 200 with updated raw material data

#### Scenario: Add stock with audit reason
- **WHEN** adding stock with reason = "purchase" or "restock"
- **THEN** the system records the reason (for future audit logging, currently logged but not displayed)

#### Scenario: Add zero or negative stock fails
- **WHEN** attempting to add stock with quantity ≤ 0
- **THEN** the system returns HTTP 400 Bad Request with validation error

#### Scenario: Add stock to non-existent raw material
- **WHEN** attempting to add stock to a raw material that doesn't exist
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Cannot add stock to raw material from different tenant
- **WHEN** user A from tenant A attempts to add stock to a raw material in tenant B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Stock addition is atomic
- **WHEN** adding stock to a raw material
- **THEN** the operation completes entirely or rolls back entirely; no partial stock additions occur

### Requirement: Remove stock from a raw material (usage/deduction)
The system SHALL allow authenticated users to decrease the stock quantity of a raw material, typically when deducting stock during a sale or recipe preparation.

#### Scenario: Remove stock successfully
- **WHEN** an authenticated user sends a POST request to `/api/v1/raw-materials/{id}/remove-stock` with quantity (positive number) and reason
- **THEN** the system decreases current_stock by the provided quantity and returns HTTP 200 with updated raw material data

#### Scenario: Remove stock with reason (sale, recipe, waste)
- **WHEN** removing stock with reason = "sale" or "recipe" or "waste"
- **THEN** the system records the reason for audit purposes

#### Scenario: Remove zero or negative stock fails
- **WHEN** attempting to remove stock with quantity ≤ 0
- **THEN** the system returns HTTP 400 Bad Request with validation error

#### Scenario: Cannot remove more stock than available
- **WHEN** attempting to remove more stock than current_stock (e.g., current_stock = 5, removing 10)
- **THEN** the system returns HTTP 400 Bad Request with error message indicating insufficient stock

#### Scenario: Cannot remove stock from raw material from different tenant
- **WHEN** user A from tenant A attempts to remove stock from a raw material in tenant B
- **THEN** the system returns HTTP 404 Not Found

#### Scenario: Stock removal is atomic
- **WHEN** removing stock from a raw material
- **THEN** the operation completes entirely or rolls back entirely; no partial stock removals occur

#### Scenario: Stock cannot go negative
- **WHEN** attempting to remove stock that would result in negative quantity
- **THEN** the system prevents the operation and returns HTTP 400 Bad Request

### Requirement: Retrieve stock level
The system SHALL provide a way to check the current stock level of a raw material without retrieving all fields.

#### Scenario: Get stock level only
- **WHEN** an authenticated user sends a GET request to `/api/v1/raw-materials/{id}/stock`
- **THEN** the system returns HTTP 200 with a JSON object containing only id and current_stock

#### Scenario: Stock level endpoint respects multi-tenancy
- **WHEN** user A from tenant A retrieves stock for a raw material in tenant A
- **THEN** the value is returned successfully
- **WHEN** user A from tenant A attempts to retrieve stock for a raw material in tenant B
- **THEN** the system returns HTTP 404 Not Found

### Requirement: Stock adjustments must maintain consistency
The system SHALL ensure that stock quantities remain consistent and accurate through all operations by using atomic transactions and preventing concurrent conflicts.

#### Scenario: Concurrent stock updates are serialized
- **WHEN** two stock adjustment requests arrive simultaneously for the same raw material
- **THEN** one is processed completely before the other begins; the final stock quantity reflects both adjustments

#### Scenario: Stock cannot be manipulated via direct update
- **WHEN** a user attempts to directly modify current_stock via a PUT request to `/api/v1/raw-materials/{id}` with a new current_stock value
- **THEN** stock is not modified via direct updates; only via add-stock or remove-stock endpoints

#### Scenario: Stock precision is maintained during adjustments
- **WHEN** adjusting stock multiple times (e.g., add 1.5, remove 0.75, add 0.25)
- **THEN** the final stock reflects the exact cumulative change with no rounding errors

### Requirement: Stock level supports decimal precision
The system SHALL store and return stock quantities using decimal precision to support fractional units (e.g., 2.50 kg, 0.75 L, 3.33 units).

#### Scenario: Fractional stock is preserved
- **WHEN** a raw material has current_stock = 2.50 kg and then 0.75 kg is removed
- **THEN** the new current_stock is exactly 1.75 kg, not rounded or truncated

#### Scenario: Very small stock quantities are supported
- **WHEN** adding a tiny quantity like 0.01 L of an expensive ingredient
- **THEN** the system stores and tracks this accurately
