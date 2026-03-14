# Sales Analytics Case Study (Week 2 Draft)

## 1. Business Problem

This project solves a common analytics gap in commerce operations: teams need reliable KPI tracking (orders, delivery quality, revenue, customer behavior), but reporting logic is often fragmented across notebooks, ad hoc queries, and BI-layer formulas.

The objective was to build a reproducible analytics workflow where:

- dimensional modeling is explicit and auditable,
- metric definitions are contract-driven,
- quality validation is first-class,
- and the model is ready for BI consumption and Fabric migration.

Target decisions enabled by this model:

- monitor delivery reliability and service performance,
- track revenue composition and basket efficiency,
- understand customer activity and review behavior,
- support monthly business reviews with one governed semantic base.

## 2. Architecture Overview

### Local Analytics Engineering Stack

- Source: transactional CSV datasets under `01-data/01-raw/`.
- Processing: DuckDB with versioned SQL models in `03-sql/models/`.
- Analytical marts: SQL views in `03-sql/marts/`.
- Orchestration and checks: notebooks under `02-notebooks/`.

### Fabric Translation Path

- Bronze: raw landing in Lakehouse Delta tables.
- Silver: conformed `stg` + `core` modeling in Warehouse SQL.
- Gold: marts + semantic model consumed by Power BI.

This keeps local development fast while preserving a direct migration path to Fabric production patterns.

## 3. Data Model and Metric Contract

The star schema contains 3 dimensions and 4 facts:

- Dimensions: `dim_date`, `dim_customers`, `dim_products`
- Facts: `fact_orders`, `fact_order_items`, `fact_order_payments`, `fact_order_reviews`

Grain and key contracts are documented in:

- `05-docs/STAR_SCHEMA.md`
- `05-docs/PHASE_4_METRIC_CONTRACT.md`

### KPI Snapshot (Model Build on 2026-03-12)

| Domain | Metric | Value |
|---|---|---:|
| Operational | Total Orders | 99,441 |
| Operational | Approval Rate | 99.98% |
| Operational | On-Time Delivery Rate | 91.88% |
| Operational | Avg Delivery Time (days) | 12.50 |
| Revenue | GMV | 13,591,643.70 |
| Revenue | Revenue Total (incl. freight) | 15,843,553.24 |
| Revenue | Avg Order Value | 137.75 |
| Revenue | Freight Ratio | 16.57% |

Full evidence and reproducibility details:

- `05-docs/case-study/CASE_STUDY_EVIDENCE_2026-03-12.md`

## 4. Data Quality and Validation Evidence

Validation strategy covers:

- row counts and model footprint,
- grain uniqueness checks,
- null key checks,
- referential integrity (orphan) checks.

Results from the latest reproducible run:

- Grain checks: 0 violations across 7 key definitions.
- Null key checks: 0 nulls across 17 key fields.
- Orphan checks: 0 orphan records across 12 FK paths.
- Product key completeness: 611 `product_id` values backfilled in `dim_products` to preserve fact referential integrity.

Supporting evidence:

- `05-docs/case-study/CASE_STUDY_EVIDENCE_2026-03-12.md`
- `02-notebooks/02_duckdb_materialization.ipynb`
- `03-sql/models/`
- `03-sql/marts/`

## 5. Dashboard Linkage

This model exposes three dashboard-ready analytical views:

- Executive KPI page:
  - source: `03-sql/marts/02_mart_monthly_business_snapshot.sql`
  - focus: monthly orders, revenue, AOV, delivery performance.
- Cohort/retention page:
  - source: `03-sql/marts/01_mart_cohort_unit_economics.sql`
  - focus: cohort activity and cumulative revenue per cohort customer.
- Customer value page:
  - source: `03-sql/marts/03_mart_customer_ltv_summary.sql`
  - focus: customer lifetime revenue, order frequency, lifecycle span.

Power BI publication status:

- Initial dashboard linkage is defined at the mart level.
- Public sharing model is tracked as a Week 2 action in `05-docs/project-memory/NEXT_ACTIONS.md`.
- Fabric parity gate: `PASS` as of 2026-03-14; public dashboard publication is now unblocked pending the final share URL.
- Public dashboard URL: `TBD` (replace with final Power BI public/app URL).

## 6. Engineering Decisions and Tradeoffs

Key decisions:

- SQL-first modeling: all business logic resides in versioned SQL, not notebooks.
- DuckDB-first local execution: fast iteration and deterministic reproducibility.
- Contract-first metrics: metric definitions are explicitly governed in one canonical file.
- Fabric alignment: local layers map to Lakehouse/Warehouse/Semantic model structure.

Current tradeoffs:

- Cohort depth is limited by the dataset grain (`customer_id` behaves close to order-level identity). A future improvement should model longitudinal behavior on `customer_unique_id`.
- Fabric apply automation is implemented and gated; first live apply evidence is captured, but credential rotation and sharing/publication hardening are still pending.

## 7. Portfolio Impact

Analytics Engineer evidence:

- dimensional modeling with explicit grain and key governance,
- reproducible SQL marts and quality controls,
- CI/CD-ready deployment workflow with guarded Fabric apply path.

Data Analyst evidence:

- KPI contract clarity with business interpretation,
- monthly performance and delivery reliability analysis,
- customer/revenue views designed for BI storytelling.

Near-term extensions:

- rotate troubleshooting-era credentials and confirm fresh-secret pipeline run stability,
- finalize public Power BI sharing path,
- publish case-study page through the portfolio’s GitHub Pages route.
