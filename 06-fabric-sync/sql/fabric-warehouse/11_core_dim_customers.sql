-- core.dim_customers

if object_id('core.dim_customers', 'U') is not null
begin
    drop table core.dim_customers;
end;

select
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
into core.dim_customers
from stg.stg_customers;
