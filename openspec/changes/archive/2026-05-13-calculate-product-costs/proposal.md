## Why

Currently, the system has product pricing, recipe costing, and raw material costing as separate concerns. Tomilomos needs a unified, performant way to calculate **the total cost of a product** that:
1. Uses recipe-based costs when a product is linked to a recipe (ingredients → raw material prices)
2. Falls back to manual cost entry when no recipe is linked
3. Ensures these costs are real-time, accurate (to 2 decimal places), and account for multi-tenancy

This enables restaurant managers to understand true profitability per product and make informed pricing decisions.

## What Changes

- **New endpoint**: `GET /api/v1/products/{id}/cost` returns the calculated cost with itemization
- **Cost calculation logic**: Service layer that determines cost source (recipe vs. manual) and computes accordingly
- **Response structure**: Standardized cost response with total, breakdown by ingredient (if recipe-based), and timestamp
- **Error handling**: Graceful failures when recipes or ingredients are incomplete or missing
- **Decimal precision**: All cost values stored and returned as DECIMAL(10,2) with 2-decimal rounding

## Capabilities

### New Capabilities
- `product-cost-calculation`: Service layer and endpoint for calculating product costs from recipes and raw materials; supports both recipe-based and manual pricing modes.

### Modified Capabilities
- `product-pricing`: Extend to support cost_price field that integrates with recipe costing
- `recipe-costing`: Ensure cost calculations are atomic and available for product cost queries
- `raw-materials-costing`: Confirm raw material unit costs are always current and consistent

## Impact

- **Backend**: New service method `calculate_product_cost()`, new repository query for cost lookup, new API endpoint
- **API**: New route `/api/v1/products/{id}/cost` with standardized cost response schema
- **Database**: No schema changes (cost_price as computed field or service-level calculation)
- **Frontend**: Optional UI improvements to display product cost breakdowns (not in scope of this change)
- **Performance**: Queries should be indexed on recipe_id and tenant_id for fast lookups
- **Multi-tenancy**: Respects existing tenant isolation through product.tenant_id
