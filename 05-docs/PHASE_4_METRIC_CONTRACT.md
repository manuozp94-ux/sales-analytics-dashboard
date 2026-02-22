# Sales Analytics Dashboard, Phase 4 — Metric Contract

## Purpose

This document defines the official analytical metrics for the Sales Analytics Dashboard.

Its objective is to:

- Establish explicit metric definitions
- Declare base facts and grain
- Prevent semantic ambiguity
- Ensure reproducibility across BI tools
- Keep calculation logic outside visualization layers

This document serves as the single source of truth for metric definitions.

---

## Data Model Overview

### Dimensions
- `dim_date`
- `dim_customers`
- `dim_products`

### Facts
- `fact_orders` (grain: 1 row per `order_id`)
- `fact_order_items` (grain: 1 row per (`order_id`,`order_item_id`))
- `fact_order_payments` (grain: 1 row per (`order_id`, `payment_sequential`))
- `fact_order_reviews` (grain: 1 row per (`review_id`, `order_id`))

---

## Metric Format (Contract Fields)

Each metric MUST specify:

- Definition
- Base Fact
- Grain
- Compatible Dimensions / Filters
- Aggregation Behavior
- SQL Expression
- Notes (where needed)

---

## Domain I - Operational Performance

---

### 1. total_orders

**Definition:**
Total distinct orders placed.

**Base Fact:**
`fact_orders`

**Grain:**
`order_id`

**Compatible Dimensions:**
- `dim_date`
- `dim_customers`
- `order_status` (attribute in `fact_orders`)

**Aggregation Behavior:**
Safe at any dimensional level.

**SQL Expression:**
```sql
count(distinct order_id)
```

**Notes:**
Primary operational volume KPI.

### 2. approval_rate

**Definition:**
Percentage of non-cancelled orders that were approved.

**Base Fact:**
`fact_orders`

**Grain**
`order_id`

**Compatible Dimensions:**
- `dim_date`
- `order_status` (attribute in `fact_orders`)

**Aggregation Behavior:**
Conditional (status-sensitive).

**SQL Expression:**
```sql
sum(
  case
    when order_status <> 'canceled'
     and order_approved_at is not null
    then 1 else 0
  end
)
/
count(
  case
    when order_status <> 'canceled'
    then 1
  end
)
```

**Notes:**
Denominator excludes cancelled orders to avoid mixing process failures with logistic/customer-driven cancellations.

### 3. on_time_delivery_rate

**Definition:**
Percentage of delivered orders that arrived on or before the estimated delivery date.

**Base Fact:**
`fact_orders`

**Grain:**
`order_id`

**Compatible Dimensions:**
- `dim_date`
- `dim_customers`

**Aggregation Behavior:**
Conditional (defined only for delivered orders).

**SQL Expression:**
```sql
sum(
  case
    when order_status = 'delivered'
     and order_delivered_customer_date <= order_estimated_delivery_date
    then 1 else 0
  end
)
/
count(
  case
    when order_status = 'delivered'
    then 1
  end
)
```

**Notes:**
Uses order_status = 'delivered' as the contract for inclusion in the denominator.

### 4. avg_delivery_time_days

**Definition:**
Average number of days between purchase and delivery (delivered orders only).

**Base Fact:**
`fact_orders`

**Grain:**
`order_id`

**Compatible Dimensions:**
- `dim_date`
- `dim_customers`

**Aggregation Behavior:**
Conditional (delivered orders only) and sensitive to outliers.

**SQL Expression:**
```sql
avg(
  case
    when order_status = 'delivered'
     and order_delivered_customer_date is not null
    then datediff('day', order_purchase_timestamp, order_delivered_customer_date)
  end
)
```

**Notes:**
Orders not delivered are excluded by contract.

---

## Domain II - Revenue & Basket Efficiency

---

### 5. gmv

**Definition:**
Gross Merchandise Value. Total merchandise value excluding freight.

**Base Fact:**
`fact_order_items`

**Grain:**
(`order_id`, `order_item_id`)

**Compatible Dimensions:**
- `dim_date`
- `dim_products`
- `dim_customers`

**Aggregation Behavior:**
Safe for aggregation across supported dimensions.

**SQL Expression:**
```sql
sum(price)
```

