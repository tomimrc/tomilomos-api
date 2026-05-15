## Why

El SaaS TomiLomos necesita una interfaz visual para que los gestores gastronómicos puedan administrar sus productos y recetas. El backend ya expone endpoints completos de CRUD, ingredientes, y cálculo de costos tanto para productos como para recetas, pero no existe ningún frontend. Esta es la primera pantalla de negocio real después del setup de autenticación.

## What Changes

- Crear la estructura de proyecto React con TypeScript, Tailwind CSS, y React Router
- Implementar pantallas de gestión de productos: listado, creación, edición, y eliminación con feedback visual (Framer Motion)
- Implementar pantallas de gestión de recetas: listado, creación, edición, y eliminación con feedback visual
- Implementar pantalla de detalle de receta: visualización y gestión de ingredientes (agregar, editar cantidad, eliminar), con visualización del costo total calculado
- Implementar vinculación producto-receta desde el formulario de producto (selector de receta)
- Implementar visualización de costo del producto (calculado desde receta o modo manual)
- Manejo de estados: loading, empty, error, y success para cada vista
- Multi-tenancy: todas las operaciones automáticamente scopeadas al tenant del usuario autenticado
- Consumir los endpoints del backend usando fetch/axios con interceptores de JWT

## Capabilities

### New Capabilities
- `frontend-product-crud`: Pantallas de listado, creación, edición y eliminación de productos con validación de precios y estados de carga
- `frontend-recipe-crud`: Pantallas de listado, creación, edición y eliminación de recetas con validación de nombres únicos
- `frontend-recipe-ingredients`: Pantalla de detalle de receta con gestión de ingredientes (agregar materia prima, editar cantidad/unidad, eliminar) y visualización de costo calculado
- `frontend-product-recipe-linking`: Vinculación de recetas a productos desde el formulario de producto, incluyendo visualización del costo calculado

### Modified Capabilities
<!-- Ninguna — es un cambio puramente de frontend, sin cambios en specs del backend -->

## Impact

- **Nuevo proyecto frontend**: Creación de directorio `frontend/` con React + TypeScript + Tailwind CSS + Framer Motion
- **APIs consumidas**: Todos los endpoints de `/api/v1/products/*` y `/api/v1/recipes/*` (ya existentes en el backend)
- **Dependencia**: Requiere que `frontend-setup-and-auth-flow` esté implementado (contexto de autenticación, manejo de JWT, axios/fetch configurado con interceptores)
- **Sin cambios en backend**: Este cambio es 100% frontend, no modifica ningún endpoint ni spec del servidor
