# Current Architecture

Layer 1 — Raw CSV
orders
customers
order_items
order_payments
order_reviews
products

Layer 2 — Staging
stg_orders
stg_customers
stg_order_items
stg_order_payments
stg_order_reviews
stg_products

Layer 3 — Models
dim_date
dim_customers
dim_products
fact_order_items

Flow:

CSV -> pandas validation -> DuckDB staging -> SQL star schema