**Notes:**
Primary revenue indicator at item level.
Safe for aggregartion by product and time.

### 6. revenue_total

**Definition:**
Total revenue including freight charges.

**Base Fact:**
`fact_order_items`

**Grain:**
(`order_id`, `order_item_id`)

**Compatible Dimensions:**
- `dim_date`
- `dim_products`
- `dim_customers`

**Aggregation Behavior:**
Safe for aggregation across supported dimensions.

**SQL Expression:**
```sql
sum(price + freight_value)
```

**Notes:**
Represents full customer payment impact at item level.

### 7. avg_order_value

**Definition:**
Average marchandise value per order (AOV)

**Base Fact:**
`fact_order_items`

**Grain:**
`order_id` (derived)

**Compatible Dimensions:**
- `dim_date`
- `dim_customers`

**Aggregatuon Behavior:**
Cross-grain sensitive (can be distorted when slicing by product)

**SQL Expression:**
```sql
sum (price) / count(distinct order_id)
```

**Notes:**
If you slice by product, you are effectively computing “AOV for orders containing that product,” which is valid but different. Document this in the dashboard layer.

### 8. avg_items_per_order

**Definition:**
Average number of items per order.

**Base Fact:**
`fact_order_items`

**Grain:**
`order_id`(derived)

**Compatible Dimensions:**
- `dim_date`
- `dim_customers`

**Aggregation Behavior:**
Cross-grain sensitive (distorted by product filtering).

**SQL Expression:**
```sql
count(*) / count(distinct order_id)
```

**Notes:**
When sliced by product, becomes “avg quantity of that product per order containing it.”

### 9. freight_ration

**Definition:**
Freight cost as a percentage of merchandise value.

**Base Fact:**
`fact_order_items`

**Grain:**
(`order_id`, `order_item_id`)

**Compatible Dimensions:**
- `dim_date`
- `dim_products`

**Aggregation Behavior:**
Sensitive when `sum(price)`is small

**SQL Expression:**
```sql
sum(freight_value) / nullif(sum(price), 0)
```

**Notes:**
nullif prevents division-by-zero artifacts.

---

## Domain III - Customer Intelligence

---

### 10. active_customers

**Definition:**
Distinct customers placing at least one non-cancelled order in the selected period.

**Base Fact:**
`fact_orders`

**Grain:**
`customer_id`

**Compatible Dimensions:**
- `dim_date`
- `dim_customers`

**Aggregation Behavior:**
Conditional (excludes cancelled orders by contract).  

**SQL Expression:**
```sql
count(distinct case when order_status <> 'canceled' then customer_id end)
```

**Notes:**
This is a behavioral activity measure; cohort metrics handle lifecycle dynamics.

### 11. repeat_customer_rate

**Definition:**
Percentage of customers with more than one non-cancelled order in the selected period.

**Base Fact:**
`fact_orders`

**Grain:**
`customer_id`

**Compatible Dimensions:**
- `dim_date`

**Aggregation Behavior:**
Conditional (meaning depends on the time window).

**SQL Expression:**
```sql
count(distinct case
with customer_orders as (
  select
    customer_id,
    count(distinct case when order_status <> 'canceled' then order_id end) as order_count
  from fact_orders
  group by customer_id
)
select
  count(distinct case when order_count > 1 then customer_id end)
  / count(distinct customer_id)
from customer_orders;
```

**Notes:**
This is “repeat within window.” For lifetime repeat, compute over full history.

### 12. avg_review_score

**Definition:**
Average customer review rating.

**Base Fact:**
`fact_order_reviews`

**Grain:**
(`review_id`, `order_id`)

**Compatible Dimension:**
- `dim_date`
- `dim_customers`

**Aggregation Behavior:**
Safe if score values are clean and castable.

**SQL Expression:**
```sql
avg(cast(review_score as integer))
```

**Notes:**
`review_score` is stored as VARCHAR in staging and must be cast.

### 13. review_coverage_rate

**Definition:**
Percentage of non-cancelled orders that received at least one review. 

**Base Fact:**
`fact_order_reviews` + `fact_orders`

**Grain:**
`order_id`

**Compatible Dimensions:**
- `dim_date`

**Aggregation Behavior:**
Conditional (requires consisten time filtering across numerator/denominator)

