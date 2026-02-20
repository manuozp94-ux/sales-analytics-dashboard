-- ==============================================================
-- Model: dim_products
-- Grain: 1 row per product_id
-- Source: stg_products
-- ==============================================================

create or replace table dim_products as
select
    *
from stg_products;