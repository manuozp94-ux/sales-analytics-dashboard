-- core.fact_order_reviews

if object_id('core.fact_order_reviews', 'U') is not null
begin
    drop table core.fact_order_reviews;
end;

select
    r.review_id,
    r.order_id,
    o.customer_id,
    case
        when try_cast(o.order_purchase_timestamp as datetime2(6)) is not null
        then cast(
            convert(char(8), cast(try_cast(o.order_purchase_timestamp as datetime2(6)) as date), 112)
            as int
        )
    end as purchase_date_key,
    try_cast(r.review_score as int) as review_score,
    r.review_comment_title,
    r.review_comment_message,
    try_cast(r.review_creation_date as datetime2(6)) as review_creation_ts,
    try_cast(r.review_answer_timestamp as datetime2(6)) as review_answer_ts
into core.fact_order_reviews
from stg.stg_order_reviews r
join stg.stg_orders o
  on o.order_id = r.order_id;
