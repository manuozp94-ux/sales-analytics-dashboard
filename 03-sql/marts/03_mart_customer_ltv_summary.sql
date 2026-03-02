-- ==============================================================
-- Mart: mart_customer_ltv_summary
-- Purpose: Customer-level LTV (observed) + basic lifecycle stats
-- Sources: fact_orders, fact_order_items
-- Grain: 1 row per customer_id
-- ==============================================================

create or replace view mart_customer_ltv_summary as

with order_revenue as (
    select
        order_id,
        sum(price + freight_value) as revenue,
        count(*) as items
    from fact_order_items
    group by order_id
),

orders_enriched as (
    select
        o.order_id,
        o.customer_id,
        o.order_status,
        o.order_purchase_timestamp,
        date_trunc('month', o.order_purchase_timestamp) as purchase_month,
        coalesce(r.revenue, 0) as revenue,
        coalesce(r.items, 0) as items
    from fact_orders o
    left join order_revenue r
      on r.order_id = o.order_id
    where o.order_status <> 'canceled'
)

select
    customer_id,

    min(order_purchase_timestamp) as first_purchase_ts,
    max(order_purchase_timestamp) as last_purchase_ts,

    datediff('day', min(order_purchase_timestamp), max(order_purchase_timestamp)) as lifetime_days,

    count(distinct order_id) as total_orders,
    sum(items) as total_items,
    sum(revenue) as total_revenue,

    sum(revenue)::double / nullif(count(distinct order_id), 0) as avg_order_value,

    count(distinct purchase_month) as active_months

from orders_enriched
group by customer_id;