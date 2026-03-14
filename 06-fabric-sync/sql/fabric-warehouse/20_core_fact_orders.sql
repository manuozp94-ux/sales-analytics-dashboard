-- core.fact_orders

if object_id('core.fact_orders', 'U') is not null
begin
    drop table core.fact_orders;
end;

select
    o.order_id,
    o.customer_id,
    case
        when try_cast(o.order_purchase_timestamp as datetime2(6)) is not null
        then cast(
            convert(char(8), cast(try_cast(o.order_purchase_timestamp as datetime2(6)) as date), 112)
            as int
        )
    end as purchase_date_key,
    o.order_status,
    try_cast(o.order_purchase_timestamp as datetime2(6)) as order_purchase_timestamp,
    try_cast(o.order_approved_at as datetime2(6)) as order_approved_at,
    try_cast(o.order_delivered_carrier_date as datetime2(6)) as order_delivered_carrier_date,
    try_cast(o.order_delivered_customer_date as datetime2(6)) as order_delivered_customer_date,
    try_cast(o.order_estimated_delivery_date as datetime2(6)) as order_estimated_delivery_date
into core.fact_orders
from stg.stg_orders o;
