-- ==============================================================
-- Model: dim_customers
-- Grain: 1 row per customer_id
-- Source: stg_customers
-- ==============================================================

create or replace table dim_customers as

select
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
from stg_customers;