# Fabric Warehouse Materialization + Parity Runbook

## Purpose

This runbook closes the architecture gap between:

- local validated model (DuckDB), and
- Fabric Warehouse implementation.

It enforces a parity gate before any public visualization/publication step.

## Canonical Scope (Contract)

Required analytical objects (10):

1. `dim_date`
2. `dim_customers`
3. `dim_products`
4. `fact_orders`
5. `fact_order_items`
6. `fact_order_payments`
7. `fact_order_reviews`
8. `mart_monthly_business_snapshot`
9. `mart_cohort_unit_economics`
10. `mart_customer_ltv_summary`

Required KPI pack (10):

- `total_orders`
- `approval_rate`
- `on_time_delivery_rate`
- `avg_delivery_time_days`
- `gmv`
- `revenue_total`
- `avg_order_value`
- `avg_items_per_order`
- `freight_ratio`
- `avg_review_score`

## DuckDB -> Fabric SQL Mapping (Fixed)

- `datediff('day', a, b)` -> `DATEDIFF(day, a, b)`
- `date_trunc('month', ts)` -> `DATEFROMPARTS(YEAR(ts), MONTH(ts), 1)`
- `count(*) filter (where ...)` -> `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`
- `expr::double` -> `CAST(expr AS FLOAT)`

## Prerequisites

- Fabric workspace ID: `1fd8df3e-883f-49d3-9386-d236f8b272ba`
- Warehouse: `wh_sales_analytics`
- Staging tables loaded in schema `stg`:
  - `stg_orders`
  - `stg_customers`
  - `stg_products`
  - `stg_order_items`
  - `stg_order_payments`
  - `stg_order_reviews`
- Local repo up to date and local DuckDB file available:
  - `04-duckdb/sales_analytics.duckdb`

## Execution Sequence (Warehouse SQL)

Run these scripts in this exact order inside Fabric Warehouse:

1. `06-fabric-sync/sql/fabric-warehouse/00_schema_bootstrap.sql`
2. (Optional one-time cleanup) `06-fabric-sync/sql/fabric-warehouse/02_drop_legacy_marts_schema_safe.sql`
3. (Optional reset) `06-fabric-sync/sql/fabric-warehouse/01_reset_core_mart_safe.sql`
4. `06-fabric-sync/sql/fabric-warehouse/05_stg_compat_views.sql`
5. `06-fabric-sync/sql/fabric-warehouse/10_core_dim_date.sql`
6. `06-fabric-sync/sql/fabric-warehouse/11_core_dim_customers.sql`
7. `06-fabric-sync/sql/fabric-warehouse/12_core_dim_products.sql`
8. `06-fabric-sync/sql/fabric-warehouse/20_core_fact_orders.sql`
9. `06-fabric-sync/sql/fabric-warehouse/21_core_fact_order_items.sql`
10. `06-fabric-sync/sql/fabric-warehouse/22_core_fact_order_payments.sql`
11. `06-fabric-sync/sql/fabric-warehouse/23_core_fact_order_reviews.sql`
12. `06-fabric-sync/sql/fabric-warehouse/30_mart_cohort_unit_economics.sql`
13. `06-fabric-sync/sql/fabric-warehouse/31_mart_monthly_business_snapshot.sql`
14. `06-fabric-sync/sql/fabric-warehouse/32_mart_customer_ltv_summary.sql`

Execution surfaces:

- Manual editor path:
  - open `wh_sales_analytics` in the Fabric SQL editor,
  - run the scripts in the order above.
- CLI apply path:
  - use `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh`,
  - forward your chosen `sqlcmd` connection/auth flags after `--`,
  - use `--include-legacy-cleanup` and `--include-reset` only when intended.
- Service principal local bootstrap path:
  - use `06-fabric-sync/scripts/bootstrap_fabric_service_principal.sh` first if you are authenticating with a Fabric service principal and want to mirror the pipeline token bootstrap locally.

Preview the ordered pack:

```bash
./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh --print-only
```

Apply the canonical pack from a terminal or CI agent:

```bash
./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh \
  --confirm-apply YES \
  -- \
  -S "<warehouse_sql_endpoint>" \
  -d "wh_sales_analytics" \
  -U "<sql_user>" \
  -P "<sql_password>"
```

Bootstrap a local service principal before the first SQL apply:

```bash
FABRIC_TENANT_ID="<tenant-id>" \
FABRIC_CLIENT_ID="<client-id>" \
FABRIC_CLIENT_SECRET="<client-secret>" \
FABRIC_WORKSPACE_ID="1fd8df3e-883f-49d3-9386-d236f8b272ba" \
./06-fabric-sync/scripts/bootstrap_fabric_service_principal.sh
```

Notes:

