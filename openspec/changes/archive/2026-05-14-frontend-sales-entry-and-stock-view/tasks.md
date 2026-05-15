## 1. Setup

- [x] 1.1 Create `src/features/sales/` directory structure (hooks/, components/, pages/) and `src/features/stock/` directory structure (components/, pages/)
- [x] 1.2 Create `src/types/sale.ts` — Sale interface with id, tenant_id, product_id, product_name, quantity (number), unit_price (string), total_price (string), total_cost (string|null), margin (string|null), created_at (string)
- [x] 1.3 Create `src/api/sales.ts` — functions: createSale (POST /sales), getSales (GET /sales?skip&limit), getSale (GET /sales/{id})

## 2. Sales Entry Components

- [x] 2.1 Create `src/features/sales/components/ProductSelector.tsx` — searchable Select using useProducts hook (reuse existing Select component with searchable={true}). Show product name + sale price in options via renderOption. Filter only is_active products. Loading/error/empty states.
- [x] 2.2 Create `src/features/sales/components/SaleForm.tsx` — React Hook Form + Zod: product_id (required), quantity (required, positive integer). Calculate subtotal in real-time from selected product's sale_price. Disable quantity when no product selected.
- [x] 2.3 Create `src/features/sales/components/SaleConfirmation.tsx` — Modal showing summary: product name, quantity, unit price (currency), total (currency), cost (currency or "—"), margin (currency or "—" if cost available). "Cancel" and "Confirm Sale" buttons with loading state.
- [x] 2.4 Create `src/features/sales/hooks/useSaleMutations.ts` — useCreateSale mutation with onSuccess (toast + invalidate ['sales'] + invalidate ['raw-material-stock'] + invalidate ['raw-materials']) and onError (toast with backend error message)

## 3. Sales History

- [x] 3.1 Create `src/features/sales/hooks/useSales.ts` — useQuery for getSales with pagination params (skip, limit)
- [x] 3.2 Create `src/features/sales/components/SalesTable.tsx` — @tanstack/react-table with columns: Date (formatted), Product, Quantity, Unit Price (currency), Total (currency), Cost (currency or "—"), Margin (currency or "—"). Sorted by date descending by default. Client-side search filter by product name.

## 4. Sales Pages

- [x] 4.1 Create `src/features/sales/pages/SalesPage.tsx` — Sales entry page: ProductSelector + SaleForm with calculated total + "Review Sale" button. SaleConfirmation modal. On confirm success: reset form. Loading/error states for products. Framer Motion page transition.
- [x] 4.2 Create `src/features/sales/pages/SalesHistoryPage.tsx` — History page: SalesTable with search. Loading skeleton → error → empty → table. "New Sale" button linking to /app/sales. Framer Motion page transition.

## 5. Stock Dashboard

- [x] 5.1 Create `src/features/stock/components/StockDashboardTable.tsx` — @tanstack/react-table reusing useRawMaterials hook. Columns: Name (clickable → /app/raw-materials/:id), Unit, Current Stock (StockLevelBadge), Supplier, Cost per Unit (currency). Sorted by stock ascending by default (low stock first). Client-side search filter. Summary stats above table: count of low stock (≤ 10) and out of stock (= 0).
- [x] 5.2 Create `src/features/stock/pages/StockDashboardPage.tsx` — Stock dashboard page: header "Stock Monitor" with summary stats, StockDashboardTable. Loading/error/empty states. Framer Motion page transition.

## 6. Navigation Integration

- [x] 6.1 Add "Sales" navigation item to Sidebar — `ShoppingCart` icon, links to `/app/sales`, positioned between Products and Recipes
- [x] 6.2 Add "Stock" navigation item to Sidebar — `Eye` icon, links to `/app/stock`, positioned after Recipes
- [x] 6.3 Add sales and stock routes in App.tsx — `/app/sales` with nested route for history, `/app/stock`

## 7. Polish

- [x] 7.1 Add Framer Motion page transitions to all new pages (already included in template)
- [x] 7.2 Add success animation feedback when sale is confirmed (brief celebration/appreciation feedback)
- [x] 7.3 Add hover and focus states to all interactive elements
- [x] 7.4 Ensure stock dashboard refreshes when navigating back from a stock adjustment (query invalidation on mount)
