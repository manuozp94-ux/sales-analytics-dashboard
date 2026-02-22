# SALES ANALYTICS DASHBOARD  
## Dimensional Model — Star Schema Specification

---

## 1. Overview

This document specifies the dimensional model (star/constellation schema) implemented in DuckDB for the Sales Analytics Dashboard project.

All transformations are implemented in SQL scripts under `03-sql/`.  
Python notebooks are used only for orchestration and validation.

This specification is the conceptual source of truth for:

- Table purposes and scope
- Explicit grain per table
- Primary and foreign key contracts
- Relationship cardinalities
- Referential integrity expectations

---

## 2. Dimensional Tables

### 2.1 dim_date

**Purpose:**  
Calendar dimension used to slice all facts consistently by purchase date.

**Grain:**  
1 row per calendar date.

**Primary Key:**  
- date_key (YYYYMMDD integer)

**Attributes (selected):**  
- date
- year, month, day
- month_name, day_name
- is_weekend

**Source:**  
- Derived from `stg_orders.order_purchase_timestamp` min/max bounds.

**Notes:**  
- Date range is continuous between observed min/max purchase dates.

---

### 2.2 dim_customers

**Purpose:**  
Customer dimension used for geographic and customer-level slicing.

**Grain:**  
1 row per customer_id.

**Primary Key:**  
- customer_id

**Attributes (selected):**  
- customer_unique_id
- customer_city
- customer_state
- customer_zip_code_prefix

**Source:**  
- `stg_customers`

**Notes:**  
- `customer_id` can appear multiple times per `customer_unique_id` in the raw dataset.

---

### 2.3 dim_products

**Purpose:**  
Product dimension used for category and product-level slicing.

**Grain:**  
1 row per product_id.

**Primary Key:**  
- product_id

**Attributes (selected):**  
- product_category_name
- product_name_lenght
- product_description_lenght
- product_photos_qty
- product_weight_g
- product_length_cm, product_height_cm, product_width_cm

**Sources:**  
- `stg_products` (catalog attributes)
- `stg_order_items` (backfill for product_id keys not present in catalog)

**Notes:**  
- Missing catalog attributes for backfilled product_id values are stored as NULL.
- This backfill exists to preserve referential integrity for item facts.

---

## 3. Fact Tables

### 3.1 fact_orders

**Purpose:**  
Order-level fact table used as the anchor for order lifecycle, customer linkage, and date slicing.

**Grain:**  
1 row per order_id.

**Primary Key:**  
- order_id

**Foreign Keys:**  
- customer_id → dim_customers.customer_id  
- purchase_date_key → dim_date.date_key

**Measures / Indicators (selected):**  
- order_status
- timestamps across lifecycle (purchase/approved/delivered/etc.)

**Source:**  
- `stg_orders`

---

### 3.2 fact_order_items

**Purpose:**  
Item-level fact table capturing product-level sales and freight at the order line level.

**Grain:**  
1 row per (order_id, order_item_id).

**Primary Key (logical):**  
- (order_id, order_item_id)

**Foreign Keys:**  
- order_id → fact_orders.order_id  
- customer_id → dim_customers.customer_id  
- product_id → dim_products.product_id  
- purchase_date_key → dim_date.date_key

**Measures:**  
- price
- freight_value

**Source:**  
- `stg_order_items` joined to orders/customers/date for conformed keys.

---

### 3.3 fact_order_payments

**Purpose:**  
Payment-level fact table capturing payment methods, installments, and payment values.

**Grain:**  
1 row per (order_id, payment_sequential).

**Primary Key (logical):**  
- (order_id, payment_sequential)

**Foreign Keys:**  
- order_id → fact_orders.order_id  
- customer_id → dim_customers.customer_id  
- purchase_date_key → dim_date.date_key

**Measures / Attributes:**  
- payment_type
- payment_installments
- payment_value

**Source:**  
- `stg_order_payments` joined to orders/customers/date for conformed keys.

---

### 3.4 fact_order_reviews

**Purpose:**  
Review-level fact table capturing customer satisfaction signals linked to orders.

**Grain:**  
1 row per (review_id, order_id).

**Primary Key (logical):**  
- (review_id, order_id)

**Foreign Keys:**  
- order_id → fact_orders.order_id  
- customer_id → dim_customers.customer_id  
- purchase_date_key → dim_date.date_key

**Measures / Attributes:**  
- review_score
- review_comment_title
- review_comment_message
- review_creation_date
- review_answer_timestamp

**Source:**  
- `stg_order_reviews` joined to orders/customers/date for conformed keys.

**Notes:**  
- review_id is not globally unique in the dataset; uniqueness is enforced at (review_id, order_id).

---

## 4. Relationships & Cardinality

- dim_date (1) → (N) fact_orders  
- dim_customers (1) → (N) fact_orders  
- fact_orders (1) → (N) fact_order_items  
- fact_orders (1) → (N) fact_order_payments  
- fact_orders (1) → (N) fact_order_reviews  
- dim_products (1) → (N) fact_order_items  

---

## 5. Referential Integrity Policy

The model targets full referential integrity across conformed keys:

- All fact foreign keys must match dimension keys (no orphans).
- Where raw datasets contain keys missing from dimension catalogs (e.g., products),
  the dimension is extended (backfilled keys) rather than filtering facts.

Validation checks for grain, null keys, and orphan keys are executed in the DuckDB materialization notebook.