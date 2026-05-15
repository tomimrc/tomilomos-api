## Context

El backend `register-sales-with-stock-deduction` (cambio hermano) expondrá endpoints para registrar ventas con deducción automática de stock de materias primas vía ingredientes de receta. El frontend ya tiene: selector de productos (ProductsPage), inventario de materias primas con stock badges (RawMaterialsPage), API client con JWT, y componentes compartidos (Modal, ConfirmDialog, Table, Form, etc.). Este cambio construye la UI de ventas y un dashboard de stock sobre esas bases.

**Stack existente**: React 18 · Vite · Tailwind CSS · TanStack Query v5 · Zustand · React Hook Form + Zod · Framer Motion · Axios · @tanstack/react-table · Lucide React

**Endpoints asumidos del backend** (contrato de `register-sales-with-stock-deduction`):
- `POST /api/v1/sales` — Registrar venta con deducción de stock. Payload: `{ product_id, quantity }`. Response: `{ id, product_name, quantity, unit_price, total_price, total_cost, margin, created_at }`
- `GET /api/v1/sales?skip=0&limit=50` — Listar ventas con paginación
- `GET /api/v1/sales/{id}` — Detalle de venta individual

**Endpoints existentes consumidos**:
- `GET /api/v1/products` — Listar productos para el selector
- `GET /api/v1/raw-materials` — Dashboard de stock (ya implementado con useRawMaterials)

## Goals / Non-Goals

**Goals:**
- Formulario de registro de venta: selector de producto con búsqueda, campo de cantidad, subtotal automático
- Resumen pre-confirmación mostrando precio unitario, costo estimado y margen aproximado
- Historial de ventas con tabla ordenable y filtrable (fecha, producto)
- Dashboard de stock mostrando todas las materias primas con badges de nivel, búsqueda y ordenamiento
- Navegación integrada en sidebar y rutas
- Animaciones Framer Motion en transiciones de página y feedback de venta exitosa

**Non-Goals:**
- Edición o anulación de ventas (el backend no lo soporta en MVP)
- Reportes de rentabilidad (es el cambio `profitability-reports-by-product`)
- Alertas automáticas de bajo stock (requiere thresholds en backend)
- Filtros avanzados por rango de fechas con datepicker (MVP: solo lista ordenada por fecha)
- Exportación de datos (CSV/PDF)

## Decisions

### 1. Estructura de archivos

```
features/sales/
├── hooks/
│   ├── useSales.ts              ← useQuery para historial
│   ├── useSale.ts               ← useQuery para detalle
│   └── useSaleMutations.ts      ← useMutation para create
├── components/
│   ├── ProductSelector.tsx      ← Select con búsqueda de productos activos
│   ├── SaleForm.tsx             ← Formulario de venta (producto + cantidad)
│   ├── SalesTable.tsx           ← Tabla de historial (@tanstack/react-table)
│   └── SaleConfirmation.tsx     ← Modal de confirmación con resumen (precio, costo, margen)
└── pages/
    ├── SalesPage.tsx            ← Página principal: formulario de venta + resumen
    └── SalesHistoryPage.tsx     ← Página de historial con tabla y filtros

features/stock/
├── components/
│   └── StockDashboardTable.tsx  ← Tabla de stock con badges, búsqueda, ordenamiento
└── pages/
    └── StockDashboardPage.tsx   ← Dashboard con tabla + acceso rápido a ajustes
```

**Stock Dashboard se separa de raw-materials** porque es una vista diferente: orientada a monitoreo rápido para decisiones de compra, no a gestión CRUD. Reutiliza los hooks existentes (`useRawMaterials`) pero tiene su propia presentación.

### 2. Flujo de registro de venta

