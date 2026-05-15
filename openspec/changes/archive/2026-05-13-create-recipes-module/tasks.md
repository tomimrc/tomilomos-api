## 1. Database Schema & Models

- [x] 1.1 Create Alembic migration for `recipes` table (id, tenant_id, name, description, created_at, updated_at)
- [x] 1.2 Create Alembic migration for `recipe_ingredients` table (id, recipe_id, raw_material_id, quantity, unit, created_at, updated_at)
- [x] 1.3 Add recipe_id (nullable) foreign key to `products` table
- [x] 1.4 Add database indexes: (tenant_id, created_at) on recipes; (recipe_id, raw_material_id) on recipe_ingredients
- [x] 1.5 Create Recipe SQLAlchemy model in db/models/
- [x] 1.6 Create RecipeIngredient SQLAlchemy model in db/models/
- [x] 1.7 Update Product SQLAlchemy model to include recipe_id field with relationship
- [x] 1.8 Add __repr__ and cascade behaviors to models

## 2. Repository Layer

- [x] 2.1 Create RecipeRepository with CRUD methods (create, read, update, delete)
- [x] 2.2 Implement recipe query methods: find_by_tenant_and_name, find_all_by_tenant (with pagination)
- [x] 2.3 Implement recipe ingredient management: add_ingredient, remove_ingredient, list_ingredients
- [x] 2.4 Implement bulk ingredient fetching for cost calculations (get_ingredients_with_costs)
- [x] 2.5 Add tenant isolation to all query methods (filter by tenant_id)
- [x] 2.6 Add foreign key validation in repository (verify raw_material exists in tenant before adding to recipe)

## 3. Service Layer - Recipe CRUD

- [x] 3.1 Create RecipeService class in services/
- [x] 3.2 Implement create_recipe(tenant_id, name, description) method
- [x] 3.3 Implement get_recipe(recipe_id, tenant_id) with tenant isolation
- [x] 3.4 Implement update_recipe(recipe_id, tenant_id, name, description) with unique name validation
- [x] 3.5 Implement delete_recipe(recipe_id, tenant_id) with cascading ingredient deletion
- [x] 3.6 Add error handling: RecipeNotFound, RecipeNameAlreadyExists, UnauthorizedAccess

## 4. Service Layer - Recipe Ingredients

- [x] 4.1 Implement add_ingredient(recipe_id, tenant_id, raw_material_id, quantity, unit) in RecipeService
- [x] 4.2 Implement remove_ingredient(ingredient_id, recipe_id, tenant_id) in RecipeService
- [x] 4.3 Implement get_ingredient(ingredient_id, recipe_id, tenant_id) in RecipeService
- [x] 4.4 Implement list_ingredients(recipe_id, tenant_id) in RecipeService
- [x] 4.5 Implement update_ingredient(ingredient_id, recipe_id, tenant_id, quantity, unit) in RecipeService
- [x] 4.6 Validate raw material exists in same tenant before adding ingredient
- [x] 4.7 Validate quantity > 0 and unit is not empty

## 5. Service Layer - Recipe Costing

- [x] 5.1 Implement calculate_recipe_cost(recipe_id, tenant_id) method in RecipeService
- [x] 5.2 Fetch current cost_per_unit for all ingredients from RawMaterial models
- [x] 5.3 Calculate ingredient_total_cost = quantity * unit_cost for each ingredient
- [x] 5.4 Sum all ingredient costs to get total_recipe_cost
- [x] 5.5 Return structured cost response with itemized breakdown
- [x] 5.6 Handle missing raw materials gracefully (return HTTP 424 with error message)
- [x] 5.7 Use Decimal(10,2) for all cost calculations (no floats)
- [x] 5.8 Add get_recipe_cost_structure() for API response formatting

## 6. Router & API Endpoints - Recipes CRUD

- [x] 6.1 Create router at api/routers/recipes.py
- [x] 6.2 Implement POST /api/v1/recipes (create recipe)
- [x] 6.3 Implement GET /api/v1/recipes (list recipes with pagination)
- [x] 6.4 Implement GET /api/v1/recipes/{id} (get single recipe)
- [x] 6.5 Implement PUT /api/v1/recipes/{id} (update recipe)
- [x] 6.6 Implement DELETE /api/v1/recipes/{id} (delete recipe)
- [x] 6.7 Add Pydantic schemas: RecipeCreate, RecipeUpdate, RecipeResponse

## 7. Router & API Endpoints - Recipe Ingredients

