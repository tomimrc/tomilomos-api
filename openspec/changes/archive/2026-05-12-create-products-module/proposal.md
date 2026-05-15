## Why

The TomiLomos system requires a products module to define what the business sells. Products are the output entities that customers purchase, each with a sale price. This module is a critical step in the business logic flow: raw materials are inputs (ingredients), products are outputs (sellable items). Without products, the system cannot register sales, calculate profitability, or create recipes. Products are a prerequisite for all revenue-focused operations.

## What Changes

- New database model and repository layer for products (final sellable items)
- API endpoints to create, read, update, and manage products
- Schema validation for product properties (name, sale price, active status)
- Multi-tenant isolation: each tenant has its own product catalog
- Product lifecycle management via is_active flag
- Support for price tracking with DECIMAL(10,2) precision to avoid floating-point errors

## Capabilities

### New Capabilities
- `products-crud`: Create, read, update, and delete products (sellable items) with full lifecycle management
- `product-pricing`: Store and manage sale prices with DECIMAL precision for accurate revenue calculations

### Modified Capabilities
<!-- No existing capabilities are modified; this is a foundational module -->

## Impact

**Code affected:**
- `db/models.py`: New Product ORM model
- `schemas/`: New Pydantic schemas for product requests/responses
- `repositories/`: New products_repository.py
- `services/`: New products_service.py
- `api/`: New products_router.py

**APIs created:**
- `POST /api/v1/products` - Create a new product
- `GET /api/v1/products` - List all products for a tenant
- `GET /api/v1/products/{id}` - Get a specific product
- `PUT /api/v1/products/{id}` - Update a product
- `DELETE /api/v1/products/{id}` - Delete a product

**Data model:**
- Product records per tenant with fields for name, sale price, and active status

**Dependencies:**
- Requires existing multi-tenant isolation system (Tenant model)
- Requires user authentication (User model)
- Prerequisite for: recipes-module (which will link products to raw materials)
