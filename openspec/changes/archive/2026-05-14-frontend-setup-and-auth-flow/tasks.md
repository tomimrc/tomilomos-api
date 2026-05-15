## 1. Setup

- [x] 1.1 Create `src/features/auth/pages/` directory structure
- [x] 1.2 Create `src/types/auth.ts` — LoginRequest (email, password), TokenResponse (access_token, token_type, expires_in) interfaces
- [x] 1.3 Create `src/api/auth.ts` — login function using a dedicated axios instance (no interceptors to avoid redirect loop). POST /auth/login with email + password.

## 2. Login Page

- [x] 2.1 Create `src/features/auth/pages/LoginPage.tsx` — Full login page component with:
  - React Hook Form + Zod validation (email required + format, password required)
  - TomiLomos branding: ChefHat icon + "TomiLomos" title
  - Email input (type="email") + Password input (type="password")
  - "Sign In" button with loading spinner state
  - Error message display: invalid credentials (401), server error (500), network error
  - JWT decoding on success: extract sub (user_id) and tenant_id from token payload using atob + JSON.parse
  - Call authStore.setAuth(token, tenantId, userId) on success
  - Navigate to /app/dashboard on success
  - Already-authenticated redirect: if token exists in authStore, redirect to /app/dashboard
  - Framer Motion page entrance animation
  - Full-screen centered layout with gradient background

## 3. Integration

- [x] 3.1 Update `App.tsx` — replace inline LoginPage placeholder with import from `@/features/auth/pages/LoginPage`
- [x] 3.2 Ensure ProtectedRoute redirects unauthenticated users to /login (already works, verify)

## 4. Polish

- [x] 4.1 Add Framer Motion error message animation (fade + slide down)
- [x] 4.2 Add hover and focus states to inputs and button
- [x] 4.3 Add keyboard support (Enter key submits form)
- [x] 4.4 Ensure responsive design (card max-width, padding on mobile)
