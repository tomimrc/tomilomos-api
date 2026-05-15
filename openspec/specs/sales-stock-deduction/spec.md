## ADDED Requirements

### Requirement: Automatic Stock Deduction on Sale
The system SHALL automatically deduct raw material stock when a sale is registered for a product with a recipe, based on the ingredients in the recipe.

#### Scenario: Stock deducted proportionally
- **WHEN** a sale of quantity 2 is registered for a product whose recipe has ingredient "Chicken Breast 200g"
- **THEN** the system deducts 400g (200g × 2) from the "Chicken Breast" raw material stock
- **AND** the deduction reason is set to "Sale: {sale_id}"

#### Scenario: Multiple ingredients deducted
- **WHEN** a product recipe has 3 ingredients (Chicken 200g, Tomato 50g, Bread 1 unit)
- **AND** a sale of quantity 3 is registered
- **THEN** Chicken stock is deducted 600g, Tomato 150g, Bread 3 units
- **AND** all deductions use the same sale_id in the reason

#### Scenario: Insufficient stock
- **WHEN** any raw material has insufficient stock for the required deduction
- **THEN** the system returns 400 with detail "Insufficient stock for {raw_material_name}: need {required}, have {available}"
- **AND** NO stock is deducted from any raw material (atomic rollback)
- **AND** the sale is NOT created

#### Scenario: Product without recipe
- **WHEN** a sale is registered for a product that has no recipe_id
- **THEN** the system does NOT attempt to deduct any stock
- **AND** the sale is created normally with total_cost and margin as null

### Requirement: Stock Deduction Transaction Atomicity
The system SHALL ensure that sale creation and all stock deductions happen in a single atomic transaction.

#### Scenario: All-or-nothing guarantee
- **WHEN** a sale would deduct from 3 raw materials but the 3rd has insufficient stock
- **THEN** no stock is deducted from any of the 3 raw materials
- **AND** the sale record is not persisted
- **AND** the database state is unchanged (full rollback)

#### Scenario: Successful atomic transaction
- **WHEN** all stock deductions succeed
- **THEN** the sale record and all stock changes are committed together
- **AND** no partial state is visible to other transactions

### Requirement: Stock Deduction Calculation Accuracy
The system SHALL calculate stock deductions using precise Decimal arithmetic.

#### Scenario: Decimal precision maintained
- **WHEN** ingredient quantity is 0.75 and sale quantity is 3
- **THEN** the deduction is 2.25 (0.75 × 3) using Decimal multiplication
- **AND** the result is stored with 2 decimal places (DECIMAL 10,2)

#### Scenario: Non-divisible units handled
- **WHEN** ingredient unit is "units" or "pieces" and the recipe calls for 1 unit
- **THEN** deductions for these ingredients are always whole numbers (integer result)

### Requirement: Stock Deduction Error Messages
The system SHALL return descriptive error messages when stock deduction fails.

#### Scenario: Single ingredient insufficient
- **WHEN** only "Chicken Breast" has insufficient stock
- **THEN** the error message identifies "Chicken Breast" specifically
- **AND** shows required amount and available amount

#### Scenario: Multiple ingredients insufficient
- **WHEN** multiple ingredients have insufficient stock
- **THEN** the error message identifies the FIRST ingredient that fails
- **AND** the sale is rolled back entirely
