## Context

TomiLomos tiene el backend de costos de producto completo (`GET /api/v1/products/{id}/cost`) y el frontend de productos y recetas (`frontend-products-and-recipes`) ya implementado. Los gestores necesitan ver rentabilidad, pero no hay backend de reportes todavía. Este cambio construye un dashboard de rentabilidad por producto usando exclusivamente los endpoints existentes, calculando márgenes client-side.

**Stack existente (del frontend)**: React 18 · Vite · Tailwind CSS · TanStack Query v5 · Zustand · React Hook Form + Zod · Framer Motion · Axios · @tanstack/react-table · Lucide React

**Endpoints disponibles**:
- `GET /api/v1/products` → lista de productos con `sale_price`
- `GET /api/v1/products/{id}/cost` → costo calculado por producto (recipe-based o manual)

**Restricción clave**: No hay endpoint batch de costos. Para N productos, se necesitan N+1 requests (1 lista + N costos individuales). Esto es aceptable para dashboards con decenas de productos.

## Goals / Non-Goals

**Goals:**
- Dashboard de rentabilidad con tarjetas KPI (margen promedio, producto más/menos rentable)
- Tabla de rentabilidad por producto con margen bruto ($) y margen porcentual (%)
- Gráfico de barras horizontal comparando márgenes (top 10 productos)
- Filtro por tipo de margen (positivo, negativo, todos)
- Ordenamiento por cualquier columna
- Cálculo client-side de márgenes usando datos existentes
- Indicadores visuales de warning para productos sin costo disponible

**Non-Goals:**
- Backend de reportes de rentabilidad (pertenece a `profitability-reports-by-product`)
- Rentabilidad basada en ventas (qty_sold, revenue por período) — depende de `register-sales-with-stock-deduction`
- Exportación de reportes (PDF, CSV)
- Filtros por fecha/período (no hay datos de ventas)
- Gráficos de tendencias o series temporales

## Decisions

### 1. Estrategia de fetching de costos

| Enfoque | Elección | Razón |
|---------|----------|-------|
| Fetch individual | `useQueries` de TanStack Query | Cada producto dispara su propio `useQuery` para el costo. `useQueries` los agrupa en un solo hook, maneja loading/error por query, y permite renderizado progresivo (mostrar datos apenas llegan). |
| Alternativa descartada: endpoint batch | — | No existe en el backend y este cambio es frontend-only. |
| Alternativa descartada: fetch secuencial | — | Muy lento. `useQueries` es paralelo. |

### 2. Librería de gráficos

| Opción | Elegida | Razón |
|--------|---------|-------|
| **Recharts** | ✅ | Construida sobre React y D3, declarativa, tipada, ligera (~150KB). `<BarChart>` horizontal con `layout="vertical"` cubre perfectamente el caso de uso. Sin dependencia directa de D3. |
| Chart.js + react-chartjs-2 | ❌ | API imperativa, más boilerplate, menos idiomática en React. |
| Custom SVG | ❌ | Reinventar la rueda para un gráfico de barras simple. Más código, más bugs. |

### 3. Cálculo de márgenes

**Fórmulas client-side**:
```
margen_bruto = sale_price - cost_price
margen_porcentual = (margen_bruto / sale_price) * 100   // solo si sale_price > 0
```

**Manejo de precisión**: Los valores vienen como strings DECIMAL(10,2) del backend. En frontend se parsean con `parseFloat()` para los cálculos, y se formatean con `formatCurrency()` para display. Esto es aceptable para un dashboard (no se hacen transacciones).

**Casos edge**:
- `cost_price = null` o `cost_source = "manual"` → costo = 0, margen = sale_price (100%).
- Error 424 (cost unavailable) → mostrar "—" en margen, warning visual.
- `sale_price = 0` → margen % indefinido, mostrar "—".

### 4. Arquitectura de datos

```
features/dashboard/
├── hooks/
│   └── useProfitabilityData.ts    ← TanStack Query useQueries para productos + costos
├── components/
│   ├── ProfitSummaryCards.tsx     ← 4 tarjetas KPI (margen promedio, top, bottom, count)
│   ├── ProfitabilityTable.tsx     ← @tanstack/react-table con márgenes
│   ├── ProfitabilityChart.tsx     ← Recharts BarChart horizontal
│   └── ProfitMarginBadge.tsx      ← Badge verde/rojo con % de margen
└── pages/
    └── DashboardPage.tsx          ← Página principal que orquesta todo
```

### 5. Flujo de datos

```
DashboardPage
  └─ useProfitabilityData()
       ├─ useQuery(['products']) → lista de productos
       └─ useQueries(products.map(p => useQuery(['product-cost', p.id])))
            → costos individuales (paralelo)
  └─ Deriva profitabilityData = productos.map(p => ({
       ...p,
       cost: costs[p.id] ?? 0,
       margin: p.sale_price - cost,
       marginPercent: (margin / p.sale_price) * 100
     }))
  └─ Pasa profitabilityData a:
       ├─ ProfitSummaryCards (calcula KPIs)
       ├─ ProfitabilityTable (tabla ordenable/filtrable)
       └─ ProfitabilityChart (top 10 por margen)
```

### 6. Navegación

Se agrega un nuevo ítem al sidebar existente:
```
/app/dashboard → DashboardPage (nuevo)
```

El sidebar ya tiene Products y Recipes. Dashboard va primero (arriba) con un ícono de `BarChart3` o `TrendingUp`.

## Risks / Trade-offs

- **[Riesgo] N+1 requests para costos** → Con 50 productos, son 51 requests. **Mitigación**: `useQueries` las paraleliza. TanStack Query cachea por 30s (staleTime). Para catálogos grandes (>200 productos), considerar agregar endpoint batch en el backend — pero eso está fuera del scope de este cambio.
- **[Riesgo] Cálculo client-side de márgenes con floats** → `parseFloat("45.99")` puede tener errores de precisión para operaciones complejas. **Mitigación**: Solo hacemos resta y división simple, no acumulaciones. Para display usamos 2 decimales. El backend ya garantiza DECIMAL(10,2).
- **[Trade-off] Sin filtro por período** → No hay datos de ventas. El dashboard muestra rentabilidad "potencial" (precio - costo), no rentabilidad "realizada" (basada en ventas). Es útil para decisiones de pricing y menú, pero no reemplaza un P&L.
- **[Dependencia] Recharts es una nueva dependencia** → ~150KB minificado. Justificado: es la única lib de gráficos necesaria, y un gráfico de barras custom sería más código y peor UX.