- `sqlcmd` runs on the caller host; the SQL executes in the remote Fabric Warehouse.
- The CLI path intentionally excludes `40_parity_query_pack.sql` and `41_warehouse_catalog_probe.sql` because they are validation queries, not materialization steps.
- The same CLI scaffold can later be invoked from Azure DevOps without duplicating the ordered SQL list in pipeline YAML.
- The bootstrap helper validates service-principal reachability through the Fabric REST workspace-items endpoint before the SQL connection step.

Canonical schema note:

- `mart` is the only canonical analytical schema in Warehouse.
- `marts` is legacy only; retire it with `02_drop_legacy_marts_schema_safe.sql` if it still exists.

Optional pre-check (recommended before/after materialization):

- `06-fabric-sync/sql/fabric-warehouse/41_warehouse_catalog_probe.sql`
- This captures schema/table/view/module inventory for naming and parity diagnostics.
- Empty result in the module-definition query is expected before mart/core programmable objects are created.

## Local Baseline Generation (Automated)

From repo root:

```bash
python3 06-fabric-sync/fabric_parity_baseline.py \
  --out-json 06-fabric-sync/state/parity/parity_local_latest.json
```

Expected result:

- output file exists,
- `status = PASS`,
- `qa_violations_total = 0`.

## Fabric Metrics/QA Capture (Manual SQL, Standardized)

Run:

- `06-fabric-sync/sql/fabric-warehouse/40_parity_query_pack.sql`

Capture each result set and populate:

- `06-fabric-sync/state/parity/parity_fabric_latest.json`

Use this template:

- `06-fabric-sync/examples/parity/fabric_parity_baseline_template.json`

Rules while filling the JSON:

- keep check names exactly as template,
- use numeric values only,
- set `qa_violations_total` as the sum of all QA violations,
- set `status` to `PASS` only if all QA violations are zero.

## Parity Comparison Gate (Automated)

Run:

```bash
python3 06-fabric-sync/fabric_parity_compare.py \
  --local 06-fabric-sync/state/parity/parity_local_latest.json \
  --fabric 06-fabric-sync/state/parity/parity_fabric_latest.json \
  --out-json 06-fabric-sync/state/parity/parity_compare_latest.json \
  --out-md 06-fabric-sync/state/parity/parity_compare_latest.md
```

Acceptance thresholds (hard-coded contract):

- counts: exact match
- QA: exact match and zero violations in both sides
- KPI count metrics: exact match
- KPI money/averages: absolute diff <= `0.01`
- KPI rates: absolute diff <= `0.0005`

Exit behavior:

- exit code `0`: parity `PASS`
- exit code `1`: parity `FAIL`

## Quality Gate Policy Before Visualization

- If parity result is `PASS`:
  - dashboard build/publication is allowed.
- If parity result is `FAIL`:
  - dashboard publication is blocked,
  - open remediation cycle with evidence.

## Required Evidence Artifacts Per Cycle

- `06-fabric-sync/state/parity/parity_local_latest.json`
- `06-fabric-sync/state/parity/parity_fabric_latest.json`
- `06-fabric-sync/state/parity/parity_compare_latest.json`
- `06-fabric-sync/state/parity/parity_compare_latest.md`
- one Fabric change note in `06-fabric-sync/notes/`
- updates in:
  - `05-docs/project-memory/PROJECT_STATUS.md`
  - `05-docs/project-memory/SESSION_LOG.md`
  - `05-docs/project-memory/NEXT_ACTIONS.md`

## Verification Scenarios (Mandatory)

1. Baseline success:

```bash
python3 06-fabric-sync/fabric_parity_baseline.py \
  --out-json 06-fabric-sync/state/parity/parity_local_latest.json
```

Expected: exit `0`, status `PASS`.

2. Baseline controlled failure (missing required objects):

```bash
tmp_db="/tmp/parity_missing_objects_test.duckdb"
python3 - <<'PY'
import duckdb
con = duckdb.connect('/tmp/parity_missing_objects_test.duckdb')
con.execute('create table only_one_table(id integer);')
con.close()
PY
python3 06-fabric-sync/fabric_parity_baseline.py --duckdb-path "$tmp_db"
```

Expected: exit `1` with missing-object error list.

3. Comparator PASS fixture:

```bash
python3 06-fabric-sync/fabric_parity_compare.py \
  --local 06-fabric-sync/state/parity/parity_local_latest.json \
  --fabric 06-fabric-sync/examples/parity/fabric_parity_baseline_fixture_pass.json
```

Expected: exit `0`.

4. Comparator FAIL fixtures:

```bash
python3 06-fabric-sync/fabric_parity_compare.py \
  --local 06-fabric-sync/state/parity/parity_local_latest.json \
  --fabric 06-fabric-sync/examples/parity/fabric_parity_baseline_fixture_fail_counts.json

python3 06-fabric-sync/fabric_parity_compare.py \
  --local 06-fabric-sync/state/parity/parity_local_latest.json \
  --fabric 06-fabric-sync/examples/parity/fabric_parity_baseline_fixture_fail_kpi.json
```

Expected: exit `1` in both cases.
