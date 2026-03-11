# Sales Analytics Case Study (Draft)

## Writing Standard

- Use explicit, professional language suitable for senior analyst audiences.
- Include assumptions, validation evidence, business interpretation, and tradeoffs.
- Keep the narrative clear and educational without internal tooling/process jargon.

## 1. Business Problem

Define the business objective solved by this project:

- Why this sales analytics workflow matters.
- Which decisions become easier/faster.
- Which KPI domains are supported.

## 2. Architecture Overview

### Local Engineering Stack

- CSV ingestion and validation in Jupyter.
- DuckDB materialization through versioned SQL.
- Validation-first dimensional modeling.

### Fabric Translation Path

- Lakehouse ingestion (Bronze).
- Warehouse modeling (`stg` and `core`) (Silver).
- Marts + semantic layer for BI (Gold).

## 3. Data Model and Metric Contract

- Star schema rationale.
- Fact and dimension grain.
- Referential integrity policy.
- Metric contract highlights and business meaning.

## 4. Data Quality and Validation Evidence

- Row count checks.
- Grain checks.
- Null key checks.
- Orphan key checks.

Add evidence links:

- Notebook outputs.
- SQL validations.
- CI run summary.

## 5. Dashboard Outcomes

- Power BI report pages and intended audience.
- Key insights found.
- Example business actions enabled by the dashboard.

## 6. Engineering Decisions and Tradeoffs

- Why DuckDB for local prototyping.
- Why Fabric as the target architecture.
- What was intentionally scoped out.

## 7. Portfolio Impact

- Skills demonstrated for Analytics Engineer roles.
- Skills demonstrated for Data Analyst roles.
- Planned extensions (near-term roadmap).
