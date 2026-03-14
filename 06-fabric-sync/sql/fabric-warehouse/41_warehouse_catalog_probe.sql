-- Warehouse catalog probe for parity and naming review.
-- Run this in Fabric Warehouse SQL editor after materialization scripts.

-- 1) Schemas currently present
SELECT
    s.name as schema_name
FROM sys.schemas AS s
ORDER BY s.name;

-- 2) Table and view inventory in target schemas
SELECT
    t.table_schema,
    t.table_name,
    t.table_type
FROM INFORMATION_SCHEMA.TABLES AS t
WHERE t.table_schema IN ('stg', 'core', 'mart')
ORDER BY t.table_schema, t.table_type, t.table_name;

-- 3) Column-level structure
SELECT
    c.table_schema,
    c.table_name,
    c.column_name,
    c.data_type,
    c.is_nullable,
    c.ordinal_position
FROM INFORMATION_SCHEMA.COLUMNS AS c
WHERE c.table_schema IN ('stg', 'core', 'mart')
ORDER BY c.table_schema, c.table_name, c.ordinal_position;

-- 4) SQL module definitions (views/procedures/functions) when available
-- If this returns empty, it means no programmable objects exist yet in core/mart.
SELECT
    s.name AS schema_name,
    o.name AS object_name,
    o.type_desc,
    m.definition
FROM sys.objects AS o
INNER JOIN sys.schemas AS s
    ON s.schema_id = o.schema_id
LEFT JOIN sys.sql_modules AS m
    ON m.object_id = o.object_id
WHERE s.name IN ('core', 'mart')
  AND o.type IN ('V', 'P', 'FN', 'IF', 'TF')
ORDER BY s.name, o.type_desc, o.name;