- [x] 7.1 Implement POST /api/v1/recipes/{id}/ingredients (add ingredient)
- [x] 7.2 Implement GET /api/v1/recipes/{id}/ingredients (list ingredients)
- [x] 7.3 Implement GET /api/v1/recipes/{recipe_id}/ingredients/{ingredient_id} (get single ingredient)
- [x] 7.4 Implement PUT /api/v1/recipes/{recipe_id}/ingredients/{ingredient_id} (update ingredient)
- [x] 7.5 Implement DELETE /api/v1/recipes/{recipe_id}/ingredients/{ingredient_id} (remove ingredient)
- [x] 7.6 Add Pydantic schemas: RecipeIngredientCreate, RecipeIngredientUpdate, RecipeIngredientResponse

## 8. Router & API Endpoints - Recipe Costing & Integration

- [x] 8.1 Implement GET /api/v1/recipes/{id}/cost (calculate and return recipe cost)
- [x] 8.2 Update POST /api/v1/products to accept optional recipe_id field
- [x] 8.3 Update PUT /api/v1/products/{id} to allow linking/unlinking recipes
- [x] 8.4 Update GET /api/v1/products/{id} to include recipe_id in response
- [x] 8.5 Update GET /api/v1/products/{id} to include calculated cost_price if recipe_id is set
- [x] 8.6 Add RecipeCostResponse schema with itemized breakdown

## 9. Testing - Unit Tests

- [x] 9.1 Test RecipeService.create_recipe with valid data
- [x] 9.2 Test RecipeService.create_recipe duplicate name validation
- [x] 9.3 Test RecipeService.update_recipe with name uniqueness
- [x] 9.4 Test RecipeService.delete_recipe cascades ingredient deletion
- [x] 9.5 Test add_ingredient validates raw material exists in tenant
- [x] 9.6 Test add_ingredient validates quantity > 0
- [x] 9.7 Test calculate_recipe_cost with multiple ingredients
- [x] 9.8 Test calculate_recipe_cost with missing raw material (HTTP 424)
- [x] 9.9 Test calculate_recipe_cost with empty recipe (returns 0.00)

## 10. Testing - Integration Tests

- [x] 10.1 Test POST /api/v1/recipes creates recipe successfully
- [x] 10.2 Test GET /api/v1/recipes lists recipes with pagination
- [x] 10.3 Test recipe tenant isolation (cross-tenant access returns 404)
- [x] 10.4 Test POST /api/v1/recipes/{id}/ingredients adds ingredient
- [x] 10.5 Test ingredient foreign key validation (invalid raw_material_id)
- [x] 10.6 Test GET /api/v1/recipes/{id}/cost returns calculated cost
- [x] 10.7 Test PUT /api/v1/products/{id} with recipe_id links recipe
- [x] 10.8 Test GET /api/v1/products/{id} includes cost_price when recipe linked
- [x] 10.9 Test DELETE /api/v1/recipes/{id} cascades to product associations (recipe_id → NULL)

## 11. Testing - Multi-Tenancy

- [x] 11.1 Test recipes are filtered by tenant_id in all queries
- [x] 11.2 Test ingredients respect tenant isolation (cannot link cross-tenant raw materials)
- [x] 11.3 Test cost calculations use only same-tenant raw materials
- [x] 11.4 Test recipe deletion does not affect other tenants

## 12. Documentation & Integration

- [x] 12.1 Update openapi.yaml with recipes CRUD endpoints
- [x] 12.2 Update openapi.yaml with recipe ingredients endpoints
- [x] 12.3 Update openapi.yaml with recipe cost endpoint
- [x] 12.4 Update openapi.yaml with product.recipe_id field
- [x] 12.5 Update API documentation with usage examples
- [x] 12.6 Document cost calculation precision (2 decimal places, half-up rounding)
- [x] 12.7 Document tenant isolation and multi-tenancy behavior
- [x] 12.8 Add recipes module to project README

## 13. Deployment & Verification

- [ ] 13.1 Run Alembic migration in staging database
- [ ] 13.2 Verify database schema: tables created, indexes present, foreign keys active
- [ ] 13.3 Test backward compatibility: existing products work without recipes
- [ ] 13.4 Run full test suite (unit + integration)
- [ ] 13.5 Load test recipe costing with 1000+ ingredient recipes
- [ ] 13.6 Verify no N+1 query issues with eager loading
- [ ] 13.7 Deploy to production
- [ ] 13.8 Monitor error logs for new recipe endpoints (first 24 hours)
