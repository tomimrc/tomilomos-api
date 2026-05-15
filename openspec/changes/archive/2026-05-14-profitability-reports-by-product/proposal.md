## Why

Los gestores necesitan saber QUÉ productos generan ganancia y cuáles están a pérdida. Con las features ya implementadas (productos con costo, materias primas con precios, recetas con ingredientes), el sistema tiene todos los datos para calcular rentabilidad por producto. Pero no hay una vista que los consolide. Las specs `frontend-profitability-summary`, `frontend-profitability-table` y `frontend-profitability-chart` ya existen en `openspec/specs/` — este cambio las implementa.

## What Changes

- **Dashboard de rentabilidad**: Nueva página `/app/profitability` con tres secciones integradas
- **KPI Summary Cards**: 4 tarjetas con métricas clave — Average Margin (%), Most Profitable Product, Least Profitable Product, Active Products count. Calculadas en el frontend a partir de los datos de productos y costos
- **Profitability Table**: Tabla sortable y filtrable con todos los productos, columnas de Sale Price, Cost Price, Gross Margin ($), Margin (%), e indicador visual (verde/rojo). Filtros: All / Profitable / Unprofitable
- **Bar Chart**: Gráfico de barras horizontales con el top 10 productos por margen. Barras verdes (positivo) / rojas (negativo). Tooltip con detalle al hover. Click navega al detalle del producto
- **Filtro consistente**: El gráfico se actualiza cuando se aplica un filtro en la tabla
- **Manejo de edge cases**: productos sin costo (424/manual pricing → "—"), márgenes negativos (rojo), división por cero (sale_price = 0), sin productos, costo no disponible

## Capabilities

### New Capabilities
<!-- Ninguna — las specs frontend-profitability-summary, frontend-profitability-table, y frontend-profitability-chart ya existen en openspec/specs/. Este cambio las IMPLEMENTA. -->

### Modified Capabilities
<!-- Ninguna — no se modifican specs existentes -->

## Impact

- **Nuevos archivos**: `features/profitability/` con estructura feature-based (hooks, components, pages)
- **APIs consumidas**: `GET /api/v1/products` (listado de productos, ya existe), `GET /api/v1/products/{id}/cost` (costo por producto, ya existe). Se necesita consultar el costo de CADA producto individualmente
- **Nuevo hook**: `useProfitabilityData` que obtiene todos los productos, luego hace batch de costos, y calcula márgenes
- **Sidebar**: Nuevo ítem "Profitability" con ícono `TrendingUp`, entre Recipes y Stock Monitor
- **Ruta nueva**: `/app/profitability` — página única con summary + table + chart
- **Sin cambios en backend** — todos los datos vienen de endpoints existentes
- **Dependencia**: Usa `formatCurrency` de `@/lib/formatters`, `useProducts` de products feature, y `getProductCost` de `@/api/products`
