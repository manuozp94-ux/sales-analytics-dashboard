-- ==============================================================
-- Model: fact_order_payments
-- Grain: 1 row per (order_id, payment_sequential)
-- Sources:
--   stg_order_payments
--   stg_orders (customer_id + purchase_date_key)
-- ==============================================================

create or replace table fact_order_payments as

select
    p.order_id,
    p.payment_sequential,

    o.customer_id,
    cast(strftime(date(o.order_purchase_timestamp), '%Y%m%d') as integer) as purchase_date_key,

    p.payment_type,
    p.payment_installments,
    p.payment_value
from stg_order_payments p
join stg_orders o
    on o.order_id = p.order_id;