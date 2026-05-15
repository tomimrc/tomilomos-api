## Context

El backend tiene toda la infraestructura de auth lista (JWT HS256, bcrypt cost 12, AuthService, dependencias FastAPI) pero el endpoint `POST /api/v1/auth/login` está stubbed (retorna 501). El frontend ya tiene: `authStore` (Zustand + localStorage con token/tenantId/userId), `ProtectedRoute` (gate), `apiClient` con interceptor JWT + auto-logout en 401, y un `LoginPage` placeholder en `App.tsx`. Este cambio reemplaza el placeholder por una página de login completa y conecta el flujo de autenticación.

**Stack**: React 18 · React Router 6 · Zustand · TanStack Query · React Hook Form + Zod · Framer Motion · Axios · Tailwind CSS

## Goals / Non-Goals

**Goals:**
- Página de login con formulario de email + password y validación inline
- Llamada a `POST /api/v1/auth/login` usando una instancia de axios sin interceptores (evitar redirect loop en 401)
- Decodificación del JWT en el cliente para extraer `tenant_id` y `sub` (user_id)
- Almacenamiento en `authStore` vía `setAuth(token, tenantId, userId)`
- Redirección a `/app/dashboard` post-login exitoso
- Manejo de errores: credenciales inválidas (401), error de servidor (500), error de red
- Diseño visual con branding TomiLomos (logo, nombre, fondo)
- Animación Framer Motion en la página

**Non-Goals:**
- Registro de usuarios (el backend tiene `POST /api/v1/users` pero no es parte de este cambio)
- Recuperación de contraseña
- Multi-tenant selector en el login (MVP: login simple email/password; tenant context se resuelve en backend)
- Fix del backend stubbed (se asume que se des-stubeará; el frontend está listo para consumirlo)
- Remember me / refresh tokens
- OAuth / SSO

## Decisions

### 1. Axios sin interceptores para login

El `apiClient` existente tiene un interceptor de respuesta que hace `window.location.href = '/login'` en 401. Si usamos `apiClient` para el login y el backend retorna 401, entramos en redirect loop. **Decisión**: Crear una instancia `authApi` con solo `baseURL: '/api/v1'` (sin interceptores) para el endpoint de login.

```ts
// api/auth.ts
import axios from 'axios';

const authApi = axios.create({ baseURL: '/api/v1' });

export async function login(email: string, password: string): Promise<TokenResponse> {
  const { data } = await authApi.post<TokenResponse>('/auth/login', { email, password });
  return data;
}
```

### 2. Decodificación JWT en el cliente

El `TokenResponse` del backend solo contiene `access_token`, `token_type` y `expires_in`. No incluye `tenant_id` ni `user_id` explícitamente. Para extraerlos, decodificamos el payload del JWT en el cliente:

```ts
function decodeJWT(token: string): { sub: string; tenant_id: string } {
  const payload = token.split('.')[1];           // middle part = payload
  const decoded = JSON.parse(atob(payload));       // base64 decode
  return { sub: decoded.sub, tenant_id: decoded.tenant_id };
}
```

**Razón**: No se requiere verificación criptográfica en el cliente — el backend ya verificó el token al generarlo. El cliente solo necesita leer los claims. Esto evita un segundo round-trip al backend.

### 3. Flujo completo

```
┌─────────────────────────────────────────────────────────────┐
│                     LOGIN FLOW                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  LoginPage                                                  │
│    │                                                        │
│    │  Email + Password form (React Hook Form + Zod)         │
│    │  Submit →                                              │
│    ▼                                                        │
│  POST /api/v1/auth/login { email, password }                │
│    │                                                        │
│    ├── 200: { access_token, token_type, expires_in }        │
│    │     │                                                  │
│    │     ▼                                                  │
│    │   Decode JWT payload → { sub, tenant_id }              │
│    │     │                                                  │
│    │     ▼                                                  │
│    │   authStore.setAuth(token, tenant_id, user_id)         │
│    │     │                                                  │
│    │     ▼                                                  │
│    │   navigate('/app/dashboard')                           │
│    │                                                        │
│    ├── 401: Show "Invalid email or password"                │
│    ├── 500: Show "Server error. Please try again."          │
│    └── Network: Show "Connection failed. Check your network."│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. Componentes

```
features/auth/
└── pages/
    └── LoginPage.tsx    ← Componente único con form + lógica + diseño
```

**Decisión**: Login es un solo componente (no se divide en subcomponentes) porque es una página simple con un formulario. Si en el futuro se agregan flujos (register, forgot-password), se refactoriza.

### 5. Diseño visual

- Layout centrado vertical y horizontalmente (full screen, flex/grid center)
- Card con fondo blanco, sombra, bordes redondeados
- Logo TomiLomos (ChefHat icon de Lucide + texto "TomiLomos")
- Campos: Email (input type="email") + Password (input type="password")
- Botón "Sign In" full-width con loading spinner
- Mensaje de error inline debajo del botón (rojo, animado)
- Background con gradiente sutil (gray-50 a white) o patrón

### 6. Validación del formulario

Zod schema:
```ts
const loginSchema = z.object({
  email: z.string().min(1, 'Email is required').email('Invalid email format'),
  password: z.string().min(1, 'Password is required'),
});
```

## Risks / Trade-offs

- **[Riesgo] Backend login devuelve 501** → El frontend no se puede testear end-to-end hasta que se des-stubee. **Mitigación**: La UI es funcional y los estados de error están cubiertos. Se puede simular la respuesta con MSW en tests futuros.
- **[Trade-off] Decodificación JWT sin librería** → `atob()` + `JSON.parse()` es simple pero no valida firma. **Mitigación**: La validación es responsabilidad del backend. El cliente solo lee claims no sensibles. Si se necesita verificación client-side en el futuro, usar `jose` o `jwt-decode`.
- **[Trade-off] Sin tenant selector en login** → Si un usuario está en múltiples tenants, no puede elegir. **Mitigación**: MVP asume un tenant por usuario. Futuro: agregar tenant selector o subdominios.
- **[Riesgo] localStorage de JWT** → XSS podría robar el token. **Mitigación**: Es el patrón estándar para SPAs. En producción, considerar httpOnly cookies con refresh token rotation. El authStore ya existe con este patrón y no se va a cambiar en este cambio.

## Open Questions

1. ¿El backend va a des-stubbear el login antes o después de este cambio? Afecta el orden de implementación y testing.
2. ¿El backend agregará `tenant_id` al `LoginRequest` o lo inferirá de otro lado? Si se agrega al request body, hay que agregar el campo al formulario.
