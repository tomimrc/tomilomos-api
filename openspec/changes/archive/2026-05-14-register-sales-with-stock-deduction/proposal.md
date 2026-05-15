## Why

El frontend de ventas (`frontend-sales-entry-and-stock-view`) ya está implementado y espera consumir endpoints de ventas que NO existen. Sin estos endpoints, no se puede registrar una venta, no hay historial, y el stock de materias primas no se deduce automáticamente al vender un producto. Este cambio construye la capa backend completa de ventas: modelo, schemas, repositorio, servicio y router, siguiendo la arquitectura existente (Router → Service → Repository → Model) y el contrato definido en el frontend.

## What Changes

- **Modelo Sale**: Nueva tabla `sales` en `db/models.py` con campos: id (UUID), tenant_id (FK), product_id (FK), quantity (int), unit_price (Decimal 10,2), total_price (Decimal 10,2), total_cost (Decimal 10,2 nullable), margin (Decimal 10,2 nullable), created_at
- **Schemas Sale**: `SaleCreate` (product_id, quantity), `SaleRead` (todos los campos + product_name)
- **Repositorio SaleRepository**: create, get_by_id, list_by_tenant con paginación
- **Servicio SaleService**: lógica de negocio — crear venta congelando precios al momento de la venta, calcular costo desde receta, deducir stock de materias primas vía ingredientes de receta
- **Router Sales**: endpoints `POST /api/v1/sales` (crear venta + deducir stock), `GET /api/v1/sales` (listar con paginación), `GET /api/v1/sales/{id}` (detalle)
- **Deducción de stock atómica**: Al crear una venta, por cada ingrediente de la receta del producto, se deduce `ingredient.quantity × sale.quantity` del raw_material correspondiente usando el `remove_stock` existente
- **Manejo de errores**: 400 si producto no existe, 400 si stock insuficiente, 404 si sale no encontrada, 500 si error inesperado
- **Registro en main.py**: Incluir el sales router

## Capabilities

### New Capabilities
- `sales-crud`: Endpoints para crear, listar y obtener ventas con validación de producto existente, cálculo de precios/costos/margen al momento de la venta, y respuesta enriquecida con product_name
- `sales-stock-deduction`: Deducción automática de stock de materias primas al registrar una venta. Por cada ingrediente de la receta del producto, deduce `ingredient.quantity × sale.quantity`. Maneja stock insuficiente con error 400, stock no afectado si el producto no tiene receta

### Modified Capabilities
<!-- Ninguna — funcionalidad nueva, no modifica specs existentes -->

## Impact

- **Nuevo modelo**: `Sale` en `db/models.py` (tabla `sales`) — requiere migración Alembic
- **Nuevos schemas**: `schemas/sales.py` — `SaleCreate`, `SaleRead`
- **Nuevo repositorio**: `repositories/sales_repository.py`
- **Nuevo servicio**: `services/sales_service.py` — orquesta creación de venta + deducción de stock + cálculo de costos
- **Nuevo router**: `api/sales_router.py` — 3 endpoints (POST, GET list, GET by id)
- **Modificado**: `main.py` — registrar sales router
- **Dependencias**: Usa `RecipeService.calculate_recipe_cost()` y `RawMaterialService.remove_stock()` existentes
- **Contrato frontend**: El frontend ya implementado espera exactamente estos endpoints y formatos de respuesta
- **Sin cambios en auth** — usa `get_tenant_id_placeholder` como los demás routers
