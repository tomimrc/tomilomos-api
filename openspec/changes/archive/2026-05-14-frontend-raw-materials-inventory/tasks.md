## 1. Setup

- [x] 1.1 Create `src/features/raw-materials/` directory structure (hooks/, components/, pages/)
- [x] 1.2 Expand `src/api/rawMaterials.ts` — add functions: getRawMaterial, createRawMaterial, updateRawMaterial, deleteRawMaterial, addStock, removeStock, getStock

## 2. Types

- [x] 2.1 Create `src/features/raw-materials/types.ts` — RawMaterial, RawMaterialCreate, RawMaterialUpdate, StockAdjustmentRequest, StockLevel interfaces matching backend schemas

## 3. Data Hooks

- [x] 3.1 Create `src/features/raw-materials/hooks/useRawMaterials.ts` — useQuery for list with pagination params (skip, limit)
- [x] 3.2 Create `src/features/raw-materials/hooks/useRawMaterial.ts` — useQuery for getRawMaterial(id) and getStock(id)
- [x] 3.3 Create `src/features/raw-materials/hooks/useRawMaterialMutations.ts` — useMutation hooks for create, update, delete, addStock, removeStock. Each invalidates relevant queries. Stock mutations invalidate ['raw-material', id] and ['raw-materials']. Cost update also invalidates ['recipe-cost'] and ['product-cost'].

## 4. Stock Level Badge

- [x] 4.1 Create `src/features/raw-materials/components/StockLevelBadge.tsx` — Color-coded badge:
  - Green (stock > 10): check icon, stock quantity, "In stock"
  - Amber (stock > 0 AND ≤ 10): warning icon, stock quantity, "Low stock"
  - Red (stock = 0): alert icon, "0", "Out of stock"
  - Accepts `stock: number` prop and optional `showLabel: boolean`

## 5. Raw Material Table

- [x] 5.1 Create `src/features/raw-materials/components/RawMaterialTable.tsx` — @tanstack/react-table with columns:
  - Name (clickable → detail page)
  - Unit of Measurement
  - Cost per Unit (formatted currency)
  - Current Stock (StockLevelBadge)
  - Supplier (or "—")
  - Actions (Edit, Delete buttons)
  - Sorted by name ascending by default, all columns sortable
  - Client-side search filter: text input above table filters by name

## 6. Raw Material Form

- [x] 6.1 Create `src/features/raw-materials/components/RawMaterialForm.tsx` — React Hook Form + Zod:
  - name: required, max 255
  - unit_of_measurement: required, must be one of VALID_UNITS (Select component)
  - cost_per_unit: required, must be > 0, max 2 decimal places
  - supplier: optional, max 255
  - Reused for create/edit via `mode` prop and optional `defaultValues`
  - Select for unit shows all valid units from constants

## 7. Stock Adjustment Modal

- [x] 7.1 Create `src/features/raw-materials/components/StockAdjustmentModal.tsx` — Reusable modal component:
  - Props: `mode` ('add' | 'remove'), `materialName`, `currentStock`, `open`, `onClose`, `onSubmit`
  - Quantity input (Decimal, > 0 validation)
  - Reason input (optional, max 255)
  - In 'remove' mode: shows "Available: X.XX unit" reference text
  - Action button: green "Add Stock" or red "Remove Stock" with loading state
  - Form validation prevents submit if quantity ≤ 0
  - Closes on successful submit

## 8. Pages

- [x] 8.1 Create `src/features/raw-materials/pages/RawMaterialsPage.tsx` — List page:
  - useRawMaterials hook
  - Loading skeleton → error → empty → RawMaterialTable
  - "New Raw Material" button in header
  - Client-side search input for name filtering
  - Delete confirmation via ConfirmDialog
  - Framer Motion page transition

- [x] 8.2 Create `src/features/raw-materials/pages/RawMaterialCreatePage.tsx` — Create page:
  - RawMaterialForm in "create" mode
  - On success: toast + navigate to list
  - Framer Motion page transition

- [x] 8.3 Create `src/features/raw-materials/pages/RawMaterialEditPage.tsx` — Edit page:
  - Fetch material by ID, pre-populate form
  - On success: toast + invalidate recipe/product cost queries + navigate to detail
  - Loading + error states
  - Framer Motion page transition

- [x] 8.4 Create `src/features/raw-materials/pages/RawMaterialDetailPage.tsx` — Detail page:
  - Material info card: name, unit, cost (currency), supplier, stock (StockLevelBadge), dates
  - Action buttons: Edit, Delete, Add Stock, Remove Stock
  - StockAdjustmentModal for add/remove operations
  - Delete confirmation via ConfirmDialog (navigate to list on success)
  - Loading + error + not-found states
  - Framer Motion page transition

## 9. Navigation Integration

- [x] 9.1 Add "Raw Materials" navigation item to Sidebar — `Boxes` icon, links to `/app/raw-materials`, positioned after Dashboard and before Products
- [x] 9.2 Add raw materials routes in App.tsx — `/app/raw-materials` with nested routes for new, :id, :id/edit

## 10. Polish

- [x] 10.1 Add Framer Motion page transitions to all raw material pages
- [x] 10.2 Add exit animations for deleted items in the table (AnimatePresence on rows)
- [x] 10.3 Ensure stock badge updates color immediately after stock adjustment (query invalidation)
- [x] 10.4 Add hover and focus states to all interactive elements
