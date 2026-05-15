# CHANGE MAP: TomiLomos API

**Versión**: 2.0  
**Última actualización**: 2026-05-14  
**Status**: 13/13 changes completados y archivados ✅

---

## 📊 RESUMEN DE LO IMPLEMENTADO

| # | Change | Capa | Tareas | Estado |
|---|--------|------|--------|--------|
| 1 | `create-project-structure` | Backend | ✅ | ✅ Archivado |
| 2 | `setup-multitenancy-auth` | Backend | ✅ (parcial) | ✅ Archivado |
| 3 | `create-raw-materials-module` | Backend | ✅ | ✅ Archivado |
| 4 | `create-products-module` | Backend | ✅ | ✅ Archivado |
| 5 | `create-recipes-module` | Backend | ✅ | ✅ Archivado |
| 6 | `calculate-product-costs` | Backend | ✅ | ✅ Archivado |
| 7 | `register-sales-with-stock-deduction` | Backend | 8/8 | ✅ Archivado |
| 8 | `frontend-setup-and-auth-flow` | Frontend | 10/10 | ✅ Archivado |
| 9 | `frontend-raw-materials-inventory` | Frontend | 20/20 | ✅ Archivado |
| 10 | `frontend-sales-entry-and-stock-view` | Frontend | 20/20 | ✅ Archivado |
| 11 | `frontend-products-and-recipes` | Frontend | ✅ | ✅ Archivado |
| 12 | `frontend-profitability-dashboard` | Frontend | ✅ | ✅ Archivado |
| 13 | `profitability-reports-by-product` | Frontend | 13/13 | ✅ Archivado |
| **Total** | | | **13 archivados** | |

---

## 🏗️ ARQUITECTURA ACTUAL

```
┌─────────────────────────────────────────────────────────────────┐
│                        TOMILOMOS API                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FRONTEND (React 18 · Vite · Tailwind · Zustand · Recharts)      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  /login              → LoginPage (email + password)      │   │
│  │  /app/dashboard      → Dashboard                         │   │
│  │  /app/raw-materials  → CRUD + stock badges               │   │
│  │  /app/products       → Products CRUD                     │   │
│  │  /app/sales          → Sales entry + history             │   │
│  │  /app/recipes        → Recipes CRUD + ingredients        │   │
│  │  /app/profitability  → Dashboard KPI + chart             │   │
│  │  /app/stock          → Stock Monitor                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                          │                                       │
│                          ▼                                       │
│  BACKEND (FastAPI · SQLAlchemy · PostgreSQL)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  /api/v1/auth/login        → 🔴 STUBBED (501)            │   │
│  │  /api/v1/auth/register     → 🔴 NO EXISTE                │   │
│  │  /api/v1/tenants           → 🟡 EXISTE en app/ NO conectado│   │
│  │  /api/v1/users             → 🟡 EXISTE en app/ NO conectado│   │
│  │  /api/v1/raw-materials     → ✅ CRUD + stock             │   │
│  │  /api/v1/products          → ✅ CRUD + recipe linking    │   │
│  │  /api/v1/recipes           → ✅ CRUD + ingredients       │   │
│  │  /api/v1/recipes/{id}/cost → ✅ Cost calculation         │   │
│  │  /api/v1/sales             → ✅ Create + list            │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ⚠️ PROBLEMA: TODOS los routers usan get_tenant_id_placeholder() │
│     → Siempre retorna 401. Nadie puede usar NINGÚN endpoint.    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Duplicación de estructura detectada

```
app/                          ← Infraestructura de auth (NO conectada)
├── api/
│   ├── auth_router.py        → Login stubbed (501)
│   ├── tenants_router.py     → Tenant CRUD (no registrado en main.py)
│   ├── users_router.py       → User CRUD (no registrado en main.py)
│   └── health_router.py
├── core/
│   ├── security.py           → hash_password, verify_password
│   ├── jwt_handler.py        → create_access_token
│   ├── dependencies.py       → Dependency injection
│   └── exceptions.py
├── services/
│   └── auth_service.py       → AuthService completo
├── repositories/
│   ├── tenant_repository.py
│   └── user_repository.py
├── schemas/
│   ├── auth.py               → LoginRequest, TokenResponse
│   ├── tenant.py
│   └── user.py
└── db/
    ├── models.py             → Tenant, User (duplicado de root)
    ├── session.py
    └── base.py

