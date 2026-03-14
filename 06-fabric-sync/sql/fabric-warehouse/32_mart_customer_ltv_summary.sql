-- mart.mart_customer_ltv_summary

create or alter view mart.mart_customer_ltv_summary as
with order_revenue as (
    select
        order_id,
        sum(price + freight_value) as revenue,
        count(*) as items
    from core.fact_order_items
    group by order_id
),
orders_enriched as (
    select
        o.order_id,
        o.customer_id,
        o.order_status,
        o.order_purchase_timestamp,
        datefromparts(year(o.order_purchase_timestamp), month(o.order_purchase_timestamp), 1) as purchase_month,
        isnull(r.revenue, 0) as revenue,
        isnull(r.items, 0) as items
    from core.fact_orders o
    left join order_revenue r
      on r.order_id = o.order_id
    where o.order_status <> 'canceled'
      and o.order_purchase_timestamp is not null
)
select
    customer_id,
    min(order_purchase_timestamp) as first_purchase_ts,
    max(order_purchase_timestamp) as last_purchase_ts,
    datediff(day, min(order_purchase_timestamp), max(order_purchase_timestamp)) as lifetime_days,
    count(distinct order_id) as total_orders,
    sum(items) as total_items,
    sum(revenue) as total_revenue,
    cast(sum(revenue) as float) / nullif(count(distinct order_id), 0) as avg_order_value,
    count(distinct purchase_month) as active_months
from orders_enriched
group by customer_id;
