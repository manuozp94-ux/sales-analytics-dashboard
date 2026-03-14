-- mart.mart_cohort_unit_economics

create or alter view mart.mart_cohort_unit_economics as
with first_purchase as (
    select
        customer_id,
        min(order_purchase_timestamp) as first_purchase_ts
    from core.fact_orders
    where order_status <> 'canceled'
    group by customer_id
),
orders_with_offsets as (
    select
        o.order_id,
        o.customer_id,
        datefromparts(year(fp.first_purchase_ts), month(fp.first_purchase_ts), 1) as cohort_month,
        datediff(month, fp.first_purchase_ts, o.order_purchase_timestamp) as months_since_first_purchase
    from core.fact_orders o
    join first_purchase fp
      on fp.customer_id = o.customer_id
    where o.order_status <> 'canceled'
      and o.order_purchase_timestamp is not null
      and fp.first_purchase_ts is not null
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
    from core.fact_order_items
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
    cast(a.active_customers as float) / nullif(cs.cohort_size, 0) as retention_rate,
    isnull(rv.revenue, 0) as revenue,
    cast(isnull(rv.revenue, 0) as float) / nullif(a.active_customers, 0) as revenue_per_active_customer,
    cast(isnull(rv.revenue, 0) as float) / nullif(cs.cohort_size, 0) as revenue_per_cohort_customer,
    sum(cast(isnull(rv.revenue, 0) as float) / nullif(cs.cohort_size, 0)) over (
        partition by a.cohort_month
        order by a.months_since_first_purchase
        rows between unbounded preceding and current row
    ) as cum_revenue_per_cohort_customer
from activity a
join cohort_sizes cs
  on cs.cohort_month = a.cohort_month
left join revenue rv
  on rv.cohort_month = a.cohort_month
 and rv.months_since_first_purchase = a.months_since_first_purchase;
