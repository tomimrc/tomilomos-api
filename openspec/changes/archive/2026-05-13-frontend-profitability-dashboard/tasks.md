## 1. Setup

- [x] 1.1 Install Recharts dependency in frontend project
- [x] 1.2 Create `src/features/dashboard/` directory structure (components/, hooks/, pages/)

## 2. Data Layer

- [x] 2.1 Create `src/features/dashboard/hooks/useProfitabilityData.ts` — fetches all products via `useQuery(['products'])`, then uses `useQueries` to batch-fetch product costs. Derives `ProfitabilityItem[]` with computed `margin` (sale_price - cost_price) and `marginPercent` ((margin / sale_price) * 100). Handles loading, error, and partial data states.
- [x] 3.1 Create `src/features/dashboard/types.ts` — `ProfitabilityItem` interface: product (Product), cost (ProductCost | null), margin (number), marginPercent (number | null), costUnavailable (boolean)
- [x] 4.1 Create `src/features/dashboard/components/ProfitSummaryCards.tsx` — Four KPI cards in a responsive grid
- [x] 5.1 Create `src/features/dashboard/components/ProfitMarginBadge.tsx` — Reusable badge component
- [x] 6.1 Create `src/features/dashboard/components/ProfitabilityTable.tsx` — @tanstack/react-table with columns
- [x] 6.2 Add filter controls to ProfitabilityTable — Segmented control / button group
- [x] 7.1 Create `src/features/dashboard/components/ProfitabilityChart.tsx` — Recharts `<BarChart>` with `layout="vertical"`
- [x] 7.2 Wire chart filter to table filter — Chart updates when table filter changes
- [x] 8.1 Create `src/features/dashboard/pages/DashboardPage.tsx` — Orchestrates the dashboard
- [x] 9.1 Add "Dashboard" navigation item to Sidebar — `BarChart3` icon, links to `/app/dashboard`, positioned first (above Products and Recipes)
- [x] 9.2 Add `/app/dashboard` route in App.tsx — Points to DashboardPage, wrapped in ProtectedRoute > AppLayout
- [x] 10.1 Add Framer Motion counter animations to summary card values (count up from 0 on mount)
- [x] 10.2 Add hover card elevation effect to KPI cards (shadow + slight scale on hover)
- [x] 10.3 Ensure responsive layout: cards stack vertically on mobile, chart and table span full width
- [x] 10.4 Verify all currency formatting is consistent with `formatCurrency()` utility