```
┌─────────────────────────────────────────────────────────────┐
│                    SALES ENTRY FLOW                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Select Product (ProductSelector)                        │
│       │                                                     │
│       ▼                                                     │
│  2. Enter Quantity (SaleForm)                               │
│       │                                                     │
│       ▼                                                     │
│  3. Show Summary (SaleConfirmation Modal)                   │
│       │  • Product name + quantity                          │
│       │  • Unit price (from product.sale_price)             │
│       │  • Total = unit_price × quantity                    │
│       │  • Estimated cost (from product.cost_price)         │
│       │  • Estimated margin = total - cost                  │
│       │                                                     │
│       ▼ (user confirms)                                     │
│  4. POST /api/v1/sales { product_id, quantity }             │
│       │                                                     │
│       ▼ (success)                                           │
│  5. Toast success + reset form + refetch history            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. ProductSelector — Select con búsqueda

Usa el componente `Select` existente con `searchable={true}`. Carga productos vía `useProducts()`. Filtra solo `is_active === true`. Muestra nombre + precio en cada opción (`renderOption`).

**Decisión**: Reutilizar `useProducts` y el Select existente en vez de crear un componente nuevo desde cero. El renderOption muestra: "Lomito Completo — $15.00".

### 4. SaleForm — React Hook Form + Zod

Campos:
- `product_id`: requerido (del ProductSelector)
- `quantity`: requerido, > 0, entero (las ventas son en unidades enteras)

No se necesita campo de precio — se obtiene del producto seleccionado. El subtotal se calcula en tiempo real: `sale_price * quantity`.

### 5. SaleConfirmation — Modal pre-confirmación

Antes de enviar la venta, se muestra un modal con:
- Producto seleccionado y cantidad
- Precio unitario (currency)
- Total (currency)
- Costo estimado (si el producto tiene `cost_price`)
- Margen estimado: total - costo

Botones: "Cancel" y "Confirm Sale". Al confirmar, se dispara el POST.

### 6. Navegación

```
/app/sales          → SalesPage (registro de venta)
/app/sales/history  → SalesHistoryPage (historial)
/app/stock          → StockDashboardPage (monitoreo)
```

Sidebar: "Sales" con ícono `ShoppingCart` entre Products y Recipes. "Stock" con ícono `Package` después de Recipes (o como sub-ítem de Raw Materials — pero es una vista diferente, más de monitoreo).

**Decisión**: Stock va como ítem independiente en sidebar porque es una vista de monitoreo gerencial, diferente de la gestión CRUD de Raw Materials. Ícono: `BarChart3` o `Eye`.

### 7. API Client

Archivo nuevo `api/sales.ts`:
```ts
export async function createSale(payload: { product_id: string; quantity: number }): Promise<Sale>
export async function getSales(skip = 0, limit = 50): Promise<Sale[]>
export async function getSale(id: string): Promise<Sale>
```

Types nuevos en `types/sale.ts`:
```ts
interface Sale {
  id: string;
  tenant_id: string;
  product_id: string;
  product_name: string;
  quantity: number;
  unit_price: string;    // DECIMAL(10,2)
  total_price: string;
  total_cost: string | null;
  margin: string | null;
  created_at: string;
}
```

## Risks / Trade-offs

- **[Riesgo] El backend no está implementado aún** → El API client se escribe contra el contrato asumido. Si el backend cambia los nombres de campos o la estructura de respuesta, habrá que ajustar. **Mitigación**: Usar los mismos nombres snake_case que usa el resto de la API. Documentar el contrato en este design.
- **[Riesgo] El producto puede no tener receta (cost_price = null)** → El margen no se puede calcular. **Mitigación**: Mostrar "—" en el campo de margen cuando no hay costo. No bloquear la venta.
- **[Trade-off] Cantidad como entero vs decimal** → Las ventas gastronómicas son en unidades (1 lomito, 2 empanadas). Usar integer simplifica validación. Si en el futuro necesitan vender por peso (ej. 0.5 kg de milanesa), se cambia a Decimal.
- **[Trade-off] Stock Dashboard duplica datos de RawMaterialsPage** → Ambas usan `useRawMaterials`, pero con distinta presentación. Stock Dashboard es más compacto, orientado a "¿qué tengo que comprar?". No es duplicación de lógica, es diferente presentación.

## Open Questions

1. ¿El backend expondrá `total_cost` y `margin` en la respuesta de POST /sales, o solo en GET /sales/{id}? Asumo que sí en POST para mostrar confirmación.
2. ¿El backend aceptará `quantity` como integer o decimal? Asumo integer para MVP.
3. ¿El historial de ventas tendrá endpoint de eliminación/anulación? Asumo que NO en MVP.
