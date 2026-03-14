# Case Study Evidence Snapshot (2026-03-12)

## Scope

- Purpose: provide reproducible KPI and data-quality evidence for the Week 2 case study draft.
- Execution date (UTC): 2026-03-12.
- Data window: `2016-09-04` to `2018-10-17`.
- Source data: `01-data/01-raw/*.csv`.

## Reproducibility Path

1. Load staging tables from raw CSV files (`stg_*`) in DuckDB.
2. Execute all model SQL files:
   - `03-sql/models/*.sql`
3. Execute all mart SQL files:
   - `03-sql/marts/*.sql`
4. Run KPI and QA aggregate queries on `fact_*`, `dim_*`, and `mart_*`.

## Model Footprint

| Table / View | Rows |
|---|---:|
| `dim_date` | 774 |
| `dim_customers` | 99,441 |
| `dim_products` | 32,951 |
| `fact_orders` | 99,441 |
| `fact_order_items` | 112,650 |
| `fact_order_payments` | 103,886 |
| `fact_order_reviews` | 100,000 |
| `mart_monthly_business_snapshot` | 24 |
| `mart_cohort_unit_economics` | 24 |
| `mart_customer_ltv_summary` | 98,816 |

## KPI Snapshot

| Domain | Metric | Value |
|---|---|---:|
| Operational | `total_orders` | 99,441 |
| Operational | `approval_rate` | 99.98% |
| Operational | `on_time_delivery_rate` | 91.88% |
| Operational | `avg_delivery_time_days` | 12.50 |
| Revenue | `gmv` | 13,591,643.70 |
| Revenue | `revenue_total` | 15,843,553.24 |
| Revenue | `avg_order_value` | 137.75 |
| Revenue | `avg_items_per_order` | 1.14 |
| Revenue | `freight_ratio` | 16.57% |
| Customer | `avg_review_score` | 4.07 |

## Monthly Mart Highlights

| Metric | Value |
|---|---:|
| Months in mart | 24 |
| Non-cancelled orders (sum) | 98,816 |
| Total revenue (sum) | 15,737,667.52 |
| Avg monthly on-time delivery rate | 90.49% |
| Avg monthly delivery time (days) | 14.31 |
| Peak revenue month | 2017-11 |
| Peak revenue (month) | 1,172,191.68 |

## Data Quality Results

| Check Type | Result |
|---|---|
| Grain checks (7 key definitions) | 0 violations |
| Null key checks (17 key fields) | 0 nulls |
| Referential integrity checks (12 FK paths) | 0 orphans |
| Product key backfill (`dim_products`) | 611 keys backfilled |

## Notes and Modeling Tradeoffs

- `dim_products` intentionally backfills `product_id` values from order items to preserve referential integrity in `fact_order_items`.
- Cohort/retention views currently rely on `customer_id` grain. With this dataset, `customer_id` behaves mostly as an order-level identifier, so longitudinal cohort depth is limited. A future enhancement should shift cohort logic to `customer_unique_id`.
