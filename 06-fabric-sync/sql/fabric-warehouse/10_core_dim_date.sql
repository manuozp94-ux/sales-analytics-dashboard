-- core.dim_date

if object_id('core.dim_date', 'U') is not null
begin
    drop table core.dim_date;
end;

if not exists (
    select 1
    from stg.stg_orders
    where try_cast(order_purchase_timestamp as datetime2(6)) is not null
)
begin
    raiserror('No valid order_purchase_timestamp values found in stg.stg_orders.', 16, 1);
end;

with parsed_orders as (
    select
        cast(try_cast(order_purchase_timestamp as datetime2(6)) as date) as purchase_date
    from stg.stg_orders
    where try_cast(order_purchase_timestamp as datetime2(6)) is not null
),
bounds as (
    select
        min(purchase_date) as min_date,
        max(purchase_date) as max_date
    from parsed_orders
),
digits as (
    select v.d
    from (values (0),(1),(2),(3),(4),(5),(6),(7),(8),(9)) v(d)
),
numbers as (
    select
        d0.d
        + (10 * d1.d)
        + (100 * d2.d)
        + (1000 * d3.d) as n
    from digits d0
    cross join digits d1
    cross join digits d2
    cross join digits d3
),
calendar as (
    select
        dateadd(day, n.n, b.min_date) as full_date
    from bounds b
    join numbers n
      on n.n <= datediff(day, b.min_date, b.max_date)
)
select
    cast(convert(char(8), full_date, 112) as int) as date_key,
    cast(full_date as date) as [date],
    datepart(year, full_date) as [year],
    datepart(month, full_date) as [month],
    cast(datename(month, full_date) as varchar(20)) as month_name,
    datepart(day, full_date) as [day],
    datepart(weekday, full_date) - 1 as day_of_week,
    cast(datename(weekday, full_date) as varchar(20)) as day_name,
    case when datename(weekday, full_date) in ('Saturday', 'Sunday') then 1 else 0 end as is_weekend
into core.dim_date
from calendar;
