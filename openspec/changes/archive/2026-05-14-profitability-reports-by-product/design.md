## Context

Las specs `frontend-profitability-summary`, `frontend-profitability-table` y `frontend-profitability-chart` ya existen en `openspec/specs/` y definen exactamente qué construir: KPI cards con métricas agregadas, tabla sortable/filtrable con márgenes por producto, y gráfico de barras del top 10. Los datos vienen de endpoints existentes: `GET /api/v1/products` (lista de productos con sale_price, cost_price, is_active) y `GET /api/v1/products/{id}/cost` (costo detallado por producto). No se requiere backend nuevo.

**Stack existente**: React 18 · TanStack Query v5 · @tanstack/react-table · Tailwind CSS · Framer Motion · Lucide React. Se agrega **Recharts** para el gráfico de barras (no está en las dependencias actuales, requiere `npm install recharts`).

## Goals / Non-Goals

**Goals:**
- Dashboard de rentabilidad en `/app/profitability` con summary cards, tabla y gráfico
- KPI cards: Average Margin (%), Most Profitable, Least Profitable, Active Products count
- Tabla sortable y filtrable (All / Profitable / Unprofitable) con indicadores verde/rojo
- Gráfico de barras horizontales top 10 con tooltip y click-to-navigate
- Filtro consistente entre tabla y gráfico
- Edge cases: costos no disponibles, márgenes negativos, división por cero, sin productos

**Non-Goals:**
- Reportes por período (mensual, semanal) — solo snapshot actual
- Exportación de reportes (PDF, CSV)
- Drill-down por ingrediente o materia prima
- Comparación histórica (mes a mes)
- Alertas de margen bajo
- Backend nuevo — todos los datos vienen de endpoints existentes

## Decisions

### 1. Data Fetching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                  DATA FLOW                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  useProducts(skip=0, limit=1000)                            │
│    │                                                        │
│    ▼                                                        │
│  products[] → filter is_active                              │
│    │                                                        │
│    ▼                                                        │
│  useQueries(products.map(p => useProductCost(p.id)))        │
│    │  (TanStack Query parallel batch)                       │
│    ▼                                                        │
│  costs[] → calculate margins                                │
│    │                                                        │
│    ▼                                                        │
│  profitabilityData[] → SummaryCards + Table + Chart          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Decisión**: Usar `useQueries` de TanStack Query para fetchear costos en paralelo. Es más eficiente que llamadas secuenciales y maneja loading/error por producto individual. Alternativa considerada: un solo endpoint batch — no existe en el backend y requeriría cambios.

### 2. Margin Calculation

```ts
interface ProfitabilityRow {
  product: Product;
  cost: ProductCost | null;
  costAvailable: boolean;
  marginDollars: number | null;
  marginPercent: number | null;
}

function calculateMargin(product: Product, cost: ProductCost | null): ProfitabilityRow {
  const salePrice = parseFloat(product.sale_price);
  const costPrice = cost ? parseFloat(cost.total_cost) : null;

  if (salePrice === 0 || costPrice === null) {
    return { ..., marginDollars: null, marginPercent: null };
  }

  const marginDollars = salePrice - costPrice;
  const marginPercent = (marginDollars / salePrice) * 100;

  return { ..., marginDollars: round2(marginDollars), marginPercent: round2(marginPercent) };
}
```

**Fórmulas**:
- `margin_dollars = sale_price - cost_price`
- `margin_percent = (margin_dollars / sale_price) * 100`
- Ambos redondeados a 2 decimales

**Edge cases**:
- `cost_price = null` (cost unavailable) → margin = null, display "—"
- `sale_price = 0` → margin_percent = null (div by zero), display "—"
- `sale_price = 0, cost_price > 0` → margin_dollars = -cost_price (raw loss)

### 3. Component Architecture

```
features/profitability/
├── hooks/
│   └── useProfitability.ts       ← useProducts + useQueries(batch cost) + calculate margins
├── components/
│   ├── ProfitabilitySummary.tsx  ← 4 KPI cards
│   ├── ProfitabilityTable.tsx    ← @tanstack/react-table with filters
│   └── ProfitabilityChart.tsx    ← Recharts BarChart
└── pages/
    └── ProfitabilityPage.tsx     ← Page layout: summary + table + chart
```

### 4. Chart Library: Recharts

**Decisión**: Recharts sobre alternativas como Chart.js o custom SVG:
- Recharts es React-native (componentes JSX, no canvas), más fácil de integrar con React patterns
- Soporta tooltips, clicks, y responsive out-of-the-box
- Es la librería más popular para dashboards React (~23k stars)
- Bundle size: ~200KB gzipped (~50KB) — aceptable para un dashboard

**Implementación**: `BarChart` horizontal con `Bar` + `Tooltip` + `Cell` para colorear verde/rojo. Layout: `layout="vertical"`.

### 5. Filter Sync (Table ↔ Chart)

El filtro (All / Profitable / Unprofitable) es estado del componente `ProfitabilityPage`. Se pasa como prop tanto a `ProfitabilityTable` como a `ProfitabilityChart`. Ambos componentes filtran sus datos según el mismo estado. El gráfico solo muestra productos con margen calculable (costAvailable = true).

### 6. KPI Summary Calculation

- **Average Margin (%)**: Promedio de `marginPercent` de productos con costAvailable = true. `sum(margins) / count`.
- **Most Profitable**: Producto con mayor `marginPercent`. Si empate, primero alfabéticamente.
- **Least Profitable**: Producto con menor `marginPercent` (puede ser negativo). Si empate, primero alfabéticamente.
- **Active Products**: Count de `is_active = true`. Subtítulo: "out of N total".

### 7. Navigation

Sidebar: "Profitability" con `TrendingUp`, entre Recipes y Stock Monitor.
Ruta: `/app/profitability` — página única (no subrutas).

## Risks / Trade-offs

- **[Riesgo] N+1 queries de costos** → Si hay 100 productos, se hacen 100 llamadas a `GET /products/{id}/cost`. **Mitigación**: TanStack Query las paraleliza y cachea. En MVP con pocos productos (< 50) es aceptable. Futuro: endpoint batch.
- **[Riesgo] Costos pueden fallar individualmente (424)** → Algunos productos pueden tener costo no disponible. **Mitigación**: `useQueries` maneja errores por query. Productos con error se marcan como `costAvailable: false` y muestran "—".
- **[Trade-off] Recharts como nueva dependencia** → Agrega ~200KB al bundle. **Mitigación**: Es tree-shakeable, solo se importa BarChart/Bar/Tooltip/Cell. Alternativa custom SVG sería más ligera pero más código para mantener.
- **[Trade-off] Sin lazy loading del gráfico** → El gráfico se renderiza siempre, incluso si no hay datos. **Mitigación**: Muestra estado empty/skeleton en vez de ocultar el contenedor, evitando layout shift.
