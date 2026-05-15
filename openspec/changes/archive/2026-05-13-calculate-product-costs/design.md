## Context

Tomilomos is a SaaS gastronomy management system with multi-tenant support. Currently:
- Products have a `sale_price` (DECIMAL 10,2) but no automatic cost calculation
- Recipes can calculate their total cost via ingredients + raw material prices
- Raw materials have unit costs (stored as DECIMAL 10,2)
- The system follows a strict layering: Router → Service → Repository → Model
- All monetary values must use DECIMAL(10,2) to avoid floating-point rounding errors
- Multi-tenancy is enforced at the query level through `tenant_id` isolation

**Stakeholder**: Restaurant managers need visibility into product costs to understand profitability.

## Goals / Non-Goals

**Goals:**
1. Provide a single endpoint (`GET /api/v1/products/{id}/cost`) to retrieve product cost
2. Support two cost modes: **recipe-based** (for products linked to recipes) and **manual** (for standalone products)
3. Return itemized cost breakdown for recipe-based products (which ingredient costs sum to total)
4. Ensure all cost calculations use DECIMAL(10,2) precision with half-up rounding
5. Respect multi-tenancy boundaries—users can only query costs for their own products
6. Handle failures gracefully (missing recipes, deleted raw materials → HTTP 424)
7. Performance: Queries should be indexed to avoid N+1 problems

**Non-Goals:**
- UI integration (frontend display of costs)
- Historical cost tracking or auditing
- Bulk cost calculation endpoint (single product only)
- Recipe cost caching (always calculate fresh)
- Changes to existing product pricing or recipe schemas
- Manual cost field on products (not in scope)

## Decisions

### Decision 1: Cost Calculation Placement (Service Layer)
**Choice**: Service layer is responsible for cost calculation logic; repository only fetches data.

**Rationale**: 
- Keeps business logic out of routes and repositories
- Simplifies testing—mock repositories, test calculation in isolation
- Aligns with project's Clean Architecture mandate (AGENTS.md)
- Cost calculation might evolve (e.g., future bulk operations) without touching repository

**Alternatives Considered**:
- Database-level calculation (view or computed column) → loses flexibility for future logic
- Router-level calculation → violates architectural principles, harder to unit test

### Decision 2: Recipe Cost Always Fresh (No Caching)
**Choice**: Every cost request calculates recipe cost in real-time from current raw material prices.

**Rationale**:
- Ensures cost accuracy—if raw material prices change, product cost reflects it immediately
- Meets the requirement "Recipe cost uses current raw material prices"
- Reduces complexity of cache invalidation
- One extra query per request is acceptable; indexed on `recipe_id` and `tenant_id`

**Alternatives Considered**:
- Cache recipe cost for N seconds → risks stale data if prices change frequently
- Store cost_price in product table → adds redundancy and sync complexity

### Decision 3: Cost Response Structure
**Choice**: Return structured response with `total_cost`, `cost_source` (recipe | manual), and `ingredients` array (for recipes only).

**Rationale**:
- Frontend has clear indication of cost source
- Itemized breakdown allows UI to show which ingredients drive cost
- Timestamp proves freshness of data
- Matches the response format already defined in recipe-costing spec

**Response Schema**:
```json
{
  "product_id": "uuid",
  "total_cost": 45.99,
  "currency": "USD",
  "cost_source": "recipe",  // or "manual"
  "ingredients": [
    {
      "raw_material_id": "uuid",
      "raw_material_name": "tomatoes",
      "quantity": 2.5,
      "unit": "kg",
      "unit_cost": 12.50,
      "ingredient_total_cost": 31.25
    }
  ],
  "calculated_at": "2025-05-13T14:30:00Z"
}
```

### Decision 4: Error Handling Strategy
**Choice**: HTTP 424 Failed Dependency when recipe or ingredients are incomplete/missing.

**Rationale**:
- 404 is reserved for product not found (tenant isolation)
- 424 clearly signals "I wanted to calculate but a dependency failed"
- Aligns with existing recipe-costing spec (HTTP 424 for missing raw materials)
- Allows frontend to distinguish between "product doesn't exist" and "cost unavailable"

**Error Scenarios**:
- Product not found → HTTP 404
- Product recipe_id references deleted recipe → HTTP 424
- Recipe has ingredient referencing deleted raw material → HTTP 424

### Decision 5: Indexing Strategy
**Choice**: Add indexes on `products(tenant_id, recipe_id)` and ensure `recipes(tenant_id, id)` and `raw_materials(tenant_id, id)` are indexed.

**Rationale**:
- Cost endpoint will be called frequently; `tenant_id + product lookup` is primary path
- `recipe_id` filter on products avoids full table scan
- Existing specs already cover raw_materials and recipes indexing
- No query will do N+1 if indexed correctly

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Real-time cost calculation overhead** | Slow endpoint if recipe has many ingredients | Ensure indexes on recipe_id, raw_material_id; consider caching if performance < 100ms |
| **Stale recipe reference** | Recipe deleted after product created → 424 error | Document that products with deleted recipes cannot be costed; add migration to handle orphaned recipes |
| **Precision rounding edge case** | Multiple small ingredient costs round inconsistently | Use Python Decimal library with ROUND_HALF_UP; validate in tests with 3+ ingredient scenarios |
| **Multi-tenant query isolation failure** | User A sees User B's costs | Enforce tenant_id in every query; test with multiple tenants in unit tests |
| **Bottleneck if endpoint hammered** | Rate limiting or caching needed | Add to future roadmap; current design assumes moderate usage |

## Migration Plan

**Phase 1: Implement (No production impact)**
- Add service method `calculate_product_cost(product_id, tenant_id) → CostResponse`
- Add endpoint `GET /api/v1/products/{id}/cost`
- Full unit test coverage
- Integration test with sample recipe + raw materials

**Phase 2: Deploy**
- Deploy to staging, validate against live data
- Monitor endpoint latency (target < 100ms)
- No database migrations required (schema unchanged)
- No breaking changes to existing endpoints

**Phase 3: Rollback (if needed)**
- Route simply returns HTTP 501 Not Implemented if rolled back
- No data loss or cleanup required

## Open Questions

1. **Should cost calculation include packaging costs or labor?** → Defer to future; assume only raw material costs for now
2. **Should we store `cost_price` in products table for quick retrieval?** → No; compute on-demand to avoid sync issues
3. **What SLA for cost calculation latency?** → Assume < 100ms; monitor and optimize if slower
