## 1. Backend Service Layer

- [x] 1.1 Create `ProductCostService` class in `app/services/product_cost_service.py`
- [x] 1.2 Implement `calculate_product_cost(product_id: UUID, tenant_id: UUID)` method
- [x] 1.3 Implement helper method to fetch product with recipe link
- [x] 1.4 Implement helper method to call recipe cost calculation
- [x] 1.5 Add error handling for missing products (404) and failed dependencies (424)
- [x] 1.6 Add Decimal precision handling with ROUND_HALF_UP for all cost values

## 2. Data Access Layer

- [x] 2.1 Create `ProductCostRepository` in `app/repositories/product_cost_repository.py`
- [x] 2.2 Implement `get_product_with_recipe(product_id: UUID, tenant_id: UUID)` query
- [x] 2.3 Implement `get_recipe_cost_data(recipe_id: UUID, tenant_id: UUID)` query
- [x] 2.4 Add database indexes on `products(tenant_id, recipe_id)` if not exists
- [x] 2.5 Verify indexes on `recipes(tenant_id, id)` and `raw_materials(tenant_id, id)`

## 3. API Endpoint

- [x] 3.1 Create `ProductCostRouter` in `api/product_cost_router.py`
- [x] 3.2 Implement `GET /api/v1/products/{id}/cost` endpoint
- [x] 3.3 Add JWT authentication to endpoint
- [x] 3.4 Extract tenant_id from request context
- [x] 3.5 Serialize cost response with correct structure (product_id, total_cost, currency, cost_source, ingredients, calculated_at)
- [x] 3.6 Handle 404 (product not found) and 424 (failed dependency) responses

## 4. Pydantic Schemas

- [x] 4.1 Create `ProductCostResponse` schema with fields: product_id, total_cost, currency, cost_source, ingredients, calculated_at
- [x] 4.2 Create `IngredientCostDetail` schema with fields: raw_material_id, raw_material_name, quantity, unit, unit_cost, ingredient_total_cost
- [x] 4.3 Add validation: total_cost and ingredient costs must be Decimal with 2 decimal places
- [x] 4.4 Add cost_source enum validation: "recipe" | "manual"

## 5. Integration with Existing Recipe Costing

- [x] 5.1 Verify recipe cost service is callable as internal method (not just HTTP) - implemented as internal method in ProductCostService
- [x] 5.2 Confirm recipe cost service returns data structure compatible with product cost response - service returns recipe cost in product response format
- [x] 5.3 Test that recipe cost endpoint reuses same calculation logic as service method - confirmed: GET /api/v1/recipes/{id}/cost calls RecipeService.get_recipe_cost_structure() (recipes_router.py:450), which uses calculate_recipe_cost() with Decimal precision handling
- [x] 5.4 Verify recipe cost respects tenant_id isolation - confirmed: endpoint enforces tenant_id via get_tenant_id_placeholder() dependency, repository queries use tenant_id filter (recipe_service.py:416 and repository.get_recipe_by_id())

## 6. Multi-Tenancy & Security

- [x] 6.1 Add tenant_id validation to product lookup (enforce 404 on cross-tenant access)
- [x] 6.2 Add tenant_id validation to recipe lookup (enforce 404 on cross-tenant access)
- [x] 6.3 Add tenant_id validation to raw material lookups (enforce 404 on cross-tenant access)
- [x] 6.4 Test cross-tenant isolation with at least 2 test tenants

## 7. Error Handling & Edge Cases

- [x] 7.1 Handle product not found → HTTP 404
- [x] 7.2 Handle recipe not found (product has invalid recipe_id) → HTTP 424
- [x] 7.3 Handle recipe with missing ingredient → HTTP 424
- [x] 7.4 Handle raw material not found in recipe → HTTP 424
- [x] 7.5 Handle recipe with no ingredients → return 200 with total_cost = 0.00
- [x] 7.6 Handle product without recipe_id → return 200 with cost_source = "manual"

## 8. Decimal Precision & Rounding

- [x] 8.1 Use Python Decimal library for all cost calculations
- [x] 8.2 Set ROUND_HALF_UP as default rounding mode
- [x] 8.3 Test edge case: 1.335 * 1 rounds to 1.34 (half-up)
- [x] 8.4 Test edge case: recipe with 3+ ingredients; sum rounds correctly
- [x] 8.5 Ensure all response costs formatted as "XX.XX" (2 decimal places)

## 9. Unit Tests

- [x] 9.1 Test `calculate_product_cost()` with recipe-linked product
- [x] 9.2 Test `calculate_product_cost()` with non-linked product
- [x] 9.3 Test cost calculation with multiple ingredients
- [x] 9.4 Test cost precision with fractional quantities (e.g., 1.33 * 7.99)
- [x] 9.5 Test 404 on missing product
- [x] 9.6 Test 424 on missing recipe
- [x] 9.7 Test 424 on missing raw material
- [x] 9.8 Test 424 on recipe with missing ingredients
- [x] 9.9 Test multi-tenant isolation (cross-tenant access returns 404)
- [x] 9.10 Test response schema (all fields present, correct types)

## 10. Integration Tests

- [x] 10.1 Test full flow: Create product → link recipe → call cost endpoint
- [x] 10.2 Test cost endpoint with live database (sample recipe + raw materials)
- [x] 10.3 Test cost updates when raw material cost changes
- [x] 10.4 Test cost endpoint performance (target < 100ms)
- [x] 10.5 Test batch ingredient lookups don't cause N+1 queries

## 11. Documentation & API Spec

- [x] 11.1 Update `openapi.yaml` with `/api/v1/products/{id}/cost` endpoint definition
- [x] 11.2 Add request/response examples to OpenAPI spec
- [x] 11.3 Document response codes: 200, 404, 424
- [x] 11.4 Document cost_source enum values in spec
- [x] 11.5 Add comments to service methods explaining cost calculation flow

## 12. Deployment & Verification

- [ ] 12.1 Run full test suite (unit + integration)
- [ ] 12.2 Deploy to staging environment
- [ ] 12.3 Verify endpoint is accessible and returns correct responses
- [ ] 12.4 Check endpoint latency in staging (target < 100ms)
- [ ] 12.5 Test with production-like data volume
