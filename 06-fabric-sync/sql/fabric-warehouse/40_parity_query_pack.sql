-- Fabric parity query pack
-- Run each block and export results to compose parity_fabric_latest.json

-- 1) Required object counts (10)
select 'dim_date' as object_name, count(*) as row_count from core.dim_date
union all
select 'dim_customers', count(*) from core.dim_customers
union all
select 'dim_products', count(*) from core.dim_products
union all
select 'fact_orders', count(*) from core.fact_orders
union all
select 'fact_order_items', count(*) from core.fact_order_items
union all
select 'fact_order_payments', count(*) from core.fact_order_payments
union all
select 'fact_order_reviews', count(*) from core.fact_order_reviews
union all
select 'mart_monthly_business_snapshot', count(*) from mart.mart_monthly_business_snapshot
union all
select 'mart_cohort_unit_economics', count(*) from mart.mart_cohort_unit_economics
union all
select 'mart_customer_ltv_summary', count(*) from mart.mart_customer_ltv_summary;

-- 2) KPI pack (10)
with orders_kpi as (
    select
        cast(count(distinct order_id) as float) as total_orders,
        cast(sum(case when order_status <> 'canceled' and order_approved_at is not null then 1 else 0 end) as float)
            / nullif(sum(case when order_status <> 'canceled' then 1 else 0 end), 0) as approval_rate,
        cast(sum(
            case
                when order_status = 'delivered'
                 and order_delivered_customer_date is not null
                 and order_estimated_delivery_date is not null
                 and order_delivered_customer_date <= order_estimated_delivery_date
                then 1 else 0
            end
        ) as float)
            / nullif(sum(case when order_status = 'delivered' then 1 else 0 end), 0) as on_time_delivery_rate,
        avg(cast(case when order_status = 'delivered' and order_delivered_customer_date is not null then datediff(day, order_purchase_timestamp, order_delivered_customer_date) end as float)) as avg_delivery_time_days
    from core.fact_orders
),
items_kpi as (
    select
        cast(sum(price) as float) as gmv,
        cast(sum(price + freight_value) as float) as revenue_total,
        cast(sum(price) as float) / nullif(count(distinct order_id), 0) as avg_order_value,
        cast(count(*) as float) / nullif(count(distinct order_id), 0) as avg_items_per_order,
        cast(sum(freight_value) as float) / nullif(sum(price), 0) as freight_ratio
    from core.fact_order_items
),
reviews_kpi as (
    select
        avg(cast(review_score as float)) as avg_review_score
    from core.fact_order_reviews
)
select
    o.total_orders,
    o.approval_rate,
    o.on_time_delivery_rate,
    o.avg_delivery_time_days,
    i.gmv,
    i.revenue_total,
    i.avg_order_value,
    i.avg_items_per_order,
    i.freight_ratio,
    r.avg_review_score
from orders_kpi o
cross join items_kpi i
cross join reviews_kpi r;

-- 3) Grain checks (7)
select 'dim_date_pk_unique' as check_name, count(*) as violation_count
from (
    select date_key
    from core.dim_date
    group by date_key
    having count(*) > 1
) x
union all
select 'dim_customers_pk_unique', count(*)
from (
    select customer_id
    from core.dim_customers
    group by customer_id
    having count(*) > 1
) x
union all
select 'dim_products_pk_unique', count(*)
from (
    select product_id
    from core.dim_products
    group by product_id
    having count(*) > 1
) x
union all
select 'fact_orders_grain_order_id', count(*)
from (
    select order_id
    from core.fact_orders
    group by order_id
    having count(*) > 1
) x
union all
select 'fact_order_items_grain_order_item', count(*)
from (
    select order_id, order_item_id
    from core.fact_order_items
    group by order_id, order_item_id
    having count(*) > 1
) x
union all
select 'fact_order_payments_grain_payment_seq', count(*)
from (
    select order_id, payment_sequential
    from core.fact_order_payments
    group by order_id, payment_sequential
    having count(*) > 1
) x
union all
select 'fact_order_reviews_grain_review_order', count(*)
from (
    select review_id, order_id
    from core.fact_order_reviews
    group by review_id, order_id
    having count(*) > 1
) x;

