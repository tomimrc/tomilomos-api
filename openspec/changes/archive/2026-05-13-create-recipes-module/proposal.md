## Why

In a gastronomic SaaS, recipes are the core business logic that connects raw materials to finished products. Currently, the system can manage products and raw materials separately, but lacks the ability to define how raw materials combine to create products. This creates friction in the workflow—users cannot:
- Define the ingredient composition of a dish
- Automatically calculate the cost of a product based on its ingredients
- Track raw material consumption tied to specific recipes
- Scale recipes up or down based on portion sizes

Adding a recipes module enables restaurants to link inventory management to product profitability, a key feature for any food business management tool.

## What Changes

- **New**: Recipes CRUD (Create, Read, Update, Delete) for defining how raw materials combine to create products
- **New**: Recipe line items (ingredient quantities) to specify ingredient composition
- **New**: Cost calculation based on recipe ingredients and current raw material costs
- **Modified**: Product pricing logic to include recipe-based cost calculations (for costing accuracy)
- **Integration**: Recipes tied to tenant-scoped data (multi-tenancy)

## Capabilities

### New Capabilities
- `recipes-crud`: Create, read, update, and delete recipes with full tenant isolation
- `recipe-ingredients`: Manage ingredient line items within recipes (quantities, unit conversions)
- `recipe-costing`: Calculate recipe cost based on current raw material prices and ingredient quantities

### Modified Capabilities
- `raw-materials-costing`: Updated to support recipe-based queries (accessing ingredient costs within a recipe context)
- `product-pricing`: Extended to optionally associate a product with a recipe for cost calculations

## Impact

- **Code**: New models (Recipe, RecipeIngredient), new routers, new services for recipe logic
- **Database**: New tables for recipes and recipe_ingredients with proper foreign keys and tenant scoping
- **API**: New endpoints `/api/v1/recipes` (CRUD), `/api/v1/recipes/{id}/ingredients` (line items)
- **Frontend**: Recipe management UI (form, list, detail views)
- **Integration Points**: Products can now reference recipes; raw material costs flow into recipe costing
- **No Breaking Changes**: Existing product and raw material endpoints remain unchanged
