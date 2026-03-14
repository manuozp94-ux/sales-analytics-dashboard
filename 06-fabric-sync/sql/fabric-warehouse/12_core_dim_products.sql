-- core.dim_products

if object_id('core.dim_products', 'U') is not null
begin
    drop table core.dim_products;
end;

if not exists (
    select 1
    from stg.stg_products
    where nullif(ltrim(rtrim(product_id)), '') is not null
)
begin
    raiserror('No valid product rows found in stg.stg_products.', 16, 1);
end;

with cleaned_products as (
    select
        lower(nullif(ltrim(rtrim(product_id)), '')) as product_id,
        nullif(ltrim(rtrim(product_category_name)), '') as product_category_name,
        nullif(ltrim(rtrim(product_name_lenght)), '') as product_name_lenght_raw,
        nullif(ltrim(rtrim(product_description_lenght)), '') as product_description_lenght_raw,
        nullif(ltrim(rtrim(product_photos_qty)), '') as product_photos_qty_raw,
        nullif(ltrim(rtrim(product_weight_g)), '') as product_weight_g_raw,
        nullif(ltrim(rtrim(product_length_cm)), '') as product_length_cm_raw,
        nullif(ltrim(rtrim(product_height_cm)), '') as product_height_cm_raw,
        nullif(ltrim(rtrim(product_width_cm)), '') as product_width_cm_raw
    from stg.stg_products
),
cleaned_order_items as (
    select
        lower(nullif(ltrim(rtrim(product_id)), '')) as product_id
    from stg.stg_order_items
    where nullif(ltrim(rtrim(product_id)), '') is not null
),
base as (
    select
        product_id,
        cast(product_category_name as varchar(255)) as product_category_name,
        try_cast(try_cast(product_name_lenght_raw as float) as int) as product_name_lenght,
        try_cast(try_cast(product_description_lenght_raw as float) as int) as product_description_lenght,
        try_cast(try_cast(product_photos_qty_raw as float) as int) as product_photos_qty,
        try_cast(product_weight_g_raw as float) as product_weight_g,
        try_cast(product_length_cm_raw as float) as product_length_cm,
        try_cast(product_height_cm_raw as float) as product_height_cm,
        try_cast(product_width_cm_raw as float) as product_width_cm
    from cleaned_products
    where product_id is not null
),
missing_keys as (
    select distinct
        oi.product_id
    from cleaned_order_items oi
    left join base p
      on p.product_id = oi.product_id
    where p.product_id is null
),
missing_rows as (
    select
        mk.product_id,
        cast(null as varchar(255)) as product_category_name,
        cast(null as int) as product_name_lenght,
        cast(null as int) as product_description_lenght,
        cast(null as int) as product_photos_qty,
        cast(null as float) as product_weight_g,
        cast(null as float) as product_length_cm,
        cast(null as float) as product_height_cm,
        cast(null as float) as product_width_cm
    from missing_keys mk
)
select
    x.product_id,
    x.product_category_name,
    x.product_name_lenght,
    x.product_description_lenght,
    x.product_photos_qty,
    x.product_weight_g,
    x.product_length_cm,
    x.product_height_cm,
    x.product_width_cm
into core.dim_products
from (
    select
        product_id,
        product_category_name,
        product_name_lenght,
        product_description_lenght,
        product_photos_qty,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm
    from base
    union all
    select
        product_id,
        product_category_name,
        product_name_lenght,
        product_description_lenght,
        product_photos_qty,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm
    from missing_rows
) x;
