-- One-time retirement of legacy `marts` schema.
-- Canonical analytical schema is `mart`.
-- This script only drops `marts` if the schema exists and is empty.
-- If objects are still present, it returns the inventory and raises an error.

set nocount on;

if not exists (select 1 from sys.schemas where name = 'marts')
begin
    select
        'marts schema not present; no action required.' as status_message;
    return;
end;

if exists (
    select 1
    from sys.objects o
    join sys.schemas s
      on s.schema_id = o.schema_id
    where s.name = 'marts'
)
begin
    select
        s.name as schema_name,
        o.name as object_name,
        o.type_desc
    from sys.objects o
    join sys.schemas s
      on s.schema_id = o.schema_id
    where s.name = 'marts'
    order by o.type_desc, o.name;

    raiserror(
        'Legacy schema `marts` is not empty. Migrate or drop those objects before dropping the schema.',
        16,
        1
    );
    return;
end;

drop schema marts;

select
    s.name as schema_name
from sys.schemas s
where s.name in ('stg', 'core', 'mart', 'marts')
order by s.name;
