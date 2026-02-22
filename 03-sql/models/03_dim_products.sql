-- ==============================================================
-- Model: dim_products
-- Grain: 1 row per product_id
-- Sources:
--   stg_products (product catalog)
--   stg_order_items (to backfill missing product_id keys)
-- Strategy:
--   Build the dimension as:
--     1) Base catalog rows from stg_products
--     2) PLUS "missing" product_id values observed in order items but absent from catalog
-- Notes:
--   This is a conformed keyset completion step to ensure referential integrity.
-- ==============================================================

create or replace table dim_products as

with base as (
    select
        product_id,
        product_category_name,
        product_name_lenght,
        product_description_lenght,
        product_photos_qty,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm
    from stg_products
),

missing_keys as (
    select distinct
        oi.product_id
    from stg_order_items oi
    left join stg_products p
        on p.product_id = oi.product_id
    where p.product_id is null
),

missing_rows as (
    select
        mk.product_id,

        -- backfill attributes as NULL when catalog data is missing
        null as product_category_name,
        null as product_name_lenght,
        null as product_description_lenght,
        null as product_photos_qty,
        null as product_weight_g,
        null as product_length_cm,
        null as product_height_cm,
        null as product_width_cm
    from missing_keys mk
)

select * from base
union all
select * from missing_rows;