## Context

El backend de materias primas está completo con 8 endpoints: CRUD completo más operaciones de stock (add-stock, remove-stock, get-stock). El modelo tiene `name`, `unit_of_measurement`, `cost_per_unit` (Decimal), `supplier` (opcional) y `current_stock`. Ya existe un cliente API parcial (`rawMaterials.ts`) creado para el selector de ingredientes. Este cambio construye la UI completa de gestión de inventario sobre esa base.

**Stack existente**: React 18 · Vite · Tailwind CSS · TanStack Query v5 · Zustand · React Hook Form + Zod · Framer Motion · Axios · @tanstack/react-table · Lucide React

**Endpoints disponibles**:
- `POST/GET/PUT/DELETE /api/v1/raw-materials` — CRUD
- `POST /api/v1/raw-materials/{id}/add-stock` — agregar stock
- `POST /api/v1/raw-materials/{id}/remove-stock` — quitar stock
- `GET /api/v1/raw-materials/{id}/stock` — consultar nivel

**Unidades válidas**: `kg, g, L, mL, units, pieces, boxes` (mismo set que ingredientes de recetas)

## Goals / Non-Goals

**Goals:**
- CRUD completo de materias primas con validación (nombre, unidad, costo > 0, proveedor opcional)
- Visualización de stock actual con indicadores de color (verde/amarillo/rojo según nivel)
- Interfaz de ajuste de stock: modal con cantidad + motivo (opcional)
- Validación de stock insuficiente al remover (error del backend → toast)
- Filtro por nombre en la lista
- Ordenamiento por nombre, costo, stock
- Navegación desde materias primas a recetas que las usan (si es factible)
- Expansión del API client existente con los endpoints de stock

**Non-Goals:**
- Dashboard de inventario o reportes de stock (puede ser un cambio futuro)
- Alertas automáticas de bajo stock (backend no tiene soporte para thresholds)
- Auditoría de movimientos de stock (el backend ya descarta el campo `reason`)
- Transferencias entre almacenes (no existe el concepto en el backend)

## Decisions

### 1. Estructura de archivos

```
features/raw-materials/
├── hooks/
│   ├── useRawMaterials.ts        ← useQuery para lista
│   ├── useRawMaterial.ts         ← useQuery para detalle + stock
│   └── useRawMaterialMutations.ts ← useMutation para CRUD + stock
├── components/
│   ├── RawMaterialTable.tsx      ← @tanstack/react-table con columnas
│   ├── RawMaterialForm.tsx       ← React Hook Form + Zod (create/edit)
│   ├── StockLevelBadge.tsx       ← Indicador visual de nivel de stock
│   └── StockAdjustmentModal.tsx  ← Modal para add/remove stock
└── pages/
    ├── RawMaterialsPage.tsx      ← Lista con filtro y tabla
    ├── RawMaterialCreatePage.tsx ← Formulario de creación
    ├── RawMaterialEditPage.tsx   ← Formulario de edición
    └── RawMaterialDetailPage.tsx ← Detalle con info + stock + acciones
```

### 2. Indicador de nivel de stock (StockLevelBadge)

| Nivel | Color | Criterio |
|-------|-------|----------|
| Normal | Verde | stock > 10 |
| Bajo | Amarillo/ámbar | stock > 0 y ≤ 10 |
| Agotado | Rojo | stock = 0 |

**Decisión**: Threshold fijo de 10 unidades como "bajo". Es un valor razonable para un MVP. En una versión futura, el backend podría exponer un `low_stock_threshold` configurable por material.

### 3. Ajuste de stock — Modal vs Inline

**Modal**: El formulario de ajuste (cantidad + motivo) se abre en un modal desde la página de detalle. Esto evita saturar la UI y permite enfocar la atención en la operación de stock.

El modal tiene:
- Tipo de operación: "Add Stock" o "Remove Stock" (dos botones separados en la página de detalle)
- Campo de cantidad (Decimal, > 0)
- Campo de motivo (opcional, max 255 chars, alineado con el backend)
- Validación: cantidad > 0, y en remove-stock el backend valida stock suficiente

### 4. Expansión del API client

El archivo `api/rawMaterials.ts` existente solo tiene `getRawMaterials()`. Se expande con:
- `getRawMaterial(id)` — GET /{id}
- `createRawMaterial(payload)` — POST
- `updateRawMaterial(id, payload)` — PUT
- `deleteRawMaterial(id)` — DELETE
- `addStock(id, quantity, reason)` — POST /{id}/add-stock
- `removeStock(id, quantity, reason)` — POST /{id}/remove-stock
- `getStock(id)` — GET /{id}/stock

### 5. Navegación

Se agrega al sidebar:
```
/app/raw-materials          → RawMaterialsPage (lista)
/app/raw-materials/new      → RawMaterialCreatePage
/app/raw-materials/:id      → RawMaterialDetailPage
/app/raw-materials/:id/edit → RawMaterialEditPage
```

Ícono en sidebar: `Boxes` (Lucide).

## Risks / Trade-offs

- **[Riesgo] El backend tiene IDs String(50) no UUID** → El API client ya funciona con strings. Las rutas de React Router usan `:id` como string. No hay impacto.
- **[Riesgo] Stock adjustments no son atómicos en el backend** → Race condition en add/remove stock del backend (read-then-write sin locking). El frontend no puede mitigarlo. Si dos usuarios ajustan stock simultáneamente, puede haber pérdida de updates. **Mitigación**: invalidar la query de stock después de cada mutación para reflejar el estado real del servidor.
- **[Trade-off] Threshold de bajo stock hardcodeado en 10** → Simple para MVP, pero no configurable. Futuro: mover al backend.
- **[Dependencia] El campo `reason` del backend se descarta** → Lo enviamos igual (el schema del backend lo acepta) para cuando se implemente la auditoría. No rompe nada.