api/                          ← Routers de negocio (SÍ conectados)
├── raw_materials_router.py   → ✅ Funcional pero tenant_id = placeholder
├── products_router.py        → ✅ Funcional pero tenant_id = placeholder
├── recipes_router.py         → ✅ Funcional pero tenant_id = placeholder
├── product_cost_router.py    → ✅ Funcional pero tenant_id = placeholder
└── sales_router.py           → ✅ Funcional pero tenant_id = placeholder

core/                         ← Configuración (SÍ conectada)
├── config.py                 → ✅ Settings (database_url, jwt_secret, etc.)
├── logging.py                → ✅ Logger
└── exceptions.py             → ✅ APIException
```

---

## 🔴 BLOQUEANTES — El sistema NO anda end-to-end

| # | Qué | Impacto | Ubicación |
|---|-----|---------|-----------|
| 🔴 1 | **Login retorna 501** | Nadie puede loguearse. Frontend no funciona | `app/api/auth_router.py:37` |
| 🔴 2 | **Auth router NO registrado en main.py** | Endpoints de auth no existen en la app | `main.py` |
| 🔴 3 | **get_tenant_id_placeholder() en TODOS los routers** | Todos los endpoints retornan 401 | 5 routers, 34 usos |
| 🔴 4 | **Sin JWT middleware de validación** | No hay forma real de extraer tenant_id del token | No existe |
| 🔴 5 | **Sin endpoint de registro de usuario** | No se pueden crear usuarios nuevos | No existe |

---

## 🟡 IMPORTANTES — El sistema anda pero es frágil

| # | Qué | Impacto |
|---|-----|---------|
| 🟡 1 | **Duplicación de estructura app/ vs root** | Confusión de imports, mantenimiento difícil |
| 🟡 2 | **Sin Alembic migrations** | No hay forma de versionar schema de BD |
| 🟡 3 | **Sin seed data / fixtures** | No se puede probar sin crear datos manualmente |
| 🟡 4 | **openapi.yaml desactualizado** | No refleja endpoints de sales ni cambios recientes |
| 🟡 5 | **Tests sin ejecutar contra auth real** | Los tests de auth usan mocks, no el flujo real |

---

## 🗺️ NUEVOS CHANGES PROPUESTOS (orden sugerido)

### Fase 1: Hacer andar el sistema (CRÍTICO)

| Orden | Change | Qué hace | Dependencias |
|-------|--------|----------|--------------|
| 1 | `implement-real-auth-login` | Des-stubbear login, conectar JWT middleware real, reemplazar get_tenant_id_placeholder en todos los routers | — |
| 2 | `add-user-registration` | Endpoint POST /api/v1/auth/register + tenant creation flow | `implement-real-auth-login` |
| 3 | `consolidate-project-structure` | Unificar app/ y root-level en una sola estructura, eliminar duplicación | `implement-real-auth-login` |

### Fase 2: Datos y robustez

| Orden | Change | Qué hace | Dependencias |
|-------|--------|----------|--------------|
| 4 | `setup-alembic-migrations` | Configurar Alembic con todos los modelos existentes | `consolidate-project-structure` |
| 5 | `seed-data-and-fixtures` | Datos de prueba: tenant, user, productos, recetas, materias primas | `setup-alembic-migrations` |
| 6 | `update-openapi-spec` | Actualizar openapi.yaml con todos los endpoints reales | `implement-real-auth-login` |

### Fase 3: Testing

| Orden | Change | Qué hace | Dependencias |
|-------|--------|----------|--------------|
| 7 | `backend-unit-tests` | Tests de servicios y repositorios con auth real | `implement-real-auth-login` |
| 8 | `backend-integration-tests` | Tests E2E del flujo completo: register → login → CRUD | `seed-data-and-fixtures` |
| 9 | `frontend-component-tests` | Tests de componentes React críticos | — |

### Fase 4: Features nuevas

| Orden | Change | Qué hace | Dependencias |
|-------|--------|----------|--------------|
| 10 | `sales-multi-product` | Ventas con múltiples productos por transacción (SaleItem) | `implement-real-auth-login` |
| 11 | `dashboard-metrics` | Dashboard con métricas reales del día (ventas, stock bajo, etc.) | `sales-multi-product` |
| 12 | `export-reports` | Exportar CSV/PDF de reportes de rentabilidad | `dashboard-metrics` |
| 13 | `recipe-stock-consumption` | Tracking de stock consumido por receta (no solo costo) | `sales-multi-product` |
| 14 | `user-profile-management` | Editar perfil, cambiar password, ver info de tenant | `add-user-registration` |
| 15 | `role-based-access-control` | Roles (admin, cocinero, cajero) con permisos por módulo | `add-user-registration` |

### Fase 5: Producción

| Orden | Change | Qué hace | Dependencias |
|-------|--------|----------|--------------|
| 16 | `docker-production-setup` | Docker Compose para prod con PostgreSQL, Nginx, health checks | Todos los anteriores |
| 17 | `monitoring-and-logging` | Structured logging, metrics, alerting | `docker-production-setup` |

---

## 📁 ARCHIVOS CLAVE

| Archivo | Rol | Estado |
|---------|-----|--------|
| `main.py` | Entry point FastAPI, registra routers | ✅ Conectado pero sin auth |
| `app/api/auth_router.py` | Login endpoint | 🔴 Stubbed (501) |
| `app/services/auth_service.py` | Auth business logic | ✅ Implementado pero no usado |
| `app/core/security.py` | Password hashing | ✅ Existe |
| `app/core/jwt_handler.py` | JWT creation/validation | ✅ Existe |
| `app/core/dependencies.py` | Dependency injection | ✅ Existe |
| `db/models.py` | Modelos SQLAlchemy (8 modelos) | ✅ Completo |
| `api/*_router.py` | Routers de negocio (5 routers) | ⚠️ Con placeholder tenant |
| `services/*_service.py` | Lógica de negocio (4 servicios) | ✅ Implementados |
| `repositories/*_repository.py` | Acceso a BD (4 repos) | ✅ Implementados |
| `schemas/*.py` | Schemas Pydantic (6 módulos) | ✅ Implementados |
| `frontend/src/` | React app | ✅ 7 páginas + auth store |
| `openspec/specs/` | Specs técnicas | ✅ ~30 capabilities |
| `openspec/changes/archive/` | 13 changes completados | ✅ |

---

## 🔑 REGLAS DEL PROYECTO (de AGENTS.md)

- ✅ Clean Architecture: Router → Service → Repository → Model
- ✅ DECIMAL(10,2) para dinero — NUNCA float
- ✅ Multi-tenant: `tenant_id` en cada tabla y query
- ✅ Conventional commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`
- ✅ SDD: specs primero, código después
- ✅ snake_case en backend, camelCase en frontend (pero campos de API en snake_case)
- ✅ Bcrypt cost ≥ 12
- ✅ Atomic transactions para stock deduction
- ✅ Secrets en variables de entorno (.env), NUNCA hardcodeados

---

## 💻 COMANDOS PARA CORRER EN LOCAL

```bash
# 1. Postgres (Docker)
docker compose up -d

# 2. Backend
cp .env.example .env          # Editar DATABASE_URL con credenciales del docker
pip install -r requirements.txt
python main.py                # FastAPI en http://localhost:8000

# 3. Frontend (otra terminal)
cd frontend
npm install
npm run dev                   # Vite en http://localhost:5173
```

---

**Sesión**: 2026-05-14  
**Metodología**: SDD (Spec-Driven Development) con OPSX  
**Versión del mapa**: 2.0 — Actualizado con estado real post-13 changes
