-- ==============================================================
-- Model: dim_date
-- Grain: 1 row per calendar date
-- Source: stg_orders.order_purchase_timestamp
-- Strategy: Continuous calendar between min/max purchase dates
-- ==============================================================

create or replace table dim_date as

with bounds as (
    select
        min(date(order_purchase_timestamp)) as min_date,
        max(date(order_purchase_timestamp)) as max_date
    from stg_orders
),

calendar as (
    select *
    from bounds,
    generate_series(min_date, max_date, interval 1 day) as t(full_date)
)

select
    cast(strftime(full_date, '%Y%m%d') as integer) as date_key,
    full_date as date,
    extract(year from full_date) as year,
    extract(month from full_date) as month,
    strftime(full_date, '%B') as month_name,
    extract(day from full_date) as day,
    extract(dow from full_date) as day_of_week,
    strftime(full_date, '%A') as day_name,
    case when extract(dow from full_date) in (0, 6) then 1 else 0 end as is_weekend
from calendar
order by full_date;