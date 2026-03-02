-- ==============================================================
-- Mart: mart_monthly_business_snapshot
-- Purpose: Monthly operational + revenue snapshot
-- Sources: fact_orders, fact_order_items
-- Grain: 1 row per purchase_month
-- ==============================================================

create or replace view mart_monthly_business_snapshot as

with order_revenue as (
    select
        order_id,
        sum(price + freight_value) as revenue
    from fact_order_items
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
        date_trunc('month', o.order_purchase_timestamp) as purchase_month,
        coalesce(r.revenue, 0) as revenue
    from fact_orders o
    left join order_revenue r
      on r.order_id = o.order_id
    where o.order_status <> 'canceled'
)

select
    purchase_month,

    -- Volume
    count(distinct order_id) as orders,
    count(distinct customer_id) as customers,

    -- Revenue
    sum(revenue) as revenue,
    sum(revenue)::double / nullif(count(distinct order_id), 0) as aov,

    -- Delivery (only meaningful for delivered orders)
    count(*) filter (where order_status = 'delivered') as delivered_orders,

    -- On-time delivery rate (denominator: delivered orders only)
    (
      count(*) filter (
        where order_status = 'delivered'
          and order_delivered_customer_date is not null
          and order_estimated_delivery_date is not null
          and date(order_delivered_customer_date) <= order_estimated_delivery_date
      )::double
      / nullif(count(*) filter (where order_status = 'delivered'), 0)
    ) as on_time_delivery_rate,

    -- Avg delivery days (delivered only)
    avg(
      datediff('day', order_purchase_timestamp, order_delivered_customer_date)
    ) filter (
      where order_status = 'delivered'
        and order_delivered_customer_date is not null
    ) as avg_delivery_days

from orders_enriched
group by purchase_month
order by purchase_month;