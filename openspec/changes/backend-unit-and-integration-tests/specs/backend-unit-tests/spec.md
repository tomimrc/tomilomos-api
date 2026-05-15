## ADDED Requirements

### Requirement: AuthService unit tests
The test suite SHALL cover all AuthService methods: `login`, `authenticate_user`, `create_user`, `create_tenant`, `generate_tokens`.

#### Scenario: Login with valid credentials returns user and token
- **WHEN** `AuthService.login()` is called with correct email and password
- **THEN** it returns the user object and a valid TokenResponse

#### Scenario: Login with wrong password raises InvalidCredentialsError
- **WHEN** `AuthService.login()` is called with correct email but wrong password
- **THEN** it raises `InvalidCredentialsError`

#### Scenario: Login with non-existent email raises UserNotFoundError
- **WHEN** `AuthService.login()` is called with an email that doesn't exist
- **THEN** it raises `UserNotFoundError`

### Requirement: Service layer unit tests
The test suite SHALL cover all service methods: RawMaterialService, ProductService, RecipeService, SaleService.

#### Scenario: RawMaterialService creates a raw material
- **WHEN** `RawMaterialService.create_raw_material()` is called with valid data
- **THEN** a new raw material is created with the correct tenant_id

#### Scenario: RecipeService calculates cost from ingredients
- **WHEN** `RecipeService.calculate_cost()` is called for a recipe with ingredients
- **THEN** it returns the sum of (quantity × unit_cost) for each ingredient

#### Scenario: SaleService creates sale and deducts stock
- **WHEN** `SaleService.create_sale()` is called for a product with a recipe
- **THEN** a sale record is created and raw material stock is deducted

### Requirement: Repository layer unit tests
The test suite SHALL cover all repository methods: UserRepository, TenantRepository, RawMaterialRepository, ProductRepository, RecipeRepository, SaleRepository.

#### Scenario: UserRepository finds user by email and tenant
- **WHEN** `UserRepository.get_user_by_email()` is called with existing email and tenant_id
- **THEN** it returns the correct user object

#### Scenario: RawMaterialRepository filters by tenant_id
- **WHEN** `RawMaterialRepository.list_by_tenant()` is called
- **THEN** only raw materials belonging to that tenant are returned
