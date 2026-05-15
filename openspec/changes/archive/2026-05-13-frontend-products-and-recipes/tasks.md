## 1. Project Scaffold & Dependencies

- [x] 1.1 Scaffold Vite + React + TypeScript project in `frontend/` directory
- [x] 1.2 Install and configure Tailwind CSS v3 with `tailwind.config.ts`
- [x] 1.3 Install core dependencies: react-router-dom, axios, @tanstack/react-query, zustand, react-hook-form, zod, @hookform/resolvers, framer-motion, react-hot-toast, lucide-react, @tanstack/react-table
- [x] 1.4 Configure TypeScript path aliases (`@/` → `src/`) in `tsconfig.json` and `vite.config.ts`
- [x] 1.5 Configure Vite proxy to backend API (avoid CORS issues in dev)

## 2. API Client & Types

- [x] 2.1 Create `src/api/client.ts` — Axios instance with base URL from env, JWT interceptor (attach Bearer token from auth store), 401 response interceptor (redirect to login)
- [x] 2.2 Create `src/types/product.ts` — Product, ProductCreate, ProductUpdate, ProductCost interfaces matching backend schemas
- [x] 2.3 Create `src/types/recipe.ts` — Recipe, RecipeCreate, RecipeUpdate, RecipeIngredient, RecipeIngredientCreate, RecipeIngredientUpdate, RecipeCost interfaces
- [x] 2.4 Create `src/api/products.ts` — API functions: getProducts, getProduct, createProduct, updateProduct, deleteProduct, getProductCost
- [x] 2.5 Create `src/api/recipes.ts` — API functions: getRecipes, getRecipe, createRecipe, updateRecipe, deleteRecipe, getRecipeCost, getRecipeIngredients, addRecipeIngredient, updateRecipeIngredient, removeRecipeIngredient
- [x] 2.6 Create `src/lib/formatters.ts` — formatCurrency (DECIMAL to $XX.XX), formatDate, truncateText utilities
- [x] 2.7 Create `src/lib/constants.ts` — valid units array (kg, g, L, mL, units, pieces, boxes), API route constants

## 3. Shared UI Components

- [x] 3.1 Create `src/components/ui/Button.tsx` — Primary, secondary, danger, ghost variants with loading state
- [x] 3.2 Create `src/components/ui/Input.tsx` — Text input with label, error message, disabled state
- [x] 3.3 Create `src/components/ui/Modal.tsx` — Confirmation modal with title, body, confirm/cancel actions, Framer Motion enter/exit
- [x] 3.4 Create `src/components/ui/Select.tsx` — Searchable dropdown with label, error message, loading state
- [x] 3.5 Create `src/components/ui/Badge.tsx` — Active/Inactive status badges with color variants
- [x] 3.6 Create `src/components/ui/Toast.tsx` — react-hot-toast configuration and custom styled Toaster
- [x] 3.7 Create `src/components/shared/LoadingSkeleton.tsx` — Table skeleton (rows with pulsing placeholders) and Card skeleton variants
- [x] 3.8 Create `src/components/shared/EmptyState.tsx` — Icon + message + CTA button component
- [x] 3.9 Create `src/components/shared/ErrorState.tsx` — Error message + "Retry" button component
- [x] 3.10 Create `src/components/shared/ConfirmDialog.tsx` — Reusable delete confirmation wrapper around Modal with danger styling

## 4. Layout & Routing

- [x] 4.1 Create `src/components/layout/Sidebar.tsx` — Navigation links (Products, Recipes) with active state highlighting, Lucide icons
- [x] 4.2 Create `src/components/layout/TopBar.tsx` — App title, tenant name, user avatar/menu placeholder
- [x] 4.3 Create `src/components/layout/AppLayout.tsx` — Sidebar + TopBar + `<Outlet />` layout with responsive behavior
- [x] 4.4 Create `src/components/layout/ProtectedRoute.tsx` — Auth guard that checks for valid token, redirects to /login if missing
- [x] 4.5 Create `src/App.tsx` — Router with createBrowserRouter: `/login` → login, `/app` → AppLayout (protected) wrapping nested routes
- [x] 4.6 Create `src/main.tsx` — ReactDOM render with QueryClientProvider, RouterProvider, Toaster

## 5. Zustand Stores

- [x] 5.1 Create `src/stores/authStore.ts` — token, user, tenantId state with login/logout actions (integration point with frontend-setup-and-auth-flow)

## 6. Product Feature — List Page

