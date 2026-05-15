# 🎯 RESUMEN: Mapa de Changes TomiLomos API

**Fecha**: 2026-05-14  
**Status**: ✅ 13 CHANGES COMPLETADOS Y ARCHIVADOS  
**Versión del mapa**: 2.0

---

## ✅ COMPLETADO (13 changes archivados)

### Phase 1: Infraestructura
1. `create-project-structure` — Estructura del proyecto, FastAPI base, pytest setup
2. `setup-multitenancy-auth` — Modelos Tenant/User, JWT, bcrypt, schemas auth

### Phase 2: Core Business
3. `create-raw-materials-module` — CRUD materias primas + stock management
4. `create-products-module` — CRUD productos con recipe linking
5. `create-recipes-module` — CRUD recetas + ingredientes + cost calculation
6. `calculate-product-costs` — Costo automático basado en precios de materias primas

### Phase 3: Operación
7. `register-sales-with-stock-deduction` — Modelo Sale, deducción atómica de stock

### Phase 4: Frontend
8. `frontend-setup-and-auth-flow` — Login page, JWT decode, auth store
9. `frontend-raw-materials-inventory` — CRUD materias primas + stock badges
10. `frontend-sales-entry-and-stock-view` — Registro de ventas + historial + stock dashboard
11. `frontend-products-and-recipes` — CRUD productos y recetas en frontend
12. `frontend-profitability-dashboard` — Dashboard de rentabilidad
13. `profitability-reports-by-product` — Tabla filtrable + gráfico Recharts

---

## 🔴 PROBLEMA CRÍTICO: El sistema NO anda end-to-end

```
┌──────────────────────────────────────────────────────────────┐
│                    CADENA DE ROTURA                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend Login  →  POST /api/v1/auth/login  →  501 ❌      │
│                                                              │
│  Cualquier CRUD  →  get_tenant_id_placeholder()  →  401 ❌  │
│                                                              │
│  app/ (auth)     →  NO conectado a main.py     →  invisible  │
│                                                              │
│  Resultado: NADIE puede usar NINGÚN endpoint                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Duplicación de estructura

```
app/                    ← Auth infrastructure (NO conectada)
├── api/auth_router.py  → Login stubbed (501)
├── api/tenants_router.py → No registrado
├── api/users_router.py   → No registrado
├── core/security.py      → hash/verify password ✅
├── core/jwt_handler.py   → create/validate token ✅
├── core/dependencies.py  → DI pattern ✅
├── services/auth_service.py → AuthService completo ✅
└── repositories/          → tenant + user repos ✅

api/                    ← Business routers (SÍ conectados)
├── raw_materials_router.py  → ⚠️ tenant_id = placeholder
├── products_router.py       → ⚠️ tenant_id = placeholder
├── recipes_router.py        → ⚠️ tenant_id = placeholder
├── product_cost_router.py   → ⚠️ tenant_id = placeholder
└── sales_router.py          → ⚠️ tenant_id = placeholder
```

---

## 📊 ESTADÍSTICAS

| Métrica | Valor |
|---------|-------|
| **Total Changes Archivados** | 13 |
| **Changes Propuestos Nuevos** | 17 |
| **Modelos SQLAlchemy** | 8 (Tenant, User, RawMaterial, Product, Recipe, RecipeIngredient, Sale) |
| **Endpoints Backend** | ~30 (5 módulos CRUD + auth stubbed) |
| **Páginas Frontend** | 7 |
| **Archivos de Test** | 13 |

---

## 🗺️ PRÓXIMOS CHANGES (orden de prioridad)

```
FASE 1: HACER ANDAR (CRÍTICO)
══════════════════════════════
  1. implement-real-auth-login    ← Des-stubbear login + JWT middleware
  2. add-user-registration        ← Register endpoint + tenant creation
  3. consolidate-project-structure← Unificar app/ y root-level

FASE 2: DATOS Y ROBUSTEZ
══════════════════════════════
  4. setup-alembic-migrations     ← Versionar schema de BD
  5. seed-data-and-fixtures       ← Datos de prueba
  6. update-openapi-spec          ← Actualizar contrato API

FASE 3: TESTING
══════════════════════════════
  7. backend-unit-tests           ← Tests con auth real
  8. backend-integration-tests    ← E2E completo
  9. frontend-component-tests     ← Tests React

FASE 4: FEATURES NUEVAS
══════════════════════════════
 10. sales-multi-product          ← Múltiples productos por venta
 11. dashboard-metrics            ← Métricas del día
 12. export-reports               ← CSV/PDF exports
 13. recipe-stock-consumption     ← Tracking consumo stock
 14. user-profile-management      ← Editar perfil, cambiar password
 15. role-based-access-control    ← Roles y permisos

FASE 5: PRODUCCIÓN
══════════════════════════════
 16. docker-production-setup      ← Docker Compose prod
 17. monitoring-and-logging       ← Metrics, alerting
```

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
