# Sales Analytics Portfolio (AE-first)

Public portfolio project focused on **Analytics Engineering** with strong Data Analyst evidence, designed for US-based hiring processes.

## Resume Here

Use these files to resume work in under 2 minutes:

- [PROJECT_STATUS.md](05-docs/project-memory/PROJECT_STATUS.md)
- [SESSION_LOG.md](05-docs/project-memory/SESSION_LOG.md)
- [NEXT_ACTIONS.md](05-docs/project-memory/NEXT_ACTIONS.md)
- [RESUME_NEXT_SESSION.md](05-docs/project-memory/RESUME_NEXT_SESSION.md)

## Session Close Checklist (Manual)

Before ending a work session, manually update:

1. `PROJECT_STATUS.md` (phase, blockers, outputs, risks)
2. `SESSION_LOG.md` (what changed, decisions, evidence)
3. `NEXT_ACTIONS.md` (top 3 actions, owner, ETA)

## What This Repository Demonstrates

- Local analytics engineering workflow with Jupyter + DuckDB + SQL models.
- Local-to-Fabric architecture translation (Lakehouse, Warehouse, QA, semantic layer path).
- Reproducible modeling discipline: explicit grain, integrity checks, metric contract, and marts.
- Portfolio delivery discipline: documentation, governance, release cadence, and collaboration standards.

## Layer Mapping (Bronze / Silver / Gold)

| Layer | Local Implementation | Fabric Translation | Outcome |
|---|---|---|---|
| Bronze | `01-data/01-raw` + staged loads in notebooks | Lakehouse raw/Delta ingestion | Reliable raw landing and traceability |
| Silver | `03-sql/models` dimensions/facts + QA checks | Warehouse `stg/core` modeling | Conformed, validated analytical model |
| Gold | `03-sql/marts` + metric contract | Warehouse marts + semantic model | BI-ready outputs and business metrics |

## Canonical Documentation

- [Project Rules](05-docs/PROJECT_RULES.md)
- [Roadmap](05-docs/ROADMAP.md)
- [History Curation Strategy](05-docs/HISTORY_CURATION_STRATEGY.md)
- [GitHub + Azure DevOps Model](05-docs/GITHUB_ADO_OPERATING_MODEL.md)
- [Model Overview](05-docs/README.md)
- [Metric Contract](05-docs/PHASE_4_METRIC_CONTRACT.md)
- [Case Study Draft (Week 2)](05-docs/case-study/CASE_STUDY_DRAFT.md)
- [Fabric Sync Bridge](06-fabric-sync/README.md)
- [Fabric Warehouse Parity Runbook](06-fabric-sync/RUNBOOK_FABRIC_WAREHOUSE_PARITY.md)
- [Fabric Change Note Template](06-fabric-sync/notes/FABRIC_CHANGE_NOTE_TEMPLATE.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Certification Tracker](05-docs/CERTIFICATION_TRACKER.md)
- [Job Application Tracker](05-docs/JOB_APPLICATION_TRACKER.md)
- [Weekly Milestone Template](05-docs/WEEKLY_MILESTONE_TEMPLATE.md)

## Collaboration Model

- **Code source of truth:** GitHub (public repo + PR workflow).
- **Planning and enterprise operations:** Azure DevOps Boards + Pipelines.
- **Release cadence:** one weekly tagged milestone (`portfolio-week-XX`).

## Portfolio Outcome Target

By Week 4, this repo should provide:

- Public case study page (GitHub Pages).
- Working Power BI dashboard sourced from gold outputs.
- Clear evidence of local engineering workflow and Fabric-ready architecture.
