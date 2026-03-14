-- Safe reset for model schemas only.
-- This script drops known model artifacts in:
--   core, mart
-- It does NOT touch stg.
--
-- Compatibility approach:
-- - no cursors
-- - no table variables
-- - no dynamic SQL
--
-- Note:
-- - legacy `marts` retirement is handled separately by
--   `02_drop_legacy_marts_schema_safe.sql`

set nocount on;

-- ------------------------------------------------------------------
-- CORE TABLES (canonical + known legacy)
-- ------------------------------------------------------------------
if object_id('core.fact_order_items', 'U') is not null drop table core.fact_order_items;
if object_id('core.fact_order_payments', 'U') is not null drop table core.fact_order_payments;
if object_id('core.fact_order_reviews', 'U') is not null drop table core.fact_order_reviews;
if object_id('core.fact_orders', 'U') is not null drop table core.fact_orders;
if object_id('core.dim_products', 'U') is not null drop table core.dim_products;
if object_id('core.dim_customers', 'U') is not null drop table core.dim_customers;
if object_id('core.dim_date', 'U') is not null drop table core.dim_date;

-- legacy/auxiliary dimensions observed in workspace
if object_id('core.dim_order_status', 'U') is not null drop table core.dim_order_status;
if object_id('core.dim_payment_types', 'U') is not null drop table core.dim_payment_types;

-- ------------------------------------------------------------------
-- MART OBJECTS (canonical schema only)
-- ------------------------------------------------------------------
if object_id('mart.mart_monthly_business_snapshot', 'V') is not null
    drop view mart.mart_monthly_business_snapshot;
if object_id('mart.mart_monthly_business_snapshot', 'U') is not null
    drop table mart.mart_monthly_business_snapshot;

if object_id('mart.mart_cohort_unit_economics', 'V') is not null
    drop view mart.mart_cohort_unit_economics;
if object_id('mart.mart_cohort_unit_economics', 'U') is not null
    drop table mart.mart_cohort_unit_economics;

if object_id('mart.mart_customer_ltv_summary', 'V') is not null
    drop view mart.mart_customer_ltv_summary;
if object_id('mart.mart_customer_ltv_summary', 'U') is not null
    drop table mart.mart_customer_ltv_summary;

-- Post-reset verification (stg untouched)
select
    s.name as schema_name,
    o.type_desc,
    count(*) as object_count
from sys.objects o
join sys.schemas s
  on s.schema_id = o.schema_id
where s.name in ('stg', 'core', 'mart')
group by s.name, o.type_desc
order by s.name, o.type_desc;
