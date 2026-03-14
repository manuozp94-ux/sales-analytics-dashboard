# Sales Analytics Dashboard  
### Dimensional Modeling & Analytics Engineering Project

---

## 0. Canonical Navigation

- Project Rules: `05-docs/PROJECT_RULES.md`
- Roadmap: `05-docs/ROADMAP.md`
- History Curation Strategy: `05-docs/HISTORY_CURATION_STRATEGY.md`
- Project Memory:
  - `05-docs/project-memory/PROJECT_STATUS.md`
  - `05-docs/project-memory/SESSION_LOG.md`
  - `05-docs/project-memory/NEXT_ACTIONS.md`

Use the project memory files as the official "where we left off" mechanism between sessions.

---

## 1. Project Purpose

This project implements a complete dimensional modeling pipeline for a transactional sales dataset.

The primary objectives are:

- Design a clean Star Schema
- Enforce explicit grain and referential integrity
- Separate transformation logic from orchestration
- Define a formal Metric Contract
- Prepare the model for BI consumption
- Architect the solution for future migration to Microsoft Fabric

This project focuses on analytics engineering discipline rather than infrastructure complexity.

---

## 2. Current Implementation (Engine-Agnostic Layer)

The project is currently implemented locally using:

- DuckDB (SQL execution engine)
- Versioned SQL scripts (`03-sql/`)
- Jupyter notebooks for orchestration and validation
- Explicit validation checks (grain, nulls, referential integrity)

### Why DuckDB?

DuckDB allows:

- Fast local iteration
- Deterministic SQL modeling
- Clear separation between data modeling and infrastructure
- Portable architecture

All transformation logic lives in SQL scripts.
Python notebooks contain no business logic.

---

## 3. Data Model

The analytical model is implemented as a star schema.

### Dimensions
- dim_date
- dim_customers
- dim_products

### Facts
- fact_orders (1 row per order_id)
- fact_order_items (1 row per order_id + order_item_id)
- fact_order_payments (1 row per order_id + payment_sequential)
- fact_order_reviews (1 row per review_id + order_id)

Each table explicitly defines:

- Grain
- Primary key
- Foreign keys
- Source staging tables
- Referential integrity policy

See `STAR_SCHEMA.md` for full specification.

---

## 4. Validation Strategy

Each table is validated using:

- Row count checks
- Grain validation (uniqueness tests)
- Null key checks
- Referential integrity (orphan detection)

All validations are executed in `02_duckdb_materialization.ipynb`.

The model enforces full referential integrity across conformed keys.

---

## 5. Metric Layer (Business Contract)

The project defines a formal Metric Contract including:

### Domain I – Operational Performance
- total_orders
- approval_rate
- on_time_delivery_rate
- avg_delivery_time_days

### Domain II – Revenue & Basket Efficiency
- gmv
- revenue_total
- avg_order_value
- avg_items_per_order
- freight_ratio

### Domain III – Customer Intelligence
- active_customers
- repeat_customer_rate
- avg_review_score
- review_coverage_rate

### Domain IV – Retention & Cohort Analysis
- cohort_size
- retention_rate

See `PHASE_4_METRIC_CONTRACT.md` for formal definitions.

---

## 6. Execution Workflow

1. Load staging tables from CSV
2. Run schema and model SQL scripts
3. Execute validation suite
4. Materialize marts (planned)
5. Expose to BI layer

The pipeline is fully reproducible.

---

## 7. Planned Evolution — Microsoft Fabric

The architecture is intentionally designed to be engine-portable.

Planned migration steps:

- Land raw and clean layers in Fabric Lakehouse (Delta format)
- Execute SQL transformations in Fabric Warehouse or Lakehouse SQL endpoint
- Persist fact/dimension tables in Fabric
- Expose semantic model to Power BI
- Implement scheduled refresh and governance

The current DuckDB implementation serves as:

- Proof of modeling correctness
- Controlled development environment
- Portable semantic layer foundation

---

## 7.1 Fabric-to-Repo Sync (Inventory Drift Control)

To keep local code and Fabric workspace state aligned, use:

- `06-fabric-sync/fabric_sync.py` to generate versioned snapshots of Fabric artifacts
- `06-fabric-sync/state/fabric_inventory_latest.json` as latest state
- `06-fabric-sync/state/fabric_inventory_diff_latest.md` as change report

This creates a traceable bridge between:

- what is built in Fabric (workspace artifacts),
- and what is versioned in this repository.

## 7.2 Fabric Parity Gate (Architecture Before Visualization)

Parity tooling is implemented under `06-fabric-sync/`:

- `fabric_parity_baseline.py` (local DuckDB baseline)
- `fabric_parity_compare.py` (local vs Fabric comparator, hard PASS/FAIL)
- `parity_contract.py` (frozen contract for objects, KPIs, and QA checks)
- `RUNBOOK_FABRIC_WAREHOUSE_PARITY.md` (manual Fabric execution runbook)

Publication rule:

- Power BI public release is blocked until parity comparison returns `PASS`.

---

## 8. Scope Boundaries

This project is intentionally not:

- A machine learning system
- A streaming platform
- A production-grade cloud deployment
- An infrastructure-heavy DevOps exercise

It is a focused analytics engineering and dimensional modeling implementation.

---

## 9. Architectural Principles

- Explicit grain definition
- Deterministic SQL transformations
- Separation of concerns
- Validation-first modeling
- Referential integrity enforcement
- Engine portability

---

## 10. Archive Note

Historical conversational material exists under `05-docs/context-consolidation/` for traceability.

Canonical decisions and operating rules must be maintained in English in the canonical docs listed in section 0.

---

## 11. Case Study Assets (Week 2)

- `05-docs/case-study/CASE_STUDY_DRAFT.md`
- `05-docs/case-study/CASE_STUDY_EVIDENCE_2026-03-12.md`
