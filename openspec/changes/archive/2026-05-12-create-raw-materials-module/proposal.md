## Why

The TomiLomos system needs a foundational raw materials (ingredients) management module. This is the core inventory layer that enables recipe creation, production costing, and stock tracking. Without raw materials, the system cannot calculate product costs, manage inventory deductions during sales, or track food waste. This module is a critical prerequisite for profitability reporting and recipe management.

## What Changes

- New database model and repository layer for raw materials (ingredients)
- API endpoints to create, read, update, and manage raw materials
- Schema validation for ingredient properties (name, unit of measurement, cost per unit, supplier)
- Multi-tenant isolation: each tenant has its own raw materials inventory
- Stock tracking capabilities for inventory management
- Support for units of measurement (kg, L, units, etc.)

## Capabilities

### New Capabilities
- `raw-materials-crud`: Create, read, update, and delete raw materials (ingredients) with full lifecycle management
- `raw-materials-stock-tracking`: Track and manage raw material inventory quantities, including stock levels and unit measurements
- `raw-materials-costing`: Store cost-per-unit information for raw materials to enable recipe and product cost calculations

### Modified Capabilities
<!-- No existing capabilities are modified; this is a foundational module -->

## Impact

**Code affected:**
- `db/models.py`: New RawMaterial ORM model
- `schemas/`: New Pydantic schemas for raw material requests/responses
- `repositories/`: New raw_materials_repository.py
- `services/`: New raw_materials_service.py
- `api/`: New raw_materials_router.py

**APIs created:**
- `POST /api/v1/raw-materials` - Create a new raw material
- `GET /api/v1/raw-materials` - List all raw materials for a tenant
- `GET /api/v1/raw-materials/{id}` - Get a specific raw material
- `PUT /api/v1/raw-materials/{id}` - Update a raw material
- `DELETE /api/v1/raw-materials/{id}` - Delete a raw material

**Data model:**
- Raw material records per tenant with fields for name, unit of measurement, cost per unit, and supplier information

**Dependencies:**
- Requires existing multi-tenant isolation system (Tenant model)
- Requires user authentication (User model)
