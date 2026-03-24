# Sales Analytics to Microsoft Fabric

This repository captures phase 1 of an analytics engineering journey: a local SQL-first sales model that was translated into Microsoft Fabric, validated with parity evidence, and wrapped with guarded delivery workflows. It now serves two purposes at once: portfolio evidence of real implementation work and a legacy foundation for the next architecture-first, agent-assisted phase of the platform.

## Current Status

- Local star schema, marts, and metric contract implemented and reproducible.
- Microsoft Fabric workspace connectivity, guarded apply flow, and Warehouse SQL path validated.
- Local vs Fabric parity closed at `PASS` across counts, QA checks, and KPI checks.
- Fabric semantic model and first MVP Power BI page drafted.
- The next phase is not “more scripts”; it is stronger architecture, reusable contracts, and BMAD-driven planning.

## What This Repository Built

- A SQL-first analytics engineering workflow using DuckDB, notebooks, and versioned models.
- A Fabric delivery path covering workspace inventory, guarded deployment, Warehouse materialization, and parity validation.
- A reusable bootstrap package for repos that need the same Fabric workspace/authentication pattern.
- A documented trail of implementation decisions, operating constraints, and capability gaps identified and corrected.

## What Reached Fabric

- Service-principal authentication and workspace inventory retrieval.
- Azure DevOps `dry-run` + manual-gated `apply` workflow for Fabric REST operations.
- Warehouse SQL materialization through the local service-principal `sqlcmd` path.
- Fabric parity evidence with a final `PASS` result.
- Fabric semantic model `sm_sales_analytics_mvp` and the first report page in Power BI Service.

## Why This Matters

- It demonstrates more than local modeling: it shows translation into Fabric with evidence, guardrails, and operational thinking.
- It shows professional growth: the later work corrected earlier code-first habits with parity gates, contracts, SQL guardrails, and runtime-auth patterns.
- It makes the next repo stronger: architecture, BMAD planning, and agent-assisted development can now build on real implementation lessons instead of assumptions.

## Evidence At A Glance

- [Case Study Draft](05-docs/case-study/CASE_STUDY_DRAFT.md)
- [Technical Documentation Index](05-docs/README.md)
- [BMAD Export Package](05-docs/bmad-export/README.md)
- [Fabric Sync Bridge](06-fabric-sync/README.md)
- [Fabric Warehouse Parity Runbook](06-fabric-sync/RUNBOOK_FABRIC_WAREHOUSE_PARITY.md)
- [Latest Parity Report](06-fabric-sync/state/parity/parity_compare_latest.md)
- [Fabric Bootstrap Package](07-fabric-bootstrap/ARCHITECTURE_AUTH_PACKAGE.md)

## Technical Highlights

- `01-data/01-raw` -> reproducible raw source layer for local modeling.
- `03-sql/models` -> conformed dimensions and facts with explicit grain and integrity rules.
- `03-sql/marts` -> dashboard-ready marts for monthly performance, cohorts, and customer value.
- `06-fabric-sync/` -> workspace sync, guarded deployment, Warehouse SQL apply, parity tooling, and operating standards.
- `07-fabric-bootstrap/` -> reusable onboarding package for other repos connecting to the same Fabric workspace/auth model.

## Layer Mapping

| Layer | Local Implementation | Fabric Translation | Outcome |
|---|---|---|---|
| Bronze | `01-data/01-raw` + staged notebook loads | Lakehouse raw/Delta ingestion | Reliable raw landing and traceability |
| Silver | `03-sql/models` + QA checks | Warehouse `stg/core` modeling | Conformed, validated analytical model |
| Gold | `03-sql/marts` + metric contract | Warehouse marts + semantic model | BI-ready outputs and governed metrics |

## Lessons And Evolution

- Early work optimized for learning Python, SQL, PySpark-adjacent thinking, and execution mechanics.
- The strongest improvements came later: runtime token generation, deployment guardrails, parity enforcement, reusable contracts, and repo-safe bootstrap assets.
- The main capability gap identified was not “coding harder”; it was moving earlier toward architecture-first planning, system boundaries, and reusable delivery patterns.
- The next stage should start from product/system briefs, environment contracts, identity strategy, and agent-assisted delivery instead of discovering those concerns late.

## Quick Links

- [Project Rules](05-docs/PROJECT_RULES.md)
- [Metric Contract](05-docs/PHASE_4_METRIC_CONTRACT.md)
- [Case Study Evidence](05-docs/case-study/CASE_STUDY_EVIDENCE_2026-03-12.md)
- [Fabric Consulting Standard](06-fabric-sync/FABRIC_CONSULTING_STANDARD.md)
- [Fabric Contract Bundle](06-fabric-sync/contracts/README.md)
- [BMAD Product Brief Input](05-docs/bmad-export/02_bmad_product_brief_input.md)
- [Implementation Findings Legacy](05-docs/bmad-export/01_implementation_findings_legacy.md)

## Internal Continuity

These files remain useful for operator continuity, but they are not the primary public entry point for the portfolio:

- [PROJECT_STATUS.md](05-docs/project-memory/PROJECT_STATUS.md)
- [SESSION_LOG.md](05-docs/project-memory/SESSION_LOG.md)
- [NEXT_ACTIONS.md](05-docs/project-memory/NEXT_ACTIONS.md)
- [RESUME_NEXT_SESSION.md](05-docs/project-memory/RESUME_NEXT_SESSION.md)
