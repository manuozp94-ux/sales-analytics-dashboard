# Fabric Warehouse Probe Report

- Generated (UTC): `2026-03-14T05:39:55+00:00`
- Workspace ID: `1fd8df3e-883f-49d3-9386-d236f8b272ba`
- Source mode: `file`
- Total workspace items: **6**
- Warehouses found: **1**
- SQL endpoint items: **1**
- Query candidate items: **1**
- Naming issues (non-snake-case): **0**

## Item Type Counts

- `CopyJob`: 1
- `DataPipeline`: 1
- `Lakehouse`: 1
- `Notebook`: 1
- `SQLEndpoint`: 1
- `Warehouse`: 1

## Warehouses

_Warehouse items were detected, but live metadata probes are skipped in file mode._

## Naming Issues

_No naming issues detected under snake_case rule._

## Contract Name Presence (Workspace Item Names)

- Matches: **0/10**
- Present: _None_

- Missing:
  - `dim_customers`
  - `dim_date`
  - `dim_products`
  - `fact_order_items`
  - `fact_order_payments`
  - `fact_order_reviews`
  - `fact_orders`
  - `mart_cohort_unit_economics`
  - `mart_customer_ltv_summary`
  - `mart_monthly_business_snapshot`

Note: workspace inventory tracks top-level Fabric items. Table/view-level presence inside Warehouse must be validated with Warehouse SQL catalog queries.
