-- mart.mart_monthly_business_snapshot

create or alter view mart.mart_monthly_business_snapshot as
with order_revenue as (
    select
        order_id,
        sum(price + freight_value) as revenue
    from core.fact_order_items
    group by order_id
),
orders_enriched as (
    select
        o.order_id,
        o.customer_id,
        o.order_status,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date,
        datefromparts(year(o.order_purchase_timestamp), month(o.order_purchase_timestamp), 1) as purchase_month,
        isnull(r.revenue, 0) as revenue
    from core.fact_orders o
    left join order_revenue r
      on r.order_id = o.order_id
    where o.order_status <> 'canceled'
      and o.order_purchase_timestamp is not null
)
select
    purchase_month,
    count(distinct order_id) as orders,
    count(distinct customer_id) as customers,
    sum(revenue) as revenue,
    cast(sum(revenue) as float) / nullif(count(distinct order_id), 0) as aov,
    sum(case when order_status = 'delivered' then 1 else 0 end) as delivered_orders,
    cast(sum(
        case
            when order_status = 'delivered'
             and order_delivered_customer_date is not null
             and order_estimated_delivery_date is not null
             and cast(order_delivered_customer_date as date) <= cast(order_estimated_delivery_date as date)
            then 1 else 0
        end
    ) as float)
    / nullif(sum(case when order_status = 'delivered' then 1 else 0 end), 0) as on_time_delivery_rate,
    avg(cast(
        case
            when order_status = 'delivered'
             and order_delivered_customer_date is not null
            then datediff(day, order_purchase_timestamp, order_delivered_customer_date)
        end
    as float)) as avg_delivery_days
from orders_enriched
group by purchase_month;
