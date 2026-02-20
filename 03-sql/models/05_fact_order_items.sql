-- ==============================================================
-- Model: fact_order_items
-- Grain: 1 row per (order_id, order_item_id)
-- Sources:
--   stg_order_items
--   stg_orders (customer_id + purchase_date_key)
-- ==============================================================

create or replace table fact_order_items as

select
    oi.order_id,
    oi.order_item_id,

    o.customer_id,
    oi.product_id,
    oi.seller_id,

    -- Date key derived from purchase timestamp
    cast(strftime(date(o.order_purchase_timestamp), '%Y%m%d') as integer) as date_key,

    -- Measures
    oi.price,
    oi.freight_value

from stg_order_items oi
join stg_orders o
    on o.order_id = oi.order_id;