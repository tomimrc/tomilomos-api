## Why

Registrar ventas es la operación central del negocio gastronómico: cada venta de un producto (ej. "2 Lomitos Completos") debe registrarse, mostrar precio/costo, y deducir automáticamente el stock de materias primas según los ingredientes de la receta. Además, los gestores necesitan una vista rápida del nivel de stock de todas las materias primas para tomar decisiones de compra. El backend `register-sales-with-stock-deduction` proveerá los endpoints; este cambio construye la UI completa del ciclo de ventas y monitoreo de stock.

## What Changes

- **Pantalla de registro de venta**: selector de producto (con búsqueda), cantidad, precio unitario (auto-completado del producto), subtotal automático, confirmación con resumen de costo/ganancia
- **Historial de ventas**: tabla con fecha, producto, cantidad, precio total, costo total, margen. Filtro por fecha y búsqueda
- **Vista de stock actual**: dashboard con todas las materias primas, stock levels con badges de color, búsqueda y ordenamiento. Vista rápida para identificar qué reponer
- **Manejo de estados**: loading, empty (sin ventas aún), error, success para cada vista
- **Animaciones**: transiciones Framer Motion en páginas, feedback visual en registro de venta exitoso

## Capabilities

### New Capabilities
- `frontend-sales-entry`: Formulario de registro de venta con selector de producto, cantidad, cálculo de subtotal, y confirmación visual al completar la venta
- `frontend-sales-history`: Tabla de ventas registradas con columnas de fecha, producto, cantidad, precio, costo y margen. Filtros por fecha y producto
- `frontend-stock-dashboard`: Vista de monitoreo de stock con todas las materias primas, badges de nivel, búsqueda y ordenamiento. Acceso rápido a ajustes de stock

### Modified Capabilities
<!-- Ninguna — no modifica specs existentes -->

## Impact

- **Nuevos archivos**: `features/sales/` con estructura feature-based (hooks, components, pages)
- **APIs consumidas**: Endpoints de ventas del backend `register-sales-with-stock-deduction` (POST/GET /api/v1/sales, GET /api/v1/sales/{id}), más endpoints existentes de productos (GET /api/v1/products) y materias primas (GET /api/v1/raw-materials)
- **Nuevo API client**: `api/sales.ts` con funciones para registro y consulta de ventas
- **Sidebar**: Nuevo ítem "Sales" con ícono `ShoppingCart`, y sub-ítem o sección "Stock" (o acceso desde Sales)
- **Rutas nuevas**: `/app/sales` (registro de venta), `/app/sales/history` (historial), `/app/stock` (dashboard de stock)
- **Dependencia**: Requiere que el backend `register-sales-with-stock-deduction` esté implementado y exponga los endpoints de ventas
- **Sin cambios en backend**
