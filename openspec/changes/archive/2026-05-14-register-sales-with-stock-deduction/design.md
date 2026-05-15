## Context

El backend ya tiene infraestructura completa para productos (CRUD + costo), materias primas (CRUD + stock), recetas (CRUD + ingredientes + costo) y autenticación (JWT). El frontend `frontend-sales-entry-and-stock-view` ya está implementado y espera consumir `POST /api/v1/sales`, `GET /api/v1/sales`, `GET /api/v1/sales/{id}` con un contrato de respuesta definido. La deducción de stock ya existe en `RawMaterialService.remove_stock()` y el cálculo de costo de receta en `RecipeService.calculate_recipe_cost()`. Este cambio conecta todo: crear una venta → calcular costo → deducir stock → guardar.

**Stack**: Python 3.11+ · FastAPI · SQLAlchemy · Pydantic · PostgreSQL · Decimal para dinero · UUID como String(50) PKs · Alembic para migraciones

## Goals / Non-Goals

**Goals:**
- Modelo `Sale` con todos los campos necesarios (id, tenant_id, product_id, quantity, unit_price, total_price, total_cost, margin, created_at)
- Schemas Pydantic: `SaleCreate` (product_id, quantity), `SaleRead` (campos completos + product_name)
- Repositorio `SaleRepository` con create, get_by_id, list_by_tenant
- Servicio `SaleService` con lógica: validar producto, congelar precios, calcular costo desde receta, deducir stock, crear sale
- Router con 3 endpoints, manejo de errores HTTP
- Deducción de stock por ingredientes de receta: `ingredient.quantity × sale.quantity`
- Registro en `main.py`

**Non-Goals:**
- Editar o anular/eliminar ventas (no hay endpoint DELETE/PUT)
- Ventas con múltiples productos por transacción (MVP: un producto por venta)
- Invoice/receipt generation (PDF)
- Payment method tracking
- Discounts o impuestos
- Reportes agregados de ventas (eso es frontend profitability)

## Decisions

### 1. Modelo Sale

```python
class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(String(50), primary_key=True, index=True)
    tenant_id = Column(String(50), ForeignKey("tenants.id"), nullable=False, index=True)
    product_id = Column(String(50), ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    total_cost = Column(Numeric(10, 2), nullable=True)
    margin = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    tenant = relationship("Tenant")
    product = relationship("Product")
```

**Decisión**: `quantity` como `Integer` (no Decimal) porque las ventas gastronómicas son en unidades enteras (1 lomito, 2 empanadas). `total_cost` y `margin` como `nullable` porque un producto puede no tener receta. `margin = total_price - total_cost` cuando cost existe. Los precios se congelan al momento de la venta (no son FK dinámicas al Product — son snapshots).

### 2. Stock Deduction Flow

```
┌─────────────────────────────────────────────────────────────┐
│              STOCK DEDUCTION FLOW                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SaleService.create_sale(tenant_id, data)                   │
│    │                                                        │
│    ├─ 1. Validar producto existe y está activo              │
│    │     ProductRepository.get_by_id(tenant_id, product_id)  │
│    │     → 404 si no existe                                 │
│    │                                                        │
│    ├─ 2. Congelar precio de venta                           │
│    │     unit_price = product.sale_price                    │
│    │     total_price = unit_price × quantity                │
│    │                                                        │
│    ├─ 3. Si el producto tiene recipe_id:                    │
│    │     ├─ RecipeService.calculate_recipe_cost(...)        │
│    │     │  → total_cost = recipe_cost.total_cost × quantity│
│    │     │  → margin = total_price - total_cost             │
│    │     │                                                  │
│    │     └─ Por cada ingredient en la receta:               │
│    │          deducción = ingredient.quantity × quantity     │
│    │          RawMaterialService.remove_stock(               │
│    │            tenant_id,                                   │
│    │            ingredient.raw_material_id,                  │
│    │            deducción,                                   │
│    │            reason=f"Sale: {{sale_id}}"                  │
│    │          )                                              │
│    │          → 400 si stock insuficiente                    │
│    │                                                        │
│    ├─ 4. Si el producto NO tiene recipe_id:                 │
│    │     total_cost = None, margin = None                   │
│    │     (no se deduce stock)                               │
│    │                                                        │
│    └─ 5. Crear Sale en DB                                   │
│         SaleRepository.create(...)                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Decisión**: La deducción de stock y la creación de la venta ocurren en la MISMA transacción de BD. Si alguna deducción falla (stock insuficiente), se hace rollback de todo (no se crea la venta). El `commit()` ocurre en el router después de que el servicio retorna exitosamente.

### 3. SaleRead — product_name

El schema `SaleRead` incluye `product_name` que NO está en la tabla (no es una columna). El servicio lo agrega haciendo un join o consulta adicional al producto. Como ya validamos el producto en el paso 1, tenemos el `Product` en memoria y podemos tomar `product.name`.

```python
class SaleRead(BaseModel):
    id: str
    tenant_id: str
    product_id: str
    product_name: str       # ← del objeto Product en memoria
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    total_cost: Optional[Decimal]
    margin: Optional[Decimal]
    created_at: datetime
    
    class Config:
        from_attributes = True
