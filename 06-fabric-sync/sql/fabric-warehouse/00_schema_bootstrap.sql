-- Fabric Warehouse schema bootstrap

if not exists (select 1 from sys.schemas where name = 'stg')
begin
    exec('create schema stg');
end;

if not exists (select 1 from sys.schemas where name = 'core')
begin
    exec('create schema core');
end;

if not exists (select 1 from sys.schemas where name = 'mart')
begin
    exec('create schema mart');
end;

-- Required staging sources for this runbook
-- Supports either:
-- 1) canonical names: stg_orders, stg_customers, ...
-- 2) short names: orders, customers, ...
select
    s.name as schema_name,
    t.name as table_name
from sys.tables t
join sys.schemas s
  on s.schema_id = t.schema_id
where s.name = 'stg'
  and t.name in (
      'orders',
      'customers',
      'products',
      'order_items',
      'order_payments',
      'order_reviews',
      'stg_orders',
      'stg_customers',
      'stg_products',
      'stg_order_items',
      'stg_order_payments',
      'stg_order_reviews'
  )
order by t.name;
