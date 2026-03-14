-- core.fact_order_items

if object_id('core.fact_order_items', 'U') is not null
begin
    drop table core.fact_order_items;
end;

select
    oi.order_id,
    oi.order_item_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,
    case
        when try_cast(o.order_purchase_timestamp as datetime2(6)) is not null
        then cast(
            convert(char(8), cast(try_cast(o.order_purchase_timestamp as datetime2(6)) as date), 112)
            as int
        )
    end as date_key,
    try_cast(oi.price as float) as price,
    try_cast(oi.freight_value as float) as freight_value,
    isnull(try_cast(oi.price as float), 0.0) + isnull(try_cast(oi.freight_value as float), 0.0) as item_revenue
into core.fact_order_items
from stg.stg_order_items oi
join stg.stg_orders o
  on o.order_id = oi.order_id;
