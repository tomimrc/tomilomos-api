# Reglas del Proyecto Tomilomos (SaaS de Gestión Gastronómica)

Este documento es la fuente de verdad para cualquier agente de Inteligencia Artificial que trabaje en este repositorio. Define los estándares técnicos, flujos de trabajo y comportamientos esperados para garantizar un código modular, escalable y profesional.

## Perfil y Skills del Agente
El agente debe actuar con los siguientes superpoderes activos:
- **frontend-design**: Creación de interfaces en React con Tailwind CSS y animaciones fluidas usando Framer Motion.
- **fastapi-templates**: Implementación de arquitecturas robustas en FastAPI siguiendo Clean Architecture.
- **code-review-excellence**: Revisión estricta de código buscando optimización, legibilidad y cumplimiento de specs.
- **sdd-orchestrator**: Maestría en Spec-Driven Development (Desarrollo Impulsado por Especificaciones).
- **gastronomic-logic**: Entendimiento profundo de inventarios, (recetas) y rentabilidad.

## Arquitectura Spec-Driven (SDD)
- **SIEMPRE** leer las especificaciones en la carpeta `openspec/` antes de escribir cualquier línea de código.
- El contrato de la Interfaz de Programación de Aplicaciones (Application Programming Interface - API) es la única fuente de verdad.
- Cualquier cambio en la lógica de datos debe reflejarse primero en el archivo `openapi.yaml`.

## Flujo del Backend (Python + FastAPI)
- **Flujo ÚNICO de Datos**: Router → Service → Repository → Model.
- **Router**: Solo manejo de rutas y validación de entrada/salida (Schemas Pydantic). NUNCA poner lógica de negocio aquí.
- **Service**: Contiene la lógica de negocio pura (ej. cálculo de descuento de stock por receta).
- **Repository**: Manejo exclusivo de consultas a la base de datos PostgreSQL.
- **Persistencia**: NUNCA ejecutar `session.commit()` dentro de un Service. El manejo de transacciones debe ser controlado por el orquestador o la capa de persistencia.

## Estado y Frontend (React)

- **Animaciones**: Usar Framer Motion para feedback visual en acciones críticas (guardado, eliminación, alertas).

## Integridad de Datos y Seguridad
- **Moneda y Precios**: Usar SIEMPRE tipos de datos DECIMAL(10,2) o equivalentes. NUNCA usar floats para dinero.
- **Stock**: Todas las operaciones de resta de inventario deben ser atómicas para evitar inconsistencias.
- **Secrets**: SIEMPRE usar variables de entorno (.env). NUNCA dejar claves o rutas hardcodeadas.
- **Contraseñas**: Usar bcrypt con un factor de costo (cost) ≥ 12.

## Estilo de Código y Commits
- **Conventional Commits**: Los mensajes de commit deben seguir el formato `feat:`, `fix:`, `refactor:`, `test:`, `docs:`.
- **Atomicidad**: Un commit debe representar un único cambio lógico. Evitar commits masivos con cambios mezclados.
- **Naming**: Variables y funciones en inglés, claras y descriptivas. Evitar abreviaciones confusas.

## Escalabilidad SaaS
- El sistema está siendo diseñado para ser modular. 
- Cada tabla principal debe contemplar la arquitectura de múltiples inquilinos (Multi-tenancy) mediante un identificador de negocio o usuario para permitir que otros colegas usen el sistema en el futuro.
