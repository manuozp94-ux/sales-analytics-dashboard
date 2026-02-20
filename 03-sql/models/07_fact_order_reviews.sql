-- ==============================================================
-- Model: fact_order_reviews
-- Grain: 1 row per review_id
-- Sources:
--   stg_order_reviews
--   stg_orders (customer_id + purchase_date_key)
-- Notes:
--   review_creation_date and review_answer_timestamp are VARCHAR
--   due to tolerant CSV load; we keep them as-is in Phase 3.
-- ==============================================================

create or replace table fact_order_reviews as

select
    r.review_id,
    r.order_id,

    o.customer_id,
    cast(strftime(date(o.order_purchase_timestamp), '%Y%m%d') as integer) as purchase_date_key,

    r.review_score,
    r.review_comment_title,
    r.review_comment_message,
    r.review_creation_date,
    r.review_answer_timestamp
from stg_order_reviews r
join stg_orders o
    on o.order_id = r.order_id;