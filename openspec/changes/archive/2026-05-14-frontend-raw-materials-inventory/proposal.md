## Why

Las materias primas son la base de todo el sistema TomiLomos: los ingredientes de recetas dependen de ellas, y los costos de productos se calculan a partir de sus precios. El backend ya expone 8 endpoints con CRUD completo y ajustes de stock, pero no hay interfaz visual para que los gestores administren su inventario de materias primas. Sin esta pantalla, crear ingredientes en recetas es imposible.

## What Changes

- Crear pantallas de gestión de materias primas: listado, creación, edición y eliminación
- Pantalla de detalle con información completa: nombre, unidad, costo, proveedor, stock actual
- Interfaz de ajuste de stock: agregar y quitar stock con cantidad + motivo, validación de stock insuficiente
- Visualización de nivel de stock con indicadores de color (bajo stock en amarillo/rojo)
- Selector de materias primas reutilizable (ya existe en IngredientForm, se extrae a componente compartido)
- Expansión del cliente API existente (`rawMaterials.ts`) con todos los endpoints de stock
- Filtro por nombre en la lista, ordenamiento por nombre/stock/costo
- Manejo de estados: loading, empty, error, success para cada vista

## Capabilities

### New Capabilities
- `frontend-raw-materials-crud`: Pantallas de listado, creación, edición, eliminación y detalle de materias primas con validación de campos (nombre, unidad, costo > 0, proveedor opcional)
- `frontend-raw-materials-stock`: Interfaz de ajuste de stock (agregar/quitar con cantidad y motivo), visualización de nivel de stock con indicadores de color, validación de stock insuficiente

### Modified Capabilities
<!-- Ninguna — cambio 100% frontend -->

## Impact

- **Nuevos archivos**: `features/raw-materials/` con estructura feature-based (hooks, components, pages)
- **Archivo modificado**: `api/rawMaterials.ts` — expandir con endpoints de stock (add-stock, remove-stock, get-stock)
- **APIs consumidas**: Los 8 endpoints de `/api/v1/raw-materials/*` (CRUD + stock — ya implementados)
- **Sidebar**: Nuevo ítem "Raw Materials" con ícono `Boxes` o `Package`
- **Ruta nueva**: `/app/raw-materials` con subrutas para detalle y edición
- **Dependencia**: Usa los mismos componentes compartidos (Button, Input, Select, Modal, Badge, etc.) y el mismo API client ya establecidos
- **Sin cambios en backend**
