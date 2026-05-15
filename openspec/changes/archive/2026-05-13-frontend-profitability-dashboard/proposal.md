## Why

Los gestores gastronómicos necesitan ver de un vistazo qué productos son rentables y cuáles no. El backend ya calcula costos de productos (vía recetas o modo manual) y expone precios de venta, pero no hay ninguna pantalla que muestre márgenes de ganancia. Este dashboard cierra esa brecha usando los endpoints existentes de productos y costos para calcular rentabilidad client-side, sin depender de APIs de backend que aún no existen.

## What Changes

- Crear una nueva página de dashboard accesible desde el sidebar con ícono de gráfico
- Mostrar tarjetas resumen: margen total promedio, producto más rentable, producto menos rentable, cantidad de productos activos
- Tabla de rentabilidad por producto: nombre, precio de venta, costo, margen bruto ($), margen porcentual (%), indicador visual (verde/rojo)
- Ordenamiento por cualquiera de las columnas (default: margen porcentual descendente)
- Filtro: mostrar solo productos con margen negativo, solo positivos, o todos
- Gráfico de barras horizontal comparando márgenes entre productos (top 10)
- Cálculo client-side: `margen = precio_venta - costo` y `margen_% = (margen / precio_venta) * 100` usando datos de GET /api/v1/products y GET /api/v1/products/{id}/cost
- Indicador visual de warning cuando el costo no está disponible (producto sin receta, o error 424)
- Estados de carga, vacío y error para cada sección
- Animaciones Framer Motion para transiciones y contadores

## Capabilities

### New Capabilities
- `frontend-profitability-summary`: Tarjetas de resumen con KPIs (margen promedio, producto más/menos rentable, productos activos) calculados desde los datos de productos y costos
- `frontend-profitability-table`: Tabla de rentabilidad por producto con columnas de margen bruto, margen porcentual, indicadores visuales, ordenamiento y filtros
- `frontend-profitability-chart`: Gráfico de barras horizontal comparando márgenes de los top productos, usando los datos de la tabla

### Modified Capabilities
<!-- Ninguna — cambio 100% frontend, sin modificar specs del backend -->

## Impact

- **Frontend**: Nueva ruta `/app/dashboard`, nuevo ítem en sidebar, nueva feature `features/dashboard/`
- **APIs consumidas**: `GET /api/v1/products` (listado), `GET /api/v1/products/{id}/cost` (costo por producto) — ambos ya implementados
- **Dependencia**: Requiere `frontend-products-and-recipes` implementado (usa los mismos tipos, API client, y componentes compartidos)
- **Cálculo client-side**: El margen se calcula en el frontend (`sale_price - cost_price`), sin depender de endpoints de rentabilidad del backend
- **Diferido**: Reportes de rentabilidad basados en ventas (`qty_sold`, `revenue`, filtro por período) dependen de `register-sales-with-stock-deduction` que aún no está implementado
