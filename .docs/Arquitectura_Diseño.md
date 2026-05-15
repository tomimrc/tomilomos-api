1. Spec-Driven Development (SDD): El Flujo de Trabajo
En SDD, el contrato de la API es la única fuente de verdad. No programamos el backend ni el frontend a ciegas.

Fase 1: Especificación (OpenAPI/Swagger). Primero, definimos los esquemas de datos (insumos, recetas, ventas) y los endpoints en un archivo openapi.yaml.

Fase 2: Generación de Tipos. El frontend (React) consume este archivo para autogenerar interfaces de TypeScript y llamadas a la API.

Fase 3: Implementación (FastAPI). El backend implementa la lógica asegurando que las respuestas cumplan estrictamente con los esquemas Pydantic definidos en el contrato.

2. Arquitectura Backend: Python + FastAPI + PostgreSQL
FastAPI es ideal para este proyecto por su velocidad, soporte nativo para asincronía y su integración perfecta con Pydantic para validar datos.

Patrones de Diseño Backend
Aplicaremos una Arquitectura Limpia (Clean Architecture) o arquitectura multicapa para separar responsabilidades.

Capa de Servicios (Service Layer): Aquí vive la lógica de negocio pura. Por ejemplo, cuando se registra una venta de un "Lomito", el servicio de ventas llama al servicio de inventario para calcular el escandallo (receta) y descontar los gramos exactos de carne, pan y queso. Esto aísla la lógica de las rutas HTTP.

Patrón Repositorio (Repository Pattern): Oculta la lógica de la base de datos (PostgreSQL/SQLAlchemy). El servicio de inventario no ejecuta sentencias SQL directas; llama a InventoryRepository.deduct_stock(). Esto permite cambiar la base de datos o facilitar el testing unitario sin tocar la lógica central.

Inyección de Dependencias: Usaremos el sistema nativo de FastAPI (Depends) para inyectar sesiones de base de datos y repositorios en los servicios, y los servicios en los controladores (routers). Esto garantiza un código modular y fácil de probar.

Multitenancy (Preparación SaaS): Para que puedas vender el sistema a otros colegas mañana, implementaremos un tenant_id (ID de negocio) en todas las tablas principales. Las consultas a la base de datos siempre filtrarán por el tenant_id del usuario autenticado, asegurando aislamiento total de datos.

Estructura de Directorios (Backend)
Plaintext
/backend
├── api/             # Routers de FastAPI (endpoints)
├── core/            # Configuraciones, seguridad (JWT), dependencias
├── db/              # Modelos de SQLAlchemy y migraciones (Alembic)
├── schemas/         # Modelos Pydantic (basados en la especificación SDD)
├── repositories/    # Lógica de acceso a datos (PostgreSQL)
└── services/        # Reglas de negocio (cálculo de mermas, rentabilidad)
3. Arquitectura Frontend: React + Tailwind CSS + Motion
El frontend debe ser rápido, responsivo y proporcionar una experiencia de usuario fluida, ideal para la carga rápida de comandas o insumos.

Patrones de Diseño Frontend
Componentes de Presentación y Contenedores (Container/Presenter Pattern):

Contenedores: Manejan la lógica, el estado y las llamadas a la API (Ej: InventoryPage.tsx).

Presentadores: Componentes "tontos" que solo reciben datos por props y los muestran. Aquí aplicamos Tailwind y Framer Motion (Ej: StockCard.tsx).

Custom Hooks para Lógica de Negocio: Encapsularemos las reglas complejas en hooks. Por ejemplo, useCalculateProfit() recibirá los costos de los insumos y los precios de venta para devolver la rentabilidad neta en tiempo real antes de guardar un producto.

Gestión de Estado de Servidor: Herramientas como TanStack Query (React Query) manejarán el caché y la sincronización con FastAPI. Si actualizas el precio de la carne, todos los componentes que dependan de ese dato se actualizarán automáticamente sin recargar la página.

Estructura y UI/UX
Tailwind CSS: Lo usaremos mediante un sistema de diseño atómico. Crearemos componentes base (Botones, Inputs, Tablas) para mantener la consistencia visual sin escribir CSS tradicional.

Motion (Framer Motion): Aplicaremos animaciones funcionales, no decorativas.

Microinteracciones: Feedback visual al guardar un insumo o registrar una venta.

Transiciones de Layout: Al reordenar listas o filtrar el inventario, los elementos se moverán con fluidez, ayudando al usuario a no perder el contexto visual.

4. Base de Datos: PostgreSQL
Diseñaremos un modelo relacional robusto para asegurar la integridad referencial.

businesses: Datos del negocio (Tomilomos y futuros clientes).

raw_materials: Insumos básicos (carne, pan, aceite) con campos de unit_measure (gr, lt, un), current_stock y cost_per_unit.

products: El ítem final de venta (Lomito Completo, Porción de Papas) con su sale_price.

recipes (Tabla intermedia): Relaciona products con raw_materials. Almacena la quantity_needed de cada insumo para formar el producto.

sales y sale_items: Registro histórico de ventas para trazar ingresos y cruzar datos de rentabilidad.