**SQL Expression (pattern):**
```sql
count(distinct r.order_id)
/
count(distinct case when o.order_status <> 'canceled' then o.order_id end)
```

**Implementation Note:**
Implement as a join between fact_order_reviews r and fact_orders o, with aligned date filters.

**Notes:**
Measures engagement and feedback participation.

---

## Domain IV - Retention & Cohort Analysis

This domain introduces longitudinal metrics. These metrics are not simple snapshots and should be exposed to BI through a dedicated cohort mart/view.

---

### 14. cohort_size

**Definition:**
Number of customers whose first purchase occurred in a given cohort month.

**Base Fact:**
`fact_orders`

**Grain:**
(`cohort_month`, `customer_id`) aggregated to `cohort_month`

**Compatible Dimensions / Filters:**
- `cohort_month`(derived)
- optional customer geography via `dim_customers`(requires join)

**Aggregation Behavior:**
Safe when grouped by `cohort_month`; avoid mixing cohort definitions.

**SQL Expression:**
```sql
with first_purchase as (
  select
    customer_id,
    date_trunc('month', min(order_purchase_timestamp)) as cohort_month
  from fact_orders
  group by customer_id
)
select
  cohort_month,
  count(distinct customer_id) as cohort_size
from first_purchase
group by cohort_month
order by cohort_month;
```

**Notes:**
- Cohort month is defined as month of first purchase timestamp (not first delivered date).
- If restricting the analysis period, cohort membership can change.
- Avoid filtering the base history unless explicitly intended.

### 15. retention_rate

**Definition:**
For each cohort month, the percentage of cohort customers who place an order in month N since first purchase.

**Base Fact:**
`fact_orders`

**Grain:**
(`cohort_month`, `months_since_first_purchase`)

**Compatible Dimensions / Filters:**
- `cohort_month`
- `month_offset``
- optional geography via `dim_customers`(requires join)

**Aggregation Behavior:**
Conditional (requires correct cohort baseline and aligned `cohort_size`).

**SQL Expression:**
```sql
with first_purchase as (
  select
    customer_id,
    min(order_purchase_timestamp) as first_purchase_ts
  from fact_orders
  group by customer_id
),
orders_with_offsets as (
  select
    o.customer_id,
    date_trunc('month', fp.first_purchase_ts) as cohort_month,
    datediff('month', fp.first_purchase_ts, o.order_purchase_timestamp) as months_since_first_purchase
  from fact_orders o
  join first_purchase fp
    on o.customer_id = fp.customer_id
),
cohort_sizes as (
  select
    cohort_month,
    count(distinct customer_id) as cohort_size
  from orders_with_offsets
  where months_since_first_purchase = 0
  group by cohort_month
),
activity as (
  select
    cohort_month,
    months_since_first_purchase,
    count(distinct customer_id) as active_customers
  from orders_with_offsets
  group by cohort_month, months_since_first_purchase
)
select
  a.cohort_month,
  a.months_since_first_purchase,
  cs.cohort_size,
  a.active_customers,
  a.active_customers::double / cs.cohort_size as retention_rate
from activity a
join cohort_sizes cs
  on cs.cohort_month = a.cohort_month
order by a.cohort_month, a.months_since_first_purchase;
```

**Notes:**
- Month 0 represents the initial purchase month (baseline).
- Retention is computed as `active_customers / cohort_size`.
- Expose via a mart/view (e.g., `mart_cohort_retention`) to avoid BI-layer recomputation.

## 6. Metric Governance Rules

1. **SQL is the source of truth.** All metric logic must be expressible in SQL.
2. **No BI-only business logic.** DAX/Power BI must not be the only place where logic exists.
3. **Notebooks orchestrate, not transform.** Python is for running scripts and validations only.
4. **Versioning discipline.** Any metric change requires updating this document and re-running validations.
5. **Aggregation behavior is contractual.** Metrics must declare if they are Safe / Conditional / Cross-grain sensitive.
6. **Longitudinal metrics require marts.** Cohort/retention metrics should be exposed through a dedicated mart/view.
7. **No duplicated definitions across layers.** Do not define different versions of the same metric in different places.

---

## 7. Change Log

- **v1:** Initial metric contract including Operational, Revenue, Customer Intelligence, and Retention/Cohort metrics.

