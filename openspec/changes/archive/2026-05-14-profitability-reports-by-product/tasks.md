## 1. Setup

- [x] 1.1 Create `src/features/profitability/` directory structure (hooks/, components/, pages/)
- [x] 1.2 Install `recharts` dependency: `npm install recharts`

## 2. Data Hook

- [x] 2.1 Create `src/features/profitability/hooks/useProfitability.ts` — custom hook that:
  - Calls useProducts(skip=0, limit=1000) to get all products
  - Uses useQueries to batch-fetch getProductCost(id) for each active product
  - Calculates margins: marginDollars = salePrice - costPrice, marginPercent = (marginDollars / salePrice) * 100
  - Handles edge cases: cost unavailable (null), salePrice = 0 (null margin), negative margins
  - Returns: profitabilityData array + isLoading + isError + refetch

## 3. Summary Cards

- [x] 3.1 Create `src/features/profitability/components/ProfitabilitySummary.tsx` — 4 KPI cards in a responsive grid:
  - Average Margin (%): avg of marginPercent across products with valid costs. Footnote: "X excluded — cost unavailable"
  - Most Profitable: product with highest margin%. Name clickable → /app/products/:id
  - Least Profitable: product with lowest margin%. Name clickable
  - Active Products: count of is_active products, subtitle "out of N total"
  - Each card: Lucide icon + label + value + subtitle
  - Edge cases: no products → "—", single product → same for most/least

## 4. Profitability Table

- [x] 4.1 Create `src/features/profitability/components/ProfitabilityTable.tsx` — @tanstack/react-table with columns:
  - Product Name (clickable → /app/products/:id, link styled)
  - Sale Price (formatCurrency)
  - Cost Price (formatCurrency, or "—" if unavailable)
  - Gross Margin $ (formatCurrency, or "—")
  - Margin % (green if > 0, red if < 0, gray if = 0, "—" if unavailable)
  - Visual indicator: TrendingUp green / TrendingDown red / Minus gray
  - Sort by margin % descending by default, all columns sortable
  - Search input for name filter
  - Filter tabs: All / Profitable (margin > 0) / Unprofitable (margin < 0)
  - Empty state when filter yields no results
  - Loading state: skeleton rows

## 5. Bar Chart

- [x] 5.1 Create `src/features/profitability/components/ProfitabilityChart.tsx` — Recharts horizontal BarChart:
  - Top N products by margin % (max 10, fewer if less products)
  - Bars: green for positive margin, red for negative
  - Tooltip on hover: product name, sale price, cost price, gross margin $, margin %
  - Click on bar → navigate to /app/products/:id
  - Y-axis: product names (truncate > 20 chars, full name in tooltip)
  - X-axis: percentage with % suffix
  - Responsive: full width on mobile, ~60% on desktop
  - Empty state when no margin data available (retains container size)
  - Loading state: pulsing placeholder bars (skeleton)

## 6. Page

- [x] 6.1 Create `src/features/profitability/pages/ProfitabilityPage.tsx` — Dashboard page layout:
  - Header: "Profitability" with subtitle
  - ProfitabilitySummary (top)
  - ProfitabilityChart (middle, optional with filter sync)
  - ProfitabilityTable (bottom, with filter tabs)
  - Filter state shared between chart and table (useState in page, passed as props)
  - Loading state: summary skeleton + table skeleton + chart skeleton
  - Error state: ErrorState with retry
  - Empty state: "No products to analyze" when 0 products
  - Framer Motion page transition

## 7. Navigation

- [x] 7.1 Add "Profitability" navigation item to Sidebar — `TrendingUp` icon, links to `/app/profitability`, positioned between Recipes and Stock Monitor
- [x] 7.2 Add profitability route in App.tsx — `/app/profitability`

## 8. Polish

- [x] 8.1 Add Framer Motion page transition
- [x] 8.2 Add hover and focus states to all interactive elements
- [x] 8.3 Ensure chart updates immediately when filter changes (no delay)
- [x] 8.4 Ensure responsive layout (summary cards stack on mobile, table scrolls horizontally)
