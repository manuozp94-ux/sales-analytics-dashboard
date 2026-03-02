-- ==============================================================
-- Mart: mart_cohort_unit_economics
-- Purpose: Cohort retention + revenue unit economics (observed)
-- Sources: fact_orders, fact_order_items
-- Grain: 1 row per (cohort_month, months_since_first_purchase)
-- ==============================================================

create or replace view mart_cohort_unit_economics as

with first_purchase as (
    select
        customer_id,
        min(order_purchase_timestamp) as first_purchase_ts
    from fact_orders
    where order_status <> 'canceled'
    group by customer_id
),

orders_with_offsets as (
    select
        o.order_id,
        o.customer_id,
        date_trunc('month', fp.first_purchase_ts) as cohort_month,
        datediff('month', fp.first_purchase_ts, o.order_purchase_timestamp) as months_since_first_purchase
    from fact_orders o
    join first_purchase fp
        on o.customer_id = fp.customer_id
    where o.order_status <> 'canceled'
),

cohort_sizes as (
    select
        cohort_month,
        count(distinct customer_id) as cohort_size
    from orders_with_offsets
    where months_since_first_purchase = 0
    group by cohort_month
),

activity as (
    select
        cohort_month,
        months_since_first_purchase,
        count(distinct customer_id) as active_customers,
        count(distinct order_id) as orders
    from orders_with_offsets
    group by cohort_month, months_since_first_purchase
),

revenue_by_order as (
    select
        order_id,
        sum(price + freight_value) as revenue_total
    from fact_order_items
    group by order_id
),

revenue as (
    select
        o.cohort_month,
        o.months_since_first_purchase,
        sum(r.revenue_total) as revenue
    from orders_with_offsets o
    join revenue_by_order r
        on r.order_id = o.order_id
    group by o.cohort_month, o.months_since_first_purchase
)

select
    a.cohort_month,
    a.months_since_first_purchase,

    cs.cohort_size,
    a.active_customers,
    a.orders,

    -- Retention
    a.active_customers::double / nullif(cs.cohort_size, 0) as retention_rate,

    -- Revenue (monthly)
    coalesce(rv.revenue, 0) as revenue,

    -- Unit economics
    coalesce(rv.revenue, 0)::double / nullif(a.active_customers, 0) as revenue_per_active_customer,
    coalesce(rv.revenue, 0)::double / nullif(cs.cohort_size, 0) as revenue_per_cohort_customer,

    -- Observed LTV (cumulative revenue per cohort customer)
    sum(coalesce(rv.revenue, 0)::double / nullif(cs.cohort_size, 0))
        over (
            partition by a.cohort_month
            order by a.months_since_first_purchase
            rows between unbounded preceding and current row
        ) as cum_revenue_per_cohort_customer

from activity a
join cohort_sizes cs
    on cs.cohort_month = a.cohort_month
left join revenue rv
    on rv.cohort_month = a.cohort_month
    and rv.months_since_first_purchase = a.months_since_first_purchase

order by a.cohort_month, a.months_since_first_purchase;