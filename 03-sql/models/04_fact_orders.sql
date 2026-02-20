-- ==============================================================
-- Model: fact_orders
-- Grain: 1 row per order_id
-- Source: stg_orders
-- ==============================================================

create or replace table fact_orders as

select
    o.order_id,
    o.customer_id,
    cast(strftime(date(o.order_purchase_timestamp), '%Y%m%d') as integer) as purchase_date_key,

    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    o.month_year
from stg_orders o;