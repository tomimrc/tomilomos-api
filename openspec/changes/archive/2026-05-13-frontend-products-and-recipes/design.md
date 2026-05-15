## Context

TomiLomos es un SaaS de gestión gastronómica multi-tenant. El backend (FastAPI + PostgreSQL) expone endpoints completos para productos y recetas con JWT Bearer auth. Este cambio crea la primera interfaz de usuario real — después del setup de autenticación — permitiendo a los gestores administrar productos y recetas visualmente.

**Estado actual**: No existe ningún frontend. El proyecto usa CORS configurado en `localhost:3000` como indicio de que se planifica un frontend React.

**Restricciones**:
- Multi-tenancy: toda operación debe ser automáticamente scopeada al tenant del usuario autenticado (el backend ya lo maneja vía token JWT)
- Precios en DECIMAL(10,2): nunca usar floats para dinero en el frontend
- El diseño debe ser profesional, con animaciones fluidas (Framer Motion) como feedback visual
- Debe depender del contexto de autenticación provisto por `frontend-setup-and-auth-flow`

## Goals / Non-Goals

**Goals:**
- CRUD completo de productos con validación de precios y estados de carga/error/empty
- CRUD completo de recetas con validación de nombres únicos
- Gestión de ingredientes dentro de una receta (agregar, editar, eliminar)
- Visualización del costo calculado de recetas y productos
- Vinculación producto-receta desde el formulario de producto
- Navegación fluida entre productos y recetas
- Animaciones de feedback para crear, editar, eliminar (Framer Motion)

**Non-Goals:**
- Autenticación / login (pertenece a `frontend-setup-and-auth-flow`)
- Gestión de materias primas (pertenece a `frontend-raw-materials-inventory`)
- Registro de ventas (pertenece a `frontend-sales-entry-and-stock-view`)
- Dashboard de rentabilidad (pertenece a `frontend-profitability-dashboard`)
- Cálculo de costos en el frontend (el backend ya los calcula; solo mostramos resultados)
- Tests end-to-end (se agregan en fase posterior)

## Decisions

### 1. Stack tecnológico

| Capa | Elección | Alternativas consideradas | Razón |
|------|----------|--------------------------|-------|
| Framework | React 18 + TypeScript | Vue, Svelte, Next.js | Consistente con AGENTS.md, ecosistema maduro, tipado estricto |
| Build tool | Vite | CRA (deprecated), Webpack | Arranque instantáneo, HMR rápido, configuración mínima |
| Estilos | Tailwind CSS v3 | CSS Modules, styled-components | Utility-first, productivo, consistente con el perfil del agente |
| Animaciones | Framer Motion v10+ | CSS transitions, react-spring | API declarativa, layout animations, presencia/exit animations |
| Routing | React Router v6 (createBrowserRouter) | TanStack Router, Next.js pages | Estándar, nested routes, loaders/actions |
| Estado global | Zustand | Redux Toolkit, React Context + useReducer | API mínima, sin boilerplate, tipado TypeScript excelente |
| Data fetching | TanStack Query (React Query) v5 | SWR, useEffect manual | Caché automático, revalidación, estados de loading/error incluidos, optimistic updates |
| Formularios | React Hook Form + Zod | Formik, forms manuales | Performante (uncontrolled), validación con Zod, integración TypeScript |
| HTTP client | Axios con interceptores | fetch nativo, ky | Interceptores para JWT, transformación automática de JSON, manejo centralizado de errores 401 |
| Notificaciones | react-hot-toast | sonner, shadcn/ui toast | Ligero, API simple, personalizable, animado |
| Íconos | Lucide React | Heroicons, react-icons | Tree-shakeable, diseño consistente, SVG puro |
| Tablas | @tanstack/react-table v8 | AG Grid, tabla manual | Headless, tipado, sorting/pagination built-in, sin imponer diseño |

### 2. Estructura de directorios

```
frontend/
├── src/
│   ├── api/                  # Cliente HTTP y funciones de API
│   │   ├── client.ts         # Instancia de Axios con interceptores JWT
│   │   ├── products.ts       # Funciones: getProducts, createProduct, etc.
│   │   └── recipes.ts        # Funciones: getRecipes, createRecipe, etc.
│   ├── components/           # Componentes reutilizables
│   │   ├── ui/               # Botones, inputs, modales, tabs, etc.
│   │   ├── layout/           # AppLayout, Sidebar, TopBar
│   │   └── shared/           # EmptyState, ErrorState, LoadingSkeleton
│   ├── features/             # Features por dominio
│   │   ├── products/
│   │   │   ├── components/   # ProductList, ProductForm, ProductCard
│   │   │   ├── hooks/        # useProducts, useProduct, useProductMutations
│   │   │   └── pages/        # ProductsPage, ProductDetailPage
│   │   └── recipes/
│   │       ├── components/   # RecipeList, RecipeForm, IngredientList, IngredientForm
│   │       ├── hooks/        # useRecipes, useRecipe, useRecipeMutations
│   │       └── pages/        # RecipesPage, RecipeDetailPage
│   ├── hooks/                # Hooks compartidos (useAuth, useDebounce)
│   ├── lib/                  # Utilidades (formatters de moneda, constantes)
│   ├── stores/               # Stores de Zustand (auth store, UI store)
│   ├── types/                # Tipos TypeScript generados/compartidos
│   ├── App.tsx               # Router principal
│   └── main.tsx              # Entry point
├── index.html
├── tailwind.config.ts
├── tsconfig.json
└── vite.config.ts
```