```

**Decisión**: `product_name` se agrega en el servicio al construir la respuesta, no en el modelo ORM. Esto evita joins innecesarios en queries de lista (donde se puede batch-fetch products) y mantiene la respuesta del frontend compatible.

### 4. Estructura de archivos

```
db/models.py              ← + class Sale
schemas/sales.py          ← SaleCreate, SaleRead
repositories/sales_repository.py  ← SaleRepository
services/sales_service.py          ← SaleService
api/sales_router.py                ← 3 endpoints
main.py                  ← + include_router(sales_router)
```

### 5. Manejo de transacciones

Siguiendo el patrón existente:
- **Repository**: solo `session.flush()` (nunca commit)
- **Service**: orquesta llamadas a repositorios y otros servicios, pero no commitea
- **Router**: llama al servicio, luego `db.commit()` en el path feliz, `db.rollback()` en errores

Esto asegura que la creación de Sale + deducciones de stock sean atómicas.

### 6. Router endpoints

| Método | Path | Request | Response | Errores |
|--------|------|---------|----------|---------|
| POST | `/api/v1/sales` | `SaleCreate` | `SaleRead` (201) | 400 (producto no encontrado, stock insuficiente, validación), 500 |
| GET | `/api/v1/sales` | `?skip=0&limit=50` | `List[SaleRead]` | — |
| GET | `/api/v1/sales/{id}` | — | `SaleRead` | 404 |

### 7. Recipe ingredients access

`RecipeService.calculate_recipe_cost()` retorna `RecipeCostResponse` que incluye `ingredients: List[RecipeCostDetailItem]` con `raw_material_id`, `quantity`, `unit`. El `SaleService` itera estos ingredientes para deducir stock.

Alternativa considerada: consultar `RecipeIngredient` directamente desde el repositorio. Se elige usar `calculate_recipe_cost()` porque ya resuelve el join con raw_materials y valida que existan.

## Risks / Trade-offs

- **[Riesgo] Race condition en deducción de stock** → Si dos ventas del mismo producto ocurren simultáneamente, ambas pueden leer el mismo stock antes de que alguna descuente. **Mitigación**: `remove_stock` hace `current_stock < quantity` check en el mismo flush, y PostgreSQL con nivel de aislamiento READ COMMITTED + row-level locking implícito en UPDATE capturará la segunda como error. No se requiere locking explícito para MVP con bajo volumen.
- **[Riesgo] Producto sin receta no deduce stock** → Si un producto se vende sin receta, el stock de materias primas no se actualiza. **Mitigación**: Es comportamiento esperado y documentado. El frontend muestra cost/margin como "—". El gestor debe crear la receta para tener tracking completo.
- **[Trade-off] Un producto por venta** → No se pueden registrar ventas con múltiples productos en una transacción. **Mitigación**: MVP. Futuro: agregar `SaleItem` con FK a `Sale`, permitiendo múltiples ítems por venta. El modelo actual escala a ese diseño sin breaking changes.
- **[Trade-off] Snapshot de precios vs reference** → Los precios se congelan al momento de la venta. Si el producto cambia de precio después, las ventas pasadas no se alteran. **Mitigación**: Es el comportamiento correcto para auditoría financiera. El historial de ventas refleja lo que realmente se cobró.
