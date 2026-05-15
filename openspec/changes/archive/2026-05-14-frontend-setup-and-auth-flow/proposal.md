## Why

El sistema no tiene una página de login funcional — solo un placeholder que dice "coming in auth setup". Sin login, ningún usuario puede acceder a las features ya construidas (raw materials, products, sales, stock). El backend ya tiene toda la infraestructura de auth (JWT, bcrypt, AuthService), pero el endpoint `/api/v1/auth/login` está stubbed (501) y necesita reactivarse. Este cambio construye la UI completa de login, conecta el flujo de autenticación frontend→backend, y reemplaza el placeholder.

## What Changes

- Reemplazar el `LoginPage` placeholder por una página de login completa con formulario de email + password
- Validación inline de email (formato) y password (no vacío)
- Llamada a `POST /api/v1/auth/login` con manejo de estados: loading, error (401/429/500), success
- Decodificación del JWT en el cliente para extraer `tenant_id` y `sub` (user_id) del payload
- Almacenamiento del token + tenant_id + user_id en `authStore` (Zustand + localStorage)
- Redirección post-login a `/app/dashboard`
- Manejo de sesión expirada: el 401 interceptor ya existe, se integra con el flujo
- Diseño visual de la página de login con branding TomiLomos (logo, nombre)
- Framer Motion para transiciones y feedback visual

## Capabilities

### New Capabilities
- `frontend-login-form`: Página de login con formulario de email/password, validación Zod, llamada a la API de auth, y manejo de estados (loading, error, success). Incluye diseño con branding TomiLomos.

### Modified Capabilities
<!-- Ninguna — reemplaza un placeholder, no modifica specs existentes -->

## Impact

- **Archivo reemplazado**: `LoginPage` inline en `App.tsx` → extraído a `features/auth/pages/LoginPage.tsx`
- **Nuevos archivos**: `features/auth/` con página de login, `types/auth.ts` con tipos de autenticación, `api/auth.ts` con función `login()`
- **API consumida**: `POST /api/v1/auth/login` (requiere que el backend lo des-stubee — actualmente retorna 501)
- **Store utilizado**: `authStore` ya existe con `setAuth(token, tenantId, userId)` y `logout()`
- **Interceptor existente**: `apiClient.ts` ya maneja 401 → logout + redirect. El login usa axios sin interceptor para evitar redirect loops.
- **Modifica `App.tsx`**: importa LoginPage del feature en vez de tenerla inline
- **Sin cambios en backend**