- [x] 6.1 Create `src/features/products/hooks/useProducts.ts` — useQuery wrapping getProducts with pagination params (skip, limit)
- [x] 6.2 Create `src/features/products/hooks/useProductMutations.ts` — useMutation hooks for create, update, delete with query invalidation and success/error toasts
- [x] 6.3 Create `src/features/products/components/ProductTable.tsx` — @tanstack/react-table with columns: Name, Sale Price (currency), Cost Price (currency), Status (Badge), Actions (Edit/Delete buttons). Sorted by name by default.
- [x] 6.4 Create `src/features/products/pages/ProductsPage.tsx` — Renders loading skeleton → error state → empty state → ProductTable based on query state. "New Product" button in header. Framer Motion page transition.
- [x] 7.1 Create `src/features/products/components/ProductForm.tsx` — React Hook Form with Zod validation: name (required, max 255), sale_price (required, > 0, max 2 decimals), recipe_id (optional select), is_active (toggle/checkbox). Reused for both create and edit via `mode` prop.
- [x] 7.2 Create `src/features/products/components/RecipeSelector.tsx` — Searchable Select fetching recipes via useQuery, with "None" option to unlink
- [x] 7.3 Create `src/features/products/pages/ProductCreatePage.tsx` — ProductForm in "create" mode. On submit: POST, toast, navigate to list.
- [x] 7.4 Create `src/features/products/pages/ProductEditPage.tsx` — Fetch product by ID, pre-populate ProductForm in "edit" mode. On submit: PUT, toast, navigate back.
- [x] 8.1 Create `src/features/products/hooks/useProduct.ts` — useQuery wrapping getProduct(id) and getProductCost(id)
- [x] 8.2 Create `src/features/products/components/ProductCostDisplay.tsx` — Shows cost amount, cost source (recipe-based vs manual), linked recipe name (clickable). Warning banner for 424/partial cost. Loading and error states.
- [x] 8.3 Create `src/features/products/pages/ProductDetailPage.tsx` — Product info card (name, price, status) + ProductCostDisplay + linked recipe link. Edit/Delete action buttons in header. Framer Motion enter animation.
- [x] 9.1 Implement delete flow in ProductsPage: "Delete" button on each row opens ConfirmDialog, on confirm calls deleteProduct mutation with optimistic removal + exit animation (AnimatePresence)

## 10. Recipe Feature — List Page

- [x] 10.1 Create `src/features/recipes/hooks/useRecipes.ts` — useQuery wrapping getRecipes with pagination params
- [x] 10.2 Create `src/features/recipes/hooks/useRecipeMutations.ts` — useMutation hooks for create, update, delete with query invalidation and toasts
- [x] 10.3 Create `src/features/recipes/components/RecipeTable.tsx` — @tanstack/react-table with columns: Name, Description (truncated), Ingredient Count, Actions (Edit/Delete). Sorted by name.
- [x] 10.4 Create `src/features/recipes/pages/RecipesPage.tsx` — Loading skeleton → error → empty → RecipeTable. "New Recipe" button in header. Framer Motion page transition.
- [x] 11.1 Create `src/features/recipes/components/RecipeForm.tsx` — React Hook Form + Zod: name (required, max 255), description (optional, max 1000). Reused for create/edit via `mode` prop.
- [x] 11.2 Create `src/features/recipes/pages/RecipeCreatePage.tsx` — RecipeForm in "create" mode. On submit: POST, toast, navigate to recipe detail.
- [x] 11.3 Create `src/features/recipes/pages/RecipeEditPage.tsx` — Fetch recipe, pre-populate RecipeForm. On submit: PUT, handle 409 conflict toast.
- [x] 12.1 Create `src/features/recipes/hooks/useRecipe.ts` — useQuery for getRecipe(id), getRecipeIngredients(id), getRecipeCost(id)
- [x] 12.2 Create `src/features/recipes/hooks/useIngredientMutations.ts` — useMutation hooks for add, update, remove ingredient with recipe + cost query invalidation
- [x] 12.3 Create `src/features/recipes/components/IngredientRow.tsx` — Displays raw material name, quantity, unit, unit cost, total cost. Inline edit mode (quantity + unit become inputs on Edit click, with Save/Cancel). Delete button with confirmation.
- [x] 12.4 Create `src/features/recipes/components/IngredientForm.tsx` — Inline form to add new ingredient: raw material selector (searchable Select), quantity input, unit select. Submit adds ingredient and resets form.
- [x] 12.5 Create `src/features/recipes/components/RecipeCostDisplay.tsx` — Total recipe cost display, warning banner for 424/missing prices. Ingredients with missing prices visually distinguished (warning icon, muted row).
- [x] 12.6 Create `src/features/recipes/pages/RecipeDetailPage.tsx` — Recipe info header (name, description, Edit/Delete buttons), RecipeCostDisplay, ingredient list with IngredientForm at top, each ingredient as IngredientRow. Empty state if no ingredients. AnimatePresence for ingredient add/remove animations. Framer Motion page transition.
- [x] 13.1 Implement delete flow in RecipesPage and RecipeDetailPage: ConfirmDialog, deleteRecipe mutation, optimistic removal with exit animation, navigate to list if deleting from detail page

## 14. Cross-Feature Integration

- [x] 14.1 Wire RecipeSelector into ProductForm (create and edit) — uses searchable Select fetching tenant's recipes
- [x] 14.2 Implement recipe name as clickable link in ProductDetailPage → navigates to `/app/recipes/:id`
- [x] 14.3 Implement product list re-fetch when a recipe is modified (React Query invalidation of products query when recipe ingredients change)
- [x] 14.4 Add "Products using this recipe" indicator on RecipeDetailPage (optional count or list)
- [x] 15.1 Add Framer Motion page transitions (fade + slide) to all page components using `motion.div` wrapper with `initial`, `animate`, `exit` props
- [x] 15.2 Add Framer Motion list animations (AnimatePresence + motion.li) for product/recipe table rows on add/remove
- [x] 15.3 Add hover and focus states to all interactive elements (buttons, table rows, nav links) using Tailwind
- [x] 15.4 Add loading states to all mutation buttons (spinner + disabled during submit)
- [x] 15.5 Verify all toast notifications render correctly: success (green check), error (red X), warning (yellow)
- [x] 15.6 Test responsive layout: sidebar collapses/hides on mobile, tables scroll horizontally, forms stack vertically
