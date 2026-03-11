# Current Architecture

## Overview

La arquitectura implementada sigue un patrón clásico de analítica:

```text
CSV DATA
   ↓
Fabric Lakehouse (Delta Tables)
   ↓
Copy Data Pipeline
   ↓
Warehouse Staging (stg)
   ↓
Core Dimensional Model (core)
   ↓
Analytical Marts (pendiente)
   ↓
BI / Semantic Layer (pendiente)
```

## Componentes

### Lakehouse
Propósito:
- almacenamiento inicial
- ingestión de archivos CSV
- conversión a Delta tables

### Pipeline

Pipeline Copy Data utilizado para:

```text
Lakehouse tables → Warehouse staging tables
```

Modo de ejecución detectado:

```text
Full Copy
```

Riesgo:
- duplicación si se ejecuta varias veces.

### Warehouse

Schemas utilizados:
- stg
- core
- marts (planificado)

### Staging tables
- stg.orders
- stg.customers
- stg.order_items
- stg.order_payments
- stg.order_reviews
- stg.products

Propósito:
- copia directa desde Lakehouse
- sin transformaciones

### Core model

Dimensiones:
- core.dim_date
- core.dim_customers
- core.dim_products
- core.dim_payment_types
- core.dim_order_status

Fact tables:
- core.fact_orders
- core.fact_order_items
- core.fact_order_payments
- core.fact_order_reviews

### QA layer

Script QA consolidado ejecutado para validar:
- row counts
- grain uniqueness
- null keys
- referential integrity

### Data contracts

Grain por tabla:

- dim_date: 1 row per calendar date
- dim_customers: 1 row per customer_id
- dim_products: 1 row per product_id
- fact_orders: 1 row per order_id
- fact_order_items: 1 row per (order_id, order_item_id)
- fact_order_payments: 1 row per (order_id, payment_sequential)
- fact_order_reviews: 1 row per order_id (deduplicated)

## Dependencias

- Lakehouse ingestion
- Pipeline copy
- Warehouse model scripts
- QA script

## Riesgos

1. Pipeline duplicación
2. Falta incremental ingestion
3. Falta control ejecución
4. Falta CI/CD SQL
