-- core.fact_order_payments

if object_id('core.fact_order_payments', 'U') is not null
begin
    drop table core.fact_order_payments;
end;

select
    p.order_id,
    p.payment_sequential,
    o.customer_id,
    case
        when try_cast(o.order_purchase_timestamp as datetime2(6)) is not null
        then cast(
            convert(char(8), cast(try_cast(o.order_purchase_timestamp as datetime2(6)) as date), 112)
            as int
        )
    end as purchase_date_key,
    p.payment_type,
    try_cast(p.payment_installments as int) as payment_installments,
    try_cast(p.payment_value as float) as payment_value
into core.fact_order_payments
from stg.stg_order_payments p
join stg.stg_orders o
  on o.order_id = p.order_id;
