## Context

The Tomilomos system currently manages:
- **Products**: Finished goods with sale prices (products-crud, product-pricing)
- **Raw Materials**: Ingredients with unit costs (raw-materials-crud, raw-materials-stock-tracking, raw-materials-costing)
- **Multi-tenancy**: All data is scoped to tenants (multi-tenant-isolation)

However, there is no connection between raw materials and products. Restaurants need to define recipes—formulas that specify which raw materials combine to create a product and in what quantities. This is essential for:
1. Calculating accurate product costs based on actual ingredient costs
2. Tracking raw material consumption by recipe
3. Supporting portion-size scaling and menu engineering

The architecture follows Clean Architecture: Router → Service → Repository → Model, with atomic transactions managed at the persistence layer.

## Goals / Non-Goals

**Goals:**
- Enable creation, retrieval, update, and deletion of recipes with full tenant isolation
- Support ingredient line items within recipes (raw material + quantity + unit)
- Provide automatic recipe cost calculation based on current raw material costs
- Maintain referential integrity between recipes, raw materials, and products
- Integrate seamlessly with existing product and costing systems
- Support optional recipe-to-product linkage for cost accuracy

**Non-Goals:**
- Recipe versioning or audit trails (future feature)
- Unit conversion system (use existing unit management or assume consistent units)
- Nutritional or allergen data (out of scope for this iteration)
- Recipe templates or duplication features
- Portion size calculation or scaling logic (deferred)

## Decisions

### 1. Data Model: Recipe and RecipeIngredient Tables
**Decision**: Create two tables:
- `recipes`: id, tenant_id, name, description, created_at, updated_at
- `recipe_ingredients`: id, recipe_id, raw_material_id, quantity, unit, created_at, updated_at

**Rationale**: Recipes are 1:N with ingredients. This normalized structure allows:
- Multiple ingredients per recipe
- Easy ingredient updates without affecting recipe metadata
- Atomic deletion of ingredients when a recipe is removed

**Alternative Considered**: Store ingredients as JSONB. Rejected because:
- Foreign key integrity would be lost
- Querying ingredient usage across recipes becomes difficult
- Alembic migrations would be more complex

### 2. Recipe Cost Calculation (Service Layer)
**Decision**: Implement recipe costing as a service method: `recipe_service.calculate_recipe_cost(recipe_id)` that:
1. Loads the recipe and its ingredients
2. Fetches current unit costs for each raw material
3. Multiplies quantity × unit_cost for each ingredient
4. Returns total recipe cost (Decimal, 2 decimal places)

**Rationale**:
- Cost is derived (not stored) because raw material prices change
- Placing logic in the Service layer keeps it testable and reusable
- Clean separation from Router and Repository

**Alternative Considered**: Store cost in database. Rejected because:
- Cost becomes stale when material prices change
- Would require continuous updates or cache invalidation
- Violates single source of truth (raw material prices)

### 3. Product-to-Recipe Association (Optional)
**Decision**: Add optional `recipe_id` field to Product model.
- Products can optionally reference a recipe
- If recipe_id is set, cost calculations use recipe costing
- If recipe_id is NULL, product cost is manual (existing behavior)

**Rationale**:
- Backward compatible (existing products without recipes continue to work)
- Allows gradual migration (products can adopt recipes incrementally)
- Supports mixed workflows (some products manual, some recipe-driven)

**Alternative Considered**: Mandatory recipe linkage. Rejected because it breaks existing products.

### 4. API Design: Nested Resources
**Decision**: Recipe ingredients are nested resources:
- POST `/api/v1/recipes` → create recipe
- GET `/api/v1/recipes/{id}` → retrieve recipe with ingredients embedded
- POST `/api/v1/recipes/{id}/ingredients` → add ingredient to recipe
- DELETE `/api/v1/recipes/{id}/ingredients/{ingredient_id}` → remove ingredient
- GET `/api/v1/recipes/{id}/cost` → calculate and return recipe cost

**Rationale**:
- Nested routes express the 1:N relationship naturally
- Client can manage ingredients without separate requests
- `/cost` endpoint separates the read-only calculation from CRUD

**Alternative Considered**: Flat structure (separate ingredients endpoint). Rejected because:
- Less intuitive for clients
- Doesn't reflect business domain naturally
- Would complicate recipe retrieval

### 5. Tenant Isolation
**Decision**: All queries filter by tenant_id. Recipes are scoped per tenant.

**Rationale**:
- Consistent with existing multi-tenant architecture
- Prevents cross-tenant data leaks
- Foreign keys to raw_materials and products must verify tenant ownership

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| **Recipe deletion breaks products referencing it** | Add ON DELETE SET NULL to recipe_id foreign key; products lose recipe link but remain valid |
| **Raw material prices change, recipe costs become inaccurate** | Documented behavior: cost is derived at query time. If historical cost tracking needed, implement in future iteration |
| **Large recipes with many ingredients cause N+1 queries** | Use eager loading (joinedload) in recipe repository; avoid lazy loading in service |
| **Ingredient unit inconsistency (kg, g, ml, L)** | Require upstream raw material unit standardization; recipes inherit units from materials. Document unit expectations in API |
| **Scaling to millions of recipes/ingredients** | Indexes on recipe_id, raw_material_id, tenant_id; pagination on ingredient lists |

## Migration Plan

1. **Database**:
   - Create new Alembic migration adding recipes and recipe_ingredients tables
   - Add recipe_id nullable foreign key to products table
   - Add indexes: (tenant_id, created_at) on recipes, (recipe_id, raw_material_id) on recipe_ingredients

2. **Code**:
   - Create Recipe and RecipeIngredient models
   - Implement RecipeRepository with CRUD + ingredient management
   - Implement RecipeService with costing logic
   - Create router with endpoints listed above
   - Update Product model to include optional recipe_id field

3. **Testing**:
   - Unit tests for recipe service (cost calculation with mock data)
   - Integration tests for recipes router (create, read, update, delete)
   - Tenant isolation tests (verify recipes are scoped correctly)
   - Foreign key constraint tests

4. **Deployment**:
   - Run Alembic migration in staging
   - Verify backward compatibility (existing products work without recipes)
   - Deploy to production
   - No data reset required

## Open Questions

1. Should recipe ingredients support "optional" flags for substitutable ingredients? (Deferred)
2. Should we implement recipe history/versioning? (Deferred to future iteration)
3. What is the maximum recipe complexity (ingredients per recipe)? Performance threshold?
4. Should ingredient quantities be stored separately from the unit, or combined (e.g., "2.5 kg")?