**Decisión**: Feature-based structure sobre file-type structure. Agrupa por dominio (products, recipes) en vez de por tipo de archivo (components, hooks, pages). Facilita el code splitting y la navegación mental: todo lo de productos está en `features/products/`.

### 3. Manejo de estado: cómo se integran Zustand, React Query y React Hook Form

**Zustand**: Solo estado de UI global que sobrevive entre navegaciones.
- Auth store (token, user info, tenant info) — consumido del contexto del setup
- UI store (sidebar collapsed, theme)

**React Query (TanStack Query)** : Estado del servidor — sincronización con el backend.
- Cachea respuestas de productos y recetas
- Invalida queries después de mutaciones (crear, editar, eliminar)
- Maneja automáticamente loading, error, refetch

**React Hook Form**: Estado de formularios — local, no se comparte.
- Validación con Zod schemas que reflejan las restricciones del backend
- Manejo de estados dirty, submitting, errores de campo

### 4. Flujo de navegación

```
/login                    → Auth setup (frontend-setup-and-auth-flow)
/app                      → Protected layout (sidebar + topbar)
/app/products             → Lista de productos
/app/products/new         → Formulario de creación
/app/products/:id         → Detalle de producto (costo, receta vinculada)
/app/products/:id/edit    → Formulario de edición
/app/recipes              → Lista de recetas
/app/recipes/new          → Formulario de creación
/app/recipes/:id          → Detalle de receta (ingredientes, costo)
/app/recipes/:id/edit     → Formulario de edición
```

`/app` es un layout route con el sidebar + topbar. Los hijos renderizan en un `<Outlet />`.

### 5. Estrategia de manejo de errores

- **Errores de red / API**: React Query expone `isError` y `error`. Se muestra un `ErrorState` con botón de reintento (invoca `refetch()`).
- **Errores 401**: El interceptor de Axios redirige al login.
- **Errores de validación (422)**: React Hook Form muestra errores inline debajo de cada campo.
- **Errores de negocio (404, 409)**: Toast de error con mensaje descriptivo.
- **Errores 500**: Toast genérico "Algo salió mal. Intentá de nuevo."

### 6. Patrones de UI

| Estado | Componente | Comportamiento |
|--------|-----------|----------------|
| Loading inicial | `LoadingSkeleton` | Skeleton cards/rows que imitan la forma del contenido |
| Lista vacía | `EmptyState` | Ícono + mensaje + botón CTA ("Crear primer producto") |
| Error | `ErrorState` | Mensaje de error + botón "Reintentar" |
| Éxito (mutación) | `toast.success()` | Notificación efímera con check verde |
| Optimistic update | React Query `onMutate` | UI responde instantáneamente, revierte si falla |

## Risks / Trade-offs

- **[Riesgo] El backend tiene dos apps FastAPI separadas con modelos divergentes** → El frontend asume la API del `main.py` raíz que registra los routers de productos y recetas. Si se migra a `app/main.py`, las rutas podrían cambiar. **Mitigación**: Centralizar todas las URLs de API en constantes (`api/products.ts`), facilitando futuros cambios de base URL.
- **[Riesgo] `frontend-setup-and-auth-flow` no está implementado aún** → El contexto de autenticación (token JWT, interceptor de Axios) no existirá. **Mitigación**: Este diseño asume que `frontend-setup-and-auth-flow` provee: (1) instancia de Axios con interceptor JWT, (2) hook `useAuth()` con `token` y `logout()`, (3) `ProtectedRoute` wrapper. Se documentan estas dependencias explícitamente para que el apply las mockee o las integre.
- **[Trade-off] Zustand + React Query = dos fuentes de verdad** → React Query maneja estado del servidor, Zustand maneja estado UI. No compiten. Se evita duplicar datos del servidor en stores de Zustand.
- **[Trade-off] No SSR/SSG con Next.js** → TomiLomos es una SPA (detrás de login), no necesita SEO. Vite + React Router es más simple y alineado con el perfil "dashboard app".