-- 4) Null key checks (17)
select 'dim_date_date_key_nulls' as check_name, count(*) as violation_count from core.dim_date where date_key is null
union all
select 'dim_customers_customer_id_nulls', count(*) from core.dim_customers where customer_id is null
union all
select 'dim_products_product_id_nulls', count(*) from core.dim_products where product_id is null
union all
select 'fact_orders_order_id_nulls', count(*) from core.fact_orders where order_id is null
union all
select 'fact_orders_customer_id_nulls', count(*) from core.fact_orders where customer_id is null
union all
select 'fact_orders_purchase_date_key_nulls', count(*) from core.fact_orders where purchase_date_key is null
union all
select 'fact_order_items_order_id_nulls', count(*) from core.fact_order_items where order_id is null
union all
select 'fact_order_items_order_item_id_nulls', count(*) from core.fact_order_items where order_item_id is null
union all
select 'fact_order_items_customer_id_nulls', count(*) from core.fact_order_items where customer_id is null
union all
select 'fact_order_items_product_id_nulls', count(*) from core.fact_order_items where product_id is null
union all
select 'fact_order_items_date_key_nulls', count(*) from core.fact_order_items where date_key is null
union all
select 'fact_order_payments_order_id_nulls', count(*) from core.fact_order_payments where order_id is null
union all
select 'fact_order_payments_customer_id_nulls', count(*) from core.fact_order_payments where customer_id is null
union all
select 'fact_order_payments_purchase_date_key_nulls', count(*) from core.fact_order_payments where purchase_date_key is null
union all
select 'fact_order_reviews_order_id_nulls', count(*) from core.fact_order_reviews where order_id is null
union all
select 'fact_order_reviews_customer_id_nulls', count(*) from core.fact_order_reviews where customer_id is null
union all
select 'fact_order_reviews_purchase_date_key_nulls', count(*) from core.fact_order_reviews where purchase_date_key is null;

-- 5) Orphan checks (12)
select 'fact_orders_orphans_dim_customers' as check_name, count(*) as violation_count
from core.fact_orders f
left join core.dim_customers d
  on d.customer_id = f.customer_id
where d.customer_id is null
union all
select 'fact_orders_orphans_dim_date', count(*)
from core.fact_orders f
left join core.dim_date d
  on d.date_key = f.purchase_date_key
where d.date_key is null
union all
select 'fact_order_items_orphans_fact_orders', count(*)
from core.fact_order_items f
left join core.fact_orders o
  on o.order_id = f.order_id
where o.order_id is null
union all
select 'fact_order_items_orphans_dim_customers', count(*)
from core.fact_order_items f
left join core.dim_customers d
  on d.customer_id = f.customer_id
where d.customer_id is null
union all
select 'fact_order_items_orphans_dim_products', count(*)
from core.fact_order_items f
left join core.dim_products d
  on d.product_id = f.product_id
where d.product_id is null
union all
select 'fact_order_items_orphans_dim_date', count(*)
from core.fact_order_items f
left join core.dim_date d
  on d.date_key = f.date_key
where d.date_key is null
union all
select 'fact_order_payments_orphans_fact_orders', count(*)
from core.fact_order_payments f
left join core.fact_orders o
  on o.order_id = f.order_id
where o.order_id is null
union all
select 'fact_order_payments_orphans_dim_customers', count(*)
from core.fact_order_payments f
left join core.dim_customers d
  on d.customer_id = f.customer_id
where d.customer_id is null
union all
select 'fact_order_payments_orphans_dim_date', count(*)
from core.fact_order_payments f
left join core.dim_date d
  on d.date_key = f.purchase_date_key
where d.date_key is null
union all
select 'fact_order_reviews_orphans_fact_orders', count(*)
from core.fact_order_reviews f
left join core.fact_orders o
  on o.order_id = f.order_id
where o.order_id is null
union all
select 'fact_order_reviews_orphans_dim_customers', count(*)
from core.fact_order_reviews f
left join core.dim_customers d
  on d.customer_id = f.customer_id
where d.customer_id is null
union all
select 'fact_order_reviews_orphans_dim_date', count(*)
from core.fact_order_reviews f
left join core.dim_date d
  on d.date_key = f.purchase_date_key
where d.date_key is null;
