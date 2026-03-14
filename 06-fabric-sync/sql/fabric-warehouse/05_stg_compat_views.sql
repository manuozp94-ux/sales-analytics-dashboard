-- Staging compatibility shim
-- Goal: allow core scripts to use canonical stg.stg_* names even when
-- ingestion created tables as stg.orders / stg.customers / etc.

-- orders -> stg_orders
if object_id('stg.stg_orders', 'U') is null
begin
    if object_id('stg.orders', 'U') is not null or object_id('stg.orders', 'V') is not null
    begin
        exec('create or alter view stg.stg_orders as select * from stg.orders;');
    end
    else if object_id('stg.stg_orders', 'V') is null
    begin
        raiserror('Missing required staging source: stg.orders', 16, 1);
    end
end;

-- customers -> stg_customers
if object_id('stg.stg_customers', 'U') is null
begin
    if object_id('stg.customers', 'U') is not null or object_id('stg.customers', 'V') is not null
    begin
        exec('create or alter view stg.stg_customers as select * from stg.customers;');
    end
    else if object_id('stg.stg_customers', 'V') is null
    begin
        raiserror('Missing required staging source: stg.customers', 16, 1);
    end
end;

-- products -> stg_products
if object_id('stg.stg_products', 'U') is null
begin
    if object_id('stg.products', 'U') is not null or object_id('stg.products', 'V') is not null
    begin
        exec('create or alter view stg.stg_products as select * from stg.products;');
    end
    else if object_id('stg.stg_products', 'V') is null
    begin
        raiserror('Missing required staging source: stg.products', 16, 1);
    end
end;

-- order_items -> stg_order_items
if object_id('stg.stg_order_items', 'U') is null
begin
    if object_id('stg.order_items', 'U') is not null or object_id('stg.order_items', 'V') is not null
    begin
        exec('create or alter view stg.stg_order_items as select * from stg.order_items;');
    end
    else if object_id('stg.stg_order_items', 'V') is null
    begin
        raiserror('Missing required staging source: stg.order_items', 16, 1);
    end
end;

-- order_payments -> stg_order_payments
if object_id('stg.stg_order_payments', 'U') is null
begin
    if object_id('stg.order_payments', 'U') is not null or object_id('stg.order_payments', 'V') is not null
    begin
        exec('create or alter view stg.stg_order_payments as select * from stg.order_payments;');
    end
    else if object_id('stg.stg_order_payments', 'V') is null
    begin
        raiserror('Missing required staging source: stg.order_payments', 16, 1);
    end
end;

-- order_reviews -> stg_order_reviews
if object_id('stg.stg_order_reviews', 'U') is null
begin
    if object_id('stg.order_reviews', 'U') is not null or object_id('stg.order_reviews', 'V') is not null
    begin
        exec('create or alter view stg.stg_order_reviews as select * from stg.order_reviews;');
    end
    else if object_id('stg.stg_order_reviews', 'V') is null
    begin
        raiserror('Missing required staging source: stg.order_reviews', 16, 1);
    end
end;

-- verification output
select
    s.name as schema_name,
    o.name as object_name,
    o.type_desc
from sys.objects o
join sys.schemas s
  on s.schema_id = o.schema_id
where s.name = 'stg'
  and o.name in (
      'stg_orders',
      'stg_customers',
      'stg_products',
      'stg_order_items',
      'stg_order_payments',
      'stg_order_reviews'
  )
order by o.name;